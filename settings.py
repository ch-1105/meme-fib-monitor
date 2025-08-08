import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 基础配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# 确保数据目录存在
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Telegram配置
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# -- Refactor Settings --

# 价格查询 API 的 URL 模板，{tokens} 将被替换为逗号分隔的代币地址
PRICE_API_URL_TEMPLATE = os.getenv('PRICE_API-URL')

# 斐波那契点位提醒的浮动范围 (例如 0.05 表示 ±5%)
FIB_LEVEL_TOLERANCE = 0.05

# 默认的代币价格下限（用于斐波那契计算）
DEFAULT_LOW_PRICE = 6000.0

# 存储用户代币信息的文件路径
TOKEN_DATA_FILE = os.path.join(BASE_DIR, 'meme-fib-monitor', 'tokens.json')

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'meme_fib_monitor.log')

# 默认配置
DEFAULT_CONFIG = {
    'tokens': []
}