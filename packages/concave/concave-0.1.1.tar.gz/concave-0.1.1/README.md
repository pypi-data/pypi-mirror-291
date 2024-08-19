


# run test
```
git clone https://github.com/concave-ai/concave.git
git clone https://github.com/concave-ai/playground.git


cd concave
pipenv install
pipenv shell
cd tests/code_search
python test_index_manager.py

```

# create index
```
zoekt-index -index /workspace/index/zoekt .
scip-python index . --project-name=pytest
mkdir /workspace/index/scip && mv index.scip /workspace/index/scip/


```