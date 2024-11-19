from functools import wraps
from fastapi import Request
import json
from config import settings

def cache_response(timeout=settings.CACHE_TIMEOUT):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get('request')
            if not request:
                return await func(*args, **kwargs)

            cache_key = f"{request.url.path}:{request.query_params}"
            redis = request.app.state.redis

            # Try to get from cache
            cached = redis.get(cache_key)
            if cached:
                return json.loads(cached)

            # Get fresh data
            response = await func(*args, **kwargs)
            
            # Cache the response
            if response:  # Only cache non-empty responses
                redis.setex(
                    cache_key,
                    timeout,
                    json.dumps(response)
                )

            return response
        return wrapper
    return decorator