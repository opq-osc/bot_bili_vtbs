import json

import socketio

sio = socketio.Client()

data = {}


def info(vtbs):
    for vtb in vtbs:
        data[vtb['mid']] = dict(
            uname=vtb['uname'],
            uuid=vtb['uuid'],
        )
    print(len(data.keys()))


sio.on('info', info)

sio.connect("wss://api.tokyo.vtbs.moe/socket.io")

try:
    sio.wait()
except Exception:
    raise
finally:
    with open('vtbs.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
