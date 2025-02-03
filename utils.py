import re

def extract_transaction_details(text):
    # Extract the date (pattern: "Month DD, YYYY")
    date_pattern = r"\b([A-Za-z]{3} \d{2}, \d{4})\b"
    date_match = re.search(date_pattern, text)
    date = date_match.group(1) if date_match else None

    # Extract the payment type (DEBIT/CREDIT)
    type_pattern = r"\b(DEBIT|CREDIT)\b"
    type_match = re.search(type_pattern, text)
    payment_type = type_match.group(1) if type_match else None

    # Extract the amount (₹ followed by digits)
    amount_pattern = r"₹([\d,]+(?:\.\d{2})?)"
    amount_match = re.search(amount_pattern, text)
    amount = amount_match.group(1) if amount_match else None

    # Extract the person's name (words after "Paid to" and before payment type)
    name_pattern = r"(?:Paid to|Payment to) (.+?) (DEBIT|CREDIT)"
    name_match = re.search(name_pattern, text)
    name = name_match.group(1).strip() if name_match else None
    
    return {
        "date": date,
        "name": name,
        "payment_type": payment_type,
        "amount": f"₹{amount}" if amount else None,
    }


def extract_time_and_transaction_id(text):
    # Extract time in "HH:MM am/pm" format
    time_pattern = r"\b(\d{1,2}:\d{2}\s?(?:am|pm))\b"
    time_match = re.search(time_pattern, text, re.IGNORECASE)
    time = time_match.group(1) if time_match else None

    # Extract transaction ID pattern (alphanumeric, typically long)
    transaction_pattern = r"Transaction ID (\w+)"
    transaction_match = re.search(transaction_pattern, text)
    transaction_id = transaction_match.group(1) if transaction_match else None

    return {
        "time": time,
        "transaction_id": transaction_id,
    }


def extract_utr(text):
    # Extract UTR No. pattern
    utr_pattern = r"UTR No\. (\d+)"
    utr_match = re.search(utr_pattern, text)
    utr = utr_match.group(1) if utr_match else None

    return {"utr": utr}

def extract_account_number(text):
    # Extract the masked account number (starts with X's followed by digits)
    account_pattern = r"Paid by (X+[\d]+)"
    account_match = re.search(account_pattern, text)
    account_number = account_match.group(1) if account_match else None

    return {"account_number": account_number}