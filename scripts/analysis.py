# -*- coding: utf-8 -*-
"""
Analisis IPM Indonesia 2026 - membaca CSV kompilasi BPS di data/,
menghitung findings.json dan membuat 12 chart PNG berlabel Bahasa Indonesia.
Korelasi lintas proyek memakai kemiskinan Mar 2025 dari proyek kemiskinan.
Jalankan: ~/workspace/mienv/bin/python scripts/analysis.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
CHARTS = os.path.join(ROOT, "charts")
KEMISKINAN_CSV = os.path.expanduser("~/workspace/kemiskinan/data/kemiskinan_provinsi.csv")
os.makedirs(CHARTS, exist_ok=True)

# Palet wajib proyek ini (kunci)
BLUE = "#2F5D8A"; SKY = "#7FB0D9"; PINK = "#D96C8A"; ROSE = "#E9B7C6"
OAT = "#FAF6EF"; SLATE = "#2E2A26"; GREY = "#8A7F76"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": SLATE, "axes.edgecolor": "#D8CFC4",
    "axes.labelcolor": SLATE, "xtick.color": SLATE, "ytick.color": SLATE,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.grid": True, "grid.color": "#EFE7DB", "grid.linewidth": 0.7,
    "font.size": 10,
})

def f2(x):
    return round(float(x), 2)

def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, name), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("chart:", name)

# ------------------------------------------------------------------ muat data
nas = pd.read_csv(os.path.join(DATA, "ipm_nasional.csv")).sort_values("tahun")
prov = pd.read_csv(os.path.join(DATA, "ipm_provinsi.csv"))
komp = pd.read_csv(os.path.join(DATA, "komponen_provinsi_2025.csv"))
assert len(nas) == 6 and nas.tahun.min() == 2020 and nas.tahun.max() == 2025
assert len(prov) == 152 and prov.provinsi.nunique() == 38
assert len(komp) == 38

p22 = prov[prov.tahun == 2022].set_index("provinsi")
p25 = prov[prov.tahun == 2025].copy()
p25i = p25.set_index("provinsi")

F = {}
F["sumber"] = "BPS, Publikasi dan BRS IPM 2025 (lihat data/SOURCES.md); semua angka dihitung dari CSV di data/"
F["pasangan_korelasi"] = "IPM 2025 x kemiskinan Mar 2025"

# ------------------------------------------------------------- tren nasional
n20 = nas[nas.tahun == 2020].iloc[0]
n25 = nas[nas.tahun == 2025].iloc[0]
gain_total = f2(n25.ipm - n20.ipm)
F["tren_nasional"] = {
    "ipm_2020": f2(n20.ipm), "ipm_2025": f2(n25.ipm),
    "gain_total_poin_2020_2025": gain_total,
    "gain_rata_rata_per_tahun_poin": round(gain_total / 5, 3),
    "kategori_per_tahun": {str(int(r.tahun)): r.kategori for r in nas.itertuples()},
    "ipm_per_tahun": {str(int(r.tahun)): f2(r.ipm) for r in nas.itertuples()},
    "komponen_2020": {"uhh_tahun": f2(n20.uhh_tahun), "hls_tahun": f2(n20.hls_tahun),
                      "rls_tahun": f2(n20.rls_tahun), "pengeluaran_ribu_rp": int(n20.pengeluaran_ribu_rp)},
    "komponen_2025": {"uhh_tahun": f2(n25.uhh_tahun), "hls_tahun": f2(n25.hls_tahun),
                      "rls_tahun": f2(n25.rls_tahun), "pengeluaran_ribu_rp": int(n25.pengeluaran_ribu_rp)},
    "komponen_delta_2020_2025": {
        "uhh_tahun": f2(n25.uhh_tahun - n20.uhh_tahun),
        "hls_tahun": f2(n25.hls_tahun - n20.hls_tahun),
        "rls_tahun": f2(n25.rls_tahun - n20.rls_tahun),
        "pengeluaran_ribu_rp": int(n25.pengeluaran_ribu_rp - n20.pengeluaran_ribu_rp),
        "pengeluaran_persen": round((n25.pengeluaran_ribu_rp / n20.pengeluaran_ribu_rp - 1) * 100, 2),
    },
}

# ------------------------------------------------------------- ranking 2025
p25s = p25.sort_values("ipm", ascending=False)
tertinggi = p25s.iloc[0]; terendah = p25s.iloc[-1]
kat_counts = p25.kategori.value_counts()
urutan_kat = ["Rendah", "Sedang", "Tinggi", "Sangat Tinggi"]
F["ranking_2025"] = {
    "tertinggi": {"provinsi": tertinggi.provinsi, "ipm": f2(tertinggi.ipm)},
    "terendah": {"provinsi": terendah.provinsi, "ipm": f2(terendah.ipm)},
    "gap_poin": f2(tertinggi.ipm - terendah.ipm),
    "gap_rasio": round(float(tertinggi.ipm / terendah.ipm), 3),
    "median_ipm": f2(p25.ipm.median()),
    "rata_rata_ipm_provinsi": f2(p25.ipm.mean()),
    "jumlah_per_kategori": {k: int(kat_counts.get(k, 0)) for k in urutan_kat},
    "provinsi_ipm_80_ke_atas": [
        {"provinsi": r.provinsi, "ipm": f2(r.ipm)} for r in p25s[p25s.ipm >= 80].itertuples()],
    "ranking_lengkap": [
        {"provinsi": r.provinsi, "ipm": f2(r.ipm), "kategori": r.kategori} for r in p25s.itertuples()],
}

# ------------------------------------------------------------- konvergensi 2022-2025
gab = pd.DataFrame({"ipm_2022": p22.ipm, "ipm_2025": p25i.ipm})
gab["gain"] = (gab.ipm_2025 - gab.ipm_2022).round(2)
gab = gab.sort_values("gain", ascending=False)
tercepat = gab.iloc[0]; terlambat = gab.iloc[-1]
bawah22 = gab.nsmallest(10, "ipm_2022")
atas22 = gab.nlargest(10, "ipm_2022")
gap22 = f2(p22.ipm.max() - p22.ipm.min())
gap25 = F["ranking_2025"]["gap_poin"]
F["konvergensi_2022_2025"] = {
    "gain_per_provinsi": {k: f2(v) for k, v in gab.gain.items()},
    "gain_tercepat": {"provinsi": gab.index[0], "gain_poin": f2(tercepat.gain),
                      "ipm_2022": f2(tercepat.ipm_2022), "ipm_2025": f2(tercepat.ipm_2025)},
    "gain_terlambat": {"provinsi": gab.index[-1], "gain_poin": f2(terlambat.gain),
                       "ipm_2022": f2(terlambat.ipm_2022), "ipm_2025": f2(terlambat.ipm_2025)},
    "gain_rata_rata_semua_provinsi": f2(gab.gain.mean()),
    "kelompok_10_terbawah_2022": {
        "provinsi": list(bawah22.index),
        "gain_rata_rata": f2(bawah22.gain.mean())},
    "kelompok_10_teratas_2022": {
        "provinsi": list(atas22.index),
        "gain_rata_rata": f2(atas22.gain.mean())},
    "kelompok_bawah_tumbuh_lebih_cepat": bool(bawah22.gain.mean() > atas22.gain.mean()),
    "selisih_gain_bawah_kurang_atas": f2(bawah22.gain.mean() - atas22.gain.mean()),
    "gap_maks_min_2022_poin": gap22, "gap_maks_min_2025_poin": gap25,
    "perubahan_gap_poin": f2(gap25 - gap22),
}

# ------------------------------------------------------------- diagnostik komponen 2025
bawah10 = komp.nsmallest(10, "ipm").copy()
kol_komp = ["uhh_tahun", "hls_tahun", "rls_tahun", "pengeluaran_ribu_rp"]
mean_bawah = {k: f2(bawah10[k].mean()) for k in kol_komp}
mean_prov = {k: f2(komp[k].mean()) for k in kol_komp}
nas25 = {"uhh_tahun": f2(n25.uhh_tahun), "hls_tahun": f2(n25.hls_tahun),
         "rls_tahun": f2(n25.rls_tahun), "pengeluaran_ribu_rp": int(n25.pengeluaran_ribu_rp)}
gap_hls_rls_bawah = f2(bawah10.hls_tahun.mean() - bawah10.rls_tahun.mean())
gap_hls_rls_nas = f2(n25.hls_tahun - n25.rls_tahun)
uhh_max = komp.loc[komp.uhh_tahun.idxmax()]; uhh_min = komp.loc[komp.uhh_tahun.idxmin()]
peng_max = komp.loc[komp.pengeluaran_ribu_rp.idxmax()]; peng_min = komp.loc[komp.pengeluaran_ribu_rp.idxmin()]
F["diagnostik_komponen_2025"] = {
    "provinsi_10_terendah": list(bawah10.sort_values("ipm").provinsi),
    "rata_rata_10_terendah": mean_bawah,
    "rata_rata_nasional_2025_bps": nas25,
    "rata_rata_semua_provinsi_2025": mean_prov,
    "selisih_10_terendah_kurang_nasional": {
        k: f2(mean_bawah[k] - nas25[k]) for k in kol_komp},
    "gap_hls_kurang_rls": {
        "kelompok_10_terendah_tahun": gap_hls_rls_bawah,
        "nasional_tahun": gap_hls_rls_nas,
        "selisih_tahun": f2(gap_hls_rls_bawah - gap_hls_rls_nas),
        "catatan": "HLS adalah harapan lama sekolah anak usia 7 tahun (aliran), RLS adalah rata-rata lama sekolah penduduk 25 tahun ke atas (stok). Gap yang lebih lebar di kelompok bawah berarti stok pendidikan orang dewasa tertinggal lebih jauh dari harapan generasi anak saat ini."},
    "rentang_uhh": {
        "maks": {"provinsi": uhh_max.provinsi, "uhh_tahun": f2(uhh_max.uhh_tahun)},
        "min": {"provinsi": uhh_min.provinsi, "uhh_tahun": f2(uhh_min.uhh_tahun)},
        "rentang_tahun": f2(uhh_max.uhh_tahun - uhh_min.uhh_tahun)},
    "rentang_pengeluaran": {
        "maks": {"provinsi": peng_max.provinsi, "pengeluaran_ribu_rp": int(peng_max.pengeluaran_ribu_rp)},
        "min": {"provinsi": peng_min.provinsi, "pengeluaran_ribu_rp": int(peng_min.pengeluaran_ribu_rp)},
        "rentang_ribu_rp": int(peng_max.pengeluaran_ribu_rp - peng_min.pengeluaran_ribu_rp),
        "rasio_maks_min": round(float(peng_max.pengeluaran_ribu_rp / peng_min.pengeluaran_ribu_rp), 3)},
}

# ------------------------------------------------------------- korelasi IPM vs kemiskinan
kem = pd.read_csv(KEMISKINAN_CSV)
kem25 = kem[kem.periode == "Mar 2025"].copy()
# Samakan ejaan nama provinsi bila perlu
peta_nama = {"D.I. Yogyakarta": "DI Yogyakarta", "D I Yogyakarta": "DI Yogyakarta",
             "Yogyakarta": "DI Yogyakarta", "Bangka Belitung": "Kepulauan Bangka Belitung"}
kem25["provinsi_norm"] = kem25.provinsi.replace(peta_nama)
komp_k = komp.copy(); komp_k["provinsi_norm"] = komp_k.provinsi.replace(peta_nama)
gabung = komp_k.merge(kem25[["provinsi_norm", "persen_miskin"]], on="provinsi_norm", how="inner")
assert len(gabung) == 38, len(gabung)
r_pearson = float(gabung.ipm.corr(gabung.persen_miskin, method="pearson"))
# Contoh ekstrem: kuadran dari ranking gabungan
tinggi_rendah = gabung.sort_values(["ipm", "persen_miskin"], ascending=[False, True]).iloc[0]
rendah_tinggi = gabung.sort_values(["ipm", "persen_miskin"], ascending=[True, False]).iloc[0]
miskin_terendah = gabung.loc[gabung.persen_miskin.idxmin()]
miskin_tertinggi = gabung.loc[gabung.persen_miskin.idxmax()]
F["korelasi_ipm_kemiskinan"] = {
    "pasangan": "IPM 2025 x kemiskinan Mar 2025",
    "pearson_r": round(r_pearson, 4),
    "n_provinsi": int(len(gabung)),
    "arah": "negatif" if r_pearson < 0 else "positif",
    "contoh_ipm_tinggi_kemiskinan_rendah": {
        "berdasarkan_ipm_tertinggi": {"provinsi": tinggi_rendah.provinsi, "ipm": f2(tinggi_rendah.ipm),
                                      "persen_miskin": f2(tinggi_rendah.persen_miskin)},
        "berdasarkan_kemiskinan_terendah": {"provinsi": miskin_terendah.provinsi, "ipm": f2(miskin_terendah.ipm),
                                            "persen_miskin": f2(miskin_terendah.persen_miskin)}},
    "contoh_ipm_rendah_kemiskinan_tinggi": {
        "berdasarkan_ipm_terendah": {"provinsi": rendah_tinggi.provinsi, "ipm": f2(rendah_tinggi.ipm),
                                     "persen_miskin": f2(rendah_tinggi.persen_miskin)},
        "berdasarkan_kemiskinan_tertinggi": {"provinsi": miskin_tertinggi.provinsi, "ipm": f2(miskin_tertinggi.ipm),
                                             "persen_miskin": f2(miskin_tertinggi.persen_miskin)}},
}

with open(os.path.join(ROOT, "findings.json"), "w", encoding="utf-8") as fh:
    json.dump(F, fh, indent=2, ensure_ascii=False)
print("findings.json tertulis")
print(json.dumps({"tren": F["tren_nasional"], "ranking_ringkas": {k: F["ranking_2025"][k] for k in ["tertinggi", "terendah", "gap_poin", "gap_rasio", "jumlah_per_kategori"]},
                  "konvergensi_ringkas": {k: F["konvergensi_2022_2025"][k] for k in ["gain_tercepat", "gain_terlambat", "kelompok_bawah_tumbuh_lebih_cepat", "gap_maks_min_2022_poin", "gap_maks_min_2025_poin"]},
                  "korelasi": F["korelasi_ipm_kemiskinan"]}, indent=1, ensure_ascii=False))

# ============================================================ 01 tren nasional
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(nas.tahun, nas.ipm, color=BLUE, lw=2.8, marker="o", ms=6)
ax.fill_between(nas.tahun, nas.ipm, 71, color=SKY, alpha=0.25)
for r in nas.itertuples():
    ax.annotate(f"{r.ipm:.2f}".replace(".", ","), (r.tahun, r.ipm), textcoords="offset points",
                xytext=(0, 9), ha="center", fontsize=9, color=BLUE, fontweight="bold")
ax.set_xticks(nas.tahun); ax.set_ylim(71, 77.5); ax.set_ylabel("IPM")
ax.set_title("Tren IPM Nasional 2020-2025: 72,81 ke 75,90 (naik 3,09 poin, kategori Tinggi)",
             fontsize=12, fontweight="bold", color=BLUE)
save(fig, "01_tren_nasional_ipm.png")

# ============================================================ 02 komponen nasional 2020 vs 2025
labels2 = ["UHH (tahun)", "HLS (tahun)", "RLS (tahun)", "Pengeluaran (ribu Rp)"]
cols2 = ["uhh_tahun", "hls_tahun", "rls_tahun", "pengeluaran_ribu_rp"]
fig, axes = plt.subplots(1, 4, figsize=(10, 5.5))
for ax, lab, c in zip(axes, labels2, cols2):
    vals = [float(n20[c]), float(n25[c])]
    ax.bar(["2020", "2025"], vals, color=[SKY, BLUE], width=0.62)
    for i, v in enumerate(vals):
        ax.annotate(f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    (i, v), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8.5, fontweight="bold", color=BLUE)
    ax.set_title(lab, fontsize=10, fontweight="bold", color=BLUE)
    ax.set_ylim(0, max(vals) * 1.22)
fig.suptitle("Komponen IPM Nasional 2020 vs 2025: Semua Komponen Naik", fontsize=12, fontweight="bold", color=BLUE)
save(fig, "02_komponen_nasional_2020_2025.png")

# ============================================================ 03 ranking provinsi 2025
p25asc = p25.sort_values("ipm")
fig, ax = plt.subplots(figsize=(10, 11))
warna_kat = {"Rendah": PINK, "Sedang": ROSE, "Tinggi": SKY, "Sangat Tinggi": BLUE}
ax.barh(p25asc.provinsi, p25asc.ipm, color=[warna_kat[k] for k in p25asc.kategori])
for r in p25asc.itertuples():
    ax.annotate(f"{r.ipm:.2f}".replace(".", ","), (r.ipm, r.provinsi), textcoords="offset points",
                xytext=(4, -3), fontsize=8, color=SLATE)
ax.axvline(80, color=PINK, ls="--", lw=1.2); ax.axvline(70, color=GREY, ls=":", lw=1.1); ax.axvline(60, color=GREY, ls=":", lw=1.1)
ax.set_xlim(0, 92); ax.set_xlabel("IPM 2025")
ax.set_title("Ranking IPM per Provinsi 2025: DKI Jakarta 85,05 - Papua Pegunungan 54,91",
             fontsize=12, fontweight="bold", color=BLUE)
save(fig, "03_ranking_provinsi_2025.png")

# ============================================================ 04 distribusi kategori
fig, ax = plt.subplots(figsize=(10, 5.5))
counts = [F["ranking_2025"]["jumlah_per_kategori"][k] for k in urutan_kat]
ax.bar(urutan_kat, counts, color=[PINK, ROSE, SKY, BLUE], width=0.6)
for i, v in enumerate(counts):
    ax.annotate(str(v), (i, v), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=12, fontweight="bold", color=BLUE)
ax.set_ylim(0, max(counts) * 1.25); ax.set_ylabel("Jumlah provinsi")
ax.set_title("Distribusi Kategori IPM Provinsi 2025: Mayoritas Tinggi, Hanya 3 Sangat Tinggi",
             fontsize=12, fontweight="bold", color=BLUE)
save(fig, "04_distribusi_kategori_2025.png")

# ============================================================ 05 gap maks-min dan median 2022-2025
rows5 = []
for th in sorted(prov.tahun.unique()):
    s = prov[prov.tahun == th]
    rows5.append({"tahun": th, "maks": s.ipm.max(), "min": s.ipm.min(),
                  "gap": s.ipm.max() - s.ipm.min(), "median": s.ipm.median()})
d5 = pd.DataFrame(rows5)
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(d5["tahun"], d5["gap"], color=PINK, lw=2.6, marker="o", ms=6, label="Gap maks - min (poin)")
ax.plot(d5["tahun"], d5["median"], color=BLUE, lw=2.6, marker="s", ms=6, label="Median provinsi")
ax.plot(d5["tahun"], d5["maks"], color=SKY, lw=1.8, marker="^", ms=5, label="Maksimum")
ax.plot(d5["tahun"], d5["min"], color=GREY, lw=1.8, marker="v", ms=5, label="Minimum")
for r in d5.itertuples():
    ax.annotate(f"{r.gap:.2f}".replace(".", ","), (r.tahun, r.gap), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=9, fontweight="bold", color=PINK)
ax.set_xticks(d5["tahun"]); ax.set_ylabel("IPM / poin")
ax.set_title("Gap Maksimum-Minimum dan Median IPM Provinsi 2022-2025", fontsize=12, fontweight="bold", color=BLUE)
ax.legend(frameon=False, fontsize=9)
save(fig, "05_gap_maks_min_median_2022_2025.png")

# ============================================================ 06 gain provinsi 2022-2025
gasc = gab.sort_values("gain")
fig, ax = plt.subplots(figsize=(10, 11))
ax.barh(gasc.index, gasc.gain, color=[BLUE if v >= gasc.gain.median() else SKY for v in gasc.gain])
for prov_n, v in gasc.gain.items():
    ax.annotate(f"{v:.2f}".replace(".", ","), (v, prov_n), textcoords="offset points",
                xytext=(4, -3), fontsize=8, color=SLATE)
ax.set_xlim(0, max(gasc.gain) * 1.22); ax.set_xlabel("Gain IPM 2022 ke 2025 (poin)")
ax.set_title(f"Gain IPM per Provinsi 2022-2025: Tercepat {gab.index[0]} - Terlambat {gab.index[-1]}",
             fontsize=12, fontweight="bold", color=BLUE)
save(fig, "06_gain_provinsi_2022_2025.png")

# ============================================================ 07 konvergensi scatter
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.scatter(gab.ipm_2022, gab.gain, color=BLUE, s=55, alpha=0.85, edgecolor="white")
coef = np.polyfit(gab.ipm_2022, gab.gain, 1)
xs = np.linspace(gab.ipm_2022.min(), gab.ipm_2022.max(), 10)
ax.plot(xs, np.polyval(coef, xs), color=PINK, lw=2, ls="--", label="Garis tren linear")
for nama in [gab.index[0], gab.index[-1], "DKI Jakarta", "Papua Pegunungan", "Papua Tengah"]:
    r = gab.loc[nama]
    ax.annotate(nama, (r.ipm_2022, r.gain), textcoords="offset points", xytext=(6, 6), fontsize=8.5, color=SLATE)
ax.set_xlabel("IPM 2022"); ax.set_ylabel("Gain 2022 ke 2025 (poin)")
ax.set_title("Konvergensi: IPM Awal 2022 vs Gain ke 2025 (tren negatif berarti mengejar ketertinggalan)",
             fontsize=11, fontweight="bold", color=BLUE)
ax.legend(frameon=False, fontsize=9)
save(fig, "07_konvergensi_scatter.png")

# ============================================================ 08 komponen bawah vs nasional
fig, axes = plt.subplots(1, 4, figsize=(10, 5.5))
for ax, lab, c in zip(axes, labels2, cols2):
    vals = [mean_bawah[c], float(nas25[c])]
    ax.bar(["10 terendah", "Nasional"], vals, color=[PINK, BLUE], width=0.62)
    for i, v in enumerate(vals):
        ax.annotate(f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    (i, v), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8.5, fontweight="bold", color=BLUE)
    ax.set_title(lab, fontsize=10, fontweight="bold", color=BLUE); ax.set_ylim(0, max(vals) * 1.25)
    ax.tick_params(axis="x", labelsize=8)
fig.suptitle("Komponen 2025: Rata-rata 10 Provinsi IPM Terendah vs Nasional", fontsize=12, fontweight="bold", color=BLUE)
save(fig, "08_komponen_bawah_vs_nasional.png")

# ============================================================ 09 gap HLS vs RLS provinsi terbawah
b9 = bawah10.sort_values("ipm")
fig, ax = plt.subplots(figsize=(10, 5.5))
y = np.arange(len(b9)); w = 0.38
ax.barh(y - w / 2, b9.hls_tahun, w, color=SKY, label="HLS (harapan lama sekolah)")
ax.barh(y + w / 2, b9.rls_tahun, w, color=PINK, label="RLS (rata-rata lama sekolah)")
for i, r in enumerate(b9.itertuples()):
    ax.annotate(f"gap {r.hls_tahun - r.rls_tahun:.2f}".replace(".", ","),
                (max(r.hls_tahun, r.rls_tahun) + 0.3, i - 0.1), fontsize=8.5, color=BLUE, fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels(b9.provinsi); ax.set_xlim(0, 17)
ax.set_xlabel("Tahun")
ax.set_title("Gap HLS vs RLS di 10 Provinsi IPM Terendah 2025: Stok Sekolah Dewasa Tertinggal",
             fontsize=11, fontweight="bold", color=BLUE)
ax.legend(frameon=False, fontsize=9, loc="lower right")
save(fig, "09_gap_hls_rls_terbawah.png")

# ============================================================ 10 rentang UHH
uasc = komp.sort_values("uhh_tahun")
fig, ax = plt.subplots(figsize=(10, 11))
ax.barh(uasc.provinsi, uasc.uhh_tahun, color=SKY)
ax.barh([uhh_max.provinsi], [uhh_max.uhh_tahun], color=BLUE)
ax.barh([uhh_min.provinsi], [uhh_min.uhh_tahun], color=PINK)
for r in uasc.itertuples():
    ax.annotate(f"{r.uhh_tahun:.2f}".replace(".", ","), (r.uhh_tahun, r.provinsi),
                textcoords="offset points", xytext=(4, -3), fontsize=8, color=SLATE)
ax.set_xlim(60, 82); ax.set_xlabel("Umur Harapan Hidup 2025 (tahun)")
ax.set_title(f"Rentang UHH per Provinsi 2025: {uhh_max.provinsi} {f2(uhh_max.uhh_tahun)} - {uhh_min.provinsi} {f2(uhh_min.uhh_tahun)}",
             fontsize=11, fontweight="bold", color=BLUE)
save(fig, "10_rentang_uhh_provinsi.png")

# ============================================================ 11 rentang pengeluaran
pasc = komp.sort_values("pengeluaran_ribu_rp")
fig, ax = plt.subplots(figsize=(10, 11))
ax.barh(pasc.provinsi, pasc.pengeluaran_ribu_rp, color=ROSE)
ax.barh([peng_max.provinsi], [peng_max.pengeluaran_ribu_rp], color=BLUE)
ax.barh([peng_min.provinsi], [peng_min.pengeluaran_ribu_rp], color=PINK)
for r in pasc.itertuples():
    ax.annotate(f"{int(r.pengeluaran_ribu_rp):,}".replace(",", "."), (r.pengeluaran_ribu_rp, r.provinsi),
                textcoords="offset points", xytext=(4, -3), fontsize=8, color=SLATE)
ax.set_xlim(0, 24500); ax.set_xlabel("Pengeluaran riil per kapita disesuaikan 2025 (ribu Rp per tahun)")
ax.set_title(f"Rentang Pengeluaran per Provinsi 2025: {peng_max.provinsi} Rp{peng_max.pengeluaran_ribu_rp:,} ribu - {peng_min.provinsi} Rp{peng_min.pengeluaran_ribu_rp:,} ribu".replace(",", "."),
             fontsize=11, fontweight="bold", color=BLUE)
save(fig, "11_rentang_pengeluaran_provinsi.png")

# ============================================================ 12 IPM vs kemiskinan
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.scatter(gabung.ipm, gabung.persen_miskin, color=BLUE, s=55, alpha=0.85, edgecolor="white")
coef12 = np.polyfit(gabung.ipm, gabung.persen_miskin, 1)
xs12 = np.linspace(gabung.ipm.min(), gabung.ipm.max(), 10)
ax.plot(xs12, np.polyval(coef12, xs12), color=PINK, lw=2, ls="--", label="Garis tren linear")
for nama in ["DKI Jakarta", "Papua Pegunungan", "Papua Tengah", "Bali", "DI Yogyakarta"]:
    r = gabung[gabung.provinsi == nama].iloc[0]
    ax.annotate(nama, (r.ipm, r.persen_miskin), textcoords="offset points", xytext=(6, 6), fontsize=8.5, color=SLATE)
ax.set_xlabel("IPM 2025"); ax.set_ylabel("Penduduk miskin Mar 2025 (%)")
ax.set_title(f"IPM 2025 vs Kemiskinan Mar 2025: Korelasi Pearson r = {r_pearson:.2f} (n = 38 provinsi)".replace(".", ","),
             fontsize=12, fontweight="bold", color=BLUE)
ax.legend(frameon=False, fontsize=9)
save(fig, "12_ipm_vs_kemiskinan.png")

print("SELESAI: findings + 12 chart")
