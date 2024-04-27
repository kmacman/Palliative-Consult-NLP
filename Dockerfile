# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./Referral/ /code/Referral/
#TODO: add classes and data processing folders?

ENV PYTHONPATH="${PYTHONPATH}:/Referral/classes"
ENV PYTHONPATH="${PYTHONPATH}:/Referral/data_processing"

# 
CMD ["uvicorn", "Referral.api:app", "--host", "0.0.0.0", "--port", "80"]