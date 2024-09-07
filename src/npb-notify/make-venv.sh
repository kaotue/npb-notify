mkdir venv
python3 -m venv venv
source ./venv/bin/activate
pip install -r ./app/requirements.txt
pip install --upgrade aws-sam-cli
