from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from pydantic import BaseModel, Field

import requests, json
import config

app = FastAPI(
    openapi_tags = config.tags_metadata, 
    title = "GateWay for FISCO BCOS",
    description = "一个基于 Python 的简易 FISCO BCOS 网关服务。",
    version = "1.0.0"
)

origins = config.origins

"""
    Routers
"""

"""
    GROUP: web3 
"""
@app.get("/1/web3/blockNumber", tags=["web3"])
async def get_block_number():
    return int(do_get_block_number().text)

@app.get("/1/web3/blockByNumber/{block_number}", tags=["web3"])
async def get_block_by_number(block_number):
    return do_get_block_by_number(block_number)

@app.get("/1/web3/transaction/{tx_hash}", tags=["web3"])
async def get_tx(tx_hash):
    return do_get_tx(tx_hash)

@app.get("/1/web3/transactionReceipt/{tx_hash}", tags=["web3"])
async def get_tx_receipt(tx_hash):
    return do_get_tx_receipt(tx_hash)  

@app.get("/1/web3/")
"""
    GROUP: contract
"""

class Deployer(BaseModel):
    groupId: int = Field(1, example = 1)
    user: str 
    contractName: str = "default_contract"
    abiInfo: list = Field("add abi here", example = config.hello_world_contract["abi"])
    bytecodeBin: str
    funcParam: list = None
    version: str = None

@app.post("/contract/deploy", tags=["contract"])
async def deploy_contract(deployer: Deployer):
    return do_deploy_contract(deployer)

# class 
"""
    Requester
"""

"""
    GROUP: web3 
"""
def do_get_block_number():
    url = config.webase_front_ip + config.webase_paths["web3"]["get_block_number"]
    print(url)
    return requests.get(url)

def do_get_block_by_number(block_number):
    url = config.webase_front_ip + config.webase_paths["web3"]["get_block_by_number"] +\
        block_number
    return requests.get(url).json()

def do_get_tx(tx_hash):
    url = config.webase_front_ip + config.webase_paths["web3"]["get_tx"] +\
        tx_hash
    return requests.get(url).json()

def do_get_tx_receipt(tx_hash):
    url = config.webase_front_ip + config.webase_paths["web3"]["get_tx_receipt"] +\
        tx_hash
    return requests.get(url).json()

"""
    GROUP: contract
"""
def do_deploy_contract(deployer):
    url = config.webase_front_ip + config.webase_paths["contract"]["deploy"]
    response =  requests.post(url, json=deployer.dict())
    return response.text
