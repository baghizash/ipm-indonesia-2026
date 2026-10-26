# -*- coding: utf-8 -*-
"""
Kompilasi data Indeks Pembangunan Manusia (IPM) Indonesia dari publikasi
resmi BPS:
  - Publikasi "Indeks Pembangunan Manusia 2025" (Volume 20, 2026;
    Katalog 4102002; No. Publikasi 07300.26007), Lampiran 1 & Lampiran 3.
  - BRS "Indeks Pembangunan Manusia (IPM) 2025" No. 104/11/Th. XXVIII,
    5 November 2025, Tabel 1 & Gambar 1.
Semua angka disalin dari tabel resmi tersebut — tidak ada angka karangan.
Detail sumber per seri ada di data/SOURCES.md.

Menghasilkan:
  data/ipm_nasional.csv            (2020-2025: IPM + 4 komponen)
  data/ipm_provinsi.csv            (2022-2025: IPM per provinsi + kategori)
  data/komponen_provinsi_2025.csv  (2025: IPM + 4 komponen + pertumbuhan)
"""
import csv
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)


def kategori(ipm):
    if ipm < 60:
        return "Rendah"
    if ipm < 70:
        return "Sedang"
    if ipm < 80:
        return "Tinggi"
    return "Sangat Tinggi"


# ------------------------------------------------------- seri nasional
# BRS IPM 2025 Tabel 1 (komponen) & Gambar 1 (IPM), 2020-2025
# tahun: (ipm, uhh, hls, rls, pengeluaran_ribu_rp)
NASIONAL = {
    2020: (72.81, 73.37, 12.98, 8.48, 11013),
    2021: (73.16, 73.46, 13.08, 8.54, 11156),
    2022: (73.77, 73.70, 13.10, 8.69, 11479),
    2023: (74.39, 73.93, 13.15, 8.77, 11899),
    2024: (75.02, 74.15, 13.21, 8.85, 12341),
    2025: (75.90, 74.47, 13.30, 9.07, 12802),
}

with open(os.path.join(DATA, "ipm_nasional.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["tahun", "ipm", "kategori", "uhh_tahun", "hls_tahun", "rls_tahun",
                "pengeluaran_ribu_rp"])
    for th in sorted(NASIONAL):
        ipm, uhh, hls, rls, peng = NASIONAL[th]
        w.writerow([th, f"{ipm:.2f}", kategori(ipm), f"{uhh:.2f}", f"{hls:.2f}",
                    f"{rls:.2f}", peng])

# ------------------------------------------------------- IPM provinsi 2022-2025
# Publikasi IPM 2025, Lampiran 3 (Perkembangan IPM Menurut Provinsi, 2022-2025)
PROV_IPM = {
    "Aceh": (74.11, 74.70, 75.36, 76.23),
    "Sumatera Utara": (74.51, 75.13, 75.76, 76.47),
    "Sumatera Barat": (75.16, 75.64, 76.43, 77.27),
    "Riau": (74.45, 74.95, 75.67, 76.31),
    "Jambi": (73.11, 73.73, 74.36, 75.13),
    "Sumatera Selatan": (72.48, 73.18, 73.84, 74.76),
    "Bengkulu": (73.68, 74.30, 74.91, 75.68),
    "Lampung": (71.79, 72.48, 73.13, 73.98),
    "Kepulauan Bangka Belitung": (73.50, 74.09, 74.55, 75.26),
    "Kepulauan Riau": (78.48, 79.08, 79.89, 80.53),
    "DKI Jakarta": (82.77, 83.55, 84.15, 85.05),
    "Jawa Barat": (73.63, 74.24, 74.92, 75.90),
    "Jawa Tengah": (72.80, 73.39, 73.87, 74.77),
    "DI Yogyakarta": (80.65, 81.09, 81.62, 82.48),
    "Jawa Timur": (74.05, 74.65, 75.35, 76.13),
    "Banten": (75.25, 75.77, 76.35, 77.25),
    "Bali": (77.40, 78.01, 78.63, 79.37),
    "Nusa Tenggara Barat": (71.65, 72.37, 73.10, 73.97),
    "Nusa Tenggara Timur": (67.63, 68.40, 69.14, 69.89),
    "Kalimantan Barat": (69.71, 70.47, 71.19, 72.09),
    "Kalimantan Tengah": (73.17, 73.73, 74.28, 74.86),
    "Kalimantan Selatan": (74.00, 74.66, 75.19, 76.10),
    "Kalimantan Timur": (77.36, 78.20, 78.79, 79.39),
    "Kalimantan Utara": (72.21, 72.88, 73.41, 74.04),
    "Sulawesi Utara": (74.52, 75.04, 75.68, 76.32),
    "Sulawesi Tengah": (71.01, 71.66, 72.24, 72.82),
    "Sulawesi Selatan": (73.96, 74.60, 75.18, 75.92),
    "Sulawesi Tenggara": (72.38, 72.94, 73.62, 74.25),
    "Gorontalo": (70.62, 71.25, 72.01, 72.62),
    "Sulawesi Barat": (69.19, 69.80, 70.46, 71.16),
    "Maluku": (72.04, 72.75, 73.40, 74.09),
    "Maluku Utara": (70.26, 70.98, 71.84, 72.52),
    "Papua Barat": (66.03, 66.84, 67.69, 68.48),
    "Papua Barat Daya": (68.60, 69.07, 69.65, 70.55),
    "Papua": (72.57, 73.23, 73.83, 74.69),
    "Papua Selatan": (67.39, 68.24, 68.86, 69.54),
    "Papua Tengah": (58.76, 59.44, 60.25, 60.64),
    "Papua Pegunungan": (52.69, 53.45, 54.43, 54.91),
}
TAHUN_PROV = [2022, 2023, 2024, 2025]

with open(os.path.join(DATA, "ipm_provinsi.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["tahun", "provinsi", "ipm", "kategori"])
    for prov, vals in PROV_IPM.items():
        for th, v in zip(TAHUN_PROV, vals):
            w.writerow([th, prov, f"{v:.2f}", kategori(v)])

# ------------------------------------------------------- komponen provinsi 2025
# Publikasi IPM 2025, Lampiran 1 (IPM Menurut Provinsi, 2025)
# provinsi: (uhh, hls, rls, pengeluaran_ribu_rp, ipm, pertumbuhan_persen)
KOMP_2025 = {
    "Aceh": (73.48, 14.40, 9.95, 11191, 76.23, 1.15),
    "Sumatera Utara": (74.19, 13.50, 10.08, 11898, 76.47, 0.94),
    "Sumatera Barat": (74.69, 14.31, 9.77, 12041, 77.27, 1.10),
    "Riau": (74.74, 13.44, 9.55, 12233, 76.31, 0.85),
    "Jambi": (74.39, 13.34, 8.95, 12018, 75.13, 1.04),
    "Sumatera Selatan": (74.58, 12.65, 8.91, 12416, 74.76, 1.25),
    "Bengkulu": (73.59, 13.76, 9.23, 12197, 75.68, 1.03),
    "Lampung": (74.71, 12.79, 8.61, 11683, 73.98, 1.16),
    "Kepulauan Bangka Belitung": (74.46, 12.50, 8.65, 13837, 75.26, 0.95),
    "Kepulauan Riau": (75.46, 13.28, 10.72, 15881, 80.53, 0.80),
    "DKI Jakarta": (76.27, 13.80, 11.59, 20676, 85.05, 1.07),
    "Jawa Barat": (75.53, 13.02, 9.14, 12447, 75.90, 1.31),
    "Jawa Tengah": (75.24, 13.05, 8.15, 12746, 74.77, 1.22),
    "DI Yogyakarta": (75.64, 15.78, 10.20, 15855, 82.48, 1.05),
    "Jawa Timur": (75.36, 13.44, 8.39, 13509, 76.13, 1.04),
    "Banten": (75.33, 13.11, 9.56, 13498, 77.25, 1.18),
    "Bali": (75.46, 13.63, 9.75, 15383, 79.37, 0.94),
    "Nusa Tenggara Barat": (72.60, 13.99, 8.21, 11922, 73.97, 1.19),
    "Nusa Tenggara Timur": (72.16, 13.34, 8.22, 8735, 69.89, 1.08),
    "Kalimantan Barat": (74.28, 12.69, 8.07, 10689, 72.09, 1.26),
    "Kalimantan Tengah": (74.01, 12.78, 8.96, 12612, 74.86, 0.78),
    "Kalimantan Selatan": (74.49, 13.12, 8.81, 13757, 76.10, 1.21),
    "Kalimantan Timur": (75.28, 14.04, 10.10, 14254, 79.39, 0.76),
    "Kalimantan Utara": (73.68, 13.31, 9.44, 10568, 74.04, 0.86),
    "Sulawesi Utara": (74.44, 12.98, 9.91, 12450, 76.32, 0.85),
    "Sulawesi Tengah": (71.10, 13.35, 9.10, 10934, 72.82, 0.80),
    "Sulawesi Selatan": (74.15, 13.56, 9.00, 12773, 75.92, 0.98),
    "Sulawesi Tenggara": (72.06, 13.72, 9.56, 10992, 74.25, 0.86),
    "Gorontalo": (71.06, 13.18, 8.38, 11937, 72.62, 0.85),
    "Sulawesi Barat": (71.44, 12.90, 8.31, 10516, 71.16, 0.99),
    "Maluku": (71.02, 14.10, 10.51, 9900, 74.09, 0.94),
    "Maluku Utara": (71.47, 13.76, 9.50, 9613, 72.52, 0.95),
    "Papua Barat": (68.76, 13.21, 8.07, 9115, 68.48, 1.17),
    "Papua Barat Daya": (70.31, 13.89, 8.69, 9076, 70.55, 1.29),
    "Papua": (70.77, 13.94, 10.01, 11342, 74.69, 1.16),
    "Papua Selatan": (68.71, 12.68, 8.64, 9983, 69.54, 0.99),
    "Papua Tengah": (68.38, 9.64, 6.13, 8036, 60.64, 0.65),
    "Papua Pegunungan": (67.55, 9.98, 4.30, 5861, 54.91, 0.88),
}

with open(os.path.join(DATA, "komponen_provinsi_2025.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["tahun", "provinsi", "uhh_tahun", "hls_tahun", "rls_tahun",
                "pengeluaran_ribu_rp", "ipm", "kategori", "pertumbuhan_persen"])
    for prov, (uhh, hls, rls, peng, ipm, gr) in KOMP_2025.items():
        w.writerow([2025, prov, f"{uhh:.2f}", f"{hls:.2f}", f"{rls:.2f}", peng,
                    f"{ipm:.2f}", kategori(ipm), f"{gr:.2f}"])

# sanity check: komponen IPM 2025 cocok dengan Lampiran 3 kolom 2025
for prov, vals in PROV_IPM.items():
    assert abs(vals[3] - KOMP_2025[prov][4]) < 0.005, prov
print("OK: 3 CSV tertulis; cek silang Lampiran 1 vs Lampiran 3 (IPM 2025) lolos untuk 38 provinsi.")
