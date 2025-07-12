import pandas as pd

def load_and_preprocess_data(file_path='data/processed/cleaned_sales_data.csv'):
    # Load data
    df = pd.read_csv(file_path)
    # Convert date to datetime and set as index
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    # Ensure daily frequency
    df = df.asfreq('D')
    return df

if __name__ == "__main__":
    df = load_and_preprocess_data()
    print(df.head())