import paho.mqtt.client as mqtt
import time

pecasNaFabrica = []
nfab = int(input("Digite o número da fábrica: "))
for i in range(0, 100):
    pecasNaFabrica[i] = 20

def on_connect(client, return_code):
    if return_code == 0:
        print("Conectado")
        client.subscribe("fabrica")
        client.subscribe("fabricas")
    else:
        print("Não foi possível conectar, código de retorno:", return_code)

def on_message(message):
    msg = str(message.payload.decode("utf-8"))
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "linha":
        pecasPedidas = comando[2].split(",")
        pecas = list(map(int, pecasPedidas))
        enviarPecas(comando[1], pecas)

def enviarPecas(linha, pecas):
    pecas_em_falta = [peca for peca in pecas if pecasNaFabrica[peca] == 0]
    if not pecas_em_falta:
        for peca in pecas:
            pecasNaFabrica[peca] -= 1
        enviaPecas(linha, pecas)
    else:
        pedirPecas(pecas_em_falta)

def enviaPecas(linha, pecas):
    envio = ",".join(map(str, pecas))
    client.publish("fabrica", f"fabrica/{linha}/{envio}")

def pedirPecas(pecas):
    pedido = ",".join(map(str, pecas))
    client.publish("fabricas", f"fabrica/{nfab}/{pedido}")

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"fabrica{nfab}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

while True:
    time.sleep(1)
