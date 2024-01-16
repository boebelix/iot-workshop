import time

import paho.mqtt.client as mqtt

# MQTT-Broker Informationen
broker_address = "192.168.2.100"
port = 1883
topic = "/stat"
username = "admin"
password = "instar"

# Anzahl der Aktoren
anzahl_aktoren = 4

# MQTT-Client erstellen
client = mqtt.Client()

# Benutzername und Passwort setzen
client.username_pw_set(username, password)


# Callback-Funktion für Verbindungsaufbau
def on_connect(client, userdata, flags, rc):
    print("Verbindung hergestellt: " + str(rc))
    # Initialisierung der Aktoren
    # for i in range(1, anzahl_aktoren + 1):
    #     client.publish(topic, f"actor_{i}/POWER/off")


# Callback-Funktion für Nachrichteneingang
def on_message(client, userdata, msg):
    print(f"Nachricht erhalten: {msg.topic} {msg.payload}")


# Callback-Funktion für Verbindungsverlust
def on_disconnect(client, userdata, rc):
    print("Verbindung verloren. Versuche erneut zu verbinden...")


# Callback-Funktion für Publish-Bestätigung
def on_publish(client, userdata, mid):
    print("Nachricht veröffentlicht")


# Callback-Funktion für Subscribe-Bestätigung
def on_subscribe(client, userdata, mid, granted_qos):
    print("Erfolgreich auf Thema abonniert")


# Callback-Funktion für Unsubscribe-Bestätigung
def on_unsubscribe(client, userdata, mid):
    print("Erfolgreich vom Thema abgemeldet")


# Callback-Funktion für Publish-Bestätigung
def on_publish(client, userdata, mid):
    print("Nachricht veröffentlicht")


# Callback-Funktion für Verbindungsaufbau
client.on_connect = on_connect
# Callback-Funktion für Nachrichteneingang
client.on_message = on_message
# Callback-Funktion für Verbindungsverlust
client.on_disconnect = on_disconnect
# Callback-Funktion für Publish-Bestätigung
client.on_publish = on_publish
# Callback-Funktion für Subscribe-Bestätigung
client.on_subscribe = on_subscribe
# Callback-Funktion für Unsubscribe-Bestätigung
client.on_unsubscribe = on_unsubscribe

# Mit dem Broker verbinden
client.connect(broker_address, port, 60)

# Auf Nachrichten auf dem "lauflicht"-Thema lauschen
client.subscribe(topic, qos=1)

# Endlosschleife für das Lauflicht
try:
    # while True:
    #     time.sleep(1)
    #     client.publish("cmnd/actor_1/POWER", f"OFF")
    while True:
        for i in range(1, anzahl_aktoren + 1):
            client.publish(f"cmnd/actor_{str(i)}/POWER", "ON")
            time.sleep(0.5)
            client.publish(f"cmnd/actor_{str(i)}/POWER", "OFF")

except KeyboardInterrupt:
    # Verbindung beenden und Programm schließen
    client.disconnect()
    print("Verbindung beendet.")
