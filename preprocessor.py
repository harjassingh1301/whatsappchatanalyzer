import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'Message': messages, 'Date': dates})
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M - ')
    users = []
    messages = []
    for message in df['Message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('groupnotification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['Message'], inplace=True)
    df = df.rename(columns={'Date': 'date'})
    df['year'] = df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df