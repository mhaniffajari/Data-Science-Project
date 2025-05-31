import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import urllib.parse
import numpy as np
from google.cloud import storage
import json

# Title of the app
st.title("KYC Hackathon Sans")

# Description
st.write(
    """Pemanfaatan KYC untuk mendapatkan Early Warning System (EWS) dari calon pelanggan.
    Silahkan isi data pelanggan sebagai berikut
    """
)

# URL-encode the password
username = 'HackathonSans'
password = urllib.parse.quote_plus('b}+JI3@hvA1N+u0:3EU@^6Z5uG0P{|@K?"{Y3@#"*d')

# Create SQLAlchemy engine and session for SQL Server
engine = create_engine(
    f'mssql+pyodbc://{username}:{password}@serverhanif.database.windows.net/DB_Hanif?driver=ODBC+Driver+17+for+SQL+Server'
)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Define the KYC table
kyc_table = Table('kyc_customer', metadata,
    Column('Nama', String),
    Column('NIK', String),
    Column('Alamat', String),
    Column('Domisili', String),
    Column('Tempat_Tanggal_Lahir', String),
    Column('Kewarganegaraan', String),
    Column('Pekerjaan', String),
    Column('Spesimen_Tanda_Tangan', String),
    Column('Sumber_Dana', String),
    Column('Tujuan_Penggunaan_Dana', String),
    Column('KTP_Picture', String),
    Column('Selfie_with_KTP', String)
)

# Create the table if it doesn't exist
metadata.create_all(engine)

# Function to create a dataframe
def create_kyc_dataframe():
    return pd.DataFrame(columns=[
        "Nama", "NIK", "Alamat", "Domisili", "Tempat dan Tanggal Lahir",
        "Kewarganegaraan", "Pekerjaan", "Spesimen Tanda Tangan", 
        "Sumber Dana", "Tujuan Penggunaan Dana", "KTP Picture", "Selfie with KTP"
    ])

# Initial KYC data storage
if "kyc_data" not in st.session_state:
    st.session_state.kyc_data = create_kyc_dataframe()

# Function to insert data into SQL Server using pandas to_sql
def insert_data_to_sql_server(df):
    df.to_sql('kyc_customer', con=engine, if_exists='append', index=False)

# Function to read KYC customer table from SQL Server
def read_kyc_table_from_sql_server():
    conn = engine.connect()
    s = kyc_table.select()
    result = conn.execute(s)
    data = result.fetchall()
    columns = result.keys()
    df = pd.DataFrame(data, columns=columns)
    conn.close()
    return df

# Function to upload file to GCS
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Initialize a storage client
    storage_client = storage.Client.from_service_account_json('/workspaces/KYC_Hackathon/xenon-blade-425311-u6-99d9f02f7eea.json')
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)
    # Create a new blob and upload the file's content
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

# Main page buttons
selected_button = st.radio("Choose your role:", ("Admin Bank", "Customer"))

# Admin Bank Button
if selected_button == "Admin Bank":
    st.write("You selected Admin Bank. Here you can read the KYC customer data directly.")
    # Read KYC customer table directly from SQL Server
    kyc_df = read_kyc_table_from_sql_server()
    st.write(kyc_df)  # Display the data in a DataFrame format

# Customer Button
if selected_button == "Customer":
    st.write("You selected Customer. Please fill in your KYC data below.")
    # Customer input form
    with st.form("customer_form"):
        nama = st.text_input("Nama", placeholder="Nama Sesuai KTP")
        NIK = st.number_input("NIK", value=None, min_value=1000000000000000, placeholder="NIK Sesuai KTP")
        alamat = st.text_area("Alamat", placeholder="Alamat Sesuai KTP")
        domisili = st.text_area("Domisili", placeholder="Domisili Sesuai KTP")
        tempat_lahir = st.text_input("Tempat Lahir", placeholder="Tempat Lahir Sesuai KTP")
        tanggal_lahir = st.date_input("Tanggal Lahir", max_value=date.today() - timedelta(days=6120), min_value=date.today() - timedelta(days=36000))
        kewarganegaraan = st.text_input("Kewarganegaraan")
        pekerjaan = st.text_input("Pekerjaan")

        # File uploader for Spesimen Tanda Tangan
        tanda_tangan = st.file_uploader("Unggah Spesimen Tanda Tangan", type=["jpg", "jpeg", "png"])
        sumber_dana = st.text_area("Sumber Dana")
        tujuan_dana = st.text_area("Tujuan Penggunaan Dana")

        # File uploaders for KTP picture and Selfie with KTP
        ktp_picture = st.file_uploader("Unggah Foto KTP", type=["jpg", "jpeg", "png"])
        selfie_ktp = st.file_uploader("Unggah Selfie dengan KTP", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Add data to the dataframe
            new_data = pd.DataFrame({
                "Nama": [nama],
                "NIK": [NIK],
                "Alamat": [alamat],
                "Domisili": [domisili],
                "TEMPAT_TANGGAL_LAHIR": [f"{tempat_lahir}, {tanggal_lahir}"],
                "Kewarganegaraan": [kewarganegaraan],
                "Pekerjaan": [pekerjaan],
                "SPESIMEN_TANDA_TANGAN": [tanda_tangan.name if tanda_tangan else ""],
                "SUMBER_DANA": [sumber_dana],
                "TUJUAN_PENGGUNAAN_DANA": [tujuan_dana],
                "KTP_PICTURE": [ktp_picture.name if ktp_picture else ""],
                "SELFIE_WITH_KTP": [selfie_ktp.name if selfie_ktp else ""]
            })

            # Save data to session state
            st.session_state.kyc_data = pd.concat([st.session_state.kyc_data, new_data], ignore_index=True)
            st.success("Data pelanggan berhasil ditambahkan")

            # Save uploaded files to disk and upload to GCS
            bucket_name = 'kyc_hackathonsans'
            if tanda_tangan is not None:
                with open(f"uploads/{tanda_tangan.name}", "wb") as f:
                    f.write(tanda_tangan.getbuffer())
                upload_to_gcs(bucket_name, f"uploads/{tanda_tangan.name}", f"signatures/{tanda_tangan.name}")

            if ktp_picture is not None:
                with open(f"uploads/{ktp_picture.name}", "wb") as f:
                    f.write(ktp_picture.getbuffer())
                upload_to_gcs(bucket_name, f"uploads/{ktp_picture.name}", f"ktp_pictures/{ktp_picture.name}")

            if selfie_ktp is not None:
                with open(f"uploads/{selfie_ktp.name}", "wb") as f:
                    f.write(selfie_ktp.getbuffer())
                upload_to_gcs(bucket_name, f"uploads/{selfie_ktp.name}", f"selfie_ktp/{selfie_ktp.name}")

            # Insert data into SQL Server
            insert_data_to_sql_server(new_data)
            st.success("Data successfully inserted into SQL Server")
