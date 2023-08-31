import paho.mqtt.client as mqtt
import random
import time

nalmoxarifado = int(input("Digite o número do fornecedor: "))

#######
class BufferEstoquePartes:
    def __init__(self, capacidade_maxima):
        self.parte = {}
        self.capacidade_maxima = capacidade_maxima
        for i in range(100):
            num_aleat = random.randint(capacidade_maxima*0.6, capacidade_maxima)
            nome_parte = "Parte_" + i
            self.parte[nome_parte] = num_aleat

    def check_out(self, quantidade, item):
        if self.parte[item] >= quantidade:
            self.parte[item] -= quantidade
            if self.parte[item] <= self.capacidade_maxima*0.40:
                 solicitarReabastecimento(item)
            return True
        return False

    def check_in(self, quantidade, item):
        if self.parte[item] + quantidade <= self.capacidade_maxima:
            self.parte[item] += quantidade
            return True
        return False

    def obter_valor_atual(self, item):
        return self.parte[item]

    def obter_cor_estoque(self, item):
        if self.parte[item] < self.capacidade_maxima * 0.33:
            return "Vermelho"
        elif self.parte[item] < self.capacidade_maxima * 0.66:
            return "Amarelo"
        else:
            return "Verde"
    
def obter_cor_parte(item):
    global buffer_estoque
    return buffer_estoque.obter_valor_atual(item)

def obter_quantia_parte(item):
    global buffer_estoque
    return buffer_estoque.obter_cor_estoque(item)

buffer_estoque = BufferEstoquePartes(capacidade_maxima=200)
##########################


def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("Conectado")
        client.subscribe("fabrica")
    else:
        print("Não foi possível conectar, código de retorno:", return_code)

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("Mensagem recebida:", msg)
    comando = msg.split("/")
    if comando[0] == "fabrica":
        pecasUtilizadas = comando[2].split(",")
        for peca in pecasUtilizadas:
            buffer_estoque.check_out(1, "Parte_" + peca)
    elif comando[0] == "fornecedor":
        peca = comando[2].split(",")
        buffer_estoque.check_out(buffer_estoque.obter_valor_atual("Parte_" + peca), "Parte_" + peca)

def atualizarEstoque(quantidade, peca):
    buffer_estoque.check_out(quantidade, "Parte_" + peca)

def solicitarReabastecimento(peca):
    client.publish("fornecedor", f"reabastecer/{nalmoxarifado}/{peca}")

broker_hostname = "localhost"
port = 1884
client = mqtt.Client(f"almoxarifado/{nalmoxarifado}")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_hostname, port)
client.loop_start()

while True:
    time.sleep(1)
