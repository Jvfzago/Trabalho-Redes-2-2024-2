#Trabalho de Redes 2 2024/2
#Aluno: João Vitor Frabis Zago 242039256
#Aluno: Leandro Coelho da Silva

"""
 ping youtube.com

Disparando youtube.com [2800:3f0:4004:809::200e] com 32 bytes de dados:
Resposta de 2800:3f0:4004:809::200e: tempo=31ms
Resposta de 2800:3f0:4004:809::200e: tempo=26ms
Resposta de 2800:3f0:4004:809::200e: tempo=24ms
Resposta de 2800:3f0:4004:809::200e: tempo=27ms

Estatísticas do Ping para 2800:3f0:4004:809::200e:
    Pacotes: Enviados = 4, Recebidos = 4, Perdidos = 0 (0% de
             perda),
Aproximar um número redondo de vezes em milissegundos:
    Mínimo = 24ms, Máximo = 31ms, Média = 27ms
"""

"""
 TRACERT youtube.com

Rastreando a rota para youtube.com [2800:3f0:4004:809::200e]
com no máximo 30 saltos:

  1     1 ms     1 ms     1 ms  2804:14c:6586:437d:0:ff:fe00:4
  2     *        *        *     Esgotado o tempo limite do pedido.
  3    15 ms    14 ms    11 ms  2804:14c:6500:a12::1
  4    11 ms    12 ms    12 ms  2804:a8:2:88::1851
  5     *        *        *     Esgotado o tempo limite do pedido.
  6    32 ms     *        *     2804:a8:2:b0::13d6
  7    27 ms    26 ms    26 ms  2800:3f0:8016::1
  8     *        *        *     Esgotado o tempo limite do pedido.
  9    30 ms    34 ms    30 ms  2001:4860:0:1::3d3d
 10    26 ms    26 ms    27 ms  2800:3f0:4004:809::200e

Rastreamento concluído.
"""
class Roteador:
    def __init__(self, name, ip, rotadorPai, taxaTransPai):
        self.name = name
        self.ip = ip
        self.roteadorPai = rotadorPai
        self.taxaTransPai = taxaTransPai
        self.listaSubRedes = []
        self.dataGrama = {}

    def __str__(self):
        return f"({self.name}): {self.ip}"
    
class Packet:
    def __init__(self, origem, destino):
        self.origem = origem
        self.destino = destino
        self.tempo = 0

#----------------------------------
roteadorRaiz = None
listaRoteadores = []

def importarDefRede(endereco):
    global listaRoteadores
    with open(endereco, "r") as file:
        linhas = file.readlines()

    name, ip, pai, taxa= linhas[0].strip().split("-")
    roteadorRaiz = Roteador(name, ip, pai, taxa)
    listaRoteadores.append(roteadorRaiz)

    for linha in linhas[1:]:
        name, ip, pai, taxa = linha.strip().split("-")
        rot = Roteador(name, ip, listaRoteadores(pai), taxa)
        listaRoteadores.append(rot)

    return roteadorRaiz

def getListaIP(ip):
    return [octeto for octeto in [ip.split(".")]]


def criarDatagramas(lstRoteadores):
    for rot in lstRoteadores:
        pass






    



roteadorRaiz = importarDefRede("Trabalho-Redes-2-2024-2/defRede.txt")

print(roteadorRaiz)



"""
              o1
          /         \
       a1             a2
      /|\\           /|\\
   e1 e2 e3 e4   e5 e6 e7 e8
"""

#------------------------------------
hostAtual = None


def enviarPacote(rotArigem, rotDestino):
    pacote = Packet
    rotAtual = rotArigem
    while(rotAtual != rotDestino):
        rotAtual.dataGrama


def ping(hostDestino):
    global hostAtual
    tempoPacoteAtual = 0
    for i in range(0,4):
        pacote = Packet()


def traceroute(hostDestino):
    pass

