## Download your FitnessHut receipts and send them to HR

This python script was created due the need to send every month receipts for my sports reimbursement to HR. 
Yes, I know this is really stupid when you have sports reimbursement agreed in your contract and you still need to send these receipts everytime..🤦🏽‍♂️🤦🏽‍♂️

This script will download your receipts for the current month and will create an email in Outlook ready to be sent. Tested on Mac with Microsoft Outlook app.

### Usage
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
```
OR you can create a `.env` file and set these variables there
```
MYHUT_PASS=user@email.com
MYHUT_USER=SuperSecretPassword
HR_EMAIL=hr@example.com
```
5. Edit subject and email body in `outlook.py`
6. Run the script:
```
python fitnesshut.py
```
Script should download receipts and open Outlook with inserted message body, subject and these receipts as attachments.
7. Press "Send"