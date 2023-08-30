import paho.mqtt.client as mqtt
import time

npecas = 10
produto1 = [0, 1, 2, 3, 4, 5, 8, 9]
pecasNaLinha = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
nlinha = int(input("Digite o número da linha: "))  # Converte a entrada para inteiro

def on_connect(client, return_code):
    if return_code == 0:
        print("Conectado")
        client.subscribe("fabrica")
    else:
        print("Não foi possível conectar, código de retorno:", return_code)

def on_message(message):
    msg = str(message.payload.decode("utf-8"))
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "fabrica" and comando[1] == str(nlinha):
        pecas = comando[2].split(",")
        for i in range(len(pecas)):
            peca = int(pecas[i])
            pecasNaLinha[peca] += 1

def pedirpecas(pecas):
    pedido = ",".join(map(str, pecas))  # Use join para criar o pedido
    result = client.publish("fabrica", f"linha/{nlinha}/{pedido}")

def montarproduto(produto):
    contador = 0
    pecas_faltantes = []
    pecas_consumidas = []
    if produto == 1:
        for peca in produto1:
            if pecasNaLinha[peca] > 0:
                pecas_consumidas.append(peca)
            else:
                contador += 1
                pecas_faltantes.append(peca)
    if contador == 0:
        for i in range(len(pecas_consumidas)):
            pecasNaLinha[pecas_consumidas[i]] -= 1
        return True
    else:
        pedirpecas(pecas_faltantes)
        return False

def montarpedido(pedido):
    return montarproduto(pedido)

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"linha{nlinha}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

pedidos = [1, 1, 1, 1]
pedidoatual = 0

while pedidoatual < len(pedidos):  # Use len(pedidos) para determinar o número de pedidos
    if client.is_connected():
        print(f"Montando pedido {pedidoatual}")
        if montarpedido(pedidos[pedidoatual]):
            pedidoatual += 1
            print("Pedido montado")
    time.sleep(1)
