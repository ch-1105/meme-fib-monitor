import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from settings import TELEGRAM_BOT_TOKEN, DEFAULT_LOW_PRICE
import token_manager
from utils.formatters import format_market_cap, parse_market_cap

# 全局Bot实例，用于从外部发送消息
bot_instance: Bot = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """发送欢迎消息和命令说明"""
    print(f"当前 chat_id: {update.message.chat.id}")
    await update.message.reply_text(
        "欢迎使用斐波那契点位监控机器人！\n"
        "可用命令：\n"
        "/add <token_address> <custom_name> <high_price> - 添加一个新的代币监控 (价格可使用 1M, 100K 等格式)\n"
        "/delete <custom_name> - 删除一个代币监控\n"
        "/list - 查看所有正在监控的代币"
    )


async def add_token_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /add 命令"""
    try:
        if len(context.args) != 3:
            await update.message.reply_text("格式错误！请使用：/add <token_address> <custom_name> <high_price>")
            return

        token_address = context.args[0]
        custom_name = context.args[1]
        high_price_str = context.args[2]

        # 解析用户输入的价格
        high_price = parse_market_cap(high_price_str)
        # 假设最低价也支持这种格式，如果需要的话
        low_price = DEFAULT_LOW_PRICE  # 如果需要，也可以解析

        success = token_manager.add_token(
            token_address=token_address,
            custom_name=custom_name,
            high_price=high_price,
            low_price=low_price
        )

        if success:
            # 格式化价格以供显示
            formatted_high_price = format_market_cap(high_price)
            formatted_low_price = format_market_cap(low_price)

            await update.message.reply_text(
                f"✅ 添加成功！\n"
                f"名称: {custom_name}\n"
                f"地址: {token_address}\n"
                f"最高价: {formatted_high_price}\n"
                f"最低价: {formatted_low_price}"
            )
        else:
            await update.message.reply_text(f"添加失败：自定义名称 '{custom_name}' 已存在。")

    except ValueError as e:
        await update.message.reply_text(f"添加失败：{e}")
    except Exception as e:
        await update.message.reply_text(f"添加时发生未知错误：{e}")


async def delete_token_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /delete 命令"""
    try:
        if len(context.args) != 1:
            await update.message.reply_text("格式错误！请使用：/delete <custom_name>")
            return

        custom_name = context.args[0]
        success = token_manager.delete_token(custom_name)

        if success:
            await update.message.reply_text(f"✅ 已成功删除 '{custom_name}'。")
        else:
            await update.message.reply_text(f"删除失败：未找到名称为 '{custom_name}' 的代币。")

    except Exception as e:
        await update.message.reply_text(f"删除时发生未知错误：{e}")


async def list_tokens_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /list 命令"""
    tokens = token_manager.list_tokens()
    if not tokens:
        await update.message.reply_text("当前没有正在监控的代币。")
        return

    message = "📊 **当前监控列表**:\n\n"
    for token in tokens:
        # 格式化价格以供显示
        formatted_high = format_market_cap(token['high_price'])
        formatted_low = format_market_cap(token['low_price'])

        message += (
            f"🔹 **{token['custom_name']}**\n"
            f"   - 地址: `{token['token_address']}`\n"
            f"   - 最高价: `{formatted_high}`\n"
            f"   - 最低价: `{formatted_low}`\n"
            f"-------------------\n"
        )

    # 注意：Telegram的MarkdownV2需要对特殊字符进行转义，但在这里我们没有使用
    # `.` 或 `-` 等需要转义的字符，所以暂时是安全的。
    await update.message.reply_text(message, parse_mode='Markdown')


async def send_alert(chat_id: str, message: str):
    """由监控循环调用的函数，用于发送提醒消息"""
    if bot_instance:
        try:
            await bot_instance.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"发送Telegram提醒时出错: {e}")
    else:
        print("Telegram Bot尚未初始化，无法发送提醒。")


def run_bot():
    """启动并运行Telegram机器人"""
    global bot_instance

    # 为这个新线程创建一个新的事件循环
    asyncio.set_event_loop(asyncio.new_event_loop())

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 在启动时获取Bot实例
    bot_instance = application.bot

    # 注册命令处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_token_handler))
    application.add_handler(CommandHandler("delete", delete_token_handler))
    application.add_handler(CommandHandler("list", list_tokens_handler))

    # 以非阻塞方式运行
    print("Telegram机器人正在启动...")
    application.run_polling()
