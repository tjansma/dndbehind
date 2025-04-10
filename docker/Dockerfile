FROM python:3.11-slim

WORKDIR /app

COPY dist/*.whl .
RUN pip install *.whl

EXPOSE 5000

CMD ["uvicorn", "dndbehind:app", "--host", "0.0.0.0", "--port", "5000"]
