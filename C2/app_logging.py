#!/usr/bin/env python3
import logging, datetime

# Logging script cannot be named logging.py. Causes conflits with the python logging module. This print shows that in the linux PATH, at runtime of the script,
# the logging.py and the python module conflit with eachother. 
# print(logging.__file__)

# Configure logging
logging.basicConfig(filename='general_log.log', level=logging.INFO, format='%(asctime)s %(message)s')


## Examples of use
# var = "value_to_print"

# logging.info('\n### INFO - Starting script ###\n')
# print(f'\nInfo with command: {var}')

# logging.error(f'ERROR - Command: {var}')
# print(f'\nError with command: {var}'
