#PYTHON 311 IMAGE
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /opt/app

# VIRTUAL ENVIRONMENT
ENV VIRTUAL_ENV=/opt/app/venv

# Create a virtual environment
RUN python -m venv $VIRTUAL_ENV

# Set PATH to include the virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install server dependencies
# Install gcc and other essential tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies using the pipfile
COPY Pipfile Pipfile.lock ./
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --ignore-pipfile
# Copy the server code into the container
COPY . .

# Create a user to run the application
RUN useradd -m appuser

# Change to the appuser
USER appuser

# Run the server
CMD ["python", "run.py"]

