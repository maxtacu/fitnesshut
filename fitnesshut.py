import requests, re
import sys, os
import json
from dotenv import load_dotenv
from datetime import date
from outlook import create_message_with_attachment


load_dotenv()
MYHUT_USER=os.getenv('MYHUT_USER')
MYHUT_PASS=os.getenv('MYHUT_PASS')
HR_EMAIL=os.getenv('HR_EMAIL')


def parse_facturas(page):
    this_month = date.today().strftime("%Y-%m")
    print(f"Getting your receipts for the month {this_month}")
    id_list = []
    page_dict = json.loads(page)
    for factura in page_dict['ConsultarExtratoResult']['Extrato']:
        if re.match(this_month, factura['Data']):
            id_list.append(factura['Id'].strip("{}"))
    print(f"Receipt IDs: {id_list}")
    return id_list

def download_factura(id):
    url = f"https://www.myhut.pt/factura/{id}"
    return

def main():
    files = []
    payload = {'myhut-login-email':MYHUT_USER, 'myhut-login-password':MYHUT_PASS}
    login_url = 'https://myhut.pt/myhut/functions/login.php'
    session = requests.Session()
    session.headers.update({
        'Host': 'www.myhut.pt'
    })
    try:
        resp = session.post(login_url, data=payload)
        # cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(session.cookies)['PHPSESSID']}
        
        resp = session.get('https://myhut.pt/myhut/functions/get-facturas.php')
        factruras_id = parse_facturas(resp.text)
        if factruras_id:
            for id in factruras_id:
                filename = f"{id}.pdf"
                print(f"Downloading receipt {filename}")
                r = session.get(f"https://www.myhut.pt/factura/{id}", allow_redirects=True)
                open(filename, 'wb').write(r.content)
                files.append(filename)
            print("Creating Email")
            create_message_with_attachment(files, HR_EMAIL)
        else:
            print("No receipts found")
    except requests.RequestException as e:
        print(e)
        sys.exit(1)
    # delete downloaded files
    for receipt in files:
        os.remove(receipt)


if __name__ == '__main__':
    main()
