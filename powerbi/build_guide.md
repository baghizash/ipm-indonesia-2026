# Panduan Merakit Dashboard: IPM Indonesia 2026

Hasil akhir: `IPM-Indonesia-2026.pbix`

1. Buka Power BI Desktop, pilih Get Data, Text/CSV, lalu muat 5 file CSV
   di folder ini: `dim_provinsi.csv`, `dim_tahun.csv`,
   `fact_ipm_provinsi.csv`, `fact_ipm_nasional.csv`, dan
   `fact_komponen_provinsi.csv`.
2. Buka Model view dan buat relasi bintang berikut:
   - `fact_ipm_provinsi[provinsi_id]` ke `dim_provinsi[provinsi_id]`
   - `fact_ipm_provinsi[tahun_id]` ke `dim_tahun[tahun_id]`
   - `fact_ipm_nasional[tahun_id]` ke `dim_tahun[tahun_id]`
   - `fact_komponen_provinsi[provinsi_id]` ke `dim_provinsi[provinsi_id]`
   - `fact_komponen_provinsi[tahun_id]` ke `dim_tahun[tahun_id]`
3. Sembunyikan kolom kunci `provinsi_id` dan `tahun_id` pada tabel fakta,
   serta kolom `provinsi` duplikat pada tabel fakta bila perlu, agar panel
   Fields bersih. Pakai `dim_provinsi[provinsi]` dan `dim_tahun[tahun]`
   untuk sumbu dan slicer.
4. Buat semua measure dari `measures_dax.md` dengan nama persis seperti
   di file itu, lalu cocokkan hasilnya dengan tabel verifikasi di file
   yang sama sebelum menyusun visual.
5. Susun 4 halaman mengikuti `dashboard_layout.md` dengan palet biru,
   biru langit, pink, dan latar oat.
6. Atur format angka: IPM, UHH, HLS, dan RLS memakai 2 desimal dengan
   koma sebagai pemisah desimal; pengeluaran memakai format ribuan
   tanpa desimal dan label ribu rupiah.
7. Simpan sebagai `IPM-Indonesia-2026.pbix`.

Jebakan yang harus dihindari:
- Jangan menjumlahkan IPM. IPM adalah indeks, selalu pakai AVERAGE,
  MAX, atau MIN sesuai konteks.
- fact_ipm_provinsi mencampur 4 tahun (2022 sampai 2025). Selalu kunci
  filter tahun sebelum membaca peringkat atau jumlah kategori.
- fact_komponen_provinsi hanya berisi tahun 2025, jadi rata-rata
  komponen selalu konteks 2025 walaupun slicer tahun digeser.
- Rata-rata komponen 38 provinsi bukan angka nasional resmi. Untuk
  kartu nasional resmi pakai fact_ipm_nasional.
- Seri provinsi tidak tersedia sebelum 2022 karena pemekaran Papua;
  jangan memperpanjang seri provinsi ke 2020 atau 2021.
