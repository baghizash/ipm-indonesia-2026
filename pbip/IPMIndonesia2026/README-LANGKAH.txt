LANGKAH MEMBUKA PAKET PBIP: IPM Indonesia 2026
====================================================================

1. Ekstrak file ZIP ini ke folder lokal (mis. C:\PowerBI\IPM).
2. Buka file IPMIndonesia2026.pbip dengan Power BI Desktop.
3. Saat diminta parameter, klik Edit Parameters atau Transform Data,
   lalu arahkan FolderData ke folder "data" di dalam hasil ekstrak
   (folder berisi 5 file CSV kit).
4. Klik Refresh agar seluruh tabel termuat.
5. Cek cepat angka kunci (Halaman 1: Ringkasan Nasional):
   - Kartu IPM Nasional 2025 harus menunjukkan 75,90
   - Kartu IPM Tertinggi 2025 harus menunjukkan 85,05 (DKI Jakarta)
   - Kartu Gap IPM 2025 harus menunjukkan 30,14 poin
   - Kartu Provinsi Sangat Tinggi 2025 harus menunjukkan 3 provinsi
   - Halaman 2: jumlah kategori 2025 adalah Sangat Tinggi 3, Tinggi 30,
     Sedang 4, Rendah 1 (total 38 provinsi)
   - Halaman 3: rata-rata komponen provinsi 2025 adalah UHH 73,18 tahun,
     HLS 13,26 tahun, RLS 9,03 tahun, Pengeluaran 11.962 ribu Rp
6. Jika semua cocok, Save As menjadi IPM-Indonesia-2026.pbix.

Catatan sentuhan pertama (wajar terjadi):
- Slicer tahun mungkin tampil sebagai daftar (list), bukan slider.
  Itu normal untuk data tahun kategori.
- Visual peta tidak dipakai (diganti bar terurut) karena visual peta PBIR
  rawan error; peringkat provinsi tetap terbaca jelas dari bar.
- Rata-rata komponen pada Halaman 3 adalah rata-rata sederhana
  38 provinsi tahun 2025, bukan angka nasional resmi BPS. Angka nasional
  resmi 2025: UHH 74,47 tahun, HLS 13,30 tahun, RLS 9,07 tahun,
  Pengeluaran 12.802 ribu Rp.
- Seri provinsi hanya 2022 sampai 2025 karena pemekaran Papua; jangan
  mencari provinsi hasil pemekaran pada tahun sebelum 2022.
