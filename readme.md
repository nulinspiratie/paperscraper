# Paperscraper
Retrieve science papers and send them in condensed daily emails

## Instructions
### Running database webpage
The database entries can be modified through a webpage.
This webpage can be started by running
```
python application.py
```

### Sending email
An email can be sent by running
```
python main.py --email {email_address}
```
where `{email_address}` should be replaced by the target email address.

### Setting up daily emails in Linux
Emails should ideally be set up as an automatic daily task.
This can be done in Linux using a cron job.
To setup a recurring cron task, run `sudo nano /etc/crontab` and add the following line at the bottom

```
00 9 * * * sudo /root/berryconda3/bin/python3.6 ~/paperscraper/main.py --email {email} --log debug --update > ~/output_paperscraper.txt 2>&1
```
