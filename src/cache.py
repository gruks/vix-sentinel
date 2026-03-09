"""
Caching Module
Simple pickle-based cache for persistent data storage
"""
import os
import pickle
import time
from typing import Any, Optional


# Cache directory
CACHE_DIR = ".cache"


def _ensure_cache_dir():
    """Ensure the cache directory exists."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def _get_cache_path(key: str) -> str:
    """Get the file path for a cache key."""
    # Sanitize key to be a valid filename
    safe_key = key.replace('/', '_').replace('\\', '_').replace(':', '_')
    return os.path.join(CACHE_DIR, f"{safe_key}.pkl")


def get_cached(key: str) -> Optional[Any]:
    """
    Retrieve cached data.
    
    Args:
        key: Cache key
    
    Returns:
        Cached value if valid, None otherwise
    """
    _ensure_cache_dir()
    
    cache_path = _get_cache_path(key)
    
    if not os.path.exists(cache_path):
        return None
    
    try:
        with open(cache_path, 'rb') as f:
            cache_data = pickle.load(f)
        
        # Check if cache is expired
        if time.time() > cache_data['expires_at']:
            # Remove expired cache
            os.remove(cache_path)
            return None
        
        return cache_data['value']
        
    except Exception as e:
        print(f"Error reading cache for {key}: {e}")
        return None


def set_cached(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Store data in cache.
    
    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds (default 1 hour)
    
    Returns:
        True if successful, False otherwise
    """
    _ensure_cache_dir()
    
    cache_path = _get_cache_path(key)
    
    try:
        cache_data = {
            'value': value,
            'created_at': time.time(),
            'expires_at': time.time() + ttl
        }
        
        with open(cache_path, 'wb') as f:
            pickle.dump(cache_data, f)
        
        return True
        
    except Exception as e:
        print(f"Error writing cache for {key}: {e}")
        return False


def clear_cache(key: str = None) -> bool:
    """
    Clear cached data.
    
    Args:
        key: Specific cache key to clear, or None to clear all
    
    Returns:
        True if successful
    """
    _ensure_cache_dir()
    
    try:
        if key is None:
            # Clear all cache files
            for filename in os.listdir(CACHE_DIR):
                if filename.endswith('.pkl'):
                    os.remove(os.path.join(CACHE_DIR, filename))
        else:
            cache_path = _get_cache_path(key)
            if os.path.exists(cache_path):
                os.remove(cache_path)
        
        return True
        
    except Exception as e:
        print(f"Error clearing cache: {e}")
        return False


def get_cache_info(key: str) -> Optional[dict]:
    """
    Get information about cached data.
    
    Args:
        key: Cache key
    
    Returns:
        Dictionary with cache info, or None if not found
    """
    _ensure_cache_dir()
    
    cache_path = _get_cache_path(key)
    
    if not os.path.exists(cache_path):
        return None
    
    try:
        with open(cache_path, 'rb') as f:
            cache_data = pickle.load(f)
        
        return {
            'key': key,
            'created_at': cache_data['created_at'],
            'expires_at': cache_data['expires_at'],
            'is_expired': time.time() > cache_data['expires_at']
        }
        
    except Exception as e:
        print(f"Error getting cache info for {key}: {e}")
        return None
