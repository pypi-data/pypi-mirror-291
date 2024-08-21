# botrun-log

**botrun-log** 是一個用於將操作記錄儲存到 Google BigQuery 和 PostgreSQL 的 Python 套件，並提供 ETL 操作功能。此套件適用於記錄使用者行為，並能進行資料的分析和統計。

## 特色

- 支援 Google BigQuery 與 PostgreSQL 資料庫
- 針對機關和使用者的每日字元使用量進行 ETL 操作
- ~~支援加密操作細節，並使用 Google KMS 進行密鑰管理~~ 待開發
- ~~支援多種操作類型的記錄和字元統計~~ 待開發

## 安裝

### 1. 使用 pip 安裝

```bash
pip install botrun-log
```

### 2. 安裝開發環境需求

如果你想進行套件的開發或測試，可以使用以下命令安裝額外的開發需求：

```bash
pip install -e .[dev]
```

## 使用方式

### 1. 初始化 Logger

你可以使用 `Logger` 類別來初始化並選擇儲存資料的資料庫（BigQuery 或 PostgreSQL）。兩者的參數有一些不同，請根據你的需求進行配置。

#### BigQuery 初始化參數

```python
from botrun_log import Logger

logger = Logger(
    department='test_org',
    db_type='bigquery',
    credentials_path='/path/to/your/credentials.json',  # Google Cloud Service Account 憑證路徑
    project_id='your_project_id',  # Google Cloud 專案 ID
    dataset_name='your_dataset_name'  # BigQuery 資料集名稱
)
```

#### PostgreSQL 初始化參數

```python
from botrun_log import Logger

logger = Logger(
    department='test_org',
    db_type='postgresql',
    pg_config={
        'dbname': 'botrun_db',
        'user': 'botrun_user',
        'password': 'botrun_password',
        'host': 'localhost',
        'port': '5432'
    }  # PostgreSQL 連線配置
)
```

#### 環境變數

`botrun-log` 使用 `.env` 檔案來讀取敏感資訊，如 AES 加密密鑰、Google Cloud 的憑證路徑、專案 ID 等。這樣可以避免在程式碼中寫入這些敏感資訊，提升安全性。你需要在專案根目錄建立 `.env` 檔案並設置以下變數：

```
BOTRUN_LOG_DEPARTMENT=test_org
BOTRUN_LOG_AES_KEY=your_base64_encoded_aes_key
BOTRUN_LOG_CREDENTIALS_PATH=/path/to/your/credentials.json
BOTRUN_LOG_PROJECT_ID=your_project_id
BOTRUN_LOG_DATASET_NAME=your_dataset_name
```

### 2. 插入記錄

`LogEntry` 是用來封裝每次操作的記錄物件。以下是必填與選填欄位的說明：

#### 必填欄位

- `timestamp`: 操作的時間戳，必須是符合 ISO 8601 標準的時間格式。
- `domain_name`: 操作所屬的網域名稱。
- `user_department`: 使用者所屬的部門或機關。
- `user_name`: 使用者的名稱或帳號。
- `source_ip`: 發出操作請求的 IP 地址。
- `session_id`: 當前操作的工作階段 ID。
- `action_type`: 操作類型（如 "登入"、"登出"、"交談"、"上傳檔案" 等）。
- `developer`: 記錄這次操作的開發者名稱或寫入記錄的套件名稱。

#### 選填欄位

- `action_details`: 操作的具體內容，可以是加密的 JSON 字串。
- `model`: 使用的模型名稱（如 "gpt-4o"）。
- `botrun`: 使用的波特人（如 "波程.botrun"）。
- `user_agent`: 使用者的客戶端資訊。
- `resource_id`: 與此次操作相關的資源 ID（如上傳的文件等）。

插入記錄範例：

```python
from botrun_log import LogEntry

log_entry = LogEntry(
    timestamp="2021-01-01T00:00:00Z",
    domain_name='botrun.ai',
    user_department="test_org",
    user_name="user_1",
    source_ip="127.0.0.1",
    session_id="session_1",
    action_type="交談",
    developer="JcXGTcW",
    action_details="~!@#$%^&*()_+台灣No.1",
    model="gpt-4o",
    botrun="波程.botrun",
    user_agent="user_agent",
    resource_id="resource_1"
)
logger.insert_log(log_entry)
```

### 3. 執行 ETL 操作

`ETLManager` 提供了針對日常字元使用量的 ETL 操作，並將結果寫入指定的資料庫中。根據使用的資料庫類型，BigQuery 和 PostgreSQL 的程式碼會略有不同。

#### BigQuery 的 ETL 操作

```python
from botrun_log import ETLManager
from datetime import date

etl_manager = ETLManager(db_type='bigquery', credentials_path='/path/to/your/credentials.json')
etl_manager.write_etl_summary(department="test_org", date=date(2021, 1, 1))
```

#### PostgreSQL 的 ETL 操作

```python
from botrun_log import ETLManager
from datetime import date

etl_manager = ETLManager(db_type='postgresql', pg_config={
    'dbname': 'botrun_db',
    'user': 'botrun_user',
    'password': 'botrun_password',
    'host': 'localhost',
    'port': '5432'
})
etl_manager.write_etl_summary(department="test_org", date=date(2021, 1, 1))
```

### 4. 獲取 ETL 結果

你可以使用 `read_etl_summary` 方法來讀取指定日期範圍內的字元使用量統計結果。

```python
results = etl_manager.read_etl_summary(start_date=date(2021, 1, 1), end_date=date(2021, 1, 1), department="test_org")
for result in results:
    print(result)
```

## 資料庫欄位說明

### 日誌表 ({department}_logs)

- `timestamp`: 操作的時間戳 (TIMESTAMP)
- `domain_name`: 操作所屬的網域名稱 (STRING)
- `user_department`: 使用者所屬的部門或機關 (STRING)
- `user_name`: 使用者的名稱或帳號 (STRING)
- `source_ip`: 發出操作請求的 IP 地址 (STRING)
- `session_id`: 當前操作的工作階段 ID (STRING)
- `action_type`: 操作類型 (STRING)
- `developer`: 記錄這次操作的開發者名稱或寫入記錄的套件名稱 (STRING)
- `action_details`: 操作的具體內容 (STRING)
- `model`: 使用的模型名稱 (STRING)
- `botrun`: 使用的 botrun 版本 (STRING)
- `user_agent`: 使用者的客戶端資訊 (STRING)
- `resource_id`: 與此次操作相關的資源 ID (STRING)
- `ch_characters`: 中文字元數量 (INTEGER)
- `en_characters`: 英文字元數量 (INTEGER)
- `total_characters`: 總字元數量 (INTEGER)

### ETL 摘要表 (daily_character_usage)

- `date`: 日期 (DATE)
- `department`: 部門或機關 (STRING)
- `user_name`: 使用者名稱 (STRING)
- `ch_characters`: 中文字元使用量 (INTEGER)
- `en_characters`: 英文字元使用量 (INTEGER)

## 測試

套件使用 `pytest` 進行單元測試。你可以在專案根目錄執行以下命令來跑測試：

```bash
pytest
```

## 貢獻

歡迎貢獻！如有問題或建議，請透過 [issues](https://github.com/bohachu/bigquery_log_jc/issues) 頁面與我們聯繫。

## 授權

此專案採用 [MIT License](https://opensource.org/licenses/MIT) 授權。