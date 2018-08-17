from crontab import CronTab

my_cron = CronTab(user='faktion')
job = my_cron.new(command='python /path/to/nvidiasmi_check.py', comment='gputil')
job.minute.every(1)
my_cron.write()

for job in my_cron:
    if job.comment=='gputil':
        print('Job created:', my_cron.crons[-1])
