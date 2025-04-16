FROM python:3.11-slim

WORKDIR /app

COPY . ./
RUN pip install .
RUN pip install uvicorn

EXPOSE 5000

CMD ["uvicorn", "dndbehind:app", "--host", "0.0.0.0", "--port", "5000"]
