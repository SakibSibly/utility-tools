from datetime import datetime, timedelta

t = datetime.strptime("08:30 PM", "%I:%M %p")
print((t + timedelta(hours=3, minutes=15)).strftime("%I:%M %p"))
