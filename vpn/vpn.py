


from pymongo import MongoClient, UpdateOne
import requests
import pandas as pd
import schedule
import time
from datetime import datetime
import calendar
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError



def update():
    
    url = 'https://raw.githubusercontent.com/X4BNet/lists_vpn/main/output/vpn/ipv4.txt'
    res = requests.get(url)
    print(res.text)
    
    client = MongoClient("mongodb://localhost:27017")
    db = client["GODEYE"]
    client = WebClient(token='xoxb-1998609471734-5025793496580-iVnkADb7D3UEM7naxx9qOYtF')
    # Check if the collection exists
    if "vpn" not in db.list_collection_names():
        collection = db.create_collection("vpn")
        collection.create_index([("cidr", "ascending")])
    else:
        collection = db["vpn"]
        if not collection.index_information():
            collection.create_index([("cidr", "ascending")])
    

    start_time = datetime.now()
    num_docs = collection.count_documents({})
    df = pd.DataFrame(res.text.strip().split('\n'), columns=['cidr'])
    
    operations = []
    for ip in df['cidr']:
        data_dict = {}
        data_dict['cidr']=ip
        data_dict['timestamp']=calendar.timegm(datetime.utcnow().utctimetuple())
        operation = UpdateOne( {'cidr': ip}, {'$set':data_dict},upsert=True)
        operations.append(operation)

    result = collection.bulk_write(operations)
    end_time = datetime.now()
    num_docs_end = collection.count_documents({})
    # Send a Slack message to confirm that the data has been sent
    try:
        # Send the message to the Slack channel
        response = client.chat_postMessage(
            channel="C05M5TZ67J6",
            text=f'VPN-DB-Insertion for {start_time} started \n Total-Docs:{num_docs}\n VPN-DB-Insertion ended! {end_time}\n Total Docs: {num_docs_end}'
        )
        print(f"Message sent to Slack: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending message to Slack: {e.response['error']}")


while True:
    schedule.every().day.at("10:00").do(update)
    # Run the schedule every minute to check for new data
    schedule.run_pending()
    time.sleep(60)
