import random
import mysql.connector
import datetime
from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "IUT/Colmar/SAE24/Maison1"
#generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

id_donnee = 0
id_capteur = 0

mydb = mysql.connector.connect(
  host="localhost",
  user="SAE24",
  password="toto",
  database="SAE24"
)

mycursor = mydb.cursor()

mycursor.execute("DELETE FROM mysae24_data")
mycursor.execute("DELETE FROM mysae24_capteur")

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

def traiter_donnee(id,piece,date,ti,temp):
    if id == "B8A5F3569EFF":
        chaine = f"{id};{piece};{date};{ti};{temp};"
        file = open("capteur1.csv", "a")
        file.write(chaine + "\n")
        file.close()

    if id == "A72E3F6B79BB":
        chaine = f"{id};{piece};{date};{ti};{temp};"
        file = open("capteur2.csv", "a")
        file.write(chaine + "\n")
        file.close()

    ep = datetime.datetime(1970, 1, 1, 0, 0, 0)
    timestamp = (datetime.datetime.utcnow() - ep).total_seconds()

    global id_donnee
    global id_capteur
    id_donnee += 1
    global mycursor

    sql_select_Query = "select * from mysae24_capteur"
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(sql_select_Query)
    capteurs = cursor.fetchall()
    test = 0
    for row in capteurs:
        mac = row["mac"]
        if mac == id:
            test = 1
    if test == 0:
        id_capteur += 1
        sql = "INSERT INTO mysae24_capteur (id,nom,mac,piece,emplacement) VALUES (%s, %s, %s, %s, %s)"
        val = (id_capteur,id,id,piece,"blank")
        mycursor.execute(sql, val)

    sql = "INSERT INTO mysae24_data (id,data,timestamp,capteur) VALUES (%s, %s, %s, %s)"
    sql_select_Query = "select * from mysae24_capteur"
    cursor = mydb.cursor(dictionary=True)
    cursor.execute(sql_select_Query)
    capteurs = cursor.fetchall()
    test = 0
    for row in capteurs:
        id_capteur = row['id']
        mac = row["mac"]
        if mac == id:
            test = id_capteur
    val = (id_donnee,temp,timestamp,test)
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