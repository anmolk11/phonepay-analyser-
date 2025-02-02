import pdfplumber
import pandas as pd
from utils import *

def read_pdf(pdf_path : str):
    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")

            for line in lines:
                if not line.startswith('Page'):
                    records.append(line)

    return records[:2], records[3:]

def convert_to_df(tail):
    data = {
    "Date" : [],
    "Paid to" : [],
    "Type" : [],
    "Amount" : [],
    "Time" : [],
    "Transaction ID" : [],
    "UTR" : [],
    "Account Number" : []
    }

    transactions = [tail[i:i + 4] for i in range(0, len(tail), 4)]

    for t in transactions:
        if len(t) == 4:
            td = extract_transaction_details(t[0])
            tm = extract_time_and_transaction_id(t[1])
            utr = extract_utr(t[2])
            acc = extract_account_number(t[3])

            data['Account Number'].append(acc['account_number'])
            data["Amount"].append(td['amount'])
            data['Date'].append(td['date'])
            data["Paid to"].append(td['name'])
            data["Time"].append(tm['time'])
            data["Transaction ID"].append(tm['transaction_id'])
            data["Type"].append(td['payment_type'])
            data["UTR"].append(utr['utr'])

    df = pd.DataFrame(data)
    return df


if __name__ == '__main__':
    pdf_path = "PhonePe_Statement_Jan2025_Feb2025.pdf"
    head, tail = read_pdf(pdf_path)