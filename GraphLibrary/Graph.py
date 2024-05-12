
import asyncio
import uuid
from queue import Queue
import aiohttp
import json

from GraphTransferLibrary import Command, RpcRequest
from .Node import Node


class Graph:
    def __init__(self, sender_endpoint):
        self._manager_id: str = str(uuid.uuid4())
        self.node_pool: list[Node] = []
        self.sender_endpoint = sender_endpoint
        self.queue: Queue = Queue()
        self.cancellation_event = asyncio.Event()

        # Create an aiohttp session
        self.session = aiohttp.ClientSession()

        # Start the queue processing task
        self.__queue_handler_task = asyncio.create_task(self.queue_processing_async())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.dispose()

    async def dispose(self):
        await asyncio.sleep(0.1)  # Delay to ensure all commands are queued
        self.cancellation_event.set()
        await self.__queue_handler_task
        await self.session.close()
        print("Graph disposed")

    def create_node(self, name="", color="", size=0.0, selected=False, visited=0, value=None):
        new_node = Node(self.queue, name=name, color=color, size=size, selected=selected, visited=visited, value=value)
        self.node_pool.append(new_node)
        return new_node

    def get_node_by_id(self, node_id):
        return next((node for node in self.node_pool if node.id == node_id), None)

    def delete_node(self, node):
        if node not in self.node_pool:
            raise ValueError(f"Node with id = {node.id} does not exist in this Graph")
        node.delete()
        self.node_pool.remove(node)

    async def queue_processing_async(self):
        print("Queue processing started")
        while not self.cancellation_event.is_set() or not self.queue.empty():
            if not self.queue.empty():
                try:
                    command = self.queue.get_nowait()
                except asyncio.QueueEmpty:
                    await asyncio.sleep(0.1)
                    continue
                except BaseException as ex:
                    print(ex)
                    continue
                success = await self.send_command_async(command)
                if not success:
                    self.queue.put(command)  # Re-queue the command if not successfully sent
                    await asyncio.sleep(1)  # Retry delay
            else:  # queue is empty
                await asyncio.sleep(0.5)

    async def send_command_async(self, command: Command):
        rpc_request = RpcRequest(command, self._manager_id, str(uuid.uuid4()))
        json_data = rpc_request.to_json()

        try:
            async with self.session.post(self.sender_endpoint, data=json_data,
                                         headers={'Content-Type': 'application/json'}) as response:
                print(response)
                if response.status == 200:
                    print("status 200")
                    response_text = await response.text()  # Получаем ответ как текст
                    try:
                        rpc_response = json.loads(response_text)  # Десериализуем текст в объект Python
                        print(f"*** response = {rpc_response}")
                        if rpc_response.get("error") is None:
                            print(f"Request processed successfully. Result: {rpc_response.get('result')}")
                            return True
                        else:
                            print(f"Request processing error: {rpc_response.get('error')}")
                    except json.JSONDecodeError:
                        print("Failed to decode JSON")
                else:
                    print(f"HTTP request error: {response.status}")
        except Exception as e:
            print(f"Error sending request: {str(e)}")
        return False

