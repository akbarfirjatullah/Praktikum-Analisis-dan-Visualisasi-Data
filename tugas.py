import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import numpy as np

# ==================================================
# 0. LOAD & CLEAN DATA
# ==================================================
file_path = r'D:\Downloads\data_praktikum_analisis_data.csv'

df = pd.read_csv(file_path)

df['Order_Date'] = pd.to_datetime(df['Order_Date'])

df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Price_Per_Unit'] = pd.to_numeric(df['Price_Per_Unit'], errors='coerce')
df['Ad_Budget'] = pd.to_numeric(df['Ad_Budget'], errors='coerce')
df['Total_Sales'] = pd.to_numeric(df['Total_Sales'], errors='coerce')

df.dropna(subset=['Total_Sales'], inplace=True)

df = df[(df['Price_Per_Unit'] > 0) & (df['Quantity'] > 0)]

print(f"Bentuk data setelah dibersihkan: {df.shape}")
print(df.info())

# ==================================================
# TUGAS 1: IDENTIFIKASI PRODUK UNDERPERFORMER
# ==================================================
print("\n========== TUGAS 1: PRODUK UNDERPERFORMER ==========")

mean_price = df['Price_Per_Unit'].mean()
median_qty = df['Quantity'].median()

print(f"Rata-rata Harga per Unit: {mean_price:.2f}")
print(f"Median Kuantitas: {median_qty}")

underperformers = df[(df['Price_Per_Unit'] > mean_price) & (df['Quantity'] < median_qty)]
print(f"Jumlah transaksi underperformer: {len(underperformers)}")

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Price_Per_Unit', y='Quantity', alpha=0.3, label='Semua Produk')
sns.scatterplot(data=underperformers, x='Price_Per_Unit', y='Quantity', color='red', label='Underperformer')
plt.axvline(mean_price, color='green', linestyle='--', label='Rata-rata Harga')
plt.axhline(median_qty, color='orange', linestyle='--', label='Median Kuantitas')
plt.title('Produk Underperformer: Harga Tinggi, Volume Rendah')
plt.xlabel('Harga per Unit')
plt.ylabel('Kuantitas Terjual')
plt.legend()
plt.savefig('figure1.png')
plt.show()

# ==================================================
# TUGAS 2: ANALISIS RFM (SEGMENTASI PELANGGAN)
# ==================================================
print("\n========== TUGAS 2: ANALISIS RFM ==========")

snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)
print(f"Tanggal snapshot: {snapshot_date.date()}")

rfm = df.groupby('CustomerID').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'count',
    'Total_Sales': 'sum'
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
print(rfm.head(10))

rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])
rfm['RFM_Score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

rfm['Segment'] = 'Regular'
rfm.loc[(rfm['R_score'].astype(int) >= 3) & (rfm['F_score'].astype(int) >= 3) & (rfm['M_score'].astype(int) >= 3), 'Segment'] = 'VIP'
rfm.loc[(rfm['R_score'].astype(int) <= 2) & (rfm['F_score'].astype(int) >= 3) & (rfm['M_score'].astype(int) >= 3), 'Segment'] = 'Loyal Berisiko'
rfm.loc[(rfm['R_score'].astype(int) >= 3) & (rfm['F_score'].astype(int) <= 2) & (rfm['M_score'].astype(int) <= 2), 'Segment'] = 'Baru/Nilai Rendah'

print("\nJumlah per segmen:")
print(rfm['Segment'].value_counts())

fig, axes = plt.subplots(1,3, figsize=(15,5))
sns.histplot(rfm['Recency'], bins=20, ax=axes[0], kde=True)
axes[0].set_title('Distribusi Recency')
sns.histplot(rfm['Frequency'], bins=20, ax=axes[1], kde=True)
axes[1].set_title('Distribusi Frequency')
sns.histplot(rfm['Monetary'], bins=20, ax=axes[2], kde=True)
axes[2].set_title('Distribusi Monetary')
plt.tight_layout()
plt.savefig('figure2.png')
plt.show()

# ==================================================
# TUGAS 3: KONTRIBUSI KATEGORI & EFISIENSI IKLAN
# ==================================================
print("\n========== TUGAS 3: EFISIENSI IKLAN PER KATEGORI ==========")

cat_stats = df.groupby('Product_Category').agg(
    Total_Revenue=('Total_Sales', 'sum'),
    Total_Ad_Spend=('Ad_Budget', 'sum')
).reset_index()

cat_stats['Efficiency_Ratio'] = cat_stats['Total_Revenue'] / cat_stats['Total_Ad_Spend']
cat_stats.sort_values('Efficiency_Ratio', ascending=True, inplace=True)

print(cat_stats)

plt.figure(figsize=(10,6))
colors = ['red' if x < 1 else 'lightgreen' for x in cat_stats['Efficiency_Ratio']]
plt.barh(cat_stats['Product_Category'], cat_stats['Efficiency_Ratio'], color=colors)
plt.axvline(1, color='black', linestyle='--', label='Titik Impas (Rasio=1)')
plt.title('Efisiensi Iklan per Kategori (Pendapatan per Pengeluaran Iklan)')
plt.xlabel('Rasio Efisiensi (Pendapatan / Biaya Iklan)')
plt.legend()
plt.tight_layout()
plt.savefig('figure3.png')
plt.show()

# ==================================================
# TUGAS 4: UJI HIPOTESIS – PENGARUH ANGGARAN IKLAN
# ==================================================
print("\n========== TUGAS 4: PENGARUH ANGGARAN IKLAN ==========")

median_ad = df['Ad_Budget'].median()
print(f"Median Anggaran Iklan: {median_ad}")

high_ad = df[df['Ad_Budget'] > median_ad]['Total_Sales']
low_ad = df[df['Ad_Budget'] <= median_ad]['Total_Sales']

print(f"Rata-rata Penjualan Grup Iklan Tinggi: {high_ad.mean():.2f}")
print(f"Rata-rata Penjualan Grup Iklan Rendah: {low_ad.mean():.2f}")

plt.figure(figsize=(8,5))
df['Ad_Group'] = np.where(df['Ad_Budget'] > median_ad, 'Iklan Tinggi', 'Iklan Rendah')
sns.boxplot(data=df, x='Ad_Group', y='Total_Sales')
plt.title('Perbandingan Total Penjualan berdasarkan Kelompok Anggaran Iklan')
plt.xlabel('Kelompok Anggaran Iklan')
plt.ylabel('Total Penjualan')
plt.savefig('figure4.png')
plt.show()

# ==================================================
# TUGAS 5: RINGKASAN SEGMENTASI RFM & REKOMENDASI
# ==================================================
print("\n========== TUGAS 5: RINGKASAN SEGMENTASI RFM & REKOMENDASI ==========")
segment_summary = rfm.groupby('Segment').agg(
    Jumlah_Pelanggan=('CustomerID', 'count'),
    Rata_Recency=('Recency', 'mean'),
    Rata_Frequency=('Frequency', 'mean'),
    Rata_Monetary=('Monetary', 'mean')
).round(2)
print(segment_summary)

print("\nRekomendasi berdasarkan segmen RFM:")
print("- VIP: Berikan akses eksklusif awal ke produk baru.")
print("- Loyal Berisiko: Kirim email re-engagement dengan diskon personal.")
print("- Regular: Dukung dengan konten edukasi dan rekomendasi kategori.")
print("- Baru/Nilai Rendah: Beri insentif diskon pembelian pertama.")

# ==================================================
# SELESAI
# ==================================================