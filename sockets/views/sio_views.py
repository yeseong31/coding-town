from config.wsgi import sio


@sio.on('connect')
def on_connect(sid):
    print('Client connected')
    
    
@sio.on('disconnect')
def on_disconnect(sid):
    print('Client disconnected')
