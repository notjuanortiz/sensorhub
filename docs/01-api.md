# Sensorhub API 
## Getting started
This guide assumes you have python3 and pip installed on your machine.
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Run server
```bash
python3 app.py
```
3. (Optional) Run using gunicorn, skip 2. While in the api directory:

```bash
gunicorn --workers=2 --bind 0.0.0.0:5001 app
```

Alternatively, docker can also be used to get the server running.

## REST Endpoints

### /sensors/ - GET
Returns the full list of sensors

#### Attributes
id [integer]

##### Example
```bash
curl http://0.0.0.0:5000/sensors/?id=1
```
