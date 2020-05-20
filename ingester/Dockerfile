FROM python:3.8
COPY app /app
COPY shoreman.sh /shoreman.sh
WORKDIR /app
RUN pip install -Ur requirements.txt && chmod +x /shoreman.xsh
CMD ["/shoreman.sh"]