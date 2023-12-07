# Use the official Python image as the base image
FROM python:3.9

# Set environment variables for Python buffering
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the container
COPY . /app/

# Expose port 8000 for the Django application
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


COPY .env /app/