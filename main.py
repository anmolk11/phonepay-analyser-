import pdfplumber
import pandas as pd
from utils import *
from tqdm import tqdm

def read_pdf(pdf_path : str):
    records = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in tqdm(pdf.pages,desc='Reading PDF'):
            text = page.extract_text()
            lines = text.split("\n")
 
            for line in lines:
                curr = []
                if not line.startswith(('Page','Date','This')):
                    records.append(line)
                
    return records[:1], records[2:]

def process_trasaction_text(tail):
    transactions = []
    i = 0 
    N = len(tail)
    while i < N:
        curr = []
        while i < N and (not tail[i].startswith('Paid by')):
            curr.append(tail[i])
            i += 1
        if i < N:    
            curr.append(tail[i])
        transactions.append(curr)
        i += 1

    return transactions

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

    transactions = process_trasaction_text(tail)

    for t in tqdm(transactions,desc='Processing'):
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
    input_file = 'PhonePe_Statement_Feb2024_Feb2025'
    pdf_path = f"Input/{input_file}.pdf"
    output_path = f"Output/{input_file}.xlsx"
    head, tail = read_pdf(pdf_path)
    df = convert_to_df(tail)
    df.to_excel(output_path, index=False)
    print(df.info())