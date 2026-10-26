# -*- coding: utf-8 -*-
"""
Membangun kit Power BI untuk proyek IPM Indonesia 2026:
CSV model bintang (grain terpisah), measures_dax.md (nama measure polos
ditambah tabel verifikasi yang dihitung dari data yang sama),
dashboard_layout.md, build_guide.md, dan dashboard_preview_halaman1.png.
Angka preview dibaca kembali dari fact CSV yang baru ditulis, bukan
hardcoded.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
PBI = os.path.join(ROOT, "powerbi")
os.makedirs(PBI, exist_ok=True)

BLUE = "#2F5D8A"; SKY = "#7FB0D9"; PINK = "#D96C8A"; OAT = "#FAF6EF"
SLATE = "#2E2A26"; GREY = "#8A7F76"

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def fmt_id(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def fmt_rp_ribu(n):
    return "Rp" + f"{int(round(n)):,}".replace(",", ".") + " ribu"


nas = pd.read_csv(os.path.join(DATA, "ipm_nasional.csv"))
prov = pd.read_csv(os.path.join(DATA, "ipm_provinsi.csv"))
komp = pd.read_csv(os.path.join(DATA, "komponen_provinsi_2025.csv"))

# Urutan provinsi mengikuti urutan sumber BPS pada file provinsi.
prov_order = list(dict.fromkeys(prov["provinsi"].tolist()))
PID = {p: i + 1 for i, p in enumerate(prov_order)}

# ------------------------------------------------------------------ dimensi
dim_provinsi = pd.DataFrame({
    "provinsi_id": [PID[p] for p in prov_order],
    "provinsi": prov_order,
})
dim_provinsi.to_csv(os.path.join(PBI, "dim_provinsi.csv"), index=False)

dim_tahun = pd.DataFrame({
    "tahun_id": nas["tahun"].astype(int),
    "tahun": nas["tahun"].astype(int),
    "kategori_nasional": nas["kategori"],
})
dim_tahun.to_csv(os.path.join(PBI, "dim_tahun.csv"), index=False)

# ------------------------------------------------------------------ fakta
fact_prov = prov.copy()
fact_prov["provinsi_id"] = fact_prov["provinsi"].map(PID)
fact_prov["tahun_id"] = fact_prov["tahun"].astype(int)
fact_prov = fact_prov[["provinsi_id", "provinsi", "tahun_id", "ipm", "kategori"]]
fact_prov = fact_prov.sort_values(["tahun_id", "provinsi_id"]).reset_index(drop=True)
fact_prov.to_csv(os.path.join(PBI, "fact_ipm_provinsi.csv"), index=False)

fact_nas = nas.copy()
fact_nas["tahun_id"] = fact_nas["tahun"].astype(int)
fact_nas = fact_nas[["tahun_id", "ipm", "uhh_tahun", "hls_tahun", "rls_tahun",
                     "pengeluaran_ribu_rp"]]
fact_nas.to_csv(os.path.join(PBI, "fact_ipm_nasional.csv"), index=False)

fact_komp = komp.copy()
fact_komp["provinsi_id"] = fact_komp["provinsi"].map(PID)
fact_komp["tahun_id"] = fact_komp["tahun"].astype(int)
fact_komp = fact_komp[["provinsi_id", "provinsi", "tahun_id", "uhh_tahun",
                       "hls_tahun", "rls_tahun", "pengeluaran_ribu_rp", "ipm",
                       "kategori", "pertumbuhan_persen"]]
fact_komp = fact_komp.sort_values("provinsi_id").reset_index(drop=True)
fact_komp.to_csv(os.path.join(PBI, "fact_komponen_provinsi.csv"), index=False)
print(f"kit CSV: dim_provinsi({len(dim_provinsi)}), dim_tahun({len(dim_tahun)}), "
      f"fact_ipm_provinsi({len(fact_prov)}), fact_ipm_nasional({len(fact_nas)}), "
      f"fact_komponen_provinsi({len(fact_komp)})")

# ------------------------------------------------------- angka verifikasi
n25 = fact_nas[fact_nas.tahun_id == 2025].iloc[0]
n20 = fact_nas[fact_nas.tahun_id == 2020].iloc[0]
p25 = fact_prov[fact_prov.tahun_id == 2025]
top25 = p25.loc[p25.ipm.idxmax()]
bot25 = p25.loc[p25.ipm.idxmin()]
gap25 = float(top25.ipm - bot25.ipm)
kat25 = p25.kategori.value_counts().to_dict()
n_st = int(kat25.get("Sangat Tinggi", 0))
n_t = int(kat25.get("Tinggi", 0))
n_s = int(kat25.get("Sedang", 0))
n_r = int(kat25.get("Rendah", 0))
p22 = fact_prov[fact_prov.tahun_id == 2022]
gap22 = float(p22.ipm.max() - p22.ipm.min())
uhh_m = float(fact_komp.uhh_tahun.mean())
hls_m = float(fact_komp.hls_tahun.mean())
rls_m = float(fact_komp.rls_tahun.mean())
peng_m = float(fact_komp.pengeluaran_ribu_rp.mean())
kenaikan = float(n25.ipm - n20.ipm)

MEASURES_MD = f"""# Measure DAX: IPM Indonesia 2026

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
| IPM Nasional 2025 | {fmt_id(float(n25.ipm))} |
| IPM Nasional 2020 | {fmt_id(float(n20.ipm))} |
| Kenaikan IPM 2020 ke 2025 | {fmt_id(kenaikan)} |
| IPM Tertinggi 2025 | {fmt_id(float(top25.ipm))} ({top25.provinsi}) |
| IPM Terendah 2025 | {fmt_id(float(bot25.ipm))} ({bot25.provinsi}) |
| Gap IPM 2025 | {fmt_id(gap25)} |
| Gap IPM 2022 (filter tahun 2022) | {fmt_id(gap22)} |
| Jumlah Provinsi Sangat Tinggi 2025 | {n_st} |
| Jumlah Provinsi Tinggi 2025 | {n_t} |
| Jumlah Provinsi Sedang 2025 | {n_s} |
| Jumlah Provinsi Rendah 2025 | {n_r} |
| Total provinsi 2025 | {len(p25)} |
| Rata-rata UHH (komponen provinsi 2025) | {fmt_id(uhh_m)} tahun |
| Rata-rata HLS (komponen provinsi 2025) | {fmt_id(hls_m)} tahun |
| Rata-rata RLS (komponen provinsi 2025) | {fmt_id(rls_m)} tahun |
| Rata-rata Pengeluaran (komponen provinsi 2025) | {fmt_rp_ribu(peng_m)} per tahun |
| UHH nasional 2025 (fact_ipm_nasional) | {fmt_id(float(n25.uhh_tahun))} tahun |
| HLS nasional 2025 (fact_ipm_nasional) | {fmt_id(float(n25.hls_tahun))} tahun |
| RLS nasional 2025 (fact_ipm_nasional) | {fmt_id(float(n25.rls_tahun))} tahun |
| Pengeluaran nasional 2025 (fact_ipm_nasional) | {fmt_rp_ribu(float(n25.pengeluaran_ribu_rp))} per tahun |

Catatan: Rata-rata UHH, HLS, RLS, dan Pengeluaran pada tabel komponen
adalah rata-rata sederhana 38 provinsi tahun 2025, bukan angka nasional
resmi. Angka nasional resmi ada di baris fact_ipm_nasional dan nilainya
sedikit berbeda karena agregasi BPS memakai pembobotan penduduk.
Kategori mengikuti ambang BPS: Rendah di bawah 60, Sedang 60 sampai di
bawah 70, Tinggi 70 sampai di bawah 80, Sangat Tinggi 80 ke atas.
"""
with open(os.path.join(PBI, "measures_dax.md"), "w", encoding="utf-8") as f:
    f.write(MEASURES_MD)

LAYOUT = f"""# Layout Dashboard Power BI: IPM Indonesia 2026

File target: `IPM-Indonesia-2026.pbix`
Tema: latar oat `#FAF6EF`, aksen biru `#2F5D8A`, biru langit `#7FB0D9`,
pink `#D96C8A`, teks slate `#2E2A26`, abu `#8A7F76`.

## Halaman 1: Ringkasan Nasional
- 4 kartu KPI: IPM Nasional 2025 ({fmt_id(float(n25.ipm))}), IPM Tertinggi
  2025 ({fmt_id(float(top25.ipm))}, {top25.provinsi}), Gap IPM 2025
  ({fmt_id(gap25)} poin), Jumlah Provinsi Sangat Tinggi 2025 ({n_st} provinsi).
- Line chart: IPM nasional per tahun 2020 sampai 2025 dari
  fact_ipm_nasional.
- Bar ranking mini: 6 provinsi IPM tertinggi tahun 2025.
- Slicer tahun (dim_tahun[tahun]).
- Textbox sumber: BPS, Publikasi IPM 2025 dan BRS IPM 2025 tanggal
  5 November 2025.

## Halaman 2: Peringkat Provinsi
- Bar terurut menurun: IPM per provinsi, filter tahun 2025, semua
  38 provinsi ({top25.provinsi} di puncak {fmt_id(float(top25.ipm))},
  {bot25.provinsi} di dasar {fmt_id(float(bot25.ipm))}).
- Tabel rinci: provinsi, IPM, kategori, filter tahun 2025.
- Kartu jumlah provinsi per kategori 2025: Sangat Tinggi {n_st},
  Tinggi {n_t}, Sedang {n_s}, Rendah {n_r}.
- Slicer tahun (2022 sampai 2025) dan slicer kategori.

## Halaman 3: Komponen
- 4 kartu rata-rata provinsi 2025: UHH {fmt_id(uhh_m)} tahun, HLS
  {fmt_id(hls_m)} tahun, RLS {fmt_id(rls_m)} tahun, Pengeluaran
  {fmt_rp_ribu(peng_m)} per tahun.
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
  {fmt_id(gap22)} poin dan gap 2025 sebesar {fmt_id(gap25)} poin, jadi
  disparitas antarprovinsi belum menyempit).
- Kartu: Kenaikan IPM 2020 ke 2025 ({fmt_id(kenaikan)} poin) dan Gap IPM
  2025 ({fmt_id(gap25)} poin).
- Textbox kesimpulan: semua provinsi naik setiap tahun, tetapi jarak
  provinsi tertinggi dan terendah bertahan di sekitar 30 poin.
"""
with open(os.path.join(PBI, "dashboard_layout.md"), "w", encoding="utf-8") as f:
    f.write(LAYOUT)

GUIDE = """# Panduan Merakit Dashboard: IPM Indonesia 2026

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
"""
with open(os.path.join(PBI, "build_guide.md"), "w", encoding="utf-8") as f:
    f.write(GUIDE)

# ------------------------------------------------------------------ preview
# Baca kembali fact CSV yang baru ditulis agar angka preview terjamin
# sama dengan isi kit.
pv_nas = pd.read_csv(os.path.join(PBI, "fact_ipm_nasional.csv"))
pv_prov = pd.read_csv(os.path.join(PBI, "fact_ipm_provinsi.csv"))
pv_n25 = pv_nas[pv_nas.tahun_id == 2025].iloc[0]
pv_p25 = pv_prov[pv_prov.tahun_id == 2025].sort_values("ipm", ascending=False)
pv_top = pv_p25.iloc[0]
pv_gap = float(pv_p25.ipm.max() - pv_p25.ipm.min())
pv_nst = int((pv_p25.kategori == "Sangat Tinggi").sum())
pv_top6 = pv_p25.head(6).iloc[::-1]

fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=OAT)

ax_t = fig.add_axes([0.045, 0.915, 0.91, 0.075], facecolor=OAT)
ax_t.axis("off")
ax_t.text(0, 0.62, "IPM Indonesia 2026, Ringkasan Nasional", fontsize=30,
          fontweight="bold", color=SLATE, va="top", ha="left")
ax_t.text(0, 0.12, "Indeks Pembangunan Manusia, BPS. Nasional 2020 sampai 2025, provinsi 2022 sampai 2025.",
          fontsize=13, color=GREY, va="top", ha="left")

cards = [
    ("IPM Nasional 2025", fmt_id(float(pv_n25.ipm)), "kategori Tinggi", BLUE),
    ("IPM Tertinggi 2025", fmt_id(float(pv_top.ipm)), str(pv_top.provinsi), PINK),
    ("Gap IPM 2025", fmt_id(pv_gap) + " poin", "tertinggi kurang terendah", BLUE),
    ("Provinsi Sangat Tinggi 2025", str(pv_nst) + " provinsi", "dari 38 provinsi", PINK),
]
gap_w = 0.015
cw = (0.91 - gap_w * (len(cards) - 1)) / len(cards)
for i, (lab, val, sub, col) in enumerate(cards):
    x = 0.045 + i * (cw + gap_w)
    ax = fig.add_axes([x, 0.775, cw, 0.12], facecolor="white")
    ax.axis("off")
    ax.text(0.06, 0.80, lab, fontsize=13, color=GREY, va="top", ha="left", transform=ax.transAxes)
    ax.text(0.06, 0.54, val, fontsize=30, fontweight="bold", color=col, va="top", ha="left", transform=ax.transAxes)
    ax.text(0.06, 0.10, sub, fontsize=12, color=GREY, va="top", ha="left", transform=ax.transAxes)

ax1 = fig.add_axes([0.045, 0.42, 0.52, 0.30], facecolor="white")
ax1.plot(pv_nas.tahun_id, pv_nas.ipm, color=BLUE, lw=2.6, marker="o", ms=7,
         markerfacecolor=BLUE, markeredgecolor="white", markeredgewidth=1.4)
for _, r in pv_nas.iterrows():
    ax1.annotate(fmt_id(float(r.ipm)), (r.tahun_id, r.ipm), textcoords="offset points",
                 xytext=(0, 10), ha="center", fontsize=11, color=BLUE, fontweight="bold")
ax1.set_ylim(float(pv_nas.ipm.min()) - 1.2, float(pv_nas.ipm.max()) + 1.6)
ax1.set_xticks(pv_nas.tahun_id.tolist())
ax1.set_title("Tren IPM nasional, 2020 sampai 2025", fontsize=15, fontweight="bold",
              color=SLATE, loc="left", pad=10)
ax1.tick_params(colors=GREY, labelsize=11)
for s in ["top", "right"]:
    ax1.spines[s].set_visible(False)
ax1.yaxis.grid(True, color="#E4E8ED", linewidth=1)
ax1.set_axisbelow(True)

ax2 = fig.add_axes([0.60, 0.42, 0.355, 0.30], facecolor="white")
ax2.barh(pv_top6.provinsi, pv_top6.ipm, color=SKY, height=0.55)
for lab, v in zip(pv_top6.provinsi, pv_top6.ipm):
    ax2.text(1.5, lab, lab, va="center", ha="left", fontsize=11.5,
             color="white", fontweight="bold")
    ax2.text(v + 0.4, lab, fmt_id(float(v)), va="center", ha="left", fontsize=11.5,
             color=SLATE, fontweight="bold")
ax2.set_yticks([])
ax2.set_xlim(0, float(pv_top6.ipm.max()) * 1.18)
ax2.set_title("Ranking mini: 6 provinsi tertinggi, 2025", fontsize=15, fontweight="bold",
              color=SLATE, loc="left", pad=10)
ax2.tick_params(colors=GREY, labelsize=11)
for s in ["top", "right"]:
    ax2.spines[s].set_visible(False)
ax2.yaxis.grid(False)
ax2.xaxis.grid(True, color="#E4E8ED", linewidth=1)
ax2.set_axisbelow(True)

ax_b = fig.add_axes([0.045, 0.09, 0.91, 0.26], facecolor="white")
ax_b.axis("off")
ax_b.text(0.01, 0.92, "Cara membaca halaman ini", fontsize=15, fontweight="bold",
          color=SLATE, va="top", ha="left", transform=ax_b.transAxes)
ax_b.text(0.01, 0.68,
          f"IPM nasional naik dari {fmt_id(float(pv_nas.iloc[0].ipm))} (2020) ke {fmt_id(float(pv_n25.ipm))} (2025). "
          f"Provinsi tertinggi tahun 2025 adalah {pv_top.provinsi} dengan {fmt_id(float(pv_top.ipm))}.",
          fontsize=12.5, color=SLATE, va="top", ha="left", transform=ax_b.transAxes)
ax_b.text(0.01, 0.42,
          f"Gap antarprovinsi tahun 2025 sebesar {fmt_id(pv_gap)} poin dan kategori Sangat Tinggi baru diisi {pv_nst} provinsi, "
          "sehingga halaman berikutnya fokus pada peringkat dan komponen pembentuk IPM.",
          fontsize=12.5, color=SLATE, va="top", ha="left", transform=ax_b.transAxes)
ax_b.text(0.01, 0.16,
          "Kategori BPS: Rendah di bawah 60, Sedang 60 sampai di bawah 70, Tinggi 70 sampai di bawah 80, Sangat Tinggi 80 ke atas.",
          fontsize=12.5, color=GREY, va="top", ha="left", transform=ax_b.transAxes)

fig.text(0.045, 0.028, "Sumber: BPS, Publikasi IPM 2025 dan BRS IPM 2025 tanggal 5 November 2025. Pratinjau tata letak dari data asli kit Power BI.",
         fontsize=11.5, color=GREY, va="baseline", ha="left")
fig.savefig(os.path.join(PBI, "dashboard_preview_halaman1.png"), facecolor=OAT)
plt.close(fig)
print(f"preview tertulis: IPM nasional 2025={fmt_id(float(pv_n25.ipm))}, "
      f"tertinggi={pv_top.provinsi} {fmt_id(float(pv_top.ipm))}, "
      f"gap={fmt_id(pv_gap)}, sangat tinggi={pv_nst}")
print("measures_dax.md, dashboard_layout.md, build_guide.md tertulis")
