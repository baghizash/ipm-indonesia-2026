# Layout Dashboard Power BI: IPM Indonesia 2026

File target: `IPM-Indonesia-2026.pbix`
Tema: latar oat `#FAF6EF`, aksen biru `#2F5D8A`, biru langit `#7FB0D9`,
pink `#D96C8A`, teks slate `#2E2A26`, abu `#8A7F76`.

## Halaman 1: Ringkasan Nasional
- 4 kartu KPI: IPM Nasional 2025 (75,90), IPM Tertinggi
  2025 (85,05, DKI Jakarta), Gap IPM 2025
  (30,14 poin), Jumlah Provinsi Sangat Tinggi 2025 (3 provinsi).
- Line chart: IPM nasional per tahun 2020 sampai 2025 dari
  fact_ipm_nasional.
- Bar ranking mini: 6 provinsi IPM tertinggi tahun 2025.
- Slicer tahun (dim_tahun[tahun]).
- Textbox sumber: BPS, Publikasi IPM 2025 dan BRS IPM 2025 tanggal
  5 November 2025.

## Halaman 2: Peringkat Provinsi
- Bar terurut menurun: IPM per provinsi, filter tahun 2025, semua
  38 provinsi (DKI Jakarta di puncak 85,05,
  Papua Pegunungan di dasar 54,91).
- Tabel rinci: provinsi, IPM, kategori, filter tahun 2025.
- Kartu jumlah provinsi per kategori 2025: Sangat Tinggi 3,
  Tinggi 30, Sedang 4, Rendah 1.
- Slicer tahun (2022 sampai 2025) dan slicer kategori.

## Halaman 3: Komponen
- 4 kartu rata-rata provinsi 2025: UHH 73,18 tahun, HLS
  13,26 tahun, RLS 9,03 tahun, Pengeluaran
  Rp11.962 ribu per tahun.
- Bar chart: UHH per provinsi tahun 2025.
- Bar chart: RLS per provinsi tahun 2025.
- Tabel komponen lengkap 38 provinsi: UHH, HLS, RLS, pengeluaran, IPM,
  pertumbuhan persen.
- Catatan: rata-rata komponen di halaman ini adalah rata-rata sederhana
  38 provinsi, bukan angka nasional resmi BPS.

## Halaman 4: Tren dan Konvergensi
- Line chart: rata-rata IPM provinsi per tahun 2022 sampai 2025.
- Line chart: IPM nasional per tahun 2020 sampai 2025.
- Column chart: Gap IPM per tahun 2022 sampai 2025 (gap 2022 sebesar
  30,08 poin dan gap 2025 sebesar 30,14 poin, jadi
  disparitas antarprovinsi belum menyempit).
- Kartu: Kenaikan IPM 2020 ke 2025 (3,09 poin) dan Gap IPM
  2025 (30,14 poin).
- Textbox kesimpulan: semua provinsi naik setiap tahun, tetapi jarak
  provinsi tertinggi dan terendah bertahan di sekitar 30 poin.
