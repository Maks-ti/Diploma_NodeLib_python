
from GraphLibrary import Edge, Node, Graph
import asyncio


async def main():
    async with Graph(sender_endpoint="http://localhost:9090/") as graph:
        node = graph.create_node()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())

