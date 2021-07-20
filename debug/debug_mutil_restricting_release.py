from random import uniform

from simple_tx import SimpleTx
from loguru import logger

rpc = 'http://10.1.1.51:6789'
chain_id = 210423
main_address, main_private_key = 'lat1rzw6lukpltqn9rk5k59apjrf5vmt2ncv8uvfn7', 'f90fd6808860fe869631d978b0582bb59db6189f7908b578a886d582cb6fccfa'
cdf_address = 'lat1kvurep20767ahvrkraglgd9t34w0w2g059pmlx'
tx = SimpleTx(rpc)
accounts = []
account_total = 500
random_amount = lambda: tx.web3.toWei(uniform(1000000, 3000000), 'ether')


'''开始运行'''
# logger.info(f'#### 开始质押节点, 块高 {tx.platon.blockNumber}')
# staking_address, staking_private_key = tx.create_account()
# tx.transfer(main_private_key, staking_address, 10 * 10 ** 18)
# plan = [{'Epoch': 80, 'Amount': random_amount()}, {'Epoch': 160, 'Amount': random_amount()}, {'Epoch': 320, 'Amount': random_amount()}]
# tx.restricting(main_private_key, staking_address, plan)
# node_url = 'http://192.168.120.121:6790'
# result = tx.staking(staking_private_key, 1, node_url, amount=550000 * 10 ** 18, reward_per=6666)
# assert result['code'] == 0
delegable_nodes = tx.get_delegable_nodes(cdf_address)
delegable_node_id = delegable_nodes[0]['NodeId']
logger.info(f'delegable node id = {delegable_node_id}')
assert delegable_node_id
logger.info(f'#### 质押节点完成, 节点 {delegable_node_id}, 块高 {tx.platon.blockNumber}')


logger.info(f'#### 开始创建账户, 块高 {tx.platon.blockNumber}')
for i in range(account_total):
    logger.info(f'创建第 {i} 个账户')
    address, private_key = tx.create_account()
    tx.transfer(main_private_key, address, 10 * 10 ** 18)
    accounts.append((address, private_key))
logger.info(f'#### 创建账户完成, 共 {len(accounts)} 个, 块高 {tx.platon.blockNumber}')


main_nonce = tx.platon.getTransactionCount(main_address)
tx.ppos.need_analyze = False
tx.ppos.need_quota_gas = True

logger.info(f'#### 开始锁仓, 块高 {tx.platon.blockNumber}')

for address, private_key in accounts:
    plan = [{'Epoch': 1, 'Amount': random_amount()}, {'Epoch': 2, 'Amount': random_amount()}, {'Epoch': 3, 'Amount': random_amount()}]
    result = tx.restricting(main_private_key, address, plan, {'nonce': main_nonce})
    main_nonce += 1
logger.info(f"最后一个锁仓交易结果：{tx.platon.waitForTransactionReceipt(result['hash'])}")
logger.info(f'#### 锁仓完成, 共 {len(accounts)} 个, 块高 {tx.platon.blockNumber}')


logger.info(f'#### 开始委托节点, 块高 {tx.platon.blockNumber}')
for i, (address, private_key) in enumerate(accounts):
    logger.info(f'## 委托第 {i} 个账户!')
    result = tx.delegate(private_key, delegable_node_id, 1, random_amount())
logger.info(f"最后一个委托交易结果：{tx.platon.waitForTransactionReceipt(result['hash'])}")
logger.info(f'#### 委托节点结束, 块高 {tx.platon.blockNumber}')

