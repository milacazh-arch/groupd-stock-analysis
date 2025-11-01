import os

# Tushare API configuration
# Set your Tushare token here or set TUSHARE_TOKEN environment variable
TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN', 'cd0342a926136018b801150b53f040b5175b7f785c0c0f092fc0c013')

# Flask configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Data retrieval settings
YEARS_OF_INCOME_DATA = 3

# Stock code examples for reference
STOCK_CODE_EXAMPLES = [
    '000001.SZ',  # 平安银行
    '600000.SH',  # 浦发银行
    '300001.SZ',  # 特锐德
    '688001.SH',  # 华兴源创
]
