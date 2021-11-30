host = '0'
port = None

DEBUG = False

# use random string for your secret key,
# ex: "FDSDFGHksoyHisHtheHauthorHFDSWERE"
FLASK_SECRET_KEY = 'FDSDFGHksoyHisHtheHauthorHFDSWERE'

# DB_CONFIG = '<database>[+<orm_lib>]://[<user>[:<password>]]<host>[:<port>]/[db_name][?charset=utf8]'
# ex: DB_CONFIG = 'mysql+pymysql://user:pass@localhost:3306/db_name?charset=utf8'
# ex: DB_CONFIG = 'sqlite+pysqlite:///db.sqlite3'
DB_CONFIG = 'mysql+pymysql://dashboard:Yang5329@localhost:3306/dashboard?charset=utf8'
DB_POOL_RECYCLE = 600
DB_POOL_SIZE = 20
QUERY_LIMIT = 1
REQUEST_TIMEOUT = 10

# IoTtalk server's 'IP' or 'DomainName' only, without any protocol 'http://' or 'https://'.
# ex: '8.8.8.8' or 'google.com',
CSM_HOST = '127.0.0.1'

# For the demo page without login
# The data format is '<Field Name>':'<token>', examples are shown as follows.
demo_token = {
    'Field1': '65761609-0f1e-4b72-adcf-1ed092454d53',
}

TIMEOUT_STRIKETHROUGH = False

# For login redirect url path check, avoid Open Redirect (ref: CWE-601)
# Allow pattern: http[s]://*.iottalk.tw/* or /*
REDIRECT_REGEX = r"^http[s]?:\/\/[\w.-]*iottalk[2]?\.tw\/|^\/"

SESSION_COOKIE_SECURE = True

RESTART_SERVER_PORT = 5001

i18n = {'English': 'en', '中文': 'zh_Hant_TW', 'ไทย': 'th'}
