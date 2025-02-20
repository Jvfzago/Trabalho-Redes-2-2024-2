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
    def __init__(self, name, ip, rotadorPai):
        self.name = name
        self.ip = ip
        self.roteadorPai = rotadorPai
        self.listaSubRedes = []

    def __str__(self):
        return f"({self.name}): {self.ip}"
    
class Packet:
    size = 32

#----------------------------------
roteadorRaiz = None

def importarDefRede(endereco):
    with open(endereco, "r") as file:
        linhas = file.readlines()

    name, ip, pai = linhas[0].strip().split("-")
    roteadorRaiz = Roteador(name, ip, pai)

    for linha in linhas[1:]:
        name, ip, pai = linha.strip().split("-")
        Roteador(name, ip, pai)

    return roteadorRaiz






    



roteadorRaiz = importarDefRede("Trabalho-Redes-2-2024-2/defRede.txt")
# o1 = Roteador("o1", [1,0,0,0], None)
print(roteadorRaiz)



# a1 = Roteador("a1", [1,1,0,0], o1)
# o1.listaSubRedes.append(a1)
# print(o1.listaSubRedes[0])
"""
              o1
          /         \
       a1             a2
      /|\\           /|\\
   e1 e2 e3 e4   e5 e6 e7 e8
"""

#------------------------------------

def ping(hostDestino):
    pass

def traceroute(hostDestino):
    pass

