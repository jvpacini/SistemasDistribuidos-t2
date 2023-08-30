import paho.mqtt.client as mqtt
import time

produtosNoDeposito = [0, 0, 0, 0, 0]  # Inicialmente, não há produtos no depósito
ndeposito = int(input("Digite o número do depósito: "))

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
        produto = int(comando[1])
        receberProduto(produto)

def receberProduto(produto):
    produtosNoDeposito[produto - 1] += 1  # O produto é indexado a partir de 1

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"deposito{ndeposito}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

while True:
    time.sleep(1)
