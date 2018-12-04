# Internet Monitor

This is the code to accompany the Medium post I wrote. The essence of which is below, but for full details go to Medium - 10 minute dev. The original post is here: https://medium.com/@jimbotops_34097/10-minute-dev-internet-monitor-7c4d2c5f98f0

# Intro 
As with a lot of people, I get infuriated by ISPs selling you one speed only to receive half that, or less, by the time it gets to my router. As there never seemed to be any 'proof' on their side, I decided to create my own internet monitoring service, which logs your upload and download every minute and allows you to graph the results. There are sample input and output files provided in this repo.

All you'll need for this is a Linux server (a Raspberry Pi will do the job) connected to the internet you want to monitor, and about 10 minutes. 
## Install the CLI
The tool used for this tutorial is speedtest-cli. It's a great, lightweight tool that can be installed in a single line (depending on your Linux version)
sudo apt-get install speedtest-cli
For more info on how to install it, or a more through digging through the docs visit https://github.com/sivel/speedtest-cli
This tool was chosen for its easy of use, another one-liner, 'speedtest'. The output of which is below, which really clearly shows the speeds.
```Retrieving speedtest.net configuration...
Retrieving speedtest.net server list...
Testing from Sky Broadband (1.2.3.4)...
Selecting best server based on latency...
Hosted by Structured Communications (London) [10.34 km]: 12.8 ms
Testing download speed........................................
Download: 30.31 Mbits/s
Testing upload speed..................................................
Upload: 5.35 Mbits/s
```

## Writing the 'script'
I've used the term script very loosely here. It's 2 lines, that concatenates the above output with a date and sticks all that in a file. The date makes it much easier to do something useful, like creating a graph, further down the line.
```
date >> internetCheckResult.txt
speedtest >> internetCheckResult.txt
```
## Automate the script
Manually running this script every time would defeat the entire point, so we'll add it to cron to automatically run it every X mins. The example below will run every minute, but if you're on a more limited connection (or less of a nerd) less frequently might be fine.
To create a new cron job type:
```
crontab -e
```

Once you're in, you might see some other jobs you've made or, if this is your first visit to cron-land, just the standard text. Either way add a new line right at the bottom of the file that looks something like this:
```
* * * * * ~/script/internetCheck.sh >> ~/scripts/cronoutput
```
The first part of all stars is cron speak for once every minute. To change this, I recommend using a calculator like https://crontab.guru/. 
The second part is calling the script we wrote above. The final part in bold is optional. All this does is capture any errors the script may throw. Can be useful for debugging but not needed for normal functionality.

## Parsing the output
Now you can let it run as it slowly logs all your internet speeds and connectivity. When you want to actually process the data (after a few weeks usually works well), then use the python script on GitHub, invoked as below. This takes 2 arguments, i is the input file that has been populated by the cron job, and o is the output. This turns that human-readable data into a neatly processed csv - now we can do something interesting with it.
```
python main.py -i internetCheckResult.txt -o results.csv
```
If you're interested in learning how the python script does its thing, it's fully commented, or add a comment below and I'll try and get back to you.
## Processing the data
Import this csv into Excel (or Google Sheets) and give it a title or two.
And the outcome is a graph mapping both the upload and download speeds.
