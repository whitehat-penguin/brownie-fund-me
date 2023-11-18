from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-1", "mainnet-fork"]

# static variables
DECIMALS = 8
STARTING_PRICE = 2000 * pow(10, 8)

def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    
    else:
        return accounts.add(config["wallets"]["from_key"])
    
def deploy_mocks():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(MockV3Aggregator) <= 0:
            print("deploying mocks")
            MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
            print("mocks deployed")
        
        else:
            print("mock existed")
        
        price_feed_address = MockV3Aggregator[-1].address
    
    else:
        print(f"using {network.show_active()}")
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    
    return price_feed_address