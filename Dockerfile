FROM python:alpine3.8
RUN pip install connexion[swagger-ui] redis

COPY ./src /app/
COPY ./swagger.yaml /api/
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["main.py"]