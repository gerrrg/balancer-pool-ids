# setup (or activate) your virtual environment
if [ ! -d ./venv ]; then
 	python3 -m venv ./venv
	source ./venv/bin/activate
	python3 -m pip install -r requirements.txt
else
	source ./venv/bin/activate
fi

git pull
python3 getPools.py

if [[ $(git status --porcelain ./pools| wc -l) -gt 0 ]]; then
  git commit ./pools/ -m "poolId file(s) updated"
  git push
else
  echo "No changes to be committed"
fi

deactivate
