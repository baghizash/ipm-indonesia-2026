# Sumber Data — IPM Indonesia 2026

Semua angka dalam proyek ini **dikompilasi dari publikasi resmi Badan Pusat
Statistik (BPS)**. Tidak ada angka karangan atau estimasi sendiri. Setiap seri
dapat ditelusuri ke dokumen, tabel, dan tanggal rilis di bawah ini.

## Dokumen sumber (bps.go.id / web-api.bps.go.id)

| Dokumen | Nomor & tanggal rilis | Dipakai untuk |
|---|---|---|
| Indeks Pembangunan Manusia 2025 (publikasi tahunan BPS, Volume 20, 2026; Katalog 4102002; No. Publikasi 07300.26007; ISSN 2086-2369) | BPS, 2026 | Lampiran 1: IPM + komponen (UHH, HLS, RLS, pengeluaran) per provinsi tahun 2025 lengkap 38 provinsi; Lampiran 3: perkembangan IPM per provinsi 2022–2025; Tabel 5.1 & Gambar 5.4 (cek silang disparitas) |
| Indeks Pembangunan Manusia (IPM) 2025 — Berita Resmi Statistik | No. 104/11/Th. XXVIII, 5 November 2025 | Tabel 1: IPM nasional + komponen (UHH, HLS, RLS, pengeluaran) 2020–2025; Gambar 1: seri IPM nasional 2020–2025 |

URL induk: https://www.bps.go.id (menu Publikasi → Indeks Pembangunan Manusia;
menu Produk → Berita Resmi Statistik → Indeks Pembangunan Manusia).
Rilis BRS: https://www.bps.go.id/id/pressrelease/2025/11/05/2480/indeks-pembangunan-manusia--ipm-.html

## Catatan metodologi (dari kedua dokumen di atas)

- IPM dihitung dengan **metode baru**: tiga dimensi (kesehatan, pendidikan,
  standar hidup layak), agregasi rata-rata ukur (geometrik) atas indeks
  dimensi; indeks pendidikan adalah rata-rata hitung indeks HLS dan indeks RLS.
- Umur Harapan Hidup (UHH) berasal dari hasil **Long Form Sensus Penduduk
  2020 (LF SP2020)**. Karena itu seri yang konsisten pada kedua dokumen sumber
  dimulai 2020 untuk nasional; seri provinsi pada publikasi 2025 mencakup
  2022–2025 (Lampiran 3). Seri tahun-tahun sebelum 2020 dengan penurunan UHH
  yang berbeda **tidak** digabungkan ke proyek ini agar tidak mencampur
  metodologi.
- Pengeluaran adalah *pengeluaran riil per kapita per tahun yang
  disesuaikan* (harga konstan 2012, paritas daya beli, wilayah rujukan
  Jakarta Selatan), dinyatakan dalam **ribu rupiah per tahun**.
- Kategori/status pembangunan manusia: Rendah (IPM < 60), Sedang
  (60 ≤ IPM < 70), Tinggi (70 ≤ IPM < 80), Sangat Tinggi (IPM ≥ 80).

## Cakupan yang dikompilasi

| File | Isi | Sumber persis |
|---|---|---|
| `ipm_nasional.csv` | IPM + UHH + HLS + RLS + pengeluaran, nasional, 2020–2025 (6 tahun) | BRS IPM 2025 Tabel 1 & Gambar 1 |
| `ipm_provinsi.csv` | IPM + kategori per provinsi, 2022–2025 (38 provinsi × 4 tahun = 152 baris) | Publikasi IPM 2025 Lampiran 3 |
| `komponen_provinsi_2025.csv` | UHH, HLS, RLS, pengeluaran, IPM, pertumbuhan (%) per provinsi, 2025 (38 baris) | Publikasi IPM 2025 Lampiran 1 |

- Cek silang: nilai IPM 2025 per provinsi pada Lampiran 1 dan Lampiran 3
  identik untuk 38/38 provinsi; baris INDONESIA pada Lampiran 1 (75,90)
  identik dengan seri nasional BRS.
- **Penanganan pemekaran provinsi Papua:** sejak 2022 Papua dimekarkan
  menjadi 6 provinsi (Papua, Papua Barat, Papua Barat Daya, Papua Selatan,
  Papua Tengah, Papua Pegunungan). Kedua dokumen sumber sudah menyajikan
  38 provinsi secara konsisten untuk 2022–2025, sehingga tidak ada
  pemetaan/backfill yang dilakukan. Seri provinsi tidak diperpanjang ke
  sebelum 2022 karena pada tahun-tahun itu provinsi hasil pemekaran belum
  ada sebagai unit terpisah.
- Data gabungan lintas proyek (korelasi IPM vs kemiskinan) memakai
  `kemiskinan_provinsi.csv` periode **Maret 2025** dari proyek
  kemiskinan-indonesia-2026 (sumber: BRS Profil Kemiskinan BPS), dipasangkan
  dengan IPM 2025. Pasangan tahun dinyatakan eksplisit di README dan modul.
