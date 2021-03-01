import random
import time
from client_sdk_python import HTTPProvider, Web3
from client_sdk_python import eth, ppos, pip
from client_sdk_python.middleware import geth_poa_middleware
from hexbytes import HexBytes
from client_sdk_python.packages.platon_account.account import Account


# 通用信息
NODE_URL = 'http://10.0.0.20:6789'
CHAIN_ID = 2021
WEB3 = Web3(HTTPProvider(NODE_URL), chain_id=CHAIN_ID)
HRP = WEB3.net_type
WEB3.middleware_stack.inject(geth_poa_middleware, layer=0)
PLATON = eth.PlatON(WEB3)
PPOS = ppos.Ppos(WEB3)
PIP = pip.Pip(WEB3)
PIP_TX_CFG = {'gasPrice': 3000000000000000}

# 创建账户
def create_account():
    print("==== create account =====")
    account = PLATON.account.create()
    address = account.address
    prikey = account.privateKey.hex()[2:]
    print(f"create account = {address}, {prikey}")
    return address, prikey

# 创建HD钱包
# TODO: coding
# def create_hd_account():
#     print("==== create hd account =====")
#     # account = WEB3.platon.account.(net_type=HRP)
#     master_key, mnemonic = HDPrivateKey.master_key_from_entropy()
#     print(master_key)
#     print(mnemonic)
#     root_keys = HDKey.from_path(master_key, "m/44'/206'/0'")
#     print(root_keys)
#     acct_priv_key = root_keys[-1]
#     print(acct_priv_key)
    # for j in range(30):
    #     keys = HDKey.from_path(acct_priv_key, '{change}/{index}'.format(change=0, index=j))
    #     private_key = keys[-1]
    #     public_address = private_key.public_key.address('atp')
    #     keystores[public_address] = json.dumps(private_key._key.to_keyfile_json(password))
    #     privateKeys[public_address] = private_key._key.get_private_key()
    #     addresses_df.loc[(prikey_manager, account_use, wallet_type, i, j), :] = [public_address]

# 转账交易
def transfer(from_privatekey, to_address, amount):
    print("==== transfer =====")
    from_address = Account.privateKeyToAccount(from_privatekey, HRP).address
    nonce = PLATON.getTransactionCount(from_address)
    transaction_dict = {
        "to": to_address,
        "gasPrice": WEB3.eth.gasPrice,
        "gas": 21000,
        "nonce": nonce,
        "data": '',
        "chainId": CHAIN_ID,
        "value": amount,
    }
    signedTransactionDict = WEB3.platon.account.signTransaction(
        transaction_dict, from_privatekey
    )
    data = signedTransactionDict.rawTransaction
    result = HexBytes(PLATON.sendRawTransaction(data)).hex()
    result = PLATON.waitForTransactionReceipt(result)
    print(f"transfer staking result = {result}")
    return result

# 锁仓交易
def restricting(from_private_key, to_address, restricting_plan):
    print("==== create restricting plan =====")
    # ppos.need_analyze = False
    result = PPOS.createRestrictingPlan(to_address, restricting_plan, from_private_key)
    print(f"create restricting plan result = {result}")
    return result

# 创建质押
def staking(staking_private_key, balance_type, node_url, amount=10 ** 18 * 2000000, reward_per=1000):
    print("==== create staking =====")
    w3 = Web3(HTTPProvider(node_url), chain_id=CHAIN_ID)
    version_info = w3.admin.getProgramVersion()
    version = version_info['Version']
    version_sign = version_info['Sign']
    node_info = w3.admin.nodeInfo
    node_id = node_info['id']
    bls_pubkey = node_info['blsPubKey']
    bls_proof = w3.admin.getSchnorrNIZKProve()
    benifit_address = Account.privateKeyToAccount(staking_private_key, HRP).address
    result = PPOS.createStaking(balance_type, benifit_address, node_id, 'external_id', 'node_name', 'website', 'details',
                                   amount, version, version_sign, bls_pubkey, bls_proof, staking_private_key, reward_per)
    print(f"create staking result = {result}")
    return result

# 增持质押
def increase_staking(staking_private_key, node_id, balance_type, amount=10 ** 18 * 100):
    print("==== increase staking =====")
    result = PPOS.increaseStaking(balance_type, node_id, amount, staking_private_key)
    print(f'incress staking result = {result}')
    return result

# 修改质押信息
def edit_staking(staking_private_key, node_id, benifit_address=None, external_id=None, node_name=None, website=None, details=None, reward_per=None):
        print("==== edit staking =====")
        result = PPOS.editCandidate(staking_private_key, node_id, benifit_address, external_id, node_name, website, details, reward_per)
        print(f'edit staking result = {result}')
        return result

# 解除质押
def withdrew_staking(staking_private_key, node_id):
    print("==== withdrew staking =====")
    result = PPOS.withdrewStaking(node_id, staking_private_key)
    print(f'withdrew staking result = {result}')
    return result

# 查询质押信息
def get_staking_info(node_id):
    print("==== get staking info =====")
    result = PPOS.getValidatorList()
    print(f'get validator list = {result}')
    result = PPOS.getVerifierList()
    print(f'get verifier list = {result}')
    result = PPOS.getCandidateList()
    print(f'get candidate list = {result}')
    result = PPOS.getCandidateInfo(node_id)
    print(f'get candidate info = {result}')

# 获取可委托节点列表
def get_delegable_nodes(cdf_account):
    candidate_list = ppos.getCandidateList()['Ret']
    delegable_nodes = [i for i in candidate_list if i['StakingAddress'] != cdf_account]
    return delegable_nodes

# 创建委托
def delegation(delegation_private_key, node_id, balance_type, amount=10 * 10 ** 18):
    print("==== delegation =====")
    result = PPOS.delegate(balance_type, node_id, amount, delegation_private_key)
    print(f'delegation result = {result}')
    return result

# 解除委托
def undelegation(delegation_private_key, node_id, amount=1 * 10 ** 18):
    print("==== undelegation =====")
    delegation_address = Account.privateKeyToAccount(delegation_private_key).address
    result = PPOS.getRelatedListByDelAddr(delegation_address)
    print(f'get related list = {result}')
    block_number = result.get('Ret')[0].get('StakingBlockNum')
    assert block_number != ''
    result = PPOS.withdrewDelegate(block_number, node_id, amount, delegation_private_key)
    print(f'undelegation result = {result}')
    return result

# 查询委托信息
def get_delegation_list(delegation_address):
    print("==== get delegation list =====")
    result = PPOS.getRelatedListByDelAddr(delegation_address)
    print(f'get delegation list = {result}')
    return result

# 领取委托分红
def withdraw_delegate_reward(delegate_private_key):
    print("==== withdraw delegate reward =====")
    result = PPOS.withdrawDelegateReward(delegate_private_key)
    print(f'withdraw delegate result = {result}')
    return result

# 创建升级提案
def version_proposal(node_private_key, node_id, upgrade_version, voting_rounds):
    print("==== create version proposal =====")
    result = PIP.submitVersion(node_id, str(time.time()), upgrade_version, voting_rounds, node_private_key, PIP_TX_CFG)
    print(f'create version proposal result = {result}')
    return result

# 创建文本提案
def text_proposal(node_private_key, node_id):
    print("==== create test proposal =====")
    result = PIP.submitText(node_id, str(time.time()), node_private_key, PIP_TX_CFG)
    print(f'create version proposal result = {result}')
    return result

# 查询提案列表
def get_proposal_list():
    print("==== get proposal list =====")
    pip_list = PIP.listProposal()
    print(f"proposal list = {pip_list}")
    return pip_list

# 提案投票
def vote(node_private_key, node_url, proposal_id, vote_type):
    print("==== vote =====")
    w3 = Web3(HTTPProvider(node_url), chain_id=CHAIN_ID)
    program_version = w3.admin.getProgramVersion()['Version']
    version_sign = w3.admin.getProgramVersion()['Sign']
    node_id = w3.admin.nodeInfo['id']
    # proposal_id = w3.pip.listProposal().get('Ret')[0].get('ProposalID')
    # assert proposal_id != ''
    print(f'vote node: {node_url}, {node_id}')
    result = PIP.vote(node_id, proposal_id, vote_type, program_version, version_sign, node_private_key)
    print(f'version proposal vote result = {result}, {proposal_id}')
    return result

# 版本声明
def declear_version(node_private_key, node_url):
    print("==== declear version =====")
    w3 = Web3(HTTPProvider(node_url), chain_id=CHAIN_ID)
    node_id = w3.admin.nodeInfo['id']
    program_version = w3.admin.getProgramVersion()['Version']
    version_sign = w3.admin.getProgramVersion()['Sign']
    result = PIP.declareVersion(node_id, program_version, version_sign, node_private_key)
    print(f'declear version result = {result}')
    return result

# 获取当前版本号
def get_version():
    print("==== get version =====")
    result = PIP.getActiveVersion()
    print(f'chain version = {result}')

# 等待块高
def wait_block(block_number):
    print("==== wait block ====")
    current_block = PLATON.blockNumber
    end_block = current_block + block_number
    while current_block < end_block:
        print(f'wait block: {current_block} -> {end_block}')
        time.sleep(5)
        current_block = PLATON.blockNumber
