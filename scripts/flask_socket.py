import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from threading import Thread, Event
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

logging.basicConfig(level=logging.INFO)
logger= logging.getLogger(__name__)

DIRECTORY = f"{Path.home()}/Portfolio-Backend/portfolios"
today_date = datetime.now().strftime('%Y%m%d')

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
background_thread_running = Event()

def get_portf_data():
    combined_portf_object = {}
    for file in os.listdir(DIRECTORY):
        if today_date in file:
            f = open(f'{DIRECTORY}/{file}','r')
            data = json.load(f)
            combined_portf_object[file] = data
    return combined_portf_object

def background_thread():
    while True:
        data = get_portf_data()
        socketio.emit('data',data)
        time.sleep(0.2)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('data',get_portf_data())
    if not background_thread_running.is_set():
        background_thread_running.set()
        thread= Thread(target=background_thread)
        thread.start()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)
                                        