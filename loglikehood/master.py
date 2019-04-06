import random
import time
import sys
import functions
import json
import logging
from iroha import Iroha, IrohaGrpc
from iroha import IrohaCrypto
from math import exp

logging.basicConfig(filename='master.log', filemode='w', format='%(message)s', level=logging.INFO)

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')

# node characteristics
master_private_key = '054e294d86bedf9a43cf20542cade6e57addfd4294a276042be4ba83c73f8d9e'
master_public_key = IrohaCrypto.derive_public_key(master_private_key)
master_name = 'master'
domain_id = 'choice'
master_account_id = master_name + '@' + domain_id
master_iroha = Iroha('master@choice')
# set the ip of one node in the iroha blockchain
asset_id = 'choicecoin#choice'
network = IrohaGrpc('3.16.203.141:50051')


##################################
# function of choice modelling
# ################################
def new_state(beta_car, beta_cost, beta_tt):
    """
    Computes a new beta using a random error. The new beta is part of the annealing process
    :param beta_car: beta parameter of the car
    :param beta_cost: beta parameter of the cost
    :param beta_tt: beta parameter of the travel time
    :return: beta plus an error
    """
    chose_beta = random.randint(1,3)
    error = random.uniform(-0.01, 0.01)
    if chose_beta == 1:
        new_beta_car = beta_car + error
        new_beta_cost = beta_cost
        new_beta_tt = beta_tt
    if chose_beta == 2:
        new_beta_car = beta_car
        new_beta_cost = beta_cost + error
        new_beta_tt = beta_tt
    if chose_beta == 3:
        new_beta_car = beta_car
        new_beta_cost = beta_cost
        new_beta_tt = beta_tt + error
    return new_beta_car, new_beta_cost, new_beta_tt


def acceptance_probability(old_cost, new_cost, t):
    """
    Acceptance probability that the new cost improves the old cost.
    Part of the annealing process
    :param old_cost: old cost obtained from the slave nodes
    :param new_cost: new cost obtained from the slave nodes. The new cost use the parameter beta plus an error
    :param t: temperature of the annealing process
    :return: probability that the new cost improves the old cost
    """
    ap = exp((new_cost - old_cost) / t)
    return ap


def simulated_annealing(beta_car, beta_cost, beta_tt):
    """
    Simulated annealing algorithm for solving the loglikehood choice model.
    1. Use the blockchain to send the model to the slave nodes.
    2. Use the blockchain to recieve the cost from the slave nodes.
    3. By using simulated annealing and sending-reciving information the master node solves the loglikehood choice model
    without the need of personal information
    :param beta_car: beta parameter of the car
    :param beta_cost: beta parameter of the cost
    :param beta_tt: beta parameter of the travel time
    """
    solutions = []
    betas_car = []
    betas_cost = []
    betas_tt = []
    cost = 0
    cost_i = 0
    x = 0
    betas = str(beta_car) + ',' + str(beta_cost) + ',' + str(beta_tt)
    # send parameters to slaves

    start_time_detail = time.time()
    functions.set_detail_to_node(master_iroha, network, 'slave1@choice', master_private_key, 'betas', betas)
    functions.set_detail_to_node(master_iroha, network, 'slave2@choice', master_private_key, 'betas', betas)
    functions.set_detail_to_node(master_iroha, network, 'slave3@choice', master_private_key, 'betas', betas)
    functions.set_detail_to_node(master_iroha, network, 'slave4@choice', master_private_key, 'betas', betas)
    elapsed_time_detail = time.time() - start_time_detail

    # get parameters from slaves
    time.sleep(5)
    # print('here')
    logging.info('while loop' + ',' + 'set details to slave nodes' + ',' + 'get cost from slave nodes')
    while x == 0:
        start_time = time.time()
        try:
            start_time_cost = time.time()
            c = functions.get_all_details(master_iroha, network, master_account_id, master_private_key)
            elapsed_time_cost = time.time() - start_time_cost
            result = json.loads(c)
            c_1 = result['slave1@choice']['cost']
            cost_1 = float(c_1)
            c_2 = result['slave2@choice']['cost']
            cost_2 = float(c_2)
            c_3 = result['slave3@choice']['cost']
            cost_3 = float(c_3)
            c_4 = result['slave4@choice']['cost']
            cost_4 = float(c_4)
            # added cost of all slaves
            cost_new = cost_1 + cost_2 + cost_3 + cost_4
            if cost == cost_new:
                continue
            else:
                print('entre')
                cost = cost_new
                elapsed_time = time.time() - start_time
                break
        except:
            x = 0
        time.sleep(1)
        elapsed_time = time.time() - start_time

    logging.info(str(elapsed_time) + ',' + str(elapsed_time_detail) + ',' + str(elapsed_time_cost))
    initial_cost = cost
    print('initial solution = ', cost)
    print('initial beta_car = ', beta_car)
    print('initial beta_cost = ', beta_cost)
    print('initial beta_tt = ', beta_tt)
    betas_car.append(beta_car)
    betas_cost.append(beta_cost)
    betas_tt.append(beta_tt)
    solutions.append(cost)
    temp = 1.0
    temp_min = 0.00001
    alpha = 0.9
    j = 0
    while temp > temp_min:
        i = 1
        while i <= 500:
            new_beta_car, new_beta_cost, new_beta_tt = new_state(beta_car, beta_cost, beta_tt)
            betas = str(new_beta_car) + ',' + str(new_beta_cost) + ',' + str(new_beta_tt)
            # send parameters to slaves

            start_time_detail = time.time()
            functions.set_detail_to_node(master_iroha, network, 'slave1@choice', master_private_key, 'betas', betas)
            functions.set_detail_to_node(master_iroha, network, 'slave2@choice', master_private_key, 'betas', betas)
            functions.set_detail_to_node(master_iroha, network, 'slave3@choice', master_private_key, 'betas', betas)
            functions.set_detail_to_node(master_iroha, network, 'slave4@choice', master_private_key, 'betas', betas)
            elapsed_time_detail = time.time() - start_time_detail

            # get parameters from slaves
            while x == 0:
                start_time = time.time()
                try:
                    start_time_cost = time.time()
                    c = functions.get_all_details(master_iroha, network, master_account_id, master_private_key)
                    elapsed_time_cost = time.time() - start_time_cost
                    result = json.loads(c)
                    c_1 = result['slave1@choice']['cost']
                    cost_1 = float(c_1)
                    c_2 = result['slave2@choice']['cost']
                    cost_2 = float(c_2)
                    c_3 = result['slave3@choice']['cost']
                    cost_3 = float(c_3)
                    c_4 = result['slave4@choice']['cost']
                    cost_4 = float(c_4)
                    # added cost of all slaves
                    cost_i_new = cost_1 + cost_2 + cost_3 + cost_4
                    if cost_i == cost_i_new:
                        continue
                    else:
                        cost_i = cost_i_new
                        elapsed_time = time.time() - start_time
                        # print('enter')
                        break
                except:
                    print("e")
                time.sleep(1)
                elapsed_time = time.time() - start_time

            logging.info(str(elapsed_time) + ',' + str(elapsed_time_detail) + ',' + str(elapsed_time_cost))
            ap = acceptance_probability(cost, cost_i, temp)
            rand = random.uniform(0, 1)
            if ap > rand:
                beta_car = new_beta_car
                beta_cost = new_beta_cost
                beta_tt = new_beta_tt
                cost = cost_i
                solutions.append(cost)
                betas_car.append(beta_car)
                betas_cost.append(beta_cost)
                betas_tt.append(beta_tt)
                print('results: ', beta_car, beta_cost, beta_tt, cost, initial_cost)
            i += 1
        temp = temp * alpha
        j += 1
        print(j)
    return beta_car, beta_cost, beta_tt, cost, initial_cost, solutions, betas_car, betas_cost, betas_tt


# Start choice modeling
beta_ca, beta_co, beta_time, optimum, init_cost, solution_space, betas_ca, betas_co, betas_time =\
    simulated_annealing(.00123, .00664, .006463)
