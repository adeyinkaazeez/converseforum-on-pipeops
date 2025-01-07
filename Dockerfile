<<<<<<< HEAD
# Pull base image
FROM python:3.12.2-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory called `app`
RUN mkdir -p /code
WORKDIR /code

# Install dependencies
COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
pip install --upgrade pip && \
pip install -r /tmp/requirements.txt && \
rm -rf /root/.cache/

# Copy local project
COPY . /code/

# Set the port number as an environment variable
ARG PORT
ENV PORT $PORT

# Expose the given port
EXPOSE $PORT

# Use gunicorn on the given port
CMD gunicorn --bind :$PORT --workers 2 converse.wsgi
=======
# Set the base image to Python 3.9
FROM python:3.11.0
# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Set the working directory to /app
WORKDIR /app
# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application code into the container
COPY . .
# Run database migrations
RUN python manage.py migrate
# Expose port 8000 for the Django application
EXPOSE 8000
# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
>>>>>>> f5a1154 (first amended commit)
