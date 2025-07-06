# Start from an official, lightweight Python base image.
FROM python:3.12-slim

# Set the working directory inside the container to /app.
WORKDIR /app

# Copy the consolidated requirements file into the container.
# Copying this first leverages Docker's layer caching.
COPY requirements.txt ./

# Install the Python dependencies inside the container.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code into the container.
COPY . .

# Inform Docker that the application inside the container listens on port 8501.
EXPOSE 8501

# Define the command that will be executed when the container starts.
# We use the 'python -m streamlit' form for robustness.
CMD ["python", "-m", "streamlit", "run", "app.py"]