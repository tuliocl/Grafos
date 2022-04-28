class grafo:
    def __init__(self):
        self.lista_adj = [
            [0,1,0,0], #A - 0
            [0,0,1,0], #B - 1
            [0,0,0,1], #C - 2
            [1,0,0,0]  #D - 3
            ]

    def print_lista(self):
        for linha in self.lista_adj:
            print(linha)

    def tem_caminho(self,destino,atual):
        print(atual)
        if(atual == destino):
            return True

        lista_atual = self.lista_adj[atual]

        for i in range(0,len(lista_atual)):
            if(lista_atual[i] == 1):
                return self.tem_caminho(destino,i)

            

def main():
    instancia = grafo()
    instancia.print_lista()
    print(instancia.tem_caminho(3,0))

main()