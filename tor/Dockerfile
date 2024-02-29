FROM python:3.9

# Install required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install the required packages
RUN pip3 install -r /app/requirements.txt

# Copy the script to the container
COPY vpn.py /app/

# Set the working directory to /app
WORKDIR /app

# Run the script when the container starts
CMD ["python3", "vpn.py"]