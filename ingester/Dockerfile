FROM python:3.8
COPY app/requirements.txt shoreman.sh /
RUN pip install -Ur /requirements.txt && chmod +x /shoreman.sh && rm /requirements.txt
COPY app /app
WORKDIR /app
CMD ["/shoreman.sh"]