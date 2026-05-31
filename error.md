
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/usr/local/lib/python3.12/site-packages/redis/utils.py", line 249, in async_wrapper

    return await func(*args, **kwargs)

           ^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/usr/local/lib/python3.12/site-packages/redis/asyncio/connection.py", line 1562, in get_connection

    await self.ensure_connection(connection)

  File "/usr/local/lib/python3.12/site-packages/redis/asyncio/connection.py", line 1603, in ensure_connection

    await connection.connect()

  File "/usr/local/lib/python3.12/site-packages/redis/asyncio/connection.py", line 350, in connect

    await self.retry.call_with_retry(

  File "/usr/local/lib/python3.12/site-packages/redis/asyncio/retry.py", line 81, in call_with_retry

    raise error

  File "/usr/local/lib/python3.12/site-packages/redis/asyncio/retry.py", line 69, in call_with_retry

    return await do()

           ^^^^^^^^^^

  File "/usr/local/lib/python3.12/site-packages/redis/asyncio/connection.py", line 407, in connect_check_health

    raise e

redis.exceptions.ConnectionError: Error Multiple exceptions: [Errno 111] Connect call failed ('::1', 6379, 0, 0), [Errno 111] Connect call failed ('127.0.0.1', 6379) connecting to localhost:6379.