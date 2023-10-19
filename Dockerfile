# Use an official Ubuntu runtime as a parent image
FROM ubuntu:latest

# Set environment variables
ENV ENV=qa

# Update and install necessary packages
RUN apt-get update && apt-get install -y python3-pip

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your application files into the container
COPY . /app

# Define the default command to run your Celery application
CMD ["celery", "-A", "tasks:app", "worker", "--loglevel=info"]
