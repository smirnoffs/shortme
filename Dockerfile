FROM python:3.11.1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY shortme /app
EXPOSE 8088

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8088" ]