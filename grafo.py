class grafo:
    def __init__(self,num_grafos):
        self.num_grafos = num_grafos
        self.lista_adj = [ [ -1, 4, -1, -1, -1, -1, -1, 8, -1,-1 ],
			[ 4, -1, 8, -1, -1, -1, -1, 11, -1,-1 ],
			[ -1, 8, -1, 7, -1, 4, -1, -1, 2,-1 ],
			[ -1, -1, 7, -1, 9, 14, -1,-1,-1,-1],
			[ -1, -1, -1, 9, -1, 10, -1, -1, -1,-1 ],
			[ -1, -1, 4, 14, 10, -1, 2, -1, -1,-1],
			[ -1, -1, -1, -1, -1, 2, -1, 1, 6,-1 ],
			[ 8, 11, -1, -1, -1, -1, 1, -1, 7,-1 ],
			[ -1, -1, 2, -1, -1, -1, 6, 7, -1,-1 ],
            [ -1, -1, -1, -1, -1, -1, -1, -1, -1,-1 ] ]

        #for i in range(0,self.num_grafos):
        #    lista = []
        ##    for j in range(0,num_grafos):
         #       lista.append(int(input("Conexão do grafo {} para {}: ".format(i,j))))

         #   self.lista_adj.append(lista)

        self.distancias = []
        self.anterior = []

        for i in range(0,self.num_grafos):
            self.distancias.append(100) #valor alto para representar inf
            self.anterior.append(-1)   #-1 representa que não temos caminho 
    
    def print_lista(self):
        for linha in self.lista_adj:
            print(linha)

    def visitou_todos(self,lista):
        for i in lista:
            if (i == 0):
                return True
        
        return False

    def procurar_menor_dist(self,lista):
        #procurar o menor valor naquele não visitado
        atual = -1
        no_escolhido = -1
        for i in range(0,self.num_grafos):
            if(lista[i] == 0 and (self.distancias[i] < atual or atual == -1)): #AQUI
                atual = self.distancias[i]
                no_escolhido = i
        
        return no_escolhido


    def minimo(self,a,b):
        if a < b:
            return a
        return b

    def dijkstra(self,origem):
        self.distancias[origem] = 0
        self.anterior[origem] = -1 #seta a origem com custo 0 e sem antecessor

        nao_visitados = [] #lista de nos visitados

        for i in range(0,self.num_grafos): #0 -> nao visitado, 1->visitado
            nao_visitados.append(0)

        while(self.visitou_todos(nao_visitados)):
            print(nao_visitados)
            #nó não visitado com menor custo de distancia
            atual = self.procurar_menor_dist(nao_visitados)
            print(atual)
            if(atual == -1):
                return
            #if atual == -1, já acabou
            nao_visitados[atual] = 1

            lista_vizinhos = self.lista_adj[atual] #[-1,1,-1,-1]

            for i in range(0, self.num_grafos):
                if(nao_visitados[i] == 0 and lista_vizinhos[i] != -1):
                    distancia = self.minimo(self.distancias[i],self.distancias[atual] + lista_vizinhos[i])
                    if(distancia < self.distancias[i]):
                        self.distancias[i] = distancia
                        self.anterior[i] = atual
        

def main():
    instancia = grafo(10)
    instancia.dijkstra(0)#origem

    print(instancia.distancias)
    print(instancia.anterior)

main()
