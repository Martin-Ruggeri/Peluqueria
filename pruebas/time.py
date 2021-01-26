from datetime import date, datetime, timedelta

today = datetime.today()
print (f'hoy: {today.hour}:{today.minute}:{today.second}')

day = today + timedelta( days= 35 )
print (f'dia: {day.strftime("%d/%m/%Y")}')

now = datetime.now()
print(f'today: {today.strftime("%d/%m/%Y %H:%M:%S")} vs now: {now.strftime("%d/%m/%Y %H:%M:%S")}')