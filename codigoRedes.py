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
    def __init__(self, name, ip, roteadorPai):
        self.name = name
        self.ip = ip
        self.roteadorPai = roteadorPai
        self.taxaTransPai = 0
        self.listaSubRedes = []
        self.dataGrama = {}

    def __str__(self):
        return f"({self.name}): {self.ip} - {self.dataGrama}"
    
class Packet:
    def __init__(self, tamanho):
        self.tamanho = tamanho

#----------------------------------
roteadorRaiz = None
listaRoteadores = []

def importarDefRede(endereco):
    global listaRoteadores
    with open(endereco, "r") as file:
        linhas = file.readlines()

    name, ip, pai= linhas[0].strip().split("-")
    roteadorRaiz = Roteador(name, ip, pai)
    listaRoteadores.append(roteadorRaiz)

    for linha in linhas[1:]:
        name, ip, pai = linha.strip().split("-")
        roteadorEncontrado = next((r for r in listaRoteadores if r.name == pai), None)
        rot = Roteador(name, ip, roteadorEncontrado)
        listaRoteadores.append(rot)
        if(roteadorEncontrado != None):
          roteadorEncontrado.listaSubRedes.append(rot)    
        

    return roteadorRaiz



def getIPToList(ip):
    return ip.split(".")

def getListToIP(list):
    return ".".join(list)


def criarDatagramas(lstRoteadores):
    for rot in lstRoteadores:
        for rotFilho in rot.listaSubRedes:
            ipFilhoLista = getIPToList(rotFilho.ip)
            for i in range(len(ipFilhoLista)):
                if ipFilhoLista[i] == "0":
                    ipFilhoLista[i] = "*"
            ipFilho = getListToIP(ipFilhoLista)
            rot.dataGrama.update({ipFilho: rotFilho})


roteadorRaiz = importarDefRede("Trabalho-Redes-2-2024-2/defRede.txt")
criarDatagramas(listaRoteadores)

# for rot in listaRoteadores:
#     print(rot)



"""
              o1
          /         \
       a1             a2
      /|\\           /|\\
   e1 e2 e3 e4   e5 e6 e7 e8
"""

#------------------------------------
hostAtual = None

def criarListaIpsCaminho(ip):
    ipList = getIPToList(ip)
    listaCaminhoIpDestino = []
    listaCaminhoIpDestino.append(f"{ipList[0]}.{ipList[1]}.*.*")
    listaCaminhoIpDestino.append(f"{ipList[0]}.{ipList[1]}.{ipList[2]}.*")
    listaCaminhoIpDestino.append(ip)
    return listaCaminhoIpDestino

def calcularTaxaTransmissao(roteador):
    if roteador.name.startswith("A"):
        return 100 * (10**9)  # 100 Gb/s
    elif roteador.name.startswith("E"):
        return 10 * (10**9)   # 10 Gb/s
    elif roteador.name.startswith("H"):
        return 50 * (10**6)   # 50 Mb/s
    else:
        return 1 * (10**9)    # Default: 1 Gb/s para outros
    
def calcular_tempo_transmissao(tamanho_bytes, taxa_bps):
    tamanho_bits = tamanho_bytes * 8
    tempo_segundos = tamanho_bits / taxa_bps
    tempo_milisegundos = tempo_segundos * 1000
    return tempo_milisegundos

def enviarPacote(rotOrigem, rotDestino):
    pac = Packet(32000)
    rotAtual = rotOrigem
    lstCaminhoIpDestino = criarListaIpsCaminho(rotDestino.ip)
    print(lstCaminhoIpDestino)
    tempoCaminho = 0
    while(rotAtual != rotDestino):
        ipComum = set(lstCaminhoIpDestino) & set(rotAtual.dataGrama.keys())
        if (list(ipComum) != []):
            rotAtual = rotAtual.dataGrama[list(ipComum)[0]]
            tempoCaminho += calcular_tempo_transmissao(pac.tamanho, calcularTaxaTransmissao(rotAtual))
        else:
            tempoCaminho += calcular_tempo_transmissao(pac.tamanho, calcularTaxaTransmissao(rotAtual))
            rotAtual = rotAtual.roteadorPai
        print(rotAtual.ip)
        print(tempoCaminho)
        


def ping(hostDestino):
    global hostAtual
    tempoPacoteAtual = 0
    for i in range(0,4):
        pacote = Packet()


def traceroute(hostDestino):
    pass

ipOrigem = "1.1.4.15"
ipDestino = "1.2.7.12"
print
enviarPacote(next((r for r in listaRoteadores if r.ip == ipOrigem)),next((r for r in listaRoteadores if r.ip == ipDestino)))