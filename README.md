# proSapientTest
passwords scraper

to run the scraper run:
1. docker-compose build
2. docker-compose up

to access the parsed data you should connect to ps01 container and type:
>1. psql -U postgres passwords
>2. select * from passwords

If you don't have time to wait for 1 week to test :) , then just change command in cron file to * * * * *.

I've spent almost 4 hours on this task, coding took ~45 minutes, the rest of time I was trying to make cron run in container. The issue was that I used python3.7 not from usr/local/bin where all my libraries were installed. Also there was a problem to see logs. because file was created but empty. Also I  was trying to do it through supervisor. But I don't think that it's necessary if we launch only one service in container.
