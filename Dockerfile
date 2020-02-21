
FROM python:3.7.2

WORKDIR /home/random05510/otomoto_scrapper

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]


