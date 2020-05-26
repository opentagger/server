FROM tiangolo/uwsgi-nginx:python3.8

COPY ./app/requirements.txt /requirements.txt
RUN pip install -Ur /requirements.txt && rm /requirements.txt
COPY ./app /app
