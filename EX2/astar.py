def get_heuritsic(self, goal):
        self.heuristic = {}
        print("\nEnter heuristic values:")
        for node in self.graph:
            if node == goal:
                self.heuristic[node] = 0
            else:
                self.heuristic[node] = int(
                    input(f"Heuristic value for {node}: ")
                )


    # ---------------- A* Search ----------------
    def aStarSearch(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal node does not exist")
            return

        openList = [(self.heuristic[start], 0, start, [start])]
        exploredList = []
        iteration = 1

        print("\n================ A* SEARCH TABLE ================")
        print(f"{'Itr':<5}{'Current':<10}{'Fringe (Open)':<35}{'Explored'}")
        print("-" * 80)

        while openList:
            openList.sort(key=lambda x: x[0])

            fringeView = [(node, f) for (f, g, node, p) in openList]

            fValue, gCost, currentNode, pathList = openList.pop(0)
            exploredList.append(currentNode)

            print(f"{iteration:<5}{currentNode:<10}{str(fringeView):<35}{exploredList}")

            if currentNode == goal:
                print("\nGOAL FOUND")
                print("Path:", " -> ".join(pathList))
                print("Total Cost:", gCost)
                return

            for neighborNode, weight in self.graph[currentNode]:
                if neighborNode in exploredList:
                    continue

                newG = gCost + weight
                newF = newG + self.heuristic[neighborNode]

                foundBetter = False
                for i, (f, g, node, p) in enumerate(openList):
                    if node == neighborNode:
                        if newF < f:
                            openList.pop(i)
                        else:
                            foundBetter = True
                        break

                if not foundBetter:
                    openList.append(
                        (newF, newG, neighborNode, pathList + [neighborNode])
                    )

            iteration += 1

        print("No path found")

