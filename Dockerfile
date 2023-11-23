
# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /spots_detector

# Copy the current directory contents into the container at /app
COPY . /spots_detector

RUN pip install dill --upgrade

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
