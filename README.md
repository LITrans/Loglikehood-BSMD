# Privacy-Aware Distributed Choice Modelling over Blockchain

A distributed tool for behavioural choice modelling is presented, where participants do not share personal raw data, while all computations are done locally. Participants share information using the [Blockchain for Smart Mobility Data-market (BSMD)](https://github.com/billjee/bsmd), where all transactions are secure and private. Nodes in BSMD can transact information with other participants as long as both parties agree to the transaction rules issued by the owner of the data. We discus the advantages and challenges of distributing choice models over the Blockchain. We present a study case for mode choice modeling using _Maximum Loglikehood method_ and solve the parameter estimation problem on a distributed version of simulated annealing. It is demonstrated that the estimated model parameters are consistent and reproducible

## Getting Started

1. To install the Iroha blockchain go to [network](network/)

2. To solve the _Maximum Loglikehood method_ using a distributed version of simulated annealing go to  [loglikelihood](loglikehood/)

### Prerequisites
1. [Python 3](https://www.python.org/download/releases/3.0/)
3. [PostgreSQL](https://www.postgresql.org/)
4. [Iroha](https://github.com/hyperledger/iroha)
