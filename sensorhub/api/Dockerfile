FROM python:3.10-alpine3.18

# Copies directory of Dockerfile to the application directory within the virtual environment
COPY . /api

# Sets the current directory to the application directory
WORKDIR /api

# Installs dependencies
RUN pip install -r requirements.txt

# Run application
CMD ["python", "app.py"]