import csv
import sys
import functions
import time
import logging
import json
from iroha import Iroha, IrohaGrpc, IrohaCrypto
from math import exp, log

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

logging.basicConfig(filename='slave_three.log', filemode='w', format='%(message)s', level=logging.INFO)

# Slave node
slave_private_key = '8c578c774f553b99ebbaf89d9314f8ceaf6b4e93119c2550e10cf0de8ee93b51'
slave_public_key = IrohaCrypto.derive_public_key(slave_private_key)
slave_name = 'slave3'
domain_id = 'choice'
slave_account_id = slave_name + '@' + domain_id
iroha_slave = Iroha('slave3@choice')
asset_id = 'choicecoin#choice'
# set the ip of one node in the iroha blockchain


##################################
# Set corresponding ip
network = IrohaGrpc('3.16.203.141:50051')
##################################


def model(beta_car, beta_cost, beta_tt):
    """
    This function run the model using private observations
    :param beta_car: beta parameter of the car
    :param beta_cost: beta parameter of the cost
    :param beta_tt: beta parameter of the travel time
    :return:
    """
    models = []
    with open('data_three.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            is_car = int(row[1])
            is_train = int(row[2])
            car_cost = int(row[3])
            car_tt = int(row[4])
            train_cost = int(row[5])
            train_tt = int(row[6])
            prob_car = exp(beta_car + beta_cost * (car_cost - train_cost) + beta_tt * (car_tt - train_tt)) / \
                       (1 + exp(beta_car + beta_cost * (car_cost - train_cost) + beta_tt * (car_tt - train_tt)))
            obs = log(is_car * prob_car + is_train * (1 - prob_car))
            models.append(obs)
    cost = sum(models)
    models.clear()
    return cost


def run_node():
    """
    This function follow the next steps
    1. Get the model from the master node
    2. Run the mode usen private observations ('data_XXX.csv)
    3. Set the model cost in the identity of the slave node
    :return:
    """
    b_car = 0
    b_cost = 0
    b_tt = 0
    x = 0
    elapsed_time_cost = 0
    logging.info('while loop' + ',' + 'get detail from master node' + ',' + 'set cost to master node')
    while x == 0:
        start_time = time.time()
        try:
            start_time_detail = time.time()
            b = functions.get_detail_from_generator(iroha_slave, network, slave_account_id, slave_private_key,
                                                    'master@choice', 'betas')
            elapsed_time_detail = time.time() - start_time_detail
            result = json.loads(b)
            # print(b)
            # print(result['master@choice']['betas'])
            beta = result['master@choice']['betas'].split(',')
            b_car_new = float(beta[0])
            b_cost_new = float(beta[1])
            b_tt_new = float(beta[2])

            if b_car == b_car_new and b_cost == b_cost_new and b_tt == b_tt_new:
                continue
            else:
                start_time_cost = time.time()
                b_car == b_car_new
                b_cost == b_cost_new
                b_tt == b_tt_new
                c = model(b_car_new, b_cost_new, b_tt_new)
                # print('beta: ', beta)
                # run model
                # send cost to master
                cost = str(c)
                # print('cost', cost)
                functions.set_detail_to_node(iroha_slave, network, 'master@choice', slave_private_key, 'cost', cost)
                elapsed_time_cost = time.time() - start_time_cost
        except:
            b = 0
        time.sleep(1)
        elapsed_time = time.time() - start_time
        logging.info(str(elapsed_time) + ',' + str(elapsed_time_detail) + ',' + str(elapsed_time_cost))


run_node()






