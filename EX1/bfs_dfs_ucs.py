from collections import deque
import heapq

class Graph:
    def __init__(self, weighted=False):
        self.graph = {}
        self.weighted = weighted

    # ---------------- Graph Creation ----------------
    def create_graph(self):
        self.graph = {}
        n = int(input("Enter number of nodes: "))
        while n > 0:
            node = input("Enter node: ")
            if not self.add_node(node):
                print("Node already exists!")
            else:
                n -= 1

        e = int(input("Enter number of edges: "))
        for i in range(e):
            while True:
                u, v = input(f"Edge {i+1} (u v): ").split()
                if self.add_edge(u, v):
                    break
                else:
                    print("Invalid edge or edge already exists!")

    # ---------------- Node ----------------
    def add_node(self, node):
        if node in self.graph:
            return False
        self.graph[node] = []
        return True

    # ---------------- Edge ----------------
    def add_edge(self, u, v):
        if u not in self.graph or v not in self.graph:
            return False

        for edge in self.graph[u]:
            if edge[0] == v:
                return False

        if self.weighted:
            weight = int(input("Enter weight: "))
        else:
            weight = 1

        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
        return True

    # ---------------- Delete ----------------
    def delete_node(self, node):
        if node not in self.graph:
            return False

        self.graph.pop(node)
        for n in self.graph:
            self.graph[n] = [edge for edge in self.graph[n] if edge[0] != node]
        return True

    def delete_edge(self, u, v):
        if u not in self.graph or v not in self.graph:
            return False

        self.graph[u] = [edge for edge in self.graph[u] if edge[0] != v]
        self.graph[v] = [edge for edge in self.graph[v] if edge[0] != u]
        return True

    # ---------------- Display ----------------
    def display_graph(self):
        if not self.graph:
            print("Graph is empty")
            return

        print("\nGraph Adjacency List:")
        for node in sorted(self.graph, key=str):
            if self.weighted:
                print(f"{node} -> {self.graph[node]}")
            else:
                neighbors = [edge[0] for edge in self.graph[node]]
                print(f"{node} -> {', '.join(neighbors) if neighbors else 'None'}")

    def display_adj(self, node):
        if node not in self.graph:
            print("Node doesn't exist")
            return

        if self.weighted:
            print(f"Adjacency of {node}: {self.graph[node]}")
        else:
            neighbors = [edge[0] for edge in self.graph[node]]
            print(f"Adjacency of {node}: {', '.join(neighbors) if neighbors else 'None'}")

    # ---------------- BFS ----------------
    def bfs(self, start, goal, left_to_right=True):
        fringe = deque([start])
        explored = set()
        parent = {start: None}
        cost = {start: 0}

        while fringe:
            node = fringe.popleft()
            if node in explored:
                continue

            explored.add(node)

            if node == goal:
                self.print_path(parent, start, goal)
                print("Total Cost =", cost[node])
                return

            neighbors = sorted(self.graph[node], key=lambda x: x[0])
            if not left_to_right:
                neighbors.reverse()

            for child, w in neighbors:
                if child not in explored and child not in fringe:
                    fringe.append(child)
                    parent[child] = node
                    cost[child] = cost[node] + w

        print("Goal not found")

    # ---------------- DFS ----------------
    def dfs(self, start, goal, left_to_right=True):
        fringe = [start]
        explored = set()
        parent = {start: None}
        cost = {start: 0}

        while fringe:
            node = fringe.pop()
            if node in explored:
                continue

            explored.add(node)

            if node == goal:
                self.print_path(parent, start, goal)
                print("Total Cost =", cost[node])
                return

            neighbors = sorted(self.graph[node], key=lambda x: x[0])
            if left_to_right:
                neighbors.reverse()

            for child, w in neighbors:
                if child not in explored and child not in fringe:
                    fringe.append(child)
                    parent[child] = node
                    cost[child] = cost[node] + w

        print("Goal not found")

    # ---------------- Uniform Cost Search ----------------
    def uniform_cost_search(self, start, goal):
        pq = []
        heapq.heappush(pq, (0, start, [start]))
        explored = {}

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node in explored:
                continue

            explored[node] = cost

            if node == goal:
                print("Path:", " -> ".join(path))
                print("Total Cost:", cost)
                return

            for child, w in self.graph[node]:
                if child not in explored:
                    heapq.heappush(pq, (cost + w, child, path + [child]))

        print("Goal not found")

    # ---------------- Path ----------------
    def print_path(self, parent, start, goal):
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        print("Path:", " -> ".join(path))

# ---------------- Menu ----------------
def menu():
    weighted = input("Is graph weighted? (y/n): ").lower() == 'y'
    g = Graph(weighted)

    while True:
        print("\n----- GRAPH MENU -----")
        print("1. Create Graph")
        print("2. Display Graph")
        print("3. Display Adjacency")
        print("4. Add Node")
        print("5. Add Edge")
        print("6. Delete Node")
        print("7. Delete Edge")
        print("8. BFS (Left-to-Right)")
        print("9. BFS (Right-to-Left)")
        print("10. DFS (Left-to-Right)")
        print("11. DFS (Right-to-Left)")
        print("12. Uniform Cost Search")
        print("13. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            g.create_graph()
        elif choice == "2":
            g.display_graph()
        elif choice == "3":
            g.display_adj(input("Enter node: "))
        elif choice == "4":
            g.add_node(input("Enter node: "))
        elif choice == "5":
            u, v = input("Enter edge (u v): ").split()
            g.add_edge(u, v)
        elif choice == "6":
            g.delete_node(input("Enter node: "))
        elif choice == "7":
            u, v = input("Enter edge (u v): ").split()
            g.delete_edge(u, v)
        elif choice == "8":
            g.bfs(input("Start: "), input("Goal: "), True)
        elif choice == "9":
            g.bfs(input("Start: "), input("Goal: "), False)
        elif choice == "10":
            g.dfs(input("Start: "), input("Goal: "), True)
        elif choice == "11":
            g.dfs(input("Start: "), input("Goal: "), False)
        elif choice == "12":
            g.uniform_cost_search(input("Start: "), input("Goal: "))
        elif choice == "13":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()
