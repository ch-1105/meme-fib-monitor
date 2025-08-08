import asyncio
import threading
import logging
from typing import Dict

from settings import FIB_LEVEL_TOLERANCE, TELEGRAM_CHAT_ID
from token_manager import list_tokens, update_token
from price_fetcher import get_token_prices
from fibonacci_calculator import calculate_fib_levels
from telegram_bot import run_bot, send_alert
from utils.formatters import format_market_cap
from utils.logger import setup_logger

# --- Configuration ---
logger = setup_logger('monitor_log')

# --- State Tracking ---
last_triggered_level: Dict[str, str] = {}

def get_level_percentage(level_name: str) -> float:
    """Extracts the percentage from a Fibonacci level name."""
    parts = level_name.split('_')
    # Handles names like 'retracement_50_0' -> ['retracement', '50', '0']
    if len(parts) == 3:
        return float(f"{parts[1]}.{parts[2]}")
    return 0.0

async def check_fibonacci_levels(token, current_price):
    """
    Checks if the current price hits any Fibonacci retracement levels and sends an alert.
    """
    custom_name = token['custom_name']
    high_price = token['high_price']
    low_price = token['low_price']

    # Only calculate for retracement levels now
    fib_levels = calculate_fib_levels(high_price, low_price)

    for level_name, fib_price in fib_levels.items():
        # We are only interested in retracement levels here
        if 'retracement' not in level_name:
            continue

        if abs(current_price - fib_price) / fib_price <= FIB_LEVEL_TOLERANCE:
            if last_triggered_level.get(custom_name) != level_name:
                last_triggered_level[custom_name] = level_name

                percentage = get_level_percentage(level_name)
                formatted_price = format_market_cap(current_price)

                message = (
                    f"🔔 **价格提醒** 🔔\n\n"
                    f"**代币:** {custom_name}\n"
                    f"**当前市值:** {formatted_price}\n"
                    f"**已到达:** 斐波那契 {percentage:.1f}% 回调点位"
                )

                logger.info(f"Alert for {custom_name}: {message}")
                await send_alert(TELEGRAM_CHAT_ID, message)
                break  # One alert per cycle is enough

async def monitor_loop():
    """
    Main monitoring loop.
    """
    logger.info("Monitoring loop started.")
    while True:
        tokens_to_monitor = list_tokens()
        if not tokens_to_monitor:
            await asyncio.sleep(15)
            continue

        token_addresses = [t['token_address'] for t in tokens_to_monitor]
        
        try:
            prices = await get_token_prices(token_addresses)
            if not prices:
                await asyncio.sleep(15)
                continue

            for token in tokens_to_monitor:
                token_addr = token['token_address']
                if token_addr in prices:
                    current_market_cap = prices[token_addr] * 1_000_000_000
                    custom_name = token['custom_name']

                    # --- Real-time High Price Update Logic ---
                    if current_market_cap > token['high_price'] + 50000:
                        new_high = current_market_cap
                        update_token(custom_name, new_high, token['low_price'])
                        token['high_price'] = new_high  # Update locally for this cycle

                        logger.info(f"New high for {custom_name}! New High: {new_high}")
                        formatted_new_high = format_market_cap(new_high)
                        message = (
                            f"🚀 **新高提醒** 🚀\n\n"
                            f"**代币:** {custom_name}\n"
                            f"**新高市值:** {formatted_new_high}"
                        )
                        await send_alert(TELEGRAM_CHAT_ID, message)
                        # Reset last triggered level on new high to allow immediate retracement alerts
                        last_triggered_level.pop(custom_name, None)

                    # Always check for Fibonacci retracement levels
                    await check_fibonacci_levels(token, current_market_cap)

        except Exception as e:
            logger.error(f"An error occurred in the monitor loop: {e}", exc_info=True)
        
        await asyncio.sleep(15)

def main():
    """
    Main function to start the bot and the monitoring loop.
    """
    logger.info("Starting the application...")
    bot_thread = threading.Thread(target=run_bot, name="TelegramBotThread", daemon=True)
    bot_thread.start()
    logger.info("Telegram bot thread started.")

    try:
        asyncio.run(monitor_loop())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user.")
    finally:
        logger.info("Application shutting down.")

if __name__ == "__main__":
    main()
