from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from logging import logger
import csv




'''
APPROACH:

1. Fast API to create a route let's say /process_text that will
either take body in a form of a dic (example below)

    {
        text: some-text,
        log_tag: word,
        clssifier: word
    }

or read form an excel file.

2. fyucntionmt count the occurance of the word in the sentence.

2. Ussing Logger to log each contents.

4. Depending on the size of the data, the logs can be stored in the no SQL DB or a CSV file in
a form of a json/dict. Similar to the repsonse body. this will made it easier for the team
 to query the stored logs latter on and read them efficiently. For example;

 {'text': 'some text here',log_type_count:21,classification:3},
 {'text': 'some text here',log_type_count:21,classification:3}

3. To ensure that the logging process does not impact the performace,
 we can use the enqueue=True option when adding a new sink to the logger. 
 This wil ensure that log maseges are written to the log file asynchronously
 without blocking the main application thread. Also, you can configure the logging level to ensure that only relevant log messages are written to the log file.

'''


class LogItem(BaseModel):
    log_type: str
    classification: str

app = FastAPI()

logger.add("requests.log", format="{message}", enqueue=True, rotation="10 MB")

@app.post("/process_text")
def process_text(log_items: List[LogItem]):

    log_type_count = {}
    classification_count = {}
    for item in log_items:
        log_type_count[item.log_type] = log_type_count.get(item.log_type, 0) + 1
        classification_count[item.classification] = classification_count.get(item.classification, 0) + 1
    logger.info(f"Processed {len(log_items)} log items")
    with open('requests.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([len(log_items), log_type_count, classification_count])
    return {"log_type": log_type_count, "classification": classification_count}
