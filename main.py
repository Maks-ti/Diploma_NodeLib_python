
from GraphLibrary import Edge, Node, Graph
import asyncio
from collections import deque


async def Test_BFS():
    async with Graph(sender_endpoint="http://localhost:9090/") as graph:
        node1 = graph.create_node("node 1", "#0ff", 30, value=12)
        node2 = graph.create_node("node 2", "#00f", 25, value=11)
        node3 = graph.create_node("node 3", "#f00", 20, value=5)
        node4 = graph.create_node("node 4", "#00f", 15, value=3)
        node5 = graph.create_node("node 5", "#f00", 22, value=1)
        node6 = graph.create_node("node 6", "#990", 35, value=75)
        node7 = graph.create_node("node 7", "#ff0", 22, value=18)
        node8 = graph.create_node("node 8", "#aaa", 23, value=17)
        node9 = graph.create_node("node 9", "#888", 42, value=15)

        node1.add_child(node2)
        node1.add_child(node3)
        node1.add_child(node4)
        node1.add_child(node5)

        node3.add_child(node6)
        node3.add_child(node7)
        node3.add_child(node8)

        node5.add_child(node8)
        node5.add_child(node9)

        await BFS(graph, node1)
        return


async def BFS(graph: Graph, start_node: Node):
    queue = deque([start_node])

    while queue:
        current_node = queue.popleft() # Извлекаем узел с начала очереди
        if not current_node.visited:
            await asyncio.sleep(1)  # debug
            input(f"node = {current_node.name}")  # debug
            await asyncio.sleep(1)  # debug
            current_node.visited = True  # посещаем узел
            current_node.color = '#0f0'  # окрашиваем для наглядности

            # Добавление непосещенных дочерних узлов в очередь
            for child in current_node.childs:
                child_node: Node = child.node_to
                if not child_node.visited:
                    queue.append(child_node)
    return


if __name__ == '__main__':
    asyncio.run(Test_BFS())


'''

def BFS(graph: Graph, start_node: Node):
    queue = deque([start_node])

    while queue:
        current_node = queue.popleft() # Извлекаем узел с начала очереди
        if not current_node.visited:
            current_node.visited = True  # посещаем узел
            current_node.color = '#0f0'  # окрашиваем для наглядности

            # Добавление непосещенных дочерних узлов в очередь
            for child in current_node.childs:
                child_node: Node = child.node_to
                if not child_node.visited:
                    queue.append(child_node)
    return

'''
