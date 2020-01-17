from Position import Position
import aws_keys
import boto3
from datetime import datetime
import json
import socket
import sys
import yfinance as yf
from yahoo_fin import stock_info as si

# Define week positions
david_positions = [
    "+18282449366",
    Position(ticker='TSLA', call=True, strike_price=575, breakeven_price=580.25),
    Position(ticker='FB', call=True, strike_price=222.5, breakeven_price=222.99),
    Position(ticker='BYND', call=True, strike_price=133, breakeven_price=140),
    Position(ticker='TSLA', call=True, strike_price=600, breakeven_price=602.34),
    Position(ticker='TSLA', call=True, strike_price=595, breakeven_price=599.2),
    Position(ticker='AAPL', call=True, strike_price=317.5, breakeven_price=322.3),
    Position(ticker='BABA', call=True, strike_price=230, breakeven_price=233.75),
    Position(ticker='NVDA', call=True, strike_price=250, breakeven_price=255.1),
    Position(ticker='AAPL', call=True, strike_price=330, breakeven_price=334.1),
    Position(ticker='SPCE', call=True, strike_price=20, breakeven_price=20.5),
    Position(ticker='TSLA', call=True, strike_price=690, breakeven_price=699.15),
]

keith_positions = [
    "+19196021971",
    Position(ticker='LK', call=True, strike_price=45, breakeven_price=46.1),
    Position(ticker='SPXL', call=True, strike_price=70, breakeven_price=70.41),
    Position(ticker='NOK', call=True, strike_price=4, breakeven_price=4.08),
]

mason_positions = [
    "+18284558967",
    Position(ticker='AMD', call=True, strike_price=52, breakeven_price=53.03),
    Position(ticker='GE', call=True, strike_price=12, breakeven_price=12.07),
    Position(ticker='CFG', call=True, strike_price=42.5, breakeven_price=42.55),
    Position(ticker='F', call=True, strike_price=9.5, breakeven_price=9.55),
]

tyler_positions = [
    "+17044952493",
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
    # mason_positions,
    # tyler_positions
]

# For each person in the all_persons list
for person in all_persons:

    # Initialize text message text
    final_text = ""

    # For each position in person's portfolio
    for stonk in person[1:]:
        need_to_breakeven = 0
        is_itm = False

        # Get current price of stock
        if socket.gethostname() == 'stonks':
            current_price = int(si.get_live_price(stonk.ticker))
        else:
            current_price = int(si.get_live_price(stonk.ticker))

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
        stonk_msg = stonk_msg + '\n\tCurrent Price: $%f' % str(round(current_price, 2))
        # Break even price to meet
        stonk_msg = stonk_msg + '\n\tBreak-Even: $%.2f' % str(round(stonk.breakeven_price, 2))

        # If in the money
        if is_itm:
            stonk_msg = stonk_msg + '\n\tITM by: $%.2f\n' % str(round(need_to_breakeven*-1, 2))
        else:
        # If out of the money
            stonk_msg = stonk_msg + '\n\tOTM by: $%.2f\n' % str(round(need_to_breakeven*-1, 2))

        final_text = final_text + stonk_msg

    # Create an AWS SNS client
    sns = boto3.client('sns')

    client = boto3.client(
        "sns",
        aws_access_key_id=aws_keys.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_keys.AWS_SECRET_ACCESS_KEY,
        region_name="us-west-2"
    )

    # Send sms message.
    response = client.publish(
        PhoneNumber=person[0],
        Message=final_text
    )
