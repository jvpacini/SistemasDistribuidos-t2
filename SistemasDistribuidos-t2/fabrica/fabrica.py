import paho.mqtt.client as mqtt
import threading
import time
import random

pecasNaFabrica = []
nfab = int(input("Digite o número da fábrica: "))

for i in range(0, 100):
    pecasNaFabrica[i] = 20
threads = []
num_linhas = 5

def linha_de_producao(i, pedido):
    client.publish("linha", f"linha/{i}/{i%5}/{pedido}")
    

def on_connect(client, return_code):
    if return_code == 0:
        print("Conectado")
        client.subscribe("fabrica")
        client.subscribe("almoxarifado")
        client.subscribe("linha")
    else:
        print("Não foi possível conectar, código de retorno:", return_code)

def on_message(message):
    msg = str(message.payload.decode("utf-8"))
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "linha" and comando[1] == "pedido":
        pecasPedidas = comando[2].split(",")
        pecas = list(map(int, pecasPedidas))
        enviarPecas(comando[1], pecas)

    if comando[0] == "linha" and comando[1] == "produto":
        produto = comando[2].split(",")
        client.publish("estoque", f"fabrica/{produto}")

    if comando[0] == "almoxarifado":
        pecasChegadas = comando[2].split(",")
        pecasNaFabrica[pecasChegadas] += 15

    if comando[0] == "cliente":
        pecasPedidas = comando[2].split(",")
        

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

def inicia_linhas(quantidade):
    for i in range(num_linhas):
        numpecas = random.randint(63, 73) #define como vao ser as peças
        inicio = random.randint(0, 99 - numpecas)
        pecas = [numpecas, inicio]
        pedido = ",".join(map(str, pecas))
        thread = threading.Thread(target=linha_de_producao, args=(i + 1, pedido))
        threads.append(thread)
        thread.start()

# Aguardar até que todas as threads terminem
for thread in threads:
    thread.join()

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"fabrica{nfab}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

while True:
    time.sleep(1)
