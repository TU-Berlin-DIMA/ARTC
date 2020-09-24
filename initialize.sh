# Requires wget, unzip, python3
# numpy, matplotlib

python3 -m venv .venv
source .venv/bin/activate
pip install numpy
pip install matplotlib

cd data 
./pullData.sh

