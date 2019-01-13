FROM python:3

MAINTAINER xwt xingweitian@gmail.com

WORKDIR /root/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]