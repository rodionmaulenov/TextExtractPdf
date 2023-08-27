FROM python:3.11.4-slim-buster

WORKDIR /work_dir

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat default-jre

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /work_dir/entrypoint.sh
RUN chmod +x /work_dir/entrypoint.sh

COPY . .

ENTRYPOINT ["/work_dir/entrypoint.sh"]