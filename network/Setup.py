#!/usr/bin/env python3
import binascii
import sys
import functions
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


admin_private_key = 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70'
iroha = Iroha('admin@test')
# set the ip of one node in the iroha blockchain
network = IrohaGrpc('3.16.203.141:50051')
asset_id = 'choicecoin#choice'
domain_id = 'choice'

# function to create private keys
# private_key = IrohaCrypto.private_key()
#############################
# Slaves node
#############################
# slave 1
slave1_private_key = '7a3a8efe3fbfac57af55e8d2a4b20e27b19444c4d240924dd1bd57701a5a0731'
slave1_public_key = IrohaCrypto.derive_public_key(slave1_private_key)
slave1_name = 'slave1'
slave1_account_id = slave1_name + '@' + domain_id
slave1_iroha = Iroha('slave1@choice')
# slave 2
slave2_private_key = '94ba95a4520107a8a9abc864db900b5c00660c48bbb0333edaa5ab081f52e2ed'
slave2_public_key = IrohaCrypto.derive_public_key(slave2_private_key)
slave2_name = 'slave2'
slave2_account_id = slave2_name + '@' + domain_id
slave2_iroha = Iroha('slave2@choice')
# slave 3
slave3_private_key = '8c578c774f553b99ebbaf89d9314f8ceaf6b4e93119c2550e10cf0de8ee93b51'
slave3_public_key = IrohaCrypto.derive_public_key(slave3_private_key)
slave3_name = 'slave3'
slave3_account_id = slave3_name + '@' + domain_id
slave3_iroha = Iroha('slave3@choice')
# slave 4
slave4_private_key = 'afa0c9cd046cbf7cb8998761c28a3dbfd8537de02d078657dcce25614a34b2d9'
slave4_public_key = IrohaCrypto.derive_public_key(slave4_private_key)
slave4_name = 'slave4'
slave4_account_id = slave4_name + '@' + domain_id
slave4_iroha = Iroha('slave4@choice')
################################
# master node
################################
master_private_key = '054e294d86bedf9a43cf20542cade6e57addfd4294a276042be4ba83c73f8d9e'
master_public_key = IrohaCrypto.derive_public_key(master_private_key)
master_name = 'master'
master_account_id = master_name + '@' + domain_id
master_iroha = Iroha('master@choice')


def trace(func):
    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result

    return tracer


@trace
def send_transaction_and_print_status(transaction):
    """
    Send a transaction to the Blockchain (BSMD)
    :param transaction: Transaction we are sending to the BSMD
    :param network: Address of the network we are sending the transaction
    :return: null
    """
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    network.send_tx(transaction)
    for status in network.tx_status_stream(transaction):
        print(status)


@trace
def create_domain_and_asset():
    """
    Create a domain, default user and define asset
    :return: null
    """
    commands = [
        iroha.command('CreateDomain', domain_id='choice', default_role='user'),
        iroha.command('CreateAsset', asset_name='choicecoin', domain_id='choice', precision=2)
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), admin_private_key)
    send_transaction_and_print_status(tx)


create_domain_and_asset()
##################################
# slaves nodes setup
# ################################
# create an account in the network
functions.create_account_user(iroha, network, slave1_name, slave1_public_key, domain_id, '1000', asset_id)
functions.create_account_user(iroha, network, slave2_name, slave2_public_key, domain_id, '1000', asset_id)
functions.create_account_user(iroha, network, slave3_name, slave3_public_key, domain_id, '1000', asset_id)
functions.create_account_user(iroha, network, slave4_name, slave4_public_key, domain_id, '1000', asset_id)
##################################
# master node setup
# ################################
# create an account in the network
functions.create_account_user(iroha, network, master_name, master_public_key, domain_id, '1000', asset_id)

##################################
# grant access
# ################################
# grant access so slave node can share us his information
functions.grants_access_to_set_details(master_iroha, network, master_account_id, master_private_key, 'slave1@choice')
functions.grants_access_to_set_details(master_iroha, network, master_account_id, master_private_key, 'slave2@choice')
functions.grants_access_to_set_details(master_iroha, network, master_account_id, master_private_key, 'slave3@choice')
functions.grants_access_to_set_details(master_iroha, network, master_account_id, master_private_key, 'slave4@choice')
# grant access so slave node can share us his information
functions.grants_access_to_set_details(slave1_iroha, network, slave1_account_id, slave1_private_key, 'master@choice')
functions.grants_access_to_set_details(slave2_iroha, network, slave2_account_id, slave2_private_key, 'master@choice')
functions.grants_access_to_set_details(slave3_iroha, network, slave3_account_id, slave3_private_key, 'master@choice')
functions.grants_access_to_set_details(slave4_iroha, network, slave4_account_id, slave4_private_key, 'master@choice')
print('done')
