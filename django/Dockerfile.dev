# Use an official Python runtime as a parent image
FROM python:3.11.6-slim as builder

# Set environment variables to non-buffered and not to write .pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set work directory
WORKDIR /app

# Install dependencies in a virtual environment
RUN python -m venv /venv
COPY requirements.txt .
RUN /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .


# Use a non-root user to run our application
RUN useradd -m myuser

# Change the ownership of the /app directory to the non-root user
RUN chown -R myuser:myuser /app && \
    chmod +x /app/django.sh
USER myuser


# Set the virtual environment as the main Python environment
ENV PATH="/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 8000

# Start the application
ENTRYPOINT ["/app/django.sh"]
