FROM python3

WORKDIR /app

# copy soursce code and start script
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]