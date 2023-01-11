import os
from concurrent import futures
from google.cloud import pubsub_v1
import time
import json
import subprocess

# Seteo de variables y directorios
project_id = "ping-streaming"
topic_id = "testtopic"
credentials_path = "/home/kjal/ping_project/ping-streaming-privatekey.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
sites = ["bancoestado", "falabella", "emol"]
script_path = '/home/kjal/ping_project/script.sh'
start_time = time.time()


def ping_site(site_script: str):
    # La librería subprocess se usa para correr el script de bash, y el resultado es capturado en la variable output
    output = subprocess.check_output([site_script], shell=True)

    # El resultado del script bash es transformado al formato adecuado JSON
    splitBySpace = str(output).split()
    splitBySlash = splitBySpace[5].split("/")
    dictMessage = {"Date": splitBySpace[0].replace("b'", ""),
                   "Time": splitBySpace[1],
                   "MinPing": float(splitBySlash[0]),
                   "AvgPing": float(splitBySlash[1]),
                   "MaxPing": float(splitBySlash[2]),
                   "Mdev": float(splitBySlash[3]),
                   "Site": site_script}
    data = json.dumps(dictMessage, indent=4)
    return data


# Se inicia el cliente de PubSub para publicar mensajes
publisher = pubsub_v1.PublisherClient()

# Se indica la ubicación del tópico de PubSub donde se van a enviar los mensajes
topic_path = publisher.topic_path(project_id, topic_id)

# Se crea un loop ininterrumpido dentro del cual se envían mensajes constantemente al tópico
while True:

    for site in sites:
        ping_info = ping_site(site)

        # Se imprime la data en pantalla para asegurarse visualmente que se está enviando información correcta
        print(ping_info)

        # Al publicar un mensaje, PubSub devuelve un objeto Future()
        publish_future = publisher.publish(topic_path, ping_info.encode("utf-8"))

        # De forma opcional se imprime el ID del mensaje creado
        print(publish_future.result())

    # Esta línea produce que el ciclo se realice cada cierta cantidad de tiempo, en este caso, 60 segundos
    time.sleep(60.0 - ((time.time() - start_time) % 60.0))
