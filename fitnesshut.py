import requests
import sys, os
import json
from dotenv import load_dotenv
import datetime
from outlook import create_message_with_attachment
from jiraticket import JIRA_ticket
import argparse
import base64


load_dotenv()
MYHUT_USER=os.getenv('MYHUT_USER')
MYHUT_PASS=os.getenv('MYHUT_PASS')
HR_EMAIL=os.getenv('HR_EMAIL')
JIRA_TOKEN=os.getenv('JIRA_TOKEN')
JIRA_SERVER=os.getenv('JIRA_SERVER')
JIRA_USER=os.getenv('JIRA_USER')
JIRA_PROJECT=os.getenv('JIRA_PROJECT')
JIRA_ISSUE_TYPE=os.getenv('JIRA_ISSUE_TYPE')
session = requests.Session()


def months_from(months_back: int):
    for i in range(months_back):
        monthsFrom = datetime.date.today() - datetime.timedelta(days=i*30)
        monthsFrom = monthsFrom.strftime("%Y-%m")
    return monthsFrom

def download_factura(months):
    files = []
    login_payload = json.dumps({
        "email": MYHUT_USER,
        "password": MYHUT_PASS
    })
    login_url = 'https://ginasios.fitnesshut.pt/api/user/authenticate'
    invoice_list_url = 'https://ginasios.fitnesshut.pt/api/invoices/get-invoices'
    download_url = 'https://ginasios.fitnesshut.pt/api/invoices/download-invoice'
    headers = {
        'Content-Type': 'application/json'
    }
    if months > 3:
        print("Months range can be not more than 3 months")
        raise SystemExit(1)
    monthTo = datetime.date.today() - datetime.timedelta(days=(months-3)*30)
    monthTo = monthTo.strftime("%Y-%m")
    monthFrom = months_from(months)
    print(f"Getting invoices between months {monthFrom} and {monthTo}")
    session.headers.update({
        'Host': 'ginasios.fitnesshut.pt'
    })
    try:
        login = session.post(login_url, data=login_payload, headers=headers)
        token = json.loads(login.content)['token']
        payload = json.dumps({
            "invoiceType": "PRIMAVERA_INVOICE",
            "monthFrom": monthFrom,
            "monthTo": monthTo
        })
        headers = {
            "Authorization": f"Bearer {token}",
            'Content-Type': 'application/json'
        }
        resp = session.post(
            invoice_list_url,
            data=payload, 
            headers=headers
        )
        # check response code 
        if resp.status_code!= 200:
            print(resp.status_code)
            print(resp.content)
            sys.exit(1)
        json_response = json.loads(resp.content)
        if len(json_response) == 0:
            print("No receipts found")
            sys.exit(0)
        else:
            for factura in json_response:
                payload = json.dumps({
                    "deductionDate": factura['deductionDate'],
                    "id": factura['id'],
                    "invoiceType": "PRIMAVERA_INVOICE"
                })
                filename = f"{factura['deductionDate']}.pdf"
                print(f"Downloading receipt {factura['deductionDate']}")
                invoice = session.post(download_url, headers=headers, data=payload)
                # decode base64 data
                invoice_data = base64.b64decode(json.loads(invoice.content)['data'])
                # write invoice file
                open(filename, 'wb').write(invoice_data)
                # save file list for further use
                files.append(filename)
            return files, monthFrom, monthTo
    except requests.RequestException as e:
        print(e)
        sys.exit(1)

def main():
    # parse script startup parameters using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--jira', action='store_true', default=False)
    parser.add_argument('--outlook', action='store_true', default=False)
    parser.add_argument('--months', '-m', type=int, default=0)
    args = parser.parse_args()

    invoices, monthFrom, monthTo = download_factura(args.months)
    if args.outlook:
        create_message_with_attachment(invoices, HR_EMAIL)
    if args.jira:
        summary = "Gym invoices"
        if monthFrom == monthTo:
            description = f"Gym invoices from {monthFrom} month"
        else:
            description = f"Gym invoices from {monthFrom} to {monthTo} months"
        jr = JIRA_ticket(server=JIRA_SERVER, token=JIRA_TOKEN)
        ticket = jr.create_ticket(project_key=JIRA_PROJECT, summary=summary, description=description, issuetype=JIRA_ISSUE_TYPE)
        for invoice in invoices:
            jr.add_attachment(ticket, invoice)
        for invoice in invoices:
            os.remove(invoice)


if __name__ == '__main__':
    main()
