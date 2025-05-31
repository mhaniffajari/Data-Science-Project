import pandas as pd
import random
from datetime import datetime, timedelta

# Define column names
columns = [
    "tanggal_data", "norek", "nomor_rekening_loan", "cif_no", "tanggal_buka", "tanggal_tutup", 
    "tipe_segment", "saldo_psak", "plafond", "usia_hari", "usia_jatuh_tempo", "tunggak_pokok", 
    "tunggak_bunga", "denda", "frekuensi_tunggakan", "angsuran", "saldo_tabungan", 
    "kolek_nasabah", "inflasi", "suku_bunga_acuan", "bi_usd_jual", "bi_usd_beli", 
    "id_tpt", "id_ikk", "id_ihp", "kolek_nasabah_encoded"
]


# Function to generate random dates in 2024
def random_date_2024():
    start_date = datetime(2024, 12, 1)
    end_date = datetime(2024, 12, 31)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

def end_of_month_date_2024():
    end_of_months = [
        "2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30", "2024-05-31", "2024-06-30",
        "2024-07-31", "2024-08-31", "2024-09-30", "2024-10-31", "2024-11-30", "2024-12-31"
    ]
    return random.choice(end_of_months)

# Generate 1000 rows of sample data
data = []
for i in range(10000):
    tanggal_data = random_date_2024()
    norek = str(random.randint(1000000000, 9999999999))
    nomor_rekening_loan = norek + str(random.randint(0, 9))
    cif_no = str(random.randint(100000000000, 999999999999))
    tanggal_buka = random_date_2024().strftime('%Y-%m-%d')
    tanggal_tutup = "1900-01-01"
    tipe_segment = "Konsumer"
    saldo_psak = round(random.uniform(10000000, 700000000), 2)
    plafond = round(saldo_psak * random.uniform(1.0, 1.5), 2)
    usia_hari = random.randint(0, 5000)
    usia_jatuh_tempo = random.uniform(0, 2000)
    tunggak_pokok = round(random.uniform(0, 1000000), 2)
    tunggak_bunga = round(random.uniform(0, 1000000), 2)
    denda = round(random.uniform(0, 5000), 2)
    frekuensi_tunggakan = round(random.uniform(0, 10), 1)
    angsuran = round(random.uniform(100000, 10000000), 2)
    saldo_tabungan = round(random.uniform(10000, 20000000), 2)
    kolek_nasabah = random.randint(1, 5)
    inflasi = round(random.uniform(0.01, 0.05), 4)
    suku_bunga_acuan = round(random.uniform(0.04, 0.07), 2)
    bi_usd_jual = round(random.uniform(16000, 17000), 2)
    bi_usd_beli = round(random.uniform(15900, 16900), 2)
    id_tpt = round(random.uniform(0.03, 0.07), 4)
    id_ikk = round(random.uniform(120, 130), 2)
    id_ihp = round(random.uniform(110, 125), 2)
    kolek_nasabah_encoded = kolek_nasabah - 1

    row = [
        tanggal_data, norek, nomor_rekening_loan, cif_no, tanggal_buka, tanggal_tutup, 
        tipe_segment, saldo_psak, plafond, usia_hari, usia_jatuh_tempo, tunggak_pokok, 
        tunggak_bunga, denda, frekuensi_tunggakan, angsuran, saldo_tabungan, 
        kolek_nasabah, inflasi, suku_bunga_acuan, bi_usd_jual, bi_usd_beli, 
        id_tpt, id_ikk, id_ihp, kolek_nasabah_encoded
    ]
    data.append(row)

# Convert to DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv('sample_data_test_2024.csv', index=False)
print("Data generation complete. Saved as 'sample_data_2024.csv'")
