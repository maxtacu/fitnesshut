# Download your FitnessHut receipts and send them to HR

This python script was created due the need to send every month receipts for my sports reimbursement to HR. 
Yes, I know this is really stupid when you have sports reimbursement agreed in your contract, but you still need to send these receipts everytime..🤦🏽‍♂️🤦🏽‍♂️

This script will download your receipts for the current month and:
- will create an email in Outlook ready to be sent  
or
- will create a Jira issue with receipts attached  

Tested on Mac with Microsoft Outlook app.

### Getting Started
1. Clone repository
2. Create and enable virtualenv (optional)
```
python -m venv .venv
source .venv/bin/activate
```
3. Install requirements
```
pip install -r requirements.txt
```
4. Export environment variables
```
export MYHUT_PASS='user@email.com'
export MYHUT_USER='Supersecretpassword'
export HR_EMAIL='hr@example.com'
export JIRA_PROJECT='HRP'
export JIRA_ISSUE_TYPE='Employee request'
export JIRA_SERVER='https://jira.yourdomain.com'
export JIRA_TOKEN='your_token'
export JIRA_USER='your_jira_email'
```
OR to set it permanent in your project folder without exporting environment variables you can create a `.env` file and set these variables there
```
MYHUT_PASS=user@email.com
MYHUT_USER=SuperSecretPassword
HR_EMAIL=hr@example.com
JIRA_PROJECT='HRP'
JIRA_ISSUE_TYPE='Employee request'
JIRA_SERVER='https://jira.yourdomain.com'
JIRA_TOKEN='your_token'
JIRA_USER='your_jira_email'
```
5. Edit subject and email body in `outlook.py`
## Usage
### Outlook
1. Review `body`(line 7-12) in `outlook.py` and edit it accordingly.
2. Run the script:
```
python fitnesshut.py --outlook
```
Script should download receipts and open Outlook with inserted message body, subject and these receipts as attachments.
2. Press "Send"
### Jira ticket
1. Run the script:
```
python fitnesshut.py --jira
```
Script should download receipts (by default for the current month only) and create Jira issue with title, description, and these receipts as attachments. It will post created issue link.  
In case you want to download receipts for the last 2-3 months, then you should pass the `-m` flag with number of months.  
For example if you want to download receipts for the last 2 months, then execute:
```
python fitnesshut.py --jira -m 2
```
**Amount of months should not exceed 3** unfortunately MyHut platform does not support filtering receipts for more than 3 months back.
