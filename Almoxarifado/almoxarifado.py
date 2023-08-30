import paho.mqtt.client as mqtt
import time

pecasNoAlmoxarifado = [100, 100, 100, 100, 100]  # Quantidade inicial de cada peça
nalmoxarifado = int(input("Digite o número do almoxarifado: "))

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Conectado")
        client.subscribe("linha")
    else:
        print("Não foi possível conectar, código de retorno:", return_code)

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "linha":
        pecasUtilizadas = comando[2].split(",")
        for peca in pecasUtilizadas:
            atualizarEstoque(int(peca))

def atualizarEstoque(peca):
    if pecasNoAlmoxarifado[peca - 1] > 0:  # Verifica se há estoque disponível
        pecasNoAlmoxarifado[peca - 1] -= 1
    else:
        solicitarReabastecimento(peca)

def solicitarReabastecimento(peca):
    client.publish("almoxarifado", f"reabastecer/{nalmoxarifado}/{peca}")

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"almoxarifado{nalmoxarifado}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

while True:
    time.sleep(1)
