# Bike Count

Visualize data from bike counters in stavanger kommune

A pet project I made to play with Python and Streamlit

### Development

```sh
# Set up environment
python -m venv .venv
source .venv/bin/activate # or one of the equivalent script if you prefer powershell / windows
pip install -r requirements.txt

# Open project folder in your favorite editor!
```

### Run locally with python / streamlit

First setup environment following the above instructions, then:

```sh
streamlit run bike_count.py
```

### Run locally with docker-compose :whale:

```sh
docker compose up -d
```

Or if you're using a recent version of compose you can run with hot-reload support using

```sh
docker compose watch
```
