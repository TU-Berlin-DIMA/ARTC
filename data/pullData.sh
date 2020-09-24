set -e

cd activities
echo "Extracting activities dataset..."
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00256/data.zip 
unzip data.zip
python3 extract.py 0
python3 extract.py 1

echo "Extracting football dataset... This may take a while!"
cd ../football
wget https://debs2013.s3-eu-west-1.amazonaws.com/+debs2013.data
python3 extract.py


echo "Extracting gas dataset..."
cd ../gas
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00322/data.zip
unzip data.zip
python3 extract.py
cd ..

echo "All datasets successfully downloaded and preprocessed :) !"
