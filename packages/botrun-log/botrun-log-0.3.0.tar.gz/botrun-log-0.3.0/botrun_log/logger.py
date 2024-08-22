import os
import datetime as dt
import pytz
from .crypto_manager import CryptoManager
from .log_entry import TextLogEntry, AudioLogEntry, ImageLogEntry, VectorDBLogEntry
from .etl_manager import ETLManager
from .database_manager import DatabaseManager

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
        str_aes_key = str_aes_key or os.getenv('BOTRUN_LOG_AES_KEY')

        self.db_manager = DatabaseManager(db_type, pg_config, credentials_path, project_id, dataset_name)
        self.db_manager.initialize_database(self.department)

        self.crypto_manager = CryptoManager(str_aes_key)
        self.etl_manager = ETLManager(self.db_manager)

    def insert_text_log(self, log_entry: TextLogEntry):
        self._insert_log(log_entry, f"{self.department}_logs")

    def insert_audio_log(self, log_entry: AudioLogEntry):
        self._insert_log(log_entry, f"{self.department}_audio_logs")

    def insert_image_log(self, log_entry: ImageLogEntry):
        self._insert_log(log_entry, f"{self.department}_image_logs")

    def insert_vector_log(self, log_entry: VectorDBLogEntry):
        self._insert_log(log_entry, f"{self.department}_vector_logs")

    def _insert_log(self, log_entry, table_name):
        log_data = log_entry.to_dict()
        log_data["create_timestamp"] = dt.datetime.now(tz=pytz.timezone("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
        if log_data["action_details"]:
            log_data["action_details"] = self.crypto_manager.encrypt(log_data["action_details"])

        self.db_manager.insert_rows(table_name, [log_data])

    # 其他方法如 analyze, init_etl_bq, etl_summary 等保持不變