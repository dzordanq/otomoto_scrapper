
FROM python:3.7.2

WORKDIR /home/random05510/python/scrapper

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]


