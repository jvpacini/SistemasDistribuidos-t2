import paho.mqtt.client as mqtt
import random
import time

ndeposito = int(input("Digite o número do depósito: "))

##############
class BufferEstoqueProdutos:
    def __init__(self, capacidade_maxima):
        self.produto = {}
        self.capacidade_maxima = capacidade_maxima
        for i in range(1, 6):
            nome = "Pv" + i
            self.produto[nome] = 0

    def check_out(self, quantidade, item):
        if self.produto[item]>= quantidade:
            self.produto[item]-= quantidade
            return True
        return False

    def check_in(self, quantidade, item):
        if self.produto[item]+ quantidade <= self.capacidade_maxima:
            self.produto[item]+= quantidade
            return True
        return False

    def obter_valor_atual(self, item):
        return self.produto[item]["quantia"]

    def obter_nivel_produto(self, item):
        if self.produto[item]< self.capacidade_maxima * 0.2:
            return 1
        elif self.produto[item]< self.capacidade_maxima * 0.4:
            return 2
        elif self.produto[item]< self.capacidade_maxima * 0.6:
            return 3
        elif self.produto[item]< self.capacidade_maxima * 0.8:
            return 4
        else:
            return 5

def obter_nivel_produto(item):
    global buffer_estoque
    return buffer_estoque.obter_valor_atual(item)

def obter_quantia_produto(item):
    global buffer_estoque
    return buffer_estoque.obter_nivel_produto(item)

buffer_estoque = BufferEstoqueProdutos(capacidade_maxima=100)
################

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
    buffer_estoque.check_in(1, "Pv"+produto)

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"deposito{ndeposito}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

while True:
    time.sleep(1)
