FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the main application folder
COPY self-healing-trigger/ ./self-healing-trigger/

# Add compressed dataset and decompress it to save space during the build
#COPY dataset.tar.gz ./self-healing-trigger/
#RUN tar -xzf ./self-healing-trigger/dataset.tar.gz -C ./self-healing-trigger/ && rm ./self-healing-trigger/dataset.tar.gz

# Set the command to run the main script
CMD ["python", "self-healing-trigger/classify-errors-and-trigger-self-healing.py"]

