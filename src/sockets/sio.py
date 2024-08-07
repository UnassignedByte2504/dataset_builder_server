import socketio

# Create a new AsyncServer instance
sio = socketio.AsyncServer(async_mode='asgi')

# Create an ASGI app with the Socket.IO server
sio_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
async def disconnect(sid):
    print('Client disconnected:', sid)
