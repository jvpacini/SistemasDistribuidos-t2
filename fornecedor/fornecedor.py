import paho.mqtt.client as mqtt
import time

nfornecedor = int(input("Digite o número do fornecedor: "))

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Conectado")
        client.subscribe("almoxarifado")
    else:
        print("Não foi possível conectar, código de retorno:", return_code)

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "almoxarifado" and int(comando[1]) == nfornecedor:
        peca = int(comando[2])
        fornecerPeca(peca)

def fornecerPeca(peca):
    enviarPecaAoAlmoxarifado(peca)

def enviarPecaAoAlmoxarifado(peca):
    client.publish("almoxarifado", f"reabastecido/{nfornecedor}/{peca}")

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"fornecedor{nfornecedor}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

while True:
    time.sleep(1)
