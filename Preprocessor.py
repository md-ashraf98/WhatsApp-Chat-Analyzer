import re
import pandas as pd
def preprocessor(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    data = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # Convert the message type
    data['message_date'] = pd.to_datetime(data['message_date'], format='%d/%m/%Y, %H:%M - ')
    data.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []
    for message in data['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Notification')
            messages.append(entry[0])
    data['user'] = users
    data['message'] = message
    data.drop(columns=['user_message'], inplace=True)
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month_name()
    data['day'] = data['date'].dt.day
    data['hour'] = data['date'].dt.hour
    data['minute'] = data['date'].dt.minute
    data['month_num'] = data['date'].dt.month
    data['date2']= data['date'].dt.date
    data['day1'] = data['date'].dt.day_name()

    period = []
    for hour in data[['day1', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    data['period'] = period

    return data