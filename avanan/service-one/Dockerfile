# Use Python 3.9 base image
FROM python:3.9

# install specific version of pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py pip==21.2.4

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8080 for FastAPI
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"] 