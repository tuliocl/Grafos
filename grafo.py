class grafo:
    def __init__(self,num_grafos):
        self.lista_adj = []

        for i in range(0,num_grafos):
            lista = []
            for j in range(0,num_grafos):
                lista.append(int(input("Conexão do grafo {} para {}: ".format(i,j))))

            self.lista_adj.append(lista)

        self.distancias = []
        self.anterior = []

        for i in range(0,num_grafos):
            self.distancias.append(100) #valor alto para representar inf
            self.anterior.append(-1)   #-1 representa que não temos caminho 
    
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
    instancia = grafo(4)
    instancia.print_lista()
    print(instancia.tem_caminho(3,0))

main()