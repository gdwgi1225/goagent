@set GEVENT_LOOP=uvent.loop.UVLoop
@set GEVENT_RESOLVER=gevent.resolver_thread.Resolver
@set LISTEN_VISIBLE=1
@"%~dp0python27.exe" "%~dp0proxy.py" || pause
