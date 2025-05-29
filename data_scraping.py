import json
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def load_bmkg_data(json_file):
    """
    Memuat data BMKG dari file JSON
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        bmkg_data = json.load(f)
    
    # Konversi ke pandas DataFrame
    df = pd.DataFrame(bmkg_data["data"])
    
    # Konversi tanggal ke datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Tambah kolom tambahan untuk analisis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    
    return df, bmkg_data["meta"]

def analyze_bmkg_data(df, meta):
    """
    Analisis dasar data BMKG
    """
    print(f"Data dari: {meta['station']}, {meta['city']}, {meta['province']}")
    print(f"Periode data: {df['date'].min().date()} hingga {df['date'].max().date()}")
    print(f"Jumlah data: {len(df)} hari\n")
    
    # Statistik dasar
    print("Statistik Dasar:")
    for param, desc in meta['parameters'].items():
        if param in df.columns:
            print(f"{desc}:")
            print(f"  Min: {df[param].min()}")
            print(f"  Max: {df[param].max()}")
            print(f"  Mean: {df[param].mean():.2f}")
            print(f"  Std: {df[param].std():.2f}\n")
    
    # Simpan ke CSV jika diperlukan
    os.makedirs("output", exist_ok=True)
    csv_file = f"output/bmkg_data_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(csv_file, index=False)
    print(f"Data disimpan ke: {csv_file}")
    
    return df

def plot_temperature_trends(df):
    """
    Plot tren temperatur
    """
    plt.figure(figsize=(12, 6))
    
    # Plot temperatur rata-rata bulanan
    monthly_avg = df.groupby(pd.Grouper(key='date', freq='M')).mean()
    
    plt.plot(monthly_avg.index, monthly_avg['Tavg'], label='Temperatur Rata-rata')
    plt.plot(monthly_avg.index, monthly_avg['Tx'], label='Temperatur Maksimum')
    plt.plot(monthly_avg.index, monthly_avg['Tn'], label='Temperatur Minimum')
    
    plt.title('Tren Temperatur Bulanan di Bandung')
    plt.xlabel('Tanggal')
    plt.ylabel('Temperatur (°C)')
    plt.legend()
    plt.grid(True)
    
    # Simpan plot
    plt.savefig('output/temperature_trends.png')
    plt.close()
    print("Plot tren temperatur disimpan ke: output/temperature_trends.png")

def plot_rainfall_patterns(df):
    """
    Plot pola curah hujan
    """
    plt.figure(figsize=(12, 6))
    
    # Plot curah hujan bulanan
    monthly_rain = df.groupby(pd.Grouper(key='date', freq='M'))['RR'].sum()
    
    plt.bar(monthly_rain.index, monthly_rain, color='blue', alpha=0.7)
    
    plt.title('Pola Curah Hujan Bulanan di Bandung')
    plt.xlabel('Tanggal')
    plt.ylabel('Curah Hujan (mm)')
    plt.grid(True, axis='y')
    
    # Simpan plot
    plt.savefig('output/rainfall_patterns.png')
    plt.close()
    print("Plot pola curah hujan disimpan ke: output/rainfall_patterns.png")

def main():
    # Cek keberadaan file JSON
    json_file = "bmkg_data_bandung.json"
    if not os.path.exists(json_file):
        print(f"File {json_file} tidak ditemukan.")
        print("Silakan buat file JSON sesuai format yang ditentukan terlebih dahulu.")
        return
    
    # Muat dan analisis data
    df, meta = load_bmkg_data(json_file)
    df = analyze_bmkg_data(df, meta)
    
    # Buat visualisasi
    plot_temperature_trends(df)
    plot_rainfall_patterns(df)

if __name__ == "__main__":
    main()