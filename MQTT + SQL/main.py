import random
import mysql.connector

from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "IUT/Colmar/SAE24/Maison1"
#generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

id_donnee = 0

mydb = mysql.connector.connect(
  host="localhost",
  user="SAE24",
  password="toto",
  database="SAE24"
)

mycursor = mydb.cursor()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def traiter_donnee(id,piece,date,time,temp):
    if id == "B8A5F3569EFF":
        chaine = f"{id};{piece};{date};{time};{temp};"
        file = open("capteur1.csv", "a")
        file.write(chaine + "\n")
        file.close()

    if id == "A72E3F6B79BB":
        chaine = f"{id};{piece};{date};{time};{temp};"
        file = open("capteur2.csv", "a")
        file.write(chaine + "\n")
        file.close()

    timestamp = date + " , " + time
    global id_donnee
    id_donnee += 1
    global mycursor
    sql = "INSERT INTO mysae24_data (data,timestamp,capteur_id) VALUES ( %s, %s, %s)"
    if id == 'A72E3F6B79BB':
        val = (temp,timestamp,3)
    if id == "B8A5F3569EFF":
        val = (temp, timestamp,1)
    mycursor.execute(sql, val)


    mydb.commit()


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        chaine = msg.payload.decode()
        chaine = chaine.split(",")
        id = chaine[0].split("=")[1]
        piece = chaine[1].split("=")[1]
        date = chaine[2].split("=")[1]
        time = chaine[3].split("=")[1]
        temp = chaine[4].split("=")[1]

        traiter_donnee(id,piece,date,time,temp)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


run()