import pandas as pd

def add_new_columns(df):
    # change the type of Birth_date to datetime
    df['Birth_date'] = pd.to_datetime(df['Birth_date'])

    # add a column clients_age with the age of the client by substracting the birth_date from the current date
    current_date = pd.to_datetime('2024-04-03')
    df['clients_age'] = (current_date - df['Birth_date']).astype('<m8[Y]').astype(int)

    return df


# Function to create the differences columns
# Remember to change to iterate through the columns

# Maybe add code to delete the columns after transformation

def create_differences_columns(df):

    # define the list of columns to iterate
    list = [[0,3], [0,6], [0,12]]
 
    for element in list:
        column = 'inc_transactions_H'

        first_column_sufix = str(element[0])
        second_column_sufix = str(element[1])

        new_column_name = column + first_column_sufix + '_H' + second_column_sufix

        df[new_column_name] = (df[column + first_column_sufix] - df[column + second_column_sufix]) / df[column + first_column_sufix]

    return df

# Function to calculate the DTI
def caclulate_DTI(df):
    # We will assume the DataFrame columns are named with the suffixes _Hx where x is from 0 to 12
    for i in range(13):
        # Column names for the current period
        inc_trans_amt = f'inc_transactions_amt_H{i}'
        out_trans_amt = f'out_transactions_amt_H{i}'
        current_installment = 'Current_installment'
        
        # Calculate the DTI for the current period
        df[f'DTI{i}'] = (
            (df[inc_trans_amt] - df[out_trans_amt])
            / df[current_installment]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
    return df