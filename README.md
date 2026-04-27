# Analisis Performa Penjualan E-commerce

## 0. Pembersihan Data (Data Wrangling)
- Dataset awal memiliki 150 baris, beberapa data `Total_Sales` kosong serta kemungkinan harga/kuantitas negatif.
- Baris dengan `Total_Sales` kosong dihapus, begitu pula data dengan `Price_Per_Unit ≤ 0` atau `Quantity ≤ 0`.
- Hasil akhir: **143 transaksi** bersih dengan 5 kategori produk (Books, Electronics, Fashion, Gadget, Home Decor).
- Tanggal transaksi dari **2 Januari 2023** sampai **26 Desember 2023**.

## 1. Identifikasi Produk Underperformer
**Business Question:** Apakah ada produk mahal yang volume penjualannya rendah (mengikat arus kas)?  
**Data Wrangling:** Menghitung rata‑rata harga dan median kuantitas, lalu menyaring transaksi dengan `Price_Per_Unit` di atas rata‑rata dan `Quantity` di bawah median.

**Insights:**
- Rata‑rata harga per unit: **Rp1.040.643**
- Median kuantitas terjual: **3 unit**
- Terdapat **30 transaksi** yang termasuk underperformer (harga tinggi, volume rendah).
- Scatter plot menunjukkan titik‑titik merah mengumpul di area harga tinggi dengan kuantitas hanya 1–2 unit.

**Recommendation:**
- Produk‑produk ini sebaiknya dikaji ulang: beri diskon terbatas, bundling dengan produk laris, atau dihapus dari katalog jika terus merugi agar arus kas tidak terbebani.

---

## 2. Segmentasi Pelanggan (RFM Analysis)
**Business Question:** Siapa pelanggan terbaik kita dan bagaimana mengelompokkannya untuk program loyalitas?  
**Data Wrangling:** Menghitung Recency (hari sejak belanja terakhir), Frequency (jumlah pesanan), Monetary (total belanja) per `CustomerID`, lalu membagi menjadi 4 segmen.

**Insights:**
- **VIP** (12 pelanggan): recency rata‑rata 41 hari, frekuensi 5×, total belanja Rp17,76 juta.  
- **Loyal Berisiko** (5 pelanggan): recency 154 hari (sudah lama tidak beli), frekuensi 3,6×, total belanja Rp12,25 juta.  
- **Regular** (26 pelanggan): recency 163 hari, frekuensi 2,1×, total belanja Rp6,33 juta.  
- **Baru/Nilai Rendah** (5 pelanggan): recency 54 hari, frekuensi 1,8×, total belanja Rp3,86 juta.

**Recommendation:**
- **VIP:** berikan akses eksklusif produk baru, undangan acara spesial.  
- **Loyal Berisiko:** kirim email re‑engagement dengan diskon personal agar kembali aktif.  
- **Regular:** dorong dengan rekomendasi produk dan konten edukasi.  
- **Baru/Nilai Rendah:** tawarkan diskon pembelian berikutnya untuk meningkatkan frekuensi.

---

## 3. Efisiensi Iklan per Kategori
**Business Question:** Kategori mana yang memberikan hasil terbaik dari setiap rupiah biaya iklan?  
**Data Wrangling:** Mengelompokkan data per `Product_Category`, menjumlahkan Total Sales dan Ad Budget, lalu menghitung rasio efisiensi `Revenue ÷ Ad Spend`.

**Insights:**
| Kategori     | Total Revenue  | Total Ad Spend | Rasio Efisiensi |
|--------------|----------------|----------------|-----------------|
| Gadget       | Rp70.523.000   | Rp68.765.000   | 1,03            |
| Home Decor   | Rp69.340.000   | Rp59.227.000   | 1,17            |
| Fashion      | Rp96.550.000   | Rp77.768.000   | 1,24            |
| Books        | Rp107.569.000  | Rp84.208.000   | 1,28            |
| Electronics  | Rp114.095.000  | Rp79.264.000   | 1,44            |

Semua kategori menghasilkan rasio >1 (iklan menghasilkan lebih besar dari biayanya).  
**Electronics** paling efisien (setiap Rp1 iklan menghasilkan Rp1,44). **Gadget** paling rendah efisiensinya (hampir impas, 1,03).

**Recommendation:**
- Alokasikan lebih banyak anggaran iklan ke **Electronics** dan **Books** yang memberi return terbaik.
- Evaluasi strategi pemasangan iklan di kategori **Gadget** – bisa jadi target audiens kurang tepat atau konten iklan perlu diperbaiki.

---

## 4. Pengaruh Anggaran Iklan terhadap Penjualan
**Business Question:** Apakah anggaran iklan di atas median benar‑benar meningkatkan penjualan secara signifikan?  
**Data Wrangling:** Membagi data menjadi dua kelompok berdasarkan median `Ad_Budget` (Rp2.703.000), lalu membandingkan rata‑rata `Total_Sales`.

**Insights:**
- Kelompok **Iklan Tinggi** (> median): rata‑rata penjualan **Rp3.114.127**
- Kelompok **Iklan Rendah** (≤ median): rata‑rata penjualan **Rp3.291.306**
- Rata‑rata penjualan kelompok iklan rendah justru sedikit lebih tinggi.
- Boxplot menunjukkan sebaran kedua kelompok hampir mirip, tidak ada perbedaan mencolok.

**Recommendation:**
- Menaikkan anggaran iklan tidak otomatis menaikkan penjualan. Fokuslah pada efisiensi: gunakan dana iklan di kategori dan pelanggan yang tepat (lihat Tugas 3 dan RFM). Uji A/B secara bertahap sebelum menaikkan budget secara besar‑besaran.

---

## 5. Rekomendasi Strategi Pemasaran (Gabungan)
**Business Question:** Strategi apa yang paling tepat berdasarkan seluruh temuan?  
**Insight & Recommendation:**
- **Fokus kategori:** Elektronik & Buku adalah "bintang" efisiensi iklan, Gadget perlu perbaikan.
- **Fokus pelanggan:** 12 VIP menyumbang nilai transaksi sangat besar dengan frekuensi tinggi – pertahankan dengan perlakuan eksklusif.
- **Pelanggan berisiko:** 5 pelanggan Loyal Berisiko punya nilai besar tapi sudah lama tidak belanja – segera reaktivasi.
- **Anggaran iklan:** Jangan sekadar menaikkan anggaran, tapi arahkan ulang ke saluran/kategori yang terbukti efisien.

---

**Kesimpulan:**  
Perusahaan dapat meningkatkan profit dengan menghapus atau mendiskon produk underperformer, memprioritaskan iklan pada kategori Electronics & Books, serta menjalankan program loyalitas bertingkat sesuai segmen RFM. Anggaran iklan harus dialokasikan berdasarkan data efisiensi, bukan sekadar dinaikkan.
