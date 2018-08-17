import subprocess
import numpy as np
import requests
import json

# Run the command nvidia-smi with a pipe to find utilization percentages
out = subprocess.Popen(['nvidia-smi'], stdout=subprocess.PIPE)
output = subprocess.check_output(('grep','%'), stdin=out.stdout).decode()

# Tidying up the results, making sure we get GPU utilization 
# and not fan utilization
output_list = output.split('\n')[:-1]
utilizations = [u.split()[-3] for u in output_list]

ut_ints = np.array([int(u.split('%')[0]) for u in utilizations])

# writing the resuts in a file
with open('gpu_utilization.txt', 'a') as f:
    f.write(str(np.median(ut_ints))+'\n')

# reading the file to get the data
with open('gpu_utilization.txt', 'r') as fr:
    data_str = fr.read().splitlines(True)
    filen = len(data_str)

# make sure to circle the writing procedure
# i.e. keep 20 lines and keep deleting the first line from then on
if filen >= 20:
    with open('gpu_utilization.txt', 'w') as fw:
        fw.writelines(data_str[1:])

data = np.array([float(i.split('\n')[0]) for i in data_str])
print(np.mean(data))

# if the mean utilization of my 3 GPUs is bellow 10, 
# then send a message to my slack account through a slack-app

if np.mean(data) < 10:
    webhook_url = 'https://hooks.slack.com/services/T*********/B*******/**********'
    slack_data = {'text': 'GPU cluster utilization is very low. Probably stuck!'}

    response = requests.post(
        webhook_url, data = json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

    # then change the job to send notifications every 2 hours
    # we don't want to get spammed too much
    my_cron = CronTab(user='kalfasyan')
    for job in my_cron:
        if job.comment == 'gputil':
            job.hour.every(2)
            job.comment = 'gputil_hourly'
            my_cron.write()
