FROM python:alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --use-pep517 -r requirements.txt

COPY . .
CMD ["python3", "empirevalue.py"]
