FROM python:3.10
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]