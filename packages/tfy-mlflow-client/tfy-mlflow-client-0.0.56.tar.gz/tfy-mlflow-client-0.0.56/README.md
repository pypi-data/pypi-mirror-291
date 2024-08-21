mlfoundry-server
---

0. Setup access to AWS via Okta SSO + aws cli


1. Setup virtual env

```shell
python3.11 -m venv .venv
. .venv/bin/activate
```

2. Setup `.env`

```shell
cp .env.example .env
```

> You might have to edit some secret values. Get help from your team

3. Install secretsfoundry

```shell
npm install -g secretsfoundry
```

4. Run

```shell
MLFLOW_FOR_SERVER=1 pip install -r requirements.txt -r dev-requirements.txt
secretsfoundry run -s "./run.sh"
```
