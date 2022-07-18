import numpy as np
from shapely import geometry

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
    #essa função retorna uma lista com todos os pontos, descosiderando os objetos
    list = [start,goal]

    for object in V:
        for point in object:
            list.append(point)

    return list

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

def Main():
    file = open("input",'r')

    start = read_point(file)
    goal = read_point(file)
    
    n_obstacles = file.readline()
    n_obstacles = int(n_obstacles)

    V = lerVertices(file,n_obstacles)
    all_points = build_list(start,goal,V)

    G = montarGrafoVisibilidade(all_points,V)
    G.sort(key=lambda x:x[2]) #ordena as arestas pelo peso


Main()
