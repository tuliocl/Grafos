import numpy as np

class node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.father = None
        self.children = []

        self.acumulated_value = 0
    
    def generate_children(self,occupancy):

        if(self.x - 1 >= 0):
            if(occupancy[self.x - 1][self.y] != np.inf):
               child = node(self.x - 1,self.y)
               child.father = self
               child.acumulated_value = self.acumulated_value + occupancy[self.x - 1][self.y]
               self.children.append(child)

        if(self.x + 1 < len(occupancy)):
           if(occupancy[self.x + 1][self.y] != np.inf):
                child = node(self.x + 1,self.y)
                child.father = self
                child.acumulated_value = self.acumulated_value + occupancy[self.x + 1][self.y]
                self.children.append(child)

        if(self.y + 1 < len(occupancy)):
            if(occupancy[self.x][self.y + 1] != np.inf):
               child = node(self.x,self.y + 1)
               child.father = self
               child.acumulated_value = self.acumulated_value + occupancy[self.x][self.y + 1]
               self.children.append(child)

        if(self.y - 1 >= 0):
            if(occupancy[self.x][self.y-1] != np.inf):
               child = node(self.x,self.y-1)
               child.father = self
               child.acumulated_value = self.acumulated_value + occupancy[self.x][self.y - 1]
               self.children.append(child)


def create_path():

    occupancy = 10 * np.random.rand(10, 10)
    occupancy[0:5, 0] = np.inf
    occupancy[5, 0:5] = np.inf
    occupancy[5:8, 5] = np.inf
    occupancy[0:3, 5:8] = np.inf
    occupancy[7:9, 3] = np.inf
    occupancy[5:10, 8] = np.inf
    
    return occupancy

def create_visited_grid(occupancy):
    visited = []
    for i in occupancy:
        list = []
        for j in range(0,len(i)):
            list.append(0) 
        visited.append(list)
    
    return visited

def check_solution(current,robot_pos_d):
    if(current.x == robot_pos_d[0] and current.y == robot_pos_d[1]):
        return True
    return False

def robot_path(robot_pos_c, robot_pos_d,occupancy):
    visited = create_visited_grid(occupancy)
    frontier = [node(robot_pos_c[0],robot_pos_c[1])]

    path = []

    while(True):
        current = frontier.pop(0)
        if(visited[current.x][current.y] == 1):
            continue
        visited[current.x][current.y] = 1
            
        if(check_solution(current,robot_pos_d)): #vejo se tó no destino
            while(current.father != None):
                path.append(current) 
                current = current.father
            break
                
        current.generate_children(occupancy)
        
        for child in current.children:
            flag = False
            if(visited[child.x][child.y] == 0):
                for i in range(0,len(frontier)):
                    if(child.acumulated_value < frontier[i].acumulated_value):
                        frontier.insert(i,child)
                        flag = True
                        break
                if(flag == False):
                    frontier.append(child)

    return path
def main():
    occupancy = create_path()

    print(occupancy)

    x = int(input("Ponto de partida (X): "))
    y = int(input("Ponto de partida (Y): "))

    robot_pos_c = [x,y]

    x = int(input("Ponto de destino (X): "))
    y = int(input("Ponto de destino (Y): "))

    robot_pos_d = [x,y]
    
    path = robot_path(robot_pos_c, robot_pos_d,occupancy)
    
    for node in path:
        print(node.x,node.y,node.acumulated_value)
    

main()
