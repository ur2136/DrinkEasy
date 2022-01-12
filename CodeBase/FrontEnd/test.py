from datetime import datetime

date = '2021-12-19'

format = "%Y-%m-%d"
  
# convert from string format to datetime format
datetime_date = datetime.strptime(date, format)

print(datetime_date.weekday())