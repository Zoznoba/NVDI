FROM python
WORKDIR /fast-api_server
COPY requirements.txt /fast-api_server
RUN python -m pip install -r requirements.txt

COPY . /fast-api_server
EXPOSE 5000

CMD ["python", "fast-api_server.py"]