import numpy as np
from shapely import geometry                

#Essa classe eu uso pra fazer a busca na arvore
#Só uso pra poder manter o controle de estado filho e pai
class Estado:
    def __init__(self,point):
        self.point = point
        self.pai = None
        self.filhos = []

    def gerar_filhos(self,all_points,lista_adjacencias):
        self.filhos = []
        for i in range(0,len(all_points)):
            if(all_points[i] == self.point):

                for aresta in lista_adjacencias[i]:
                    filho = Estado(aresta[0])
                    filho.pai = self

                    self.filhos.append(filho)

#Classe que monta a arvore recebendo as arestas computadas por prim e kruskal

class Tree:
    def montar_prim(self,all_points,link,custo):
        self.arestas = []
        #aqui eu vejo o array de link e o de custo e monto as arestas resultantes
        for i in range(0,len(link)):
            if(link[i] != -1):
                aresta = (all_points[i],all_points[link[i]],custo[i])
                self.arestas.append(aresta)
        
        #aqui eu monto as adjancencias para cada vertice
        self.lista_adjacencias = []
        for i in range(0,len(all_points)):
            adjacencia = []

            for aresta in self.arestas:
                if(aresta[0] == all_points[i]):
                    adjacencia.append((aresta[1],aresta[2]))
                if(aresta[1] == all_points[i]):
                    adjacencia.append((aresta[0],aresta[2]))

            self.lista_adjacencias.append(adjacencia)
    
    def achar_caminho(self,start,goal,all_points):
        #Fiz uma versão de busca em largura
        #Tenho o estado inicial, gero os filhos, coloca na fronteira pra serem analisados,repito até achar
        caminho = []
        lista_estados = [Estado(start)]
        
        for estado in lista_estados:
            if(estado.point == goal):
                while(estado.pai != None):
                    caminho.insert(0,estado)
                    estado = estado.pai
                break
            
            estado.gerar_filhos(all_points,self.lista_adjacencias)

            for filho in estado.filhos:
                lista_estados.append(filho)
        
        for vertice in caminho:
            print(vertice.point)
                    

        
#--------------------------------funções para PRIM---------------------

def procurar_vizinhos(all_points,atual,G):
    #Essa função retorna todas as arestas que possuem o vértice atual
    #lembrando que uma aresta é (ponto1,ponto2,peso)
    lista = []
    for aresta in G:
        if(all_points[atual] == aresta[0] or all_points[atual] == aresta[1]):
            lista.append(aresta)
    return lista

def procurar_vertice(all_points,atual):
    #essa função recebe um ponto e procura qual a posição dele no array dos pontos

    for i in range(0,len(all_points)):
        if(atual == all_points[i]):
            return i

def extrair_minimo(fila,pesos):
    escolhido = -1
    peso = -1

    for i in range(0,len(fila)):
        if(fila[i] == 0):
            if(escolhido == -1 or peso > pesos[i]):
                escolhido = i
                peso = pesos[i]

    return escolhido

def mstPrim(G,all_points,start):

    fila = [] #Fila dos vértices que ainda não foram explorados (0 indica nao visitado, 1 já visitado)
    for i in range(0,len(all_points)):
        fila.append(0)
    
    pesos = []
    link = []

    for i in range(0,len(all_points)):
        pesos.append(np.inf)
        link.append(-1)

    pesos[0] = 0  #ponto start

    while(0 in fila):
        atual = extrair_minimo(fila,pesos) #procuro o vertice não visitado com menor valor (atual = index de all_points)
        lista_vizinhos = procurar_vizinhos(all_points,atual,G) #lista de todas as arestas que saem desse vertice

        for aresta in lista_vizinhos:
            analisando = -1

            if(aresta[0] == all_points[atual]):
                analisando = procurar_vertice(all_points,aresta[1])
            
            if(aresta[1] == all_points[atual]):
                analisando = procurar_vertice(all_points,aresta[0])

            if(pesos[analisando] > aresta[2] and fila[analisando] == 0):
                link[analisando] = atual
                pesos[analisando] = aresta[2]
                
        
        fila[atual] = 1 #marco o vertice como visitado

    T = Tree()
    T.montar_prim(all_points,link,pesos)
    return T

#--------------------------------funções para leitura e montar arestas com visada---------------------
def read_point(file):
    #Essa função lê uma linha do arquivo, trata a entrada e retorna uma tupla representando um ponto
    line = file.readline()
    line = line.split(',')
    
    for i in range(0,len(line)):
        line[i] = line[i].strip()
        line[i] = line[i].strip('\n')

    point = geometry.Point(float(line[0]),float(line[1]))
    return point

def build_list(start,goal,V):
    #essa função retorna uma lista com todos os pontos (Vértices), descosiderando os objetos
    list = [start,goal]

    for object in V:
        for point in object:
            list.append(point)

    return list


def ja_tem_aresta(aresta,G):
    #Essa função analisa as arestas com visadas para evitar duplicatas

    #Tem que checar se existe o oposto
    #se tem a aresta (a,b,10) não precisa da aresta (b,a,10)
    procurar = (aresta[1],aresta[0],aresta[2])
    if(procurar not in G):
        return False
    return True


def tem_visada(ponto_a,ponto_b,V):
    #essa função recebe dois pontos e checa se existe visada direta entre eles
    #Lembrando que V são os vertices relacionados com 3 listas (objetos)

    ponto1_x = ponto_a.x
    ponto1_y = ponto_a.y

    ponto2_x = ponto_b.x
    ponto2_y = ponto_b.y

    s = 0.0
    while(s <= 1):
        
        x1 = ponto1_x * s
        y1 = ponto1_y * s

        x2 = ponto2_x * (1.0-s)
        y2 = ponto2_y * (1.0-s)

        new_point = geometry.Point((x1 + x2),(y1 + y2))

        visada = True
        for object in V:
            poligono = geometry.Polygon(object)
            if(poligono.contains(new_point)):
                visada = False
        
        if(not visada):
            return False 

        s += 0.1
    
    return True


def montarGrafoVisibilidade(list,V):
    #G = Lista de todos as arestas que tem visada direta
    G = []

    for i in range(0,len(list)):
        for j in range(0,len(list)):
            if(i != j):
                if(tem_visada(list[i],list[j],V)):
                    peso = list[i].distance(list[j])
                    aresta = (list[i],list[j],peso)
                    if(not ja_tem_aresta(aresta,G)):
                        G.append(aresta)

    return G


def lerVertices(file,n_obstacles):
    #V é uma lista com 3 listas, representando os 3 obstaculos. As 3 listas são formadas por tuplas, representando os vertices
    V = [] 

    while(n_obstacles > 0):
        n_vertices = file.readline()
        n_vertices = int(n_vertices)

        obstaculo = []
        
        while(n_vertices > 0):
            vertice = read_point(file)
            obstaculo.append(vertice)

            n_vertices -= 1

        V.append(obstaculo)
        n_obstacles -= 1

    return V


#--------------------------------FUNÇÃO MAIN---------------------

def Main():
    file = open("input",'r')

    start = read_point(file)
    goal = read_point(file)
    
    n_obstacles = file.readline()
    n_obstacles = int(n_obstacles)

    V = lerVertices(file,n_obstacles) #Vertices relacionados com os obstaculos

    all_points = build_list(start,goal,V) #lista de todos os pontos sem distinção de obstaculo
    print("Lista de vértices: ")
    for i in range (0,len(all_points)):
        print(i,all_points[i])

    G = montarGrafoVisibilidade(all_points,V) #G se torna uma lista de todas as arestas existentes
    G.sort(key=lambda x:x[2]) #ordena as arestas pelo peso

    T = mstPrim(G,all_points,start)

    print("\n\nLISTA DE ARESTAS PARA A ÁRVORE DE PRIM\n")
    i = 0
    for vertice in T.lista_adjacencias:
        print(i,all_points[i], "SE CONECTA com:")
        for conexao in vertice:
            print(conexao[0],conexao[1])
        print("Indo para o proximo vertice...\n")
        i += 1
    print("O caminho é: ")
    T.achar_caminho(start,goal,all_points)
    

Main()
