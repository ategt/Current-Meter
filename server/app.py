from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True

socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory(os.path.join("..","client","distribution"),"index.html", as_attachment=False)

@app.route('/<path:filename>')
def socket_file(filename):
    return send_from_directory(os.path.join("..","client","distribution"), filename, as_attachment=False)

@app.route('/reading/', methods={"GET"})
def get_readings():
	data = request.get_json()

	return flask.jsonify(result='OK')

@socketio.on('board response event')
def test_sensor(message):
    emit('board response broadcast', {'data': message['data']}, broadcast=True)

@app.after_request
def add_header(response):
  response.headers['Access-Control-Allow-Origin'] = "*"
  response.headers['Access-Control-Allow-Headers'] = "*"

  return response

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass

if __name__ == '__main__':
    socketio.run(app)