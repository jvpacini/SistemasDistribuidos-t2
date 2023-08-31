import paho.mqtt.client as mqtt
import time

nlinha = int(input("Digite o número da linha: ")) 

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
    if comando[0] == "linha":
        pedido = comando[3].split(",")
        montarproduto(comando[2], pedido[0], pedido[1])

def pedirpecas(pecas):
    pedido = ",".join(map(str, pecas))  # Use join para criar o pedido
    client.publish("fabrica", f"linha/{nlinha}/{pedido}")

def montarproduto(nversao, npecas, inicio):
    for i in range(inicio, inicio+npecas):
        client.publish("linha", f"pedido/{i}")
    client.publish("linha", f"produto/{nversao}")
    

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
