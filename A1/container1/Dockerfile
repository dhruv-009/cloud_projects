FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app.py .

EXPOSE 6000

CMD ["python", "app.py"]