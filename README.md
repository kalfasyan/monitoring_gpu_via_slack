# monitoring_gpu_via_slack
Simple script to help me get notified when a neural network training gets stuck and GPUs are not being used anymore.

## description
Basically we create a cronjob (cronjob.py) that will run the monitoring script every minute. 
The monitoring script (nvidiasmi_check.py) checks the gpu utilization from the output of the command "nvidia-smi". In my case, there are 3 GPUs, so I take the mean utilization and if it's bellow a threshold (e.g. 10), then I use a slack-app to send me a message in Slack. Then the cron interval is changed to 2 hours, so that I get a notification every 2 hours, until I fix the GPU issue.

For more information about slack-apps check this: https://api.slack.com/slack-apps
You just need to anable incoming web hooks.
