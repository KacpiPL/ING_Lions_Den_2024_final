import pandas as pd

def add_new_columns(df):
    # change the type of Birth_date to datetime
    df['Birth_date'] = pd.to_datetime(df['Birth_date'])

    # add a column clients_age with the age of the client by substracting the birth_date from the current date
    current_date = pd.to_datetime('2024-04-03')
    df['clients_age'] = (current_date - df['Birth_date']).astype('<m8[Y]').astype(int)

    # delete the column Birth_date
    df.drop(columns=['Birth_date'], inplace=True)

    