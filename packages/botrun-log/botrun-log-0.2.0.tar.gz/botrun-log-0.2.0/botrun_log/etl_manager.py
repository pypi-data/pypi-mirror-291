import os
from dotenv import load_dotenv
import psycopg2
import pytz
import datetime as dt
from google.cloud import bigquery
from google.oauth2 import service_account

load_dotenv('.env')
class ETLManager:
    def __init__(self, db_type='bigquery', pg_config=None, credentials_path=None, project_id=None, dataset_name=None):
        self.db_type = db_type.lower()

        if self.db_type == 'bigquery':
            credentials_path = credentials_path or os.getenv('BOTRUN_LOG_CREDENTIALS_PATH')
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.project_id = project_id or os.getenv('BOTRUN_LOG_PROJECT_ID')
            self.dataset_name = dataset_name or os.getenv('BOTRUN_LOG_DATASET_NAME')
            self.client = bigquery.Client(credentials=credentials, project=self.project_id)
            self.table_id = f"{self.project_id}.{self.dataset_name}.daily_character_usage"
            self._init_etl_bq()

        elif self.db_type == 'postgresql':
            if pg_config is None:
                raise ValueError("pg_config is required when using PostgreSQL.")
            self.pg_conn = psycopg2.connect(**pg_config)
            self.pg_cursor = self.pg_conn.cursor()
            self.table_name = 'daily_character_usage'
            self._init_etl_pg()

        else:
            raise ValueError(f"Invalid db_type '{self.db_type}'. Supported values are 'bigquery' or 'postgresql'.")

    def _init_etl_pg(self):
        """
        Initializes the PostgreSQL table for ETL summary.
        """
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            department VARCHAR(255) NOT NULL,
            user_name VARCHAR(255) NOT NULL,
            ch_characters INT NOT NULL,
            en_characters INT NOT NULL
        );
        """
        self.pg_cursor.execute(create_table_query)
        self.pg_conn.commit()

    def _init_etl_bq(self):
        schema = [
            bigquery.SchemaField("date", "DATE", "REQUIRED", description="日期"),
            bigquery.SchemaField("department", "STRING", "REQUIRED", description="機關"),
            bigquery.SchemaField("user_name", "STRING", "REQUIRED", description="使用者帳號"),
            bigquery.SchemaField("ch_characters", "INT64", "REQUIRED", description="中文字元數"),
            bigquery.SchemaField("en_characters", "INT64", "REQUIRED", description="英文字元數"),
        ]
        table = bigquery.Table(self.table_id, schema=schema)
        self.client.create_table(table, exists_ok=True)

    def write_etl_summary(self, department, date=None):
        if date is None:
            tz = pytz.timezone('Asia/Taipei')
            date = (dt.datetime.now(tz) - dt.timedelta(days=1)).date()

        if self.db_type == 'bigquery':
            # BigQuery邏輯保持不變
            delete_query = f"""
            DELETE FROM `{self.table_id}`
            WHERE date = '{date}' AND department = '{department}'
            """
            delete_job = self.client.query(delete_query)
            print(delete_job.result())  # 等待刪除作業完成

            query = f"""
            SELECT
                DATE(timestamp) as date,
                '{department}' as department,
                user_name,
                SUM(ch_characters) as ch_characters,
                SUM(en_characters) as en_characters
            FROM `{self.client.project}.{self.dataset_name}.{department}_logs`
            WHERE DATE(timestamp) = '{date}'
            GROUP BY date, user_name
            """

            job_config = bigquery.QueryJobConfig(destination=self.table_id, write_disposition="WRITE_APPEND")
            query_job = self.client.query(query, job_config=job_config)
            print(query_job.result())  # 等待作業完成

        elif self.db_type == 'postgresql':
            # 刪除已存在的相同日期和機關的數據
            delete_query = f"""
            DELETE FROM {self.table_name}
            WHERE date = %s AND department = %s
            """
            self.pg_cursor.execute(delete_query, (date, department))
            self.pg_conn.commit()

            # 執行ETL查詢並插入新的數據
            insert_query = f"""
            INSERT INTO {self.table_name} (date, department, user_name, ch_characters, en_characters)
            SELECT
                %s as date,
                %s as department,
                user_name,
                SUM(ch_characters) as ch_characters,
                SUM(en_characters) as en_characters
            FROM {department}_logs
            WHERE DATE(timestamp) = %s
            GROUP BY user_name
            """
            self.pg_cursor.execute(insert_query, (date, department, date))
            self.pg_conn.commit()


    def read_etl_summary(self, start_date: dt.date, end_date: dt.date, department: str = None, user_name: str = None):
        if self.db_type == 'bigquery':
            # BigQuery邏輯保持不變
            query = f"""
            SELECT
                date,
                department,
                user_name,
                ch_characters,
                en_characters
            FROM `{self.table_id}`
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            """

            if department:
                query += f" AND department = '{department}'"

            if user_name:
                query += f" AND user_name = '{user_name}'"

            query_job = self.client.query(query)
            results = query_job.result()  # 等待作業完成

            return [row for row in results]

        elif self.db_type == 'postgresql':
            # PostgreSQL邏輯
            query = f"""
            SELECT
                date,
                department,
                user_name,
                ch_characters,
                en_characters
            FROM {self.table_name}
            WHERE date BETWEEN %s AND %s
            """
            
            params = [start_date, end_date]
            if department:
                query += " AND department = %s"
                params.append(department)
            
            if user_name:
                query += " AND user_name = %s"
                params.append(user_name)

            self.pg_cursor.execute(query, tuple(params))
            results = self.pg_cursor.fetchall()

            return results
