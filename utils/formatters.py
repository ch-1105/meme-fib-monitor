import re

def parse_market_cap(market_cap_str: str) -> float:
    """
    Parses a market cap string (e.g., 1.23M, 450.5K) into a float.
    """
    market_cap_str = market_cap_str.upper().strip()
    
    # 使用正则表达式匹配数字和单位
    match = re.match(r'^(\d+\.?\d*)\s*([B|M|K]?)$', market_cap_str)
    
    if not match:
        raise ValueError(f"无效的市值格式: '{market_cap_str}'。请使用 '100K', '1.5M', '2B' 等格式。")

    value_str, unit = match.groups()
    value = float(value_str)

    if unit == 'B':
        return value * 1_000_000_000
    elif unit == 'M':
        return value * 1_000_000
    elif unit == 'K':
        return value * 1_000
    else:
        return value

def format_market_cap(market_cap: float) -> str:
    """
    Formats a market cap float into a human-readable string (e.g., 1.23M, 450.5K).
    """
    if market_cap >= 1_000_000_000:
        return f"{market_cap / 1_000_000_000:.2f}B"
    elif market_cap >= 1_000_000:
        return f"{market_cap / 1_000_000:.2f}M"
    elif market_cap >= 1_000:
        return f"{market_cap / 1_000:.2f}K"
    else:
        return f"{market_cap:.2f}"