import base64
import json
import hmac
import time
from datetime import datetime
start_time = time.time()
currentTime = False
while currentTime == False:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    if current_time == '00:44:30':
        print('Found')
        break


# refreshTime = 15  # 15 second refresh
#
# currentTime = False
# while currentTime == False:
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     print("Current Time =", current_time)
#     if current_time == '08:45:00':
#         print('Found')
#         break