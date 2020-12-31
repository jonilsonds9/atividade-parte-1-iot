#!/usr/bin/python3
import paho.mqtt.client as mqtt

topico1="dev1"
topico2="dev2"

lamp1="0"
lamp2="0"
fan="0"

def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("#")

def on_message(client, userdata, msg):
        top_atual = msg.topic
        msg = msg.payload.decode("utf8")
        global lamp1
        global lamp2
        global fan
        print("Topico: "+top_atual+"\tMensagem: "+msg)

        if top_atual==topico1+"/lamp1":
            change_status_lamp1(msg)
        elif top_atual==topico1+"/lamp2":
            change_status_lamp2(msg)
        elif top_atual==topico2:
            change_status_device2(msg)
        elif top_atual=="status":
                print("Status geral")
                print("Lamp1: "+lamp1)
                print("Lamp2: "+lamp2)
                print("Fan: "+fan)

def change_status_lamp1(msg):
    global lamp1
    if msg!=lamp1:
        lamp1 = msg


def change_status_lamp2(msg): 
    global lamp2   
    if msg!=lamp2:
        lamp2 = msg


def change_status_device2(msg):
    global fan
    if int(msg) >= 0 and int(msg) <=3:
        fan = msg


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("jonilson", "123123qwe")
client.connect("broker", 1883, 60)
client.loop_forever()
