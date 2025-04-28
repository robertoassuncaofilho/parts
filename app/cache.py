from redis import Redis
import os
import json
import logging
from typing import Optional, List
from app.schemas.part import WordCount

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Cache:
    def __init__(self):
        self.redis = Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
        self.key = "parts:common-words"
        self.expire_time = 60 * 60 * 24  # 24 hours

    def get(self) -> Optional[List[WordCount]]:
        """Get cached common words."""
        try:
            data = self.redis.get(self.key)
            if data:
                return [WordCount(**item) for item in json.loads(data)]
            return None
        except Exception as e:
            logger.error(f"Error getting cache: {str(e)}")
            return None

    def set(self, words: List[WordCount]):
        """Cache common words."""
        try:
            data = [word.model_dump() for word in words]
            self.redis.setex(self.key, self.expire_time, json.dumps(data))
        except Exception as e:
            logger.error(f"Error setting cache: {str(e)}")

    def clear(self):
        """Clear the cache."""
        try:
            self.redis.delete(self.key)
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")

# Create a singleton instance
cache = Cache() 