from Position import Position
import aws_keys
import boto3
from datetime import datetime
import json
import sys
import yfinance as yf

# Define week positions
david_positions = [
    '+18282449366',
    Position(ticker='TSLA', call=True, strike_price=490, breakeven_price=497.7),
    Position(ticker='AAPL', call=True, strike_price=310, breakeven_price=314.25),
    Position(ticker='BLK', call=True, strike_price=515, breakeven_price=520),
    Position(ticker='SPXL', call=True, strike_price=70, breakeven_price=70.35),
    Position(ticker='LK', call=True, strike_price=44, breakeven_price=45.9)
]

keith_positions = [
    '+19196021971',
    Position(ticker='LK', call=True, strike_price=45, breakeven_price=46.1),
    Position(ticker='SPXL', call=True, strike_price=70, breakeven_price=70.41),
    Position(ticker='NOK', call=True, strike_price=4, breakeven_price=4.08),
]

tyler_positions = [
    '+17044952493',
    Position(ticker='MSFT', call=True, strike_price=162.5, breakeven_price=163.35),
    Position(ticker='AAPL', call=True, strike_price=320, breakeven_price=322.65),
    Position(ticker='SBUX', call=True, strike_price=100, breakeven_price=100.08),
    Position(ticker='LK', call=True, strike_price=47, breakeven_price=49.6),
    Position(ticker='PINS', call=True, strike_price=21.5, breakeven_price=21.85)
]

# Create list containing all people
all_persons = [
    david_positions,
    # keith_positions,
    # tyler_positions
]

# For each person in the all_persons list
for person in all_persons:

    # Initialize text message text
    final_text = ''

    # For each position in person's portfolio
    for stonk in person[1:]:
        need_to_breakeven = 0
        is_itm = False

        # Get current price of stock
        current_price = int(yf.Ticker(stonk.ticker).info['ask'])

        # If a call, want current price to be above breakeven price
        if stonk.call:
            need_to_breakeven = stonk.breakeven_price - current_price
        else:
        # If a put, want current price to be below breakeven price
            need_to_breakeven = current_price - int(stonk.breakeven_price)
        
        # If has broken even
        if need_to_breakeven < 0:
            is_itm = True
        
        # Name of stock
        stonk_msg = '%s: %s' % (stonk.ticker, 'CALL' if stonk.call else 'PUT')
        # Current price of stock
        stonk_msg = stonk_msg + '\n\tCurrent Price: $%.2f' % (current_price)
        # Break even price to meet
        stonk_msg = stonk_msg + '\n\tBreak-Even: $%.2f' % (stonk.breakeven_price)

        # If in the money
        if is_itm:
            stonk_msg = stonk_msg + '\n\tITM by: $%.2f\n' % (need_to_breakeven*-1)
        else:
        # If out of the money
            stonk_msg = stonk_msg + '\n\tOTM by: $%.2f\n' % (need_to_breakeven*-1)

        final_text = final_text + stonk_msg

    # Create an AWS SNS client
    sns = boto3.client('sns')

    client = boto3.client(
        "sns",
        aws_access_key_id=aws_keys.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_keys.AWS_SECRET_ACCESS_KEY
    )

    # Send sms message.
    client.publish(
        PhoneNumber=person[0],
        Message=final_text
    )
