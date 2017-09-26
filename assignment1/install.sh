python3 -m venv --without-pip .
source bin/activate
curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py
pip install -r requirements.txt
echo
echo 'Dependencies installed. Run `source bin/activate` to enable virtual environment.'
