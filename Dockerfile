FROM python:3.12.7-slim-bullseye
LABEL authors="Laca"

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000/tcp
ENTRYPOINT ["gunicorn"]

CMD ["--workers", "2", "--bind", "0.0.0.0:8000", "--timeout","240", "main:app"]
