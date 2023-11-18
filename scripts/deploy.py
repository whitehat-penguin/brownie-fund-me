from brownie import FundMe, network, config
from scripts.helpful_scripts import get_account, deploy_mocks

def deploy_fund_me():
    account = get_account()
    price_feed = deploy_mocks()
    
    fund_me = FundMe.deploy(price_feed, {"from": account}, publish_source = config["networks"][network.show_active()]["verify"])
    print(f"contract deployed at {fund_me.address}")

    eth_price = fund_me.getPrice()

    print(eth_price/pow(10,8))

def main():
    deploy_fund_me()