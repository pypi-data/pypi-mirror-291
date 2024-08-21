import os
import datetime as dt
import psycopg2
import pytz
from google.api_core import retry
from google.cloud import bigquery
from google.oauth2 import service_account
from .crypto_manager import CryptoManager
from .log_entry import LogEntry
from .etl_manager import ETLManager

class Logger:
    def __init__(self, department=None, str_aes_key=None, db_type='bigquery', credentials_path=None, pg_config=None, project_id=None, dataset_name=None):
        """
        Initializes a Logger object.

        Args:
            department (str): The department name.  If not provided, it will be retrieved from the environment variable 'BOTRUN_LOG_DEPARTMENT'.
            str_aes_key (str, optional): The AES key. If not provided, it will be retrieved from the environment variable 'BOTRUN_LOG_AES_KEY'.
            db_type (str, optional): The type of database to use ('bigquery' or 'postgresql').
            credentials_path (str, optional): The path to the service account credentials file for BigQuery. 
                If not provided, it will be retrieved from the environment variable 'BOTRUN_LOG_CREDENTIALS_PATH'.
            pg_config (dict, optional): The PostgreSQL configuration dictionary (only required if db_type is 'postgresql').
            project_id (str, optional): The Google Cloud project ID. If not provided, it will be retrieved from the environment variable 'BOTRUN_LOG_PROJECT_ID'.
            dataset_name (str, optional): The BigQuery dataset name. If not provided, it will be retrieved from the environment variable 'BOTRUN_LOG_DATASET_NAME'.

        Returns:
            None

        Raises:
            ValueError: If the provided db_type is invalid.
        """
        self.department = department or os.getenv('BOTRUN_LOG_DEPARTMENT')
        self.db_type = db_type.lower()
        self.project_id = project_id or os.getenv('BOTRUN_LOG_PROJECT_ID')
        self.dataset_name = dataset_name or os.getenv('BOTRUN_LOG_DATASET_NAME')
        str_aes_key = str_aes_key or os.getenv('BOTRUN_LOG_AES_KEY')

        if self.db_type == 'bigquery':  
            self.credentials_path = credentials_path or os.getenv('BOTRUN_LOG_CREDENTIALS_PATH')
            self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
            self.client = bigquery.Client(credentials=self.credentials, project=self.project_id)
            self.table_id = f"{self.project_id}.{self.dataset_name}.{self.department}_logs"
            self.crypto_manager = CryptoManager(str_aes_key)
            self._init_bq()
            self.etl_manager = ETLManager(credentials_path=self.credentials_path, project_id=self.project_id, dataset_name=self.dataset_name)
            self.etl_manager._init_etl_bq()

        elif self.db_type == 'postgresql':
            if pg_config is None:
                raise ValueError("pg_config is required when using PostgreSQL.")
            
            self.pg_conn = psycopg2.connect(**pg_config)
            self.pg_cursor = self.pg_conn.cursor()
            self.crypto_manager = CryptoManager(str_aes_key)
            self._init_pg()
            self.etl_manager = ETLManager(db_type='postgresql', pg_config=pg_config, project_id=self.project_id, dataset_name=self.dataset_name)
            self.etl_manager._init_etl_pg()

        else:
            raise ValueError(f"Invalid db_type '{self.db_type}'. Supported values are 'bigquery' or 'postgresql'.")


    def _init_pg(self):
        """
        Initializes the PostgreSQL table for logging.
        """
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.department}_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            domain_name VARCHAR(255) NOT NULL,
            user_department VARCHAR(255) NOT NULL,
            user_name VARCHAR(255) NOT NULL,
            source_ip VARCHAR(255) NOT NULL,
            session_id VARCHAR(255) NOT NULL,
            action_type VARCHAR(255) NOT NULL,
            action_details TEXT,
            model VARCHAR(255),
            botrun VARCHAR(255),
            user_agent VARCHAR(255),
            resource_id VARCHAR(255),
            developer VARCHAR(255) NOT NULL,
            ch_characters INT NOT NULL,
            en_characters INT NOT NULL,
            total_characters INT NOT NULL,
            create_timestamp TIMESTAMP NOT NULL
        );
        """
        self.pg_cursor.execute(create_table_query)
        self.pg_conn.commit()


    def _init_bq(self):
        """
        Initializes the BigQuery dataset and table for logging.

        This method creates a BigQuery dataset and table with the specified schema and time partitioning.
        The dataset and table names are derived from the project ID, dataset name, and department name.
        The dataset is created in the "asia-east1" location.

        Parameters:
            None

        Returns:
            None
        """
        dataset_id = f"{self.project_id}.{self.dataset_name}"
        table_id = f"{dataset_id}.{self.department}_logs"

        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "asia-east1"
        self.client.create_dataset(dataset, exists_ok=True)

        schema = [
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED", description="時間戳"),
            bigquery.SchemaField("domain_name", "STRING", mode="REQUIRED", description="波特人網域"),
            bigquery.SchemaField("user_department", "STRING", mode="REQUIRED", description="使用者部門"),
            bigquery.SchemaField("user_name", "STRING", mode="REQUIRED", description="使用者帳號"),
            bigquery.SchemaField("source_ip", "STRING", mode="REQUIRED", description="使用者的IP地址"),
            bigquery.SchemaField("session_id", "STRING", mode="REQUIRED", description="工作階段ID"),
            bigquery.SchemaField("action_type", "STRING", mode="REQUIRED", description="操作類型"),
            bigquery.SchemaField("action_details", "STRING", mode="NULLABLE", description="操作內容，加密"),
            bigquery.SchemaField("model", "STRING", mode="NULLABLE", description="使用的模型"),
            bigquery.SchemaField("botrun", "STRING", mode="NULLABLE", description="Botrun 資訊"),
            bigquery.SchemaField("user_agent", "STRING", mode="NULLABLE", description="使用者的客戶端資訊"),
            bigquery.SchemaField("resource_id", "STRING", mode="NULLABLE", description="資源ID（上傳的文件等）"),
            bigquery.SchemaField("developer", "STRING", mode="REQUIRED", description="寫入log的套件或開發者"),
            bigquery.SchemaField("ch_characters", "INT64", mode="REQUIRED", description="中文字元數"),
            bigquery.SchemaField("en_characters", "INT64", mode="REQUIRED", description="英數字元數"),
            bigquery.SchemaField("total_characters", "INT64", mode="REQUIRED", description="總字元數"),
            bigquery.SchemaField("create_timestamp", "TIMESTAMP", mode="REQUIRED", description="寫入BigQuery的時間戳"),
        ]
        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(field="timestamp")
        self.client.create_table(table, exists_ok=True)

    def insert_log(self, log_entry: LogEntry):
        """
        Inserts a log entry into the BigQuery or PostgreSQL table.

        Args:
            log_entry (LogEntry): The log entry to be inserted.

        Raises:
            Exception: If there are errors while inserting the rows.

        Returns:
            None
        """
        log_data = log_entry.to_dict()
        log_data["create_timestamp"] = dt.datetime.now(tz=pytz.timezone("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
        if log_data["action_details"]:
            log_data["action_details"] = self.crypto_manager.encrypt(log_data["action_details"])

        if self.db_type == 'bigquery':
            errors = self.client.insert_rows_json(self.table_id, [log_data], retry=retry.Retry(deadline=60))
            if errors:
                print(log_data)
                raise Exception(f"Encountered errors while inserting rows: {errors}")

        elif self.db_type == 'postgresql':
            insert_query = f"""
            INSERT INTO {self.department}_logs (timestamp, domain_name, user_department, user_name, source_ip, session_id,
                                                action_type, action_details, model, botrun, user_agent, resource_id, developer,
                                                ch_characters, en_characters, total_characters, create_timestamp)
            VALUES (%(timestamp)s, %(domain_name)s, %(user_department)s, %(user_name)s, %(source_ip)s, %(session_id)s,
                    %(action_type)s, %(action_details)s, %(model)s, %(botrun)s, %(user_agent)s, %(resource_id)s, %(developer)s,
                    %(ch_characters)s, %(en_characters)s, %(total_characters)s, %(create_timestamp)s);
            """
            self.pg_cursor.execute(insert_query, log_data)
            self.pg_conn.commit()

    # 其他方法如 analyze, init_etl_bq, etl_summary 等
