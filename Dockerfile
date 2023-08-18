FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "Current time: $(date)"

COPY . .

CMD [ "python", "./main.py" ]