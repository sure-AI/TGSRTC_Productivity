# Use the official Python 3.12 image as the base image
FROM python:3.12

# Update package lists, install CMake, build tools, and AWS CLI
RUN apt update -y && apt install awscli -y

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . /app
RUN pip install -r requirements.txt

# Command to run the Python application
CMD ["python3", "app.py"]