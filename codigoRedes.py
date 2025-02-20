#Trabalho de Redes 2 2024/2
#Aluno: João Vitor Frabis Zago 242039256
#Aluno: Leandro Coelho da Silva

class Roteador:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.listaSubRedes = []
    
    def __str__(self):
        return f"({self.name}): {self.ip[0]}.{self.ip[1]}.{self.ip[2]}.{self.ip[3]}"

o1 = Roteador("o1", [1,0,0,0])
print(o1)

a1 = Roteador("a1", [1,1,0,0])
o1.listaSubRedes.append(a1)
print(o1.listaSubRedes[0])
"""
              o1
          /         \
       a1             a2
      /|\\           /|\\
   e1 e2 e3 e4   e5 e6 e7 e8
"""

