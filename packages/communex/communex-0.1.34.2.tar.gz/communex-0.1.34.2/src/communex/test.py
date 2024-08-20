from communex.client import CommuneClient
from time import sleep
from communex._common import get_node_url



node = get_node_url(use_testnet=True)
print(node)
for _ in range(1000):
    print("#########################")
    print("trying to connect to node")
    try:
        x = CommuneClient(node)
    except Exception as e:
        breakpoint()
        exit(0)
    block = x.get_block()
    print(f"block: {block}")
    print("estabilished connection")
    print("-------------------------")

    sleep(1)
