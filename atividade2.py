import numpy as np
import re

class grafo:
    def __init__(self,num_grafos,num_arestas,file,direcionado):        
        self.num_grafos = num_grafos
        self.num_arestas = num_arestas
        self.lista_adj = [] #matriz de adj

        #cada posição i indica um nó. Com isso temos a distancia para outros nós,
        # os nós anteriores, a soma dos custos e o maior custo
        self.distancias = []  #Matriz de distancias
        self.anterior = []  #Matriz de anterior
        self.custos = []
        self.maior_custo = []   #array de maior custo
   
        self.gerar_tabela_dist(file,direcionado) #função para gerar a matriz de adj

        for i in range(0,self.num_grafos): #seta a distancia,anterior,custos e maior custo com valores vazios
            self.custos.append(0)   #todos os custos vão ter valor 0 
            self.maior_custo.append(-1) #não tem um maior custo no momento (-1)
            lista1 = [] #Lista de distancia
            lista2 = [] #lista de anterior

            for j in range(0,self.num_grafos):
                lista1.append(np.inf) #todas as distancias são inicializadas com infinito
                lista2.append(-1)   #-1 representa que não temos caminho 

            self.distancias.append(lista1)
            self.anterior.append(lista2)

        for i in range(0,self.num_grafos): #roda djistra e acha os melhores caminhos para cad nó
            self.dijkstra(i,self.distancias[i],self.anterior[i]) #djkistra já monta a distancia e anterior de cada nó
            self.maior_custo[i] = max(self.distancias[i])
            self.custos[i] = self.soma_de_custo(self.distancias[i])
        
        print("Matriz de distancias: ")
        for i in self.distancias:
            print(i)
        

    def soma_de_custo(self,lista): #função para fazer a soma dos custos de um nó
        soma = 0
        for i in lista:
            soma += i
        return soma

    def gerar_tabela_dist(self,file,direcionado): #gera a tabela de adj
        for i in range(0,self.num_grafos):
            lista = []
            for i in range(0,self.num_grafos):
                lista.append(np.inf)
            self.lista_adj.append(lista)
        
        for i in range(0,self.num_arestas):
            line = re.findall("(\d+)\s+(\d+)\s+(\d+)",file.readline())    

            x = int(line[0][0])
            y = int(line[0][1])
            valor = int(line[0][2])

            self.lista_adj[x - 1][y - 1] = valor
            if(not direcionado):
                self.lista_adj[y - 1][x - 1] = valor


    def escolher_no(self):
        no_escolhido = 0
        menor_soma = self.custos[0]

        for i in range(1,self.num_grafos):
            if self.custos[i] < menor_soma:
                menor_soma = self.custos[i]
                no_escolhido = i
            elif self.custos[i] == menor_soma:
                if(self.maior_custo[no_escolhido] > self.maior_custo[i]):
                    menor_soma = self.custos[i]
                    no_escolhido = i

        return no_escolhido            

    #aqui pra baixo são funções do djkistra
    def visitou_todos(self,lista):
        for i in lista:
            if (i == 0):
                return True
        
        return False

    def procurar_menor_dist(self,lista,distancias):
        #procurar o menor valor naquele não visitado
        atual = -1
        no_escolhido = -1
        for i in range(0,self.num_grafos):
            if(lista[i] == 0 and (distancias[i] < atual or atual == -1)): #AQUI
                atual = distancias[i]
                no_escolhido = i
        
        return no_escolhido


    def minimo(self,a,b):
        if a < b:
            return a
        return b

    def dijkstra(self,origem,distancias,anterior):
        distancias[origem] = 0
        anterior[origem] = -1 #seta a origem com custo 0 e sem antecessor

        nao_visitados = [] #lista de nos visitados

        for i in range(0,self.num_grafos): #0 -> nao visitado, 1->visitado
            nao_visitados.append(0)

        while(self.visitou_todos(nao_visitados)):
            #nó não visitado com menor custo de distancia
            atual = self.procurar_menor_dist(nao_visitados,distancias)
            if(atual == -1):
                return
            #if atual == -1, já acabou
            nao_visitados[atual] = 1

            lista_vizinhos = self.lista_adj[atual] #[-1,1,-1,-1]

            for i in range(0, self.num_grafos):
                if(nao_visitados[i] == 0 and lista_vizinhos[i] != -1):
                    distancia = self.minimo(distancias[i],distancias[atual] + lista_vizinhos[i])
                    if(distancia < distancias[i]):
                        distancias[i] = distancia
                        anterior[i] = atual

def main():
    file = open("grafo01.txt",'r')
    line = re.findall("(\d+)\s+(\d+)",file.readline())

    num_grafos = int(line[0][0])
    num_arestas = int(line[0][1]) 

    print("Para a primeira entrada: ")
    G = grafo(num_grafos,num_arestas,file,False)#false indica que não é direcionado
    print("O nó escolhido foi: ",G.escolher_no() + 1)

    file = open("grafo02.txt",'r')
    line = re.findall("(\d+)\s+(\d+)",file.readline())

    num_grafos = int(line[0][0])
    num_arestas = int(line[0][1]) 
    
    print("Para a segunda entrada:")
    G = grafo(num_grafos,num_arestas,file,True)#true = direcionado
    print("O nó escolhido foi: ",G.escolher_no() + 1)
    

main()
