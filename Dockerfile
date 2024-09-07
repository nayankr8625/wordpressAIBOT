# Use a base Python image
FROM python:3.10.5

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8501

# Define the command to run the Streamlit application
CMD ["streamlit", "run", "app.py"]