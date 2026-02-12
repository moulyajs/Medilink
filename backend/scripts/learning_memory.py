def log_failed(text):

    with open("failed_rows.jsonl","a") as f:
        f.write(text + "\n")
