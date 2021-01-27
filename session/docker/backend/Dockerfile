FROM python:3.8

WORKDIR /

COPY backend /app
RUN pip install -r /app/requirements.txt

EXPOSE 80:5000

CMD python /app/main.py
