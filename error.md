async-llm-api       | INFO:     172.20.0.1:39262 - "GET /openapi.json HTTP/1.1" 200 OK
async-llm-api       | INFO:     172.20.0.1:39276 - "POST /batch HTTP/1.1" 500 Internal Server Error
async-llm-api       | ERROR:    Exception in ASGI application
async-llm-api       |   + Exception Group Traceback (most recent call last):
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/uvicorn/protocols/http/httptools_impl.py", line 421, in run_asgi
async-llm-api       |   |     result = await app(  # type: ignore[func-returns-value]
async-llm-api       |   |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
async-llm-api       |   |     return await self.app(scope, receive, send)
async-llm-api       |   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/fastapi/applications.py", line 1159, in __call__
async-llm-api       |   |     await super().__call__(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/applications.py", line 90, in __call__
async-llm-api       |   |     await self.middleware_stack(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/middleware/errors.py", line 186, in __call__
async-llm-api       |   |     raise exc
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/middleware/errors.py", line 164, in __call__
async-llm-api       |   |     await self.app(scope, receive, _send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
async-llm-api       |   |     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
async-llm-api       |   |     raise exc
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
async-llm-api       |   |     await app(scope, receive, sender)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
async-llm-api       |   |     await self.app(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 660, in __call__
async-llm-api       |   |     await self.middleware_stack(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 680, in app
async-llm-api       |   |     await route.handle(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/routing.py", line 276, in handle
async-llm-api       |   |     await self.app(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/fastapi/routing.py", line 134, in app
async-llm-api       |   |     await wrap_app_handling_exceptions(app, request)(scope, receive, send)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
async-llm-api       |   |     raise exc
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
async-llm-api       |   |     await app(scope, receive, sender)
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/fastapi/routing.py", line 120, in app
async-llm-api       |   |     response = await f(request)
async-llm-api       |   |                ^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/fastapi/routing.py", line 674, in app
async-llm-api       |   |     raw_response = await run_endpoint_function(
async-llm-api       |   |                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/usr/local/lib/python3.12/site-packages/fastapi/routing.py", line 328, in run_endpoint_function
async-llm-api       |   |     return await dependant.call(**values)
async-llm-api       |   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/app/app/api/routes/batch.py", line 20, in submit_batch
async-llm-api       |   |     batch_results = await engine.batch_execute(
async-llm-api       |   |                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/app/app/services/batch_processor.py", line 128, in batch_execute
async-llm-api       |   |     async with asyncio.TaskGroup() as tg:
async-llm-api       |   |                ^^^^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/usr/local/lib/python3.12/asyncio/taskgroups.py", line 71, in __aexit__
async-llm-api       |   |     return await self._aexit(et, exc)
async-llm-api       |   |            ^^^^^^^^^^^^^^^^^^^^^^^^^^
async-llm-api       |   |   File "/usr/local/lib/python3.12/asyncio/taskgroups.py", line 164, in _aexit
async-llm-api       |   |     raise BaseExceptionGroup(
async-llm-api       |   | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
async-llm-api       |   +-+---------------- 1 ----------------
async-llm-api       |     | Traceback (most recent call last):
async-llm-api       |     |   File "/app/app/services/batch_processor.py", line 57, in _run_single
async-llm-api       |     |     provider_result, attempts = await retry_with_backoff(
async-llm-api       |     |                                       ^^^^^^^^^^^^^^^^^^^
async-llm-api       |     | TypeError: retry_with_backoff() got an unexpected keyword argument 'max_attempts'
async-llm-api       |     | 
async-llm-api       |     | During handling of the above exception, another exception occurred:
async-llm-api       |     | 
async-llm-api       |     | Traceback (most recent call last):
async-llm-api       |     |   File "/app/app/services/batch_processor.py", line 122, in wrapped
async-llm-api       |     |     results[index] = await self._run_single(
async-llm-api       |     |                      ^^^^^^^^^^^^^^^^^^^^^^^
async-llm-api       |     |   File "/app/app/services/batch_processor.py", line 87, in _run_single
async-llm-api       |     |     usage = ProviderUsage(
async-llm-api       |     |             ^^^^^^^^^^^^^^
async-llm-api       |     | TypeError: ProviderUsage.__init__() got an unexpected keyword argument 'input_tokens'
async-llm-api       |     +------------------------------------