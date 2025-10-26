FROM python:3.10-slim

WORKDIR /messaging

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#EXPOSE -p 8000
EXPOSE 8000 

CMD ["python" ,"manage.py","runserver","0.0.0.0:8000"]
