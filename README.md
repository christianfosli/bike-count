# Bike Count

Playing with Python and Streamlit.
**Work-in-Progress**

## Development

```sh
# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Open project folder in your favorite editor!

# Run locally with streamlit (installed into venv by the above pip install command)
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
