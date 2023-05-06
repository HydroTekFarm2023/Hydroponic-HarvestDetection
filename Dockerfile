# Use a Python 3 base image
FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Flask app source code
COPY app.py .

# Copy the model file
COPY model.tflite .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
