
# Fibonacci Levels Price Alerter

This project is a Python-based monitoring tool that tracks the market capitalization of specified cryptocurrencies and sends real-time alerts via Telegram based on Fibonacci retracement levels and new price highs.

## ✨ Features

- **Real-time Price Monitoring**: Fetches current market cap data for a list of tokens.
- **Fibonacci Retracement Alerts**: Sends alerts when a token's price approaches key Fibonacci levels (e.g., 38.2%, 50.0%, 61.8%).
- **New High Alerts**: Instantly notifies you when a token's price surpasses its previously recorded all-time high.
- **Dynamic Price Range Updates**: Automatically updates the high-price benchmark whenever a new high is detected, ensuring that Fibonacci levels are always calculated from the most relevant price range.
- **Telegram Integration**: Delivers all alerts directly to a specified Telegram chat.
- **Configuration via JSON**: Easily manage the list of monitored tokens through a simple `tokens.json` file.

## 📂 Project Structure

```
meme-fib-monitor/
├── .env                  # Stores environment variables (API keys, etc.)
├── main.py               # Main application entry point, contains the monitoring loop
├── fibonacci_calculator.py # Calculates Fibonacci retracement and extension levels
├── price_fetcher.py      # Fetches token prices from an external API
├── token_manager.py      # Manages the list of monitored tokens (CRUD operations on tokens.json)
├── telegram_bot.py       # Handles sending alerts via the Telegram Bot API
├── settings.py           # Application settings and constants
├── tokens.json           # Database of tokens to monitor
├── requirements.txt      # Python dependencies
├── logs/                   # Directory for log files
│   └── rsi_monitor.log
└── utils/                  # Utility modules
    ├── logger.py         # Logging configuration
    └── formatters.py     # Data formatting helpers
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A Telegram Bot Token and Chat ID

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd meme-fib-monitor
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment:**
    Create a `.env` file in the root directory and add your Telegram credentials:
    ```
    TELEGRAM_BOT_TOKEN="your_bot_token_here"
    TELEGRAM_CHAT_ID="your_chat_id_here"
    PRICE_API-URL="your_price_api_url_here"
    ```

5.  **Set up your tokens:**
    Edit the `tokens.json` file to add the tokens you want to monitor. The `high_price` should be the initial all-time high you want to track.
    ```json
    [
      {
        "token_address": "0x123...",
        "custom_name": "MyToken",
        "high_price": 1000000,
        "low_price": 100000
      }
    ]
    ```

### Usage

Run the main application:
```bash
python main.py
```
The application will start, and you will begin receiving alerts in your configured Telegram chat.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
