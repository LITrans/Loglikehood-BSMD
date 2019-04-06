# Dsitributed simulated anneling
The experiment will run a distributed version of simulated annealing on each participant of the BSMD (Iroha network).

First, on each machine (master and 4 RPIs) install the iroha SDK
```
pip install iroha
```

## Setup

Copy the [Setup.py](Setup.py) file to the master (you can run this file on any computer if you like) and in the parameter `network` set the IP of one machine runnig the Iroha netwrok. Then in terminal do:
```
python3 setup.py
```
The procedure will create the slave and master nodes in the BSMD. Also, this procedure will grant the necesary persmissions so the nodes can transfer information

## Run experiment
The experiment follows the next steps:
1. The master node use the BSMD (Iroha) to send the beta paramentes to the slave nodes. 
2. The slave node get the beta paramenters from the BSMD and run the model using his personal observations (e.g. the personal observations of slave 1 are in the [data_one.csv](data_one.csv) file)
3. The slave nodes use the BSMD to send the results of the model
4. Master node collect all results from the BSMD and starte the anneling proccess. In This proccess master and slaves will share beta parameters and model results
5. Once the anneling proccess finish the master node will have the result of the _loglikehood_ method 

### Master node
Copy the [master.py](master.py) file to the master and set the parameter `network` set the IP of one machine runnig the iroha netwrok. 

### Slave nodes
1. Copy the [slave_one.py](slave_one.py) file to one RPI and in the parameter `network` set the IP of one machine runnig the iroha netwrok.
1. Copy the [slave_two.py](slave_two.py) file to one RPI and in the parameter `network` set the IP of one machine runnig the iroha netwrok.
1. Copy the [slave_three.py](slave_three.py) file to one RPI and in the parameter `network` set the IP of one machine runnig the iroha netwrok.
1. Copy the [slave_four.py](slave_four.py) file to one RPI and in the parameter `network` set the IP of one machine runnig the iroha netwrok.

Now, on each machine run master.py, slave_one.py, slave_two.py, slave_three.py and slave_four.py. After some hours you will have the results

**NOTE**: For a local version of the whole procces run `main.py` 
