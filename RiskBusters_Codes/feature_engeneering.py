import pandas as pd
import numpy as np

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

# ----------------------------

def add_clients_age(df):
    # change the type of Birth_date to datetime
    df['Birth_date'] = pd.to_datetime(df['Birth_date'])

    # add a column clients_age with the age of the client by substracting the birth_date from the current date
    current_date = pd.to_datetime('2024-04-03')
    df['clients_age'] = (current_date - df['Birth_date']).astype('<m8[Y]').astype(int)

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
        df[f'DTI_H{i}'] = (
            (df[inc_trans_amt] - df[out_trans_amt])
            / df[current_installment]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
    return df

def calculate_overdue_to_income_ratios_df(df):
    # We will assume the DataFrame columns are named with the suffixes _Hx where x is from 0 to 12
    for i in range(13):
        # Column names for the current period
        overdue_term_loan_col = f'Overdue_term_loan_H{i}'
        overdue_credit_card_col = f'Overdue_credit_card_H{i}'
        overdue_mortgage_col = f'Overdue_mortgage_H{i}'
        income_col = f'Income_H{i}'
        
        # Calculate the ratio and create a new column for it
        df[f'Overdue_to_Income_Ratio_H{i}'] = (
            (df[overdue_term_loan_col] + df[overdue_credit_card_col] + df[overdue_mortgage_col])
            / df[income_col]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
        
    return df

def calculate_financial_liquidity_ratio(df):
    # Assuming 'Current_installment' is a constant column across all periods
    for i in range(13):
        # Column names for the current and savings amounts for the current period
        current_amount_col = f'Current_amount_balance_H{i}'
        savings_amount_col = f'Savings_amount_balance_H{i}'
        
        # Calculate the Financial Liquidity Ratio for each period
        df[f'Financial_Liquidity_Ratio_H{i}'] = (
            (df[current_amount_col] + df[savings_amount_col]) / df['Current_installment']
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
        
    return df

def calculate_months_to_contract_end_simplified(df):
    # Convert 'Ref_month' and 'Contract_end_date' from string to datetime format
    df['Ref_month_dt'] = pd.to_datetime(df['Ref_month'], format='%m-%Y')
    df['Contract_end_date_dt'] = pd.to_datetime(df['Contract_end_date'], format='%d-%m-%Y')
    
    # Calculate the number of months to contract end directly
    df['Months_to_Contract_End'] = ((df['Contract_end_date_dt'] - df['Ref_month_dt']) / np.timedelta64(1, 'M')).astype(int)
    
    # Cleanup by dropping intermediate datetime columns
    #df.drop(['Ref_month_dt', 'Contract_end_date_dt'], axis=1, inplace=True)
    
    return df

def calculate_financial_history_length(df):
    """
    Calculate the length of a customer's financial history based on the 'Oldest_account_date'
    and the reference month 'Ref_month'.
    
    Args:
    - df (pd.DataFrame): DataFrame containing the columns 'Oldest_account_date' and 'Ref_month'.
    
    Returns:
    - pd.DataFrame: Original DataFrame with an additional column 'Financial_History_Length' representing
      the financial history length in full months.
    """
    # Convert 'Oldest_account_date' and 'Ref_month' to datetime format
    df['Oldest_account_date_dt'] = pd.to_datetime(df['Oldest_account_date'], format='%d-%m-%Y')
    df['Ref_month_dt'] = pd.to_datetime(df['Ref_month'], format='%m-%Y')
    
    # Calculate the difference in months
    df['Financial_History_Length'] = ((df['Ref_month_dt'] - df['Oldest_account_date_dt']) / np.timedelta64(1, 'M')).astype(int)
    
    # Drop intermediate datetime columns
    #df.drop(['Oldest_account_date_dt', 'Ref_month_dt'], axis=1, inplace=True)
    
    return df

def calculate_std_dev_inc_transactions(df):
    """
    Calculate the standard deviation of incoming transaction amounts across multiple periods
    specified by the suffix Hx, where x is from 0 to 12.
    
    Args:
    - df (pd.DataFrame): DataFrame containing columns for incoming transaction amounts
      with suffixes from H0 to H12, e.g., 'inc_transactions_amt_H0', 'inc_transactions_amt_H1', etc.
      
    Returns:
    - pd.DataFrame: Original DataFrame with an additional column 'Std_Dev_Inc_Transactions' representing
      the standard deviation of the incoming transaction amounts.
    """
    # Extracting the columns related to incoming transaction amounts
    inc_transaction_cols = [col for col in df.columns if 'inc_transactions_amt_H' in col]
    
    # Calculate the standard deviation across the specified columns and add it to the DataFrame
    df['Std_Dev_Inc_Transactions'] = df[inc_transaction_cols].std(axis=1)
    
    return df

# To use this function, pass your DataFrame to it:
# df = calculate_std_dev_inc_transactions(df)
# This will append a new column 'Std_Dev_Inc_Transactions' to your DataFrame.

def calculate_financial_stability_index_df(df):
    # We will assume the DataFrame columns are named with the suffixes _Hx where x is from 0 to 12
    for i in range(13):
        # Column names for the current period
        Savings_amount_balance_col = f'Savings_amount_balance_H{i}'
        Current_amount_balance_col = f'Current_amount_balance_H{i}'
        
        # Calculate the ratio and create a new column for it
        df[f'Financial_stability_index_H{i}'] = (
            (df[Savings_amount_balance_col])
            / df[Current_amount_balance_col]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
        
    return df

def calculate_overdue_aggregation_df(df):
    # We will assume the DataFrame columns are named with the suffixes _Hx where x is from 0 to 12
    for i in range(13):
        # Column names for the current period

        Overdue_term_loan_col = f'Overdue_term_loan_H{i}'
        Overdue_credit_card_col = f'Overdue_credit_card_H{i}'
        Overdue_mortgage_col = f'Overdue_mortgage_H{i}'
        
        # Calculate the ratio and create a new column for it
        df[f'Overdue_aggregation_H{i}'] = (
            df[Overdue_term_loan_col] + df[Overdue_credit_card_col] + df[Overdue_mortgage_col]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
        
    return df

# Średnia kwota transakcji: Obliczanie średniej wartości transakcji 
# przychodzących i wychodzących w poszczególnych okresach 
# (dzielenie 'inc_transactions_amt_Hx' przez 'inc_transactions_Hx' 
# i analogicznie dla transakcji wychodzących).inc_transactions_Hx
# out_transactions_Hx
# inc_transactions_amt_Hx
# out_transactions_amt_Hx


def calculate_mean_transactions_df(df):
    # We will assume the DataFrame columns are named with the suffixes _Hx where x is from 0 to 12
    for i in range(13):
        # Column names for the current period

        inc_transactions_col = f'inc_transactions_H{i}'
        out_transactions_col = f'out_transactions_H{i}'
        inc_transactions_amt_col = f'inc_transactions_amt_H{i}'
        out_transactions_amt_col = f'out_transactions_amt_H{i}'
        
        # Calculate the ratio and create a new column for it
        df[f'Avg_inc_transactions_H{i}'] = (
            df[inc_transactions_amt_col]/df[inc_transactions_col]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None

        df[f'Avg_out_transactions_H{i}'] = (
            df[out_transactions_amt_col]/df[out_transactions_col]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
        
    return df

#Wskaźnik wykorzystania kredytu: Dla 'utilized_limit_in revolving_loans_Hx', 
# stosunek wykorzystanego limitu do dostępnego limitu ('limit_in_revolving_loans_Hx') 
# może dać informację o tym, jak klient zarządza swoim dostępnym kredytem.

def calculate_credit_utilization_df(df):
    # We will assume the DataFrame columns are named with the suffixes _Hx where x is from 0 to 12
    for i in range(13):
        # Column names for the current period
        Savings_amount_balance_col = f'Savings_amount_balance_H{i}'
        Current_amount_balance_col = f'Current_amount_balance_H{i}'
        
        # Calculate the ratio and create a new column for it
        df[f'Financial_stability_index_H{i}'] = (
            (df[Savings_amount_balance_col])
            / df[Current_amount_balance_col]
        ).replace([float('inf'), -float('inf')], None)  # Replace infinite values with None
        
    return df

def modify_df(df):
    df = add_clients_age(df)
    df = caclulate_DTI(df)
    df = calculate_overdue_to_income_ratios_df(df)
    df = calculate_financial_liquidity_ratio(df)
    df = calculate_months_to_contract_end_simplified(df)
    df = calculate_financial_history_length(df)
    df = calculate_std_dev_inc_transactions(df)
    df = calculate_financial_stability_index_df(df)
    df = calculate_overdue_aggregation_df(df)
    df = calculate_mean_transactions_df(df)
    df = calculate_credit_utilization_df(df)

    return df

def drop_columns(df, columns_to_delete_H, columns_to_delete):
    # delete columns from list columns_to_delete_H

    """for colname in columns_to_delete_H:
        for i in range(1, 13):
            colname2 = colname + str(i)
            if colname2 in df.columns:
                df = df.drop(colname2, axis=1)"""
    # Generate a list of columns to drop
    columns_to_drop = [col + str(i) for col in columns_to_delete_H for i in range(1, 13)]

    # Filter out columns that exist in the DataFrame
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]

    # Drop the selected columns
    df = df.drop(columns_to_drop, axis=1)

    # drop all columns from columns_to_delete
    df = df.drop(columns_to_delete, axis=1)

    return df

def create_differences_columns(df, columns_H):

    # define the list of columns to iterate
    list = [[0,3], [0,6], [0,12]]
    
    for column in columns_H:
        for element in list:
            first_column_sufix = str(element[0])
            second_column_sufix = str(element[1])

            new_column_name = column + first_column_sufix + '_H' + second_column_sufix

            df[new_column_name] = (df[column + first_column_sufix] - df[column + second_column_sufix])
             # / df[column + first_column_sufix]

    return df

# drop columns with _H in the name
def drop_columns_after_transformation(df, columns_H):
    columns_to_drop = [colname + str(i) for colname in columns_H for i in range(1, 13)]
    df = df.drop(columns_to_drop, axis=1, errors='ignore')
    return df
