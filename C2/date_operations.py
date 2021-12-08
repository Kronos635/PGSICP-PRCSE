#!/usr/bin/env python3
# coding: utf-8
from datetime import datetime, timezone, timedelta

# Create the timestamp in miliseconds, used for password
def converto_to_ms(days_valid):
    # Convert number of days, currently a string, to int
    days_valid = int(days_valid)
    # The method "strptime" creates a datetime object from the given string. This string is created using "strftime"
    # Creating the current date string, like "2021-12-08"
    current_date = datetime.strptime(datetime.now(timezone.utc).strftime("%Y%m%d"),'%Y%m%d')
    # Creates the expiration date string. "timedelta" is a class that allows the input of a duration, expressing the difference between two dates, in our case the variable "days" 
    expiration_date = current_date + timedelta(days=days_valid)
    # Convert date to miliseconds
    expiration_milisec_date = expiration_date.timestamp() * 1000
    return expiration_milisec_date

#days_valid = input("How many days should this password be valid for: ")
#print(converto_to_ms(days_valid))

# Convert the timestamp in miliseconds to date, used for password expiration
def converto_from_ms(date_to_convert):
    # Convert value received, currently a string, to int
    date_to_convert = int(date_to_convert)
    # Convert from miliseconds to date Year-Month-Day HH:MM:SS
    date_converted = datetime.fromtimestamp(date_to_convert/1000.0)
    # Show only Year-Month-Day, removing HH:MM:SS
    date_converted = date_converted.strftime('%Y-%m-%d')
    return date_converted

#print(converto_from_ms(converto_to_ms(days_valid)))
