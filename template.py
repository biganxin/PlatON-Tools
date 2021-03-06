from simple_tx import SimpleTx
from platon import Web3, HTTPProvider

# 准备
rpc = 'http://10.0.0.11:6789'
# rpc = 'http://192.168.120.121:6789'
# main_address, main_private_key = 'lat1fyeszufxwxk62p46djncj86rd553skppy4qgz4', 'a11859ce23effc663a9460e332ca09bd812acc390497f8dc7542b6938e13f8d7'
tx = SimpleTx(rpc)
tx.ppos.need_quota_gas = False
tx.pip.need_quota_gas = False

print(tx.decode_rlp(bytes.fromhex('c786333031313131')))

# print(tx.hrp)
# print(tx.platon.chainId)
# print(tx.admin.getProgramVersion())
# print(tx.pip.getActiveVersion())
# print(tx.pip.getGovernParamValue('restricting', 'minimumRelease'))
# print(tx.pip.getActiveVersion())


# **** 交易模块 ****
# to_address, to_private_key = tx.create_account()
# # 普通交易
# tx.transfer(main_private_key, 'atp19tdhg4e2z2pd3fx2029datt5p46nlg3mft733j', 2000000 * 10 ** 18)
# print(f'## Balance: {tx.platon.getBalance(to_address)}')
# # 锁仓交易
# plan = [{'Epoch': 1, 'Amount': 5000 * 10 ** 18}, {'Epoch': 2, 'Amount': 5000 * 10 ** 18}, {'Epoch': 4, 'Amount': 10000 * 10 ** 18}]
# tx.restricting(main_private_key, to_address, plan)
# print(f'## Restricting: {tx.ppos.getRestrictingInfo(to_address)}')


# **** 质押模块 ****
# node_url = 'http://192.168.120.124:6790'
# node_id = '7038eb30c06683c97282d0d7acbf939c15bcfc390eb461983445c2d58328d88b85a3d4c79867c18a5ed9442a13062c4b5a9f9e03ea7026e000c9b13c2a1d3255'
# bls_pubkey = 'd2f1be8a9832048f745d30095e483fd187dd37972ef7bd6491bc6cd957372ab16ca3f9d6f4c20a41b9b9d235fca51f12ab2c21029b495647692482714573bef10d444858ddc404c97d117cb7950b1b157e3bffb1be13f31623612fd057efc605'
# staking_address, staking_private_key = tx.create_account()
# # 创建质押
# tx.transfer(main_private_key, staking_address, 30000 * 10 ** 18)
# plan = [{'Epoch': 10, 'Amount': 5000 * 10 ** 18},
#         {'Epoch': 20, 'Amount': 5000 * 10 ** 18},
#         {'Epoch': 40, 'Amount': 10000 * 10 ** 18}]
# tx.restricting(main_private_key, staking_address, plan)
# tx.staking(staking_private_key, 0, node_url, 20000 * 10 ** 18, 1000)
# # 增持质押
# tx.transfer(main_private_key, staking_address, 20 * 10 ** 18)
# plan = [{'Epoch': 1, 'Amount': 80 * 10 ** 18}]
# tx.restricting(main_private_key, staking_address, plan)
# tx.increase_staking(staking_private_key, node_id, 0, 10 * 10 ** 18)
# # 修改质押信息
# tx.edit_staking(staking_private_key, node_id, external_id='shinnng')
# # 解除质押
# tx.wait_block(40 * 4 * 2)      # 等待2个结算周期
# staking_address, staking_private_key = 'atp1mee8mwugjmyl4jj8jz0z4c0sjh3heypd6enz5y', '50b2e5ac9ca2bc3f56eb6258c8eca63d4dbe1dac7b5f9997e73ea3d8078f7ca7'
# tx.withdrew_staking(staking_private_key, node_id)


# **** 委托模块 ****
# node_id = 'bc9dabae54a13202ec765c1537c57b9f6659161596eae7c0344a606e9396c63c96a2a76aadc320100e9a56c5acdb8faddfb61733bddeff7b9f261ac54a46d775'
# delegation_address, delegation_private_key = tx.create_account()
# # 创建委托
# tx.transfer(main_private_key, delegation_address, 30 * 10 ** 18)
# plan = [{'Epoch': 1, 'Amount': 80 * 10 ** 18}]
# tx.restricting(main_private_key, delegation_address, plan)
# tx.delegation(delegation_private_key, node_id, 0, 20 * 10 ** 18)
# # 领取委托分红
# tx.withdraw_delegate_reward(delegation_private_key)
# # 撤销委托
# delegation_address, delegation_private_key = 'atp1chcxl7scekg66te7e5r5lhuwyd2us9tgzn3grx', 'c96b51aee0b0ee66f82aed631bfb989b1a0b3a08d323af2fd125cedf835d4095'
# tx.undelegation(delegation_private_key, node_id, 10 * 10 ** 18)


# **** 治理模块 ****
# upgrade_version = 65792
# upgrade_voting_rounds = 4
# # 升级提案
# staking_private_key = 'a42964a1a001fe909d93ea1cae5a14cdcb285dd00148d966d7d8210b86ee7ba5'
# node_id = tx.web3.admin.nodeInfo.id

# tx.version_proposal(staking_private_key, node_id, upgrade_version, upgrade_voting_rounds)
# proposals = tx.get_proposal_list()
# print(f'proposals == {proposals}')
#
# # # 提案投票
# proposal_id = proposals['Ret'][0]['ProposalID']
# print(proposal_id)
#
# node_list = [('http://192.168.112.30:6700', 'a42964a1a001fe909d93ea1cae5a14cdcb285dd00148d966d7d8210b86ee7ba5'),
#              ('http://192.168.112.31:6700', 'a42964a1a001fe909d93ea1cae5a14cdcb285dd00148d966d7d8210b86ee7ba5'),
#              ('http://192.168.112.32:6700', 'a42964a1a001fe909d93ea1cae5a14cdcb285dd00148d966d7d8210b86ee7ba5'),
#              ('http://192.168.112.33:6700', 'a42964a1a001fe909d93ea1cae5a14cdcb285dd00148d966d7d8210b86ee7ba5')]
#
# # for node_url, private_key in node_list:
# #     w3 = Web3(HTTPProvider(node_url), chain_id=chain_id, hrp_type=hrp)
# #     print(w3.getAddressHrp)
#
# for node_url, private_key in node_list:
#     try:
#         tx.vote(private_key, node_url, proposal_id, 1)
#     except Exception as e:
#         print(f'ERROR: {node_url}, {e}')
# 版本声明
# node_list = [('http://192.168.120.121:6790', '64bc85af4fa0e165a1753b762b1f45017dd66955e2f8eea00333db352198b77e'),
#              ('http://192.168.120.122:6790', '64bc85af4fa0e165a1753b762b1f45017dd66955e2f8eea00333db352198b77e'),
#              ('http://192.168.120.123:6790', '971bd2cf5c08841ef7ea08f2a863c4fdfe70bfacaa1ff87800c889a0ecab462a'),
#              ('http://192.168.120.124:6790', '971bd2cf5c08841ef7ea08f2a863c4fdfe70bfacaa1ff87800c889a0ecab462a'),
#              ]
# for node_url, private_key in node_list:
#     tx.declear_version(private_key, node_url)
#
#
# # **** 检查信息 ****
# print(tx.platon.blockNumber)
# print(tx.platon.getBalance('atx1h0ssa942rrwy7yt8m4tjcsvpkr5z5qhmwx55av'))
# print(tx.platon.gasPrice)
# print(tx.ppos.getRestrictingInfo('atx1h0ssa942rrwy7yt8m4tjcsvpkr5z5qhmwx55av'))
# print(tx.platon.getTransactionCount('atx1zkrxx6rf358jcvr7nruhyvr9hxpwv9unj58er9'))
# print(tx.platon.waitForTransactionReceipt('0xda81aab7e6d9f5188081fbd281fd0eaaebef1f1be03ff2c98fd1f76c36c16ec5'))
# print(tx.platon.getCode('atx1rdlcxzxk88e7k7mm0w93ald07g52l6pw97gzzz'))
# print(tx.ppos.getValidatorList())
# print(tx.ppos.getVerifierList())
# print(tx.ppos.getCandidateList())
# print(tx.ppos.getCandidateInfo('bc9dabae54a13202ec765c1537c57b9f6659161596eae7c0344a606e9396c63c96a2a76aadc320100e9a56c5acdb8faddfb61733bddeff7b9f261ac54a46d775'))
# print(tx.pip.listProposal())
# print(tx.pip.getProposal('0x9552914c57933ad207d2c028cf71445de40b99f3b088155f31f07bdc4ddab2e2')['Ret']['ActiveBlock'])
# print(tx.pip.getAccuVerifiersCount('0x7991b9bb943c0fc67df975975e34602ca501610b31ea842079137c59be5e6b0d', tx.platon.getBlock(tx.platon.blockNumber)['hash'].hex()))
# print(tx.pip.getTallyResult('0x15e460705e953944b5523b4b26413d94d9ef9ef88e50e1911bf4e4f0ba4897a7'))
# print(tx.pip.getTallyResult('0x2bc2f6212e903c66fb027b7e9f80b77f28a2fb46bc815866fd5f7027915b89af'))
# print(tx.pip.getActiveVersion())