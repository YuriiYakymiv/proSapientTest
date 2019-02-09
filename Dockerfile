FROM python:3.7

Maintainer Yurii

RUN apt-get update; \
	apt-get install -y \
	vim cron

COPY PasswordsParser /home/PasswordsParser
RUN pip3 install -r /home/PasswordsParser/requirements.txt
RUN chmod +x /home/PasswordsParser/tasks/parser_task.sh

COPY docker/cron /etc/cron.d/cron
RUN chmod 0644 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron


CMD [ "cron", "-f" ]