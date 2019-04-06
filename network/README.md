# Install Iroha

Iorha is installed in 4 _t3.medium_ Amazon cloud EC2 virtual machines with 2cores at 3.1GHz and 4GB of RAM. 

# Instrucctions
In terminal do
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get -y --no-install-recommends install apt-utils software-properties-common wget
sudo add-apt-repository -y ppa:git-core/ppa
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add -
sudo nano /etc/apt/sources.list
```
In nano add the following lines at the end of the file
```
deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-7 main
deb-src http://apt.llvm.org/bionic/ llvm-toolchain-bionic-7 main
```
In terminal do
```
sudo apt-get update

sudo apt-get -y --no-install-recommends install software-properties-common automake libtool build-essential clang-6.0 lldb-6.0 lld-6.0 g++-7 libssl-dev zlib1g-dev libcurl4-openssl-dev libc6-dbg golang git ssh tar gzip ca-certificates gnupg python-pip python3-pip python3-setuptools python-dev curl file gdb gdbserver ccache gcovr cppcheck doxygen rsync graphviz libgraphviz-dev unzip vim zip; sudo apt-get -y clean

sudo apt install postgresql postgresql-contrib
```
Configure postgres
```
sudo passwd postgres
```
Set a pasword #(recommend for testing "postgres")
```
su - postgres
psql -d template1 -c "ALTER USER postgres WITH PASSWORD 'postgres';"
exit

sudo nano /etc/postgresql/10/main/postgresql.conf
```
In nano search a uncomment line
```
max_prepared_transactions = 100
```
Download this [file]() and this [file]()

In terminal
```
unzip build-deb.zip -d /home/ubuntu

sudo unzip dependencies.zip -d /opt

nano ~/.bashrc
```
In nano add the following lines at the end of the file
```
export PATH=$PATH:/home/ubuntu/build/bin
export PATH="$PATH:$HOME/bin"
```
In terminal
```
source ~/.bashrc

sudo dpkg -i /home/ubuntu/build/iroha-0x731d2c7afb5829f9ff716e4b8ff2bc986caca870-Linux.deb
sudo apt --fix-broken install
sudo dpkg -i /home/ubuntu/build/iroha-0x731d2c7afb5829f9ff716e4b8ff2bc986caca870-Linux.deb

sudo cp /opt/dependencies/soci/lib64/libsoci_core.so.3.2 /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/soci/lib64/libsoci_postgresql.so.3.2 /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/grpc/lib/libgrpc.so /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/grpc/lib/libgpr.so /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/c-ares/lib/libcares.so.2 /usr/lib/x86_64-linux-gnu/

sudo cp /opt/dependencies/grpc/lib/libaddress_sorting.so /usr/lib/x86_64-linux-gnu/
```


