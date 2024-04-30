FROM python:3.9

# Assuming Dockerfile is next to the directories it needs to copy
COPY ./App/ /code/

WORKDIR /code/

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set PYTHONPATH if your application depends on modules in classes or data_processing
ENV PYTHONPATH="${PYTHONPATH}:/code/classes:/code/data_processing"

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
