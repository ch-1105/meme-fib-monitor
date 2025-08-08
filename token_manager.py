import json
from typing import List, Dict, Any
from settings import TOKEN_DATA_FILE
import threading

# A lock to ensure thread-safe writes to the JSON file
file_lock = threading.Lock()

def _read_tokens() -> List[Dict[str, Any]]:
    """Reads all tokens from the JSON file."""
    try:
        with open(TOKEN_DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _write_tokens(tokens: List[Dict[str, Any]]) -> None:
    """Writes a list of tokens to the JSON file."""
    with file_lock:
        with open(TOKEN_DATA_FILE, 'w') as f:
            json.dump(tokens, f, indent=2)

def add_token(token_address: str, custom_name: str, high_price: float, low_price: float) -> bool:
    """Adds a new token to the list. Returns False if a token with the same name already exists."""
    tokens = _read_tokens()
    if any(t['custom_name'] == custom_name for t in tokens):
        return False  # Duplicate name
    
    tokens.append({
        "token_address": token_address,
        "custom_name": custom_name,
        "high_price": high_price,
        "low_price": low_price
    })
    _write_tokens(tokens)
    return True

def delete_token(custom_name: str) -> bool:
    """Deletes a token by its custom name. Returns False if the token was not found."""
    tokens = _read_tokens()
    original_count = len(tokens)
    
    tokens = [t for t in tokens if t['custom_name'] != custom_name]
    
    if len(tokens) < original_count:
        _write_tokens(tokens)
        return True
    return False

def list_tokens() -> List[Dict[str, Any]]:
    """Returns the full list of all monitored tokens."""
    return _read_tokens()

def update_token(custom_name: str, new_high: float, new_low: float) -> bool:
    """Updates the high and low prices of a token by its custom name."""
    tokens = _read_tokens()
    token_found = False
    for t in tokens:
        if t['custom_name'] == custom_name:
            t['high_price'] = new_high
            t['low_price'] = new_low
            token_found = True
            break
    
    if token_found:
        _write_tokens(tokens)
        return True
    return False
