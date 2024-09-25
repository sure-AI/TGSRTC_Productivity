# Use the official Python 3.8 Alpine image as the base image
FROM python:3.8-alpine

# Install necessary packages, including build tools and AWS CLI
RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    make \
    cmake \
    libffi-dev \
    musl-dev \
    linux-headers \
    bash \
    aws-cli

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]