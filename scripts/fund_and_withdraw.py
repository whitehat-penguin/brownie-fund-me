from brownie import FundMe, network, config
from scripts.helpful_scripts import get_account, deploy_mocks

def fund():
    fund_me = FundMe[-1]
    account = get_account()
    # entrance_fee_in_usd = fund_me.getMinUsd() + 1
    entrance_fee_in_usd = 2000
    entrance_fee_in_wei = fund_me.usdToWei(entrance_fee_in_usd)
    entrance_fee_actual_in_wei = fund_me.getConversionRate(entrance_fee_in_wei)
   
    fund_me.fund({"from": account, "value": entrance_fee_in_wei})

def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdrawFull({"from": account})

def main():
    fund()
    withdraw()