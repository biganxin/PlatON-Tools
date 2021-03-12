from threading import Lock
from setting import cdf_address, load_funcs, load_ratios, web3


def gen_func_list(funcs, ratios):
    func_list = []
    for i, func in enumerate(funcs):
        for _ in range(ratios[i]):
            func_list.append(func)
    return func_list


def get_delegable_nodes(cdf_account):
    result = web3.ppos.getCandidateList()
    delegable_nodes = [i for i in result['Ret'] if i['StakingAddress'] != cdf_account]
    return delegable_nodes


def create_account(w3):
    account = w3.platon.account.create()
    address = account.address
    private_key = account.privateKey.hex()[2:]
    return address, private_key


# 获取账户对某个节点的委托信息
def get_delegate_list_for_node(address, node_id):
    delegateds = []
    result = web3.ppos.getRelatedListByDelAddr(address)
    if result['Code'] == 0:
        for delegated_info in result['Ret']:
            if delegated_info['NodeId'] is node_id:
                delegateds.append(delegated_info)
    return delegateds

# 压测信息生成
delegable_nodes = get_delegable_nodes(cdf_address)
funcs_list = gen_func_list(load_funcs, load_ratios)
lock = Lock()