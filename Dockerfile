# Use Python 3.11 to avoid the CatBoost compilation error you saw earlier
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy all your project files into the container
COPY . /app

# Hugging Face requires Docker spaces to run as a non-root user for security
RUN useradd -m -u 1000 user
USER user

# Hugging Face Spaces expose port 7860 by default! 
# We must tell Uvicorn to use this specific port.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]