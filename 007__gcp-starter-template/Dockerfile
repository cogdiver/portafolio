# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /service
WORKDIR /service

# Copy the current directory contents into the container at /service
COPY . /service

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Create temporal folder
RUN mkdir temp

# Run your application
CMD ["cookiecutter", ".", "--output-dir", "temp"]
