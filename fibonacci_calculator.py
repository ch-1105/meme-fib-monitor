from typing import Dict

FIB_LEVELS = {
    # Retracement Levels (High to Low)
    "retracement_100_0": 1.0,    # High
    "retracement_78_6": 0.786,
    "retracement_61_8": 0.618,
    "retracement_50_0": 0.5,
    "retracement_38_2": 0.382,
    "retracement_23_6": 0.236,
    "retracement_0_0": 0.0,      # Low

    # Extension Levels (based on the range)
    "extension_161_8": 1.618,
    "extension_261_8": 2.618,
    "extension_361_8": 3.618,
}


def calculate_fib_levels(high_price: float, low_price: float) -> Dict[str, float]:
    """
    Calculates the Fibonacci retracement and extension levels based on a high and low price.
    Returns a dictionary mapping level name to its price.
    """
    if high_price <= low_price:
        return {}
        
    price_range = high_price - low_price
    
    fib_prices = {
        level_name: low_price + price_range * ratio
        for level_name, ratio in FIB_LEVELS.items()
    }
    
    return fib_prices