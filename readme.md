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

This command should ideally be set up as an automatic daily task
