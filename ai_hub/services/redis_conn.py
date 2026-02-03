import os
import ssl
import logging

from redis import Redis

logger = logging.getLogger(__name__)


def _select_redis_url():
    for key in ("REDIS_URL", "HEROKU_REDIS_TEAL_URL", "HEROKU_REDIS_AMBER_URL"):
        value = os.getenv(key, "").strip()
        if value:
            return key, value
    return "", ""


def get_redis_connection():
    key, url = _select_redis_url()
    if not url:
        logger.warning("Redis URL not configured.")
        return None
    logger.info("Redis connection configured via %s", key)
    if url.startswith("rediss://"):
        return Redis.from_url(url, ssl_cert_reqs=ssl.CERT_NONE)
    return Redis.from_url(url)
