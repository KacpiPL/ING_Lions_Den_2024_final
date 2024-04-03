import pandas as pd

def clean_df(df):
    df = df.replace(-9999, pd.np.nan)
    df['Active_mortgages'] = df['Active_mortgages'].fillna(0)

    # change NAs in selected columns to 0
    columns_to_fill_with_0 = ['Active_mortgages', 
                            'Active_credit_card_lines', 
                            'External_term_loan_balance',
                            'External_mortgage_balance',
                            'External_credit_card_balance']

    for column in columns_to_fill_with_0:
        df[column] = df[column].fillna(0)

    # change NAs in all columns which contains selected names in column name to 0
    columns_to_fill_with_0 = ['limit_in_revolving_loans_', 'utilized_limit_in_revolving_loans_']

    for column in df.columns:
        for name in columns_to_fill_with_0:
            if name in column:
                df[column] = df[column].fillna(0)

    return df