import aws_keys
import boto3
from datetime import date

phone_numbers = [
     "+17044952493", #Tyler
     "+18284558967", #Mason
     "+19196021971", #Keith
    "+18282449366", #David
]

for number in phone_numbers:
    # Create an AWS SNS client
    sns = boto3.client('sns')

    client = boto3.client(
        "sns",
        aws_access_key_id=aws_keys.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_keys.AWS_SECRET_ACCESS_KEY,
        region_name="us-west-2",
    )

    # Send sms message.
    response = client.publish(
        PhoneNumber=number,
        Message="🚨 Market Open: " + str(date.today().strftime("%m/%d")) + " 🚨\n\nHead Down 🤡👇\nMoney Up 💰🆙\nNo Questions 🚫❓\n\n📈🚀🚀🚀🌕"
    )
