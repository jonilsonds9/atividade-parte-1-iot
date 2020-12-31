import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

eventlet.monkey_patch()

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'jonilson'
app.config['MQTT_PASSWORD'] = '123123qwe'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

@app.route('/')
def index():
    mqtt.subscribe("dev1/lamp1")
    mqtt.subscribe("dev1/lamp2")
    mqtt.subscribe("dev2")
    return render_template('index.html')

@app.route('/dev1/<lamp>/<value>')
def send_message_device1(lamp, value):
    if lamp!="lamp1" and lamp!="lamp2":
        return '<h1>nome do dispositivo inválido!</h1><br><h3>O nome deve ser "lamp1" ou "lamp2"</h3>'
    if int(value) < 0 or int(value) > 1:
        return '<h1>Valor inválido!</h1><br><h3>Os valores aceitos são: 0 ou 1</h3>'
    mqtt.publish('dev1/'+lamp, value)
    return '<h1>Mensagem enviada!</h1><br><h3>Dispositivo: '+ lamp +' | Valor: '+ value +'</h3>'


@app.route('/dev2/<value>')
def send_message_device2(value):
    if int(value) < 0 or int(value) >3:
        return '<h1>Valor inválido!</h1><br><h3>Os valores aceitos são: 0,1,2 ou 3</h3>'
    mqtt.publish('dev2', value)
    return '<h1>Mensagem enviada!</h1><br><h3>Dispositivo: dev2 | Valor: '+ value +'</h3>'


socketio.run(app, host='0.0.0.0', port=8080, use_reloader=False, debug=True)