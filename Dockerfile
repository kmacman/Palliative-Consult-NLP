FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY ./App /code/App

# Install any needed packages specified in requirements.txt
COPY App/requirements.txt /code/App/requirements.txt
RUN pip install --no-cache-dir -r /code/App/requirements.txt

# Set the environment variable to ensure Python files can find each other
ENV PYTHONPATH="${PYTHONPATH}:/code/App"

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
