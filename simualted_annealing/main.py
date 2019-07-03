from math import exp, log, sqrt, pow
import random
import csv
import statistics


def probability_car(beta_car, beta_cost, beta_tt, car_cost, train_cost, car_tt, train_tt):
    prob_car = exp(beta_car + beta_cost * (car_cost - train_cost) + beta_tt * (car_tt - train_tt)) / \
               (1 + exp(beta_car + beta_cost * (car_cost - train_cost) + beta_tt * (car_tt - train_tt)))

    return prob_car


def observation(is_car, is_train, prob_car):
    func = log(is_car * prob_car + is_train * (1 - prob_car))
    return func


def model(beta_car, beta_cost, beta_tt):
    models = []
    with open('data.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            is_car = int(row[1])
            is_train = int(row[2])
            car_cost = int(row[3])
            car_tt = int(row[4])
            train_cost = int(row[5])
            train_tt = int(row[6])
            prob_car = probability_car(beta_car, beta_cost, beta_tt, car_cost, train_cost, car_tt, train_tt)
            obs = observation(is_car, is_train, prob_car)
            models.append(obs)
    obj_func = sum(models)
    return obj_func


def new_state(beta_car, beta_cost, beta_tt):
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
    ap = exp((new_cost - old_cost) / t)
    return ap


def simulated_annealing(beta_car, beta_cost, beta_tt):
    solutions = []
    betas_car = []
    betas_cost = []
    betas_tt = []
    cost = model(beta_car, beta_cost, beta_tt)
    initial_cost = cost
    print('Null Loglikelihood = ', cost)
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
    steps = 0
    while temp > temp_min:
        i = 1
        while i <= 1000:
            new_beta_car, new_beta_cost, new_beta_tt = new_state(beta_car, beta_cost, beta_tt)
            cost_i = model(new_beta_car, new_beta_cost, new_beta_tt)
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
                # print('results: ', beta_car, beta_cost, beta_tt, cost, initial_cost)
            i += 1
            steps += 1
        temp = temp * alpha
        j += 1

    return steps, beta_car, beta_cost, beta_tt, cost, initial_cost, solutions, betas_car, betas_cost, betas_tt


steps, beta_ca, beta_co, beta_time, optimum, init_cost, solution_space, betas_ca, betas_co, betas_time =\
    simulated_annealing(.00123, .00664, .006463)

print('----------------------')
print('-----Solutions--------')
print('beta_car = ', beta_ca)
print('beta_cost = ', beta_co)
print('beta_tt = ', beta_time)
print('Null Loglikelihood = ', init_cost)
print('Final Loglikelihood = ', optimum)
print('number of steps = ', steps)


print('-Standard deviations--')
print('std_beta_car = ', statistics.stdev(betas_ca))
print('std_beta_cost = ', statistics.stdev(betas_co))
print('std_beta_tt = ', statistics.stdev(betas_time))
print('std_optimum = ', statistics.stdev(solution_space))

print('-Standard errors------')
print('ste_beta_car = ', statistics.stdev(betas_ca) / sqrt(len(betas_ca)))
print('ste_beta_cost = ', statistics.stdev(betas_co) / sqrt(len(betas_co)))
print('ste_beta_tt = ', statistics.stdev(betas_time) / sqrt(len(betas_time)))
print('ste_optimum = ', statistics.stdev(solution_space) / sqrt(len(solution_space)))

print('----------------------')
print('rho sqr = ', 1 - (optimum/init_cost))


# Null Loglikelihood =  -257.5839352638025
# initial beta_car =  0.00123
# initial beta_cost =  0.00664
# initial beta_tt =  0.006463
# ----------------------
# -----Solutions--------
# beta_car =  0.3428052631999551
# beta_cost =  -0.006267055652646666
# beta_tt =  -0.0008542129101878765
# Null Loglikelihood =  -257.5839352638025
# Final Loglikelihood =  -166.31634438876375
# number of steps =  110000
# -Standard deviations--
# std_beta_car =  0.19084542318190212
# std_beta_cost =  0.0026559231732976077
# std_beta_tt =  0.0004818276377620665
# std_optimum =  1.686722593467537
# -Standard errors------
# ste_beta_car =  0.0011874155533775376
# ste_beta_cost =  1.6524810665978125e-05
# ste_beta_tt =  2.9978692786387504e-06
# ste_optimum =  0.010494569942123612
# ----------------------
# rho sqr =  0.3543217506230262
