import pandas as pd
import pickle
from datetime import datetime, timedelta

def data_preprocessing(df):
    # Transform 'tanggal_data' to numerical features
    df['tanggal_data'] = pd.to_datetime(df['tanggal_data'])
    df['year'] = df['tanggal_data'].dt.year
    df['month'] = df['tanggal_data'].dt.month
    df['day'] = df['tanggal_data'].dt.day

    # Sort and reset index
    df = df.sort_values(by=['nomor_rekening_loan', 'year', 'month', 'day']).reset_index(drop=True)

    # Create lag features
    lag_features = ['usia_hari', 'tunggak_pokok', 'tunggak_bunga', 'frekuensi_tunggakan', 'suku_bunga_acuan']

    for feature in lag_features:
        for lag in range(1, 4):  # Lag up to 3 months
            df[f'{feature}_lag{lag}'] = df.groupby('nomor_rekening_loan')[feature].shift(lag)

    df = df.fillna(0)
    data_pred = df[df['tanggal_data'] == max(df['tanggal_data'])]
    
    # List columns to drop, ensure they exist in the DataFrame
    columns_to_drop = ['norek', 'tanggal_buka', 'tanggal_tutup', 'tipe_segment', 'kolek_nasabah_encoded', 'tanggal_data', 'nomor_rekening_loan', 'kolek_nasabah']
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]  # Avoid dropping non-existent columns
    
    data_pred.drop(columns=columns_to_drop, inplace=True)
    return data_pred

def loan_prediction(data_pred):
    # Load the model
    with open('lgb_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    # Predict the probability of default
    y_pred_loaded = loaded_model.predict(data_pred)
    data_pred['kolek_nasabah'] = y_pred_loaded
    return data_pred  # Returning the modified DataFrame instead of just predictions

def write_data(data_pred):
    # Create 'tanggal_prediksi' from 'year', 'month', 'day'
    data_pred['tanggal_data'] = pd.to_datetime(data_pred[['year', 'month', 'day']])
    data_pred['tanggal_prediksi'] = data_pred['tanggal_data'].apply(
        lambda x: datetime(x.year + 1, 1, 1) if x.month == 12 else datetime(x.year, x.month + 1, 1)
    )
    
    # Save the DataFrame to CSV
    data_pred.to_csv('data_pred.csv', index=False)
    return data_pred

def write_log(data_pred):
    # Get the count of records
    record_count = len(data_pred)
    
    # Get current date and time
    run_date = datetime.today().strftime('%Y-%m-%d')
    run_time = datetime.today().strftime('%H:%M:%S')
    
    # Create the log filename based on 'tanggal_data' (assuming 'tanggal_data' has one value in the data_pred)
    log_filename = f"log_loan_modeling_{data_pred['tanggal_data'].iloc[0].strftime('%Y-%m-%d')}.txt"
    
    # Prepare log data as a dictionary
    log_data = {
        'Record Count': [record_count],
        'Run Date': [run_date],
        'Run Time': [run_time]
    }

    # Convert the log data to DataFrame
    log_df = pd.DataFrame(log_data)

    # Write the log data to a CSV file
    log_df.to_csv(log_filename, index=False)

if __name__ == '__main__':
    # Load the data
    df = pd.read_csv('sample_data_test_2024.csv')

    # Preprocess the data
    data_pred = data_preprocessing(df)

    # Predict the probability of default
    data_pred = loan_prediction(data_pred)

    # Write the data
    write_data(data_pred)

    # Write log data to a CSV log file
    write_log(data_pred)
