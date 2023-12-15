from flask import Flask, redirect, send_from_directory, request
from dotenv import load_dotenv
load_dotenv('.env')
from os import getenv
from json import dumps

from pipeline import PipeLine
from position import Position
from config import Config
import gps
import running_stats


app = Flask(__name__)

@app.route('/app/<path:path>')
def serve_static(path):
    return send_from_directory('pwa', path)
 

@app.route('/')
def serve_app():
    return redirect('/app/index.html')


@app.route('/api/packets')
def get_packets():
    packets = running_stats.stats.get_packets()
    ready = list(map(lambda p: p.serializable(), packets))
    return dumps(ready)


@app.route('/api/gps')
def get_gps():
    position: Position = gps.global_gps.current_position()
    return dumps(position.serializable())

@app.route('/api/metadata')
def get_metadata():
    config = Config.from_file(getenv('CONFIG_FILE'))
    return dumps({"name":getenv('NAME'), "WEBSOCKET_PORT": getenv("WEBSOCKET_PORT"),"gps": config.gps, "pipeline": config.pipeline})

if __name__ == "__main__":
    config = Config.from_file(getenv('CONFIG_FILE'))
    gps.global_gps = gps.GPS_Factory(config).get_gps()
    pipeline = PipeLine(config)
    app.run(debug=False, port=getenv("PORT"), host="0.0.0.0")
    pipeline.close()
    gps.global_gps.close()

