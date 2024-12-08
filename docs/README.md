## Steps to build the documentation

```bash
cd docs
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
cd source
# Might need to open a new terminal (with same python environment as above) before you can execute the command below.
sphinx-build -b html . build # or can use make html
```