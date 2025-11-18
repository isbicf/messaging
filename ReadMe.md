# Message Processing System
A containerized message-processing system using Flask, Celery, Redis, and SQLite. 
Messages are submitted via REST API, stored in the database, processed asynchronously 
by Celery workers, and results are returned through the API.

- OS: Windows 11 Pro

# Setup
## Python
1. Go to [Python Download](https://www.python.org/downloads)
2. Download Python 3.13.x and install
3. Confirm installation
   ```
   python --version
   ```

## Source download
```
git clone https://github.com/isbicf/messaging.git
```

## Virtual environment
```
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate
```

## Packages
```
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Docker
1. Go to [Docker Desktop Download](https://www.docker.com/products/docker-desktop/)
2. Download installer for "Windows – AMD64" and install
3. Confirm installation
   ```
   docker --version
   docker compose version
   ```
