# Measure DAX: IPM Indonesia 2026

Model bintang: `fact_ipm_provinsi`, `fact_ipm_nasional`, dan
`fact_komponen_provinsi` terhubung ke `dim_tahun` lewat `tahun_id` dan ke
`dim_provinsi` lewat `provinsi_id` (untuk dua tabel provinsi).
Semua nama measure polos, tanpa karakter khusus selain tanda hubung pada
nama yang memang memakai kata Rata-rata. Tahun dikunci lewat filter
`dim_tahun[tahun]` pada measure yang menyebut tahun tertentu.

## Measure utama

```dax
IPM Terpilih =
AVERAGE ( fact_ipm_provinsi[ipm] )
```

```dax
IPM Nasional =
AVERAGE ( fact_ipm_nasional[ipm] )
```

```dax
IPM Nasional 2025 =
CALCULATE ( [IPM Nasional], dim_tahun[tahun] = 2025 )
```

```dax
IPM Nasional 2020 =
CALCULATE ( [IPM Nasional], dim_tahun[tahun] = 2020 )
```

```dax
Kenaikan IPM 2020 ke 2025 =
[IPM Nasional 2025] - [IPM Nasional 2020]
```

```dax
Jumlah Provinsi Sangat Tinggi =
CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Sangat Tinggi" )
```

```dax
Jumlah Provinsi Sangat Tinggi 2025 =
CALCULATE ( [Jumlah Provinsi Sangat Tinggi], dim_tahun[tahun] = 2025 )
```

```dax
Jumlah Provinsi Tinggi 2025 =
CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Tinggi", dim_tahun[tahun] = 2025 )
```

```dax
Jumlah Provinsi Sedang 2025 =
CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Sedang", dim_tahun[tahun] = 2025 )
```

```dax
Jumlah Provinsi Rendah 2025 =
CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Rendah", dim_tahun[tahun] = 2025 )
```

```dax
IPM Tertinggi =
MAX ( fact_ipm_provinsi[ipm] )
```

```dax
IPM Terendah =
MIN ( fact_ipm_provinsi[ipm] )
```

```dax
Gap IPM =
[IPM Tertinggi] - [IPM Terendah]
```

```dax
IPM Tertinggi 2025 =
CALCULATE ( [IPM Tertinggi], dim_tahun[tahun] = 2025 )
```

```dax
Gap IPM 2025 =
CALCULATE ( [Gap IPM], dim_tahun[tahun] = 2025 )
```

```dax
Rata-rata UHH =
AVERAGE ( fact_komponen_provinsi[uhh_tahun] )
```

```dax
Rata-rata RLS =
AVERAGE ( fact_komponen_provinsi[rls_tahun] )
```

```dax
Rata-rata HLS =
AVERAGE ( fact_komponen_provinsi[hls_tahun] )
```

```dax
Rata-rata Pengeluaran =
AVERAGE ( fact_komponen_provinsi[pengeluaran_ribu_rp] )
```

## Tabel verifikasi (dihitung dari CSV kit yang sama)

| Measure | Nilai yang harus tampil |
|---|---|
| IPM Nasional 2025 | 75,90 |
| IPM Nasional 2020 | 72,81 |
| Kenaikan IPM 2020 ke 2025 | 3,09 |
| IPM Tertinggi 2025 | 85,05 (DKI Jakarta) |
| IPM Terendah 2025 | 54,91 (Papua Pegunungan) |
| Gap IPM 2025 | 30,14 |
| Gap IPM 2022 (filter tahun 2022) | 30,08 |
| Jumlah Provinsi Sangat Tinggi 2025 | 3 |
| Jumlah Provinsi Tinggi 2025 | 30 |
| Jumlah Provinsi Sedang 2025 | 4 |
| Jumlah Provinsi Rendah 2025 | 1 |
| Total provinsi 2025 | 38 |
| Rata-rata UHH (komponen provinsi 2025) | 73,18 tahun |
| Rata-rata HLS (komponen provinsi 2025) | 13,26 tahun |
| Rata-rata RLS (komponen provinsi 2025) | 9,03 tahun |
| Rata-rata Pengeluaran (komponen provinsi 2025) | Rp11.962 ribu per tahun |
| UHH nasional 2025 (fact_ipm_nasional) | 74,47 tahun |
| HLS nasional 2025 (fact_ipm_nasional) | 13,30 tahun |
| RLS nasional 2025 (fact_ipm_nasional) | 9,07 tahun |
| Pengeluaran nasional 2025 (fact_ipm_nasional) | Rp12.802 ribu per tahun |

Catatan: Rata-rata UHH, HLS, RLS, dan Pengeluaran pada tabel komponen
adalah rata-rata sederhana 38 provinsi tahun 2025, bukan angka nasional
resmi. Angka nasional resmi ada di baris fact_ipm_nasional dan nilainya
sedikit berbeda karena agregasi BPS memakai pembobotan penduduk.
Kategori mengikuti ambang BPS: Rendah di bawah 60, Sedang 60 sampai di
bawah 70, Tinggi 70 sampai di bawah 80, Sangat Tinggi 80 ke atas.
