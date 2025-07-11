from fastapi import Request
import time
from collections import defaultdict
from typing import Dict, Tuple
from .exceptions import RateLimitExceeded

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def _cleanup_old_requests(self, ip: str):
        """Remove requests older than 1 minute"""
        current_time = time.time()
        self.requests[ip] = [
            req_time for req_time in self.requests[ip]
            if current_time - req_time < 60
        ]
    
    def is_rate_limited(self, ip: str) -> bool:
        """Check if the IP has exceeded the rate limit"""
        self._cleanup_old_requests(ip)
        
        if len(self.requests[ip]) >= self.requests_per_minute:
            return True
        
        self.requests[ip].append(time.time())
        return False

async def rate_limit_middleware(request: Request, call_next):
    """ASGI middleware for rate limiting"""
    rate_limiter = RateLimiter()
    ip = request.client.host if request.client else "0.0.0.0"
    
    if rate_limiter.is_rate_limited(ip):
        raise RateLimitExceeded()
    
    response = await call_next(request)
    return response
