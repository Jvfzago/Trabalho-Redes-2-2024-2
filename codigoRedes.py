#Trabalho de Redes 2 2024/2
#Aluno: João Vitor Frabis Zago 242039256
#Aluno: Leandro Coelho da Silva 232011396

import os  # Para limpar o terminal
import time

class Roteador:
    def __init__(self, name, ip, roteadorPai):
        self.name = name
        self.ip = ip
        self.roteadorPai = roteadorPai
        self.taxaTransPai = 0
        self.listaSubRedes = []
        self.dataGrama = {}

    def __str__(self):
        return f"{self.ip}"
    
class Packet:
    def __init__(self, tamanho):
        self.tamanho = tamanho

#----------------------------------

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

#----------------------------------------

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


#------------------------------------


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

    tempoCaminho = 0
    lstCaminho = []
    while(rotAtual != rotDestino):
        ipComum = set(lstCaminhoIpDestino) & set(rotAtual.dataGrama.keys())
        if (list(ipComum) != []):
            rotAtual = rotAtual.dataGrama[list(ipComum)[0]]
            tempoCaminho += calcular_tempo_transmissao(pac.tamanho, calcularTaxaTransmissao(rotAtual))
        else:
            tempoCaminho += calcular_tempo_transmissao(pac.tamanho, calcularTaxaTransmissao(rotAtual))
            rotAtual = rotAtual.roteadorPai
        lstCaminho.append(rotAtual.ip)

    rotDestino, rotOrigem = rotOrigem, rotDestino
    rotAtual = rotOrigem
    lstCaminhoIpDestino = criarListaIpsCaminho(rotDestino.ip)

    while(rotAtual != rotDestino):
        ipComum = set(lstCaminhoIpDestino) & set(rotAtual.dataGrama.keys())
        if (list(ipComum) != []):
            rotAtual = rotAtual.dataGrama[list(ipComum)[0]]
            tempoCaminho += calcular_tempo_transmissao(pac.tamanho, calcularTaxaTransmissao(rotAtual))
        else:
            tempoCaminho += calcular_tempo_transmissao(pac.tamanho, calcularTaxaTransmissao(rotAtual))
            rotAtual = rotAtual.roteadorPai

    return tempoCaminho, lstCaminho

#----------------------------------------
    
def ping(hostAtual, hostDestino):
    tempos_resposta = []
    pacotes_enviados = 0
    pacotes_recebidos = 0

    print(f"Disparando {hostDestino.ip} [IP_SIMULADO] com 32.000 bytes de dados:")

    for i in range(4):
        pacotes_enviados += 1
        tempoPacoteAtual, dictCaminho = enviarPacote(hostAtual, hostDestino)
        tempos_resposta.append(tempoPacoteAtual)
        pacotes_recebidos += 1
        print(f"Resposta de {hostDestino.ip}: tempo={tempoPacoteAtual:.5f}ms")

    pacotes_perdidos = pacotes_enviados - pacotes_recebidos
    tempo_minimo = min(tempos_resposta)
    tempo_maximo = max(tempos_resposta)
    tempo_medio = sum(tempos_resposta) / len(tempos_resposta)

    print("\nEstatísticas do Ping para", hostDestino.ip + ":")
    print(f"    Pacotes: Enviados = {pacotes_enviados}, Recebidos = {pacotes_recebidos}, Perdidos = {pacotes_perdidos} ({(pacotes_perdidos/pacotes_enviados)*100}% de perda),")
    print(f"Aproximar um número redondo de vezes em milissegundos:")
    print(f"    Mínimo = {tempo_minimo:.5f}ms, Máximo = {tempo_maximo:.5f}ms, Média = {tempo_medio:.2f}ms")


def traceroute(hostAtual, hostDestino):
    global listaRoteadores
    max_saltos = 30
    saltos = []

    # Exibe o IP de destino simulado
    print(f"Rastreando a rota para {hostDestino.ip} com no máximo {max_saltos} saltos:")

    temp, lstCaminho = enviarPacote(hostAtual, hostDestino)
    for ipInter in lstCaminho:
        rotInter = next((r for r in listaRoteadores if r.ip == ipInter))
        tempos = []
        for i in range(3):
            tempo , temp = enviarPacote(hostAtual, rotInter)
            tempos.append(tempo)
        print(f"  {i+1}    {tempos[0]:.5f} ms   {tempos[1]:.5f} ms   {tempos[2]:.5f} ms  {ipInter}")
    
    print(f"Rastreamento concluído.")

#----------------------------------------
# ipAtual = "1.1.4.15"
# hostAtual = next((r for r in listaRoteadores if r.ip == ipAtual))
# ipDestino = "1.2.7.12"
# hostDestino = next((r for r in listaRoteadores if r.ip == ipDestino))

# ping(hostDestino)
# print("\n---------------------------------------\n")
# traceroute(hostDestino)

#----------------------------------------

def mostrarMenu(hostAtual):
    print("\n=== MENU ===")
    print(f"Host atual: {hostAtual}")
    print("1. Executar Ping")
    print("2. Executar Traceroute")
    print("3. Trocar Host Atual")
    print("4. Sair")
    opcao = input("Escolha uma opção (1/2/3/4): ")
    return opcao

def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def esperar():
    input("\nPressione Enter para continuar...")

# Função principal do game loop
def gameLoop():
    global hostAtual
    print("Iniciando o programa...")
    time.sleep(1)
    
    # Carregar configurações de rede (simulado)
    print("Configurando rede...")
    importarDefRede("defRede.txt")
    criarDatagramas(listaRoteadores)

    time.sleep(1)
    # Exemplo: Carregar lista de roteadores e hosts de configuração
    # listaRoteadores = importarDefRede("configuracoes.txt")
    # Para o exemplo, vou manter uma variável fixa para o host de origem.
    hostAtual = "1.1.4.15"  # Exemplo de host de origem
    hostAtual = next((r for r in listaRoteadores if r.ip == hostAtual))
    print(f"Host atual: {hostAtual}")
    time.sleep(2)
    while True:
        limparTela()  # Limpar a tela a cada iteração para mostrar um menu limpo
        opcao = mostrarMenu(hostAtual)

        if opcao == '1':  # Ping
            
            ipDestino = input("Digite o IP host de destino para o Ping: ")
            hostDestino = next((r for r in listaRoteadores if r.ip == ipDestino))
            ping(hostAtual, hostDestino)  # Chamando a função ping (já definida anteriormente)
            esperar()

        elif opcao == '2':  # Traceroute
            
            ipDestino = input("Digite o IP do host de destino para o Traceroute: ")
            hostDestino = next((r for r in listaRoteadores if r.ip == ipDestino))
            traceroute(hostAtual, hostDestino)  # Chamando a função traceroute (já definida anteriormente)
            esperar()
            

        elif opcao == '3':  # Trocar Host Atual
            novoHostIP = input("Digite o novo host atual: ")
            hostAtual = next((r for r in listaRoteadores if r.ip == novoHostIP))
            print(f"Host atual trocado para: {hostAtual.ip}")
            time.sleep(2)  # Pausar um pouco antes de continuar o loop

        elif opcao == '4':  # Sair
            print("Encerrando o programa...")
            time.sleep(2)
            break  # Encerra o loop e termina o programa

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")
            time.sleep(1)  # Pausar antes de continuar o loop

if __name__ == "__main__":
    gameLoop()
