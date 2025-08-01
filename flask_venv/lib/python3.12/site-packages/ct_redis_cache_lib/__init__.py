import logging
from flask import Flask

from ct_redis_cache_lib.cache import CtRedis, configure_redis_pool


def init_cache(app: Flask, logger: logging.Logger) -> CtRedis:
    """
    Initializes the CtRedis library and attaches it to the Flask app instance for centralized Redis caching.

    This function sets up a Redis caching extension for the application, allowing cached values to be
    stored and retrieved using the CtRedis client. It adds the CtRedis instance to the app’s extensions
    for easy access throughout the application, configured with caching timeout and pooling settings.

    Parameters:
    -----------
    app : Flask
        The Flask application instance where the Redis extension will be initialized.
    logger : logging.Logger
        The logger instance for logging cache-related information, errors, and debugging.

    Configuration:
    --------------
    `app.config['REDIS_CACHE']`: bool
        Boolean flag indicating whether Redis caching is enabled.
    `app.config['REDIS_CACHE_EXPIRE_TIME']`: int
        Expiration time for cached data, in seconds.
    `app.config['CACHE_REDIS_HOST']`: str
        Redis Host.
    `app.config['CACHE_REDIS_PORT']`: int
        Redis Port.
    `app.config['CACHE_CLIENT_NAME']`: str
        Client name.

    Cache Key Specification:
    ------------------------
    - To access nested attribute values from a dictionary or an object, prefix the key with a `$`:
      - For a dictionary: `template_cache_key='idle_time_value:$dict[key1][key2]'`
      - For an object: `template_cache_key='idle_time_value:$obj.key1.key2'`
    - To use a static string as part of the cache key, specify it without a `$`:
      - Example: `template_cache_key='idle_time'` will set the cache key directly to "idle_time".

    Usage:
    ------
    ```python
    from flask import Flask
    from ct_redis_cache_lib import init_cache
    import logging

    app = Flask(__name__)
    logger = logging.getLogger(__name__)

    # Initialize the Redis cache
    ct_redis = init_cache(app, logger)

    # Example usage of Redis caching with the decorator
    @ct_redis.cache(template_cache_key='idle_time_value:$idle_time', field='$idle_time')
    def get_idle_time_value(idle_time: str) -> str:
        # function logic here
    ```

    Returns:
    --------
    CtRedis
        The initialized CtRedis instance, configured for the application.
    """

    redis_pool = configure_redis_pool(
        host=app.config['CACHE_REDIS_HOST'],
        port=app.config['CACHE_REDIS_PORT'],
        client_name=app.config['CACHE_CLIENT_NAME'],
        max_connections=30,
        cache_enabled=app.config['REDIS_CACHE']
    )

    redis_instance = CtRedis(app.config['REDIS_CACHE'], logger,
                             redis_pool, app.config['REDIS_CACHE_EXPIRE_TIME'])

    app.extensions['ct_redis'] = redis_instance
    return redis_instance
