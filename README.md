# simserialED

1. Create an environment with 
```
python -m venv .venv
```

2. Activate the environment with 
```
.venv/Scripts/activate
```
on windows, or
```
.venv/bin/activate
```
on linux/mac (I think)

3. Install with
```
git submodule update --init
cd lib/orix
pip install .
cd ..
cd diffsims
pip install .
cd ..
cd ..
pip install .
```

4. Run the GUI with
```
simserialED.gui
```

5. It might complain about a missing .env-file. Create it with 
```
simserialED.setup
```
and try again.
