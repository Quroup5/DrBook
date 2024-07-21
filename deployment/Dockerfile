FROM ubuntu:22.04
LABEL authors="ahmadrv"

RUN apt update && apt upgrade -y
RUN apt install -y git python3-pip curl

WORKDIR /home

RUN git clone https://github.com/Quroup5/DrBook.git

WORKDIR /home/DrBook/

RUN pip install -r ./requirements.txt

EXPOSE 8000

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000", "--settings=core.production_settings.py" ]