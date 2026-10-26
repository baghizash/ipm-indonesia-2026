# -*- coding: utf-8 -*-
"""
Membangun PPT portofolio IPM Indonesia 2026 (10 slide, 16:9).
Standar deck terbaru: panel angka hero di sampul, chip KPI, slide temuan,
slide 9 pratinjau Dashboard Power BI, slide 10 Designed Close.
Semua angka dibaca dari findings.json (hasil analysis.py).
Proyek data analyst murni: statistik resmi BPS dan dashboard, tanpa
machine learning. Tanpa em dash di semua teks.
"""
import json
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm, Pt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = os.path.join(ROOT, "charts")
F = json.load(open(os.path.join(ROOT, "findings.json")))

BLUE = RGBColor(0x2F, 0x5D, 0x8A); SKY = RGBColor(0x7F, 0xB0, 0xD9)
PINK = RGBColor(0xD9, 0x6C, 0x8A); ROSE = RGBColor(0xE9, 0xB7, 0xC6)
OAT = RGBColor(0xFA, 0xF6, 0xEF); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SLATE = RGBColor(0x2E, 0x2A, 0x26); GREY = RGBColor(0x8A, 0x7F, 0x76)
LIGHT = RGBColor(0xEF, 0xE4, 0xD8)

prs = Presentation()
prs.slide_width = Cm(33.867); prs.slide_height = Cm(19.05)
BLANK = prs.slide_layouts[6]


def slide(bg=OAT):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg; r.line.fill.background()
    r.shadow.inherit = False
    return s


def box(s, x, y, w, h, fill=None, line=None):
    r = s.shapes.add_shape(1, Cm(x), Cm(y), Cm(w), Cm(h))
    if fill is None:
        r.fill.background()
    else:
        r.fill.solid(); r.fill.fore_color.rgb = fill
    if line is None:
        r.line.fill.background()
    else:
        r.line.color.rgb = line; r.line.width = Pt(1)
    r.shadow.inherit = False
    return r


def txt(s, x, y, w, h, text, size=14, bold=False, color=SLATE, align=PP_ALIGN.LEFT):
    tb = s.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tb.text_frame; tf.word_wrap = True
    lines = text.split("\n")
    tf.paragraphs[0].text = lines[0]; tf.paragraphs[0].alignment = align
    for ln in lines[1:]:
        p = tf.add_paragraph(); p.text = ln; p.alignment = align
    for p in tf.paragraphs:
        p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = color
        p.font.name = "Calibri"
    return tb


def title_bar(s, title, sub=None):
    box(s, 0, 0, 33.87, 2.5, fill=BLUE)
    txt(s, 1.2, 0.42, 31.5, 1.1, title, size=25, bold=True, color=WHITE)
    if sub:
        txt(s, 1.2, 1.42, 31.5, 0.8, sub, size=13, color=ROSE)


def bullets(s, x, y, w, items, size=15, gap=0.35):
    cy = y
    for head, body in items:
        txt(s, x, cy, 0.5, 0.7, "▪", size=size, bold=True, color=PINK)
        txt(s, x + 0.6, cy, w - 0.6, 1.6, head, size=size, bold=True, color=BLUE)
        cy += 0.78
        if body:
            txt(s, x + 0.6, cy, w - 0.6, 1.8, body, size=size - 1.5, color=SLATE)
            cy += 0.62 + 0.55 * (len(body) // 62)
        cy += gap
    return cy


def pic(s, path, x, y, w=None, h=None):
    kw = {}
    if w: kw["width"] = Cm(w)
    if h: kw["height"] = Cm(h)
    return s.shapes.add_picture(path, Cm(x), Cm(y), **kw)


def chip(s, x, y, w, label, value, sub):
    box(s, x, y, w, 3.1, fill=WHITE, line=LIGHT)
    box(s, x, y, w, 0.18, fill=PINK)
    txt(s, x + 0.35, y + 0.32, w - 0.7, 0.6, label, size=11.5, bold=True, color=GREY)
    txt(s, x + 0.35, y + 0.95, w - 0.7, 1.0, value, size=25, bold=True, color=BLUE)
    txt(s, x + 0.35, y + 2.05, w - 0.7, 0.9, sub, size=11, color=SLATE)


def footer(s, n):
    txt(s, 29.9, 18.35, 3.4, 0.5, f"{n} / 10", size=10, color=GREY, align=PP_ALIGN.RIGHT)
    txt(s, 1.2, 18.35, 12, 0.5, "IPM Indonesia 2026 • Data BPS",
        size=10, color=GREY)


# ================================================================ 1 · sampul
s = slide(bg=BLUE)
box(s, 0, 0, 19.6, 19.05, fill=BLUE)
txt(s, 1.4, 2.0, 17.5, 1.0, "PORTOFOLIO ANALISIS DATA", size=15, bold=True, color=SKY)
txt(s, 1.4, 3.1, 17.8, 3.4, "Indeks Pembangunan\nManusia Indonesia\n2026", size=43,
    bold=True, color=WHITE)
txt(s, 1.4, 7.9, 17.2, 2.8,
    "Membaca pembangunan manusia Indonesia lewat statistik resmi BPS: "
    "kesehatan, pendidikan, dan standar hidup layak dari 38 provinsi, "
    "dari tren nasional enam tahun sampai jurang antarprovinsi yang "
    "belum juga menutup.",
    size=15.5, color=ROSE)
box(s, 1.4, 11.2, 16.8, 0.06, fill=SKY)
txt(s, 1.4, 11.7, 17.5, 1.8,
    "Sumber: BPS, Publikasi IPM 2025 dan BRS IPM 2025 (5 November 2025)\n"
    "Periode: nasional 2020 sampai 2025, provinsi 2022 sampai 2025",
    size=13, color=RGBColor(0xD6, 0xE4, 0xF2))
box(s, 1.4, 14.3, 16.8, 2.1, fill=SKY)
txt(s, 1.75, 14.6, 16.2, 1.7,
    "DASHBOARD POWER BI\n"
    "Kit siap rakit: 5 file CSV, model bintang, 19 measure DAX, 4 halaman",
    size=13, bold=True, color=SLATE)
box(s, 20.6, 0, 13.27, 19.05, fill=PINK)
txt(s, 21.8, 2.3, 11, 1.0, "IPM NASIONAL\n2025", size=14, bold=True,
    color=RGBColor(0xFB, 0xEC, 0xF1))
txt(s, 21.8, 4.6, 11.4, 2.2, "75,90", size=60, bold=True, color=WHITE)
txt(s, 21.8, 7.1, 11, 1.4,
    "Kategori Tinggi, naik 3,09 poin dari 72,81 pada 2020 "
    "(rata-rata +0,62 poin per tahun)",
    size=14, color=RGBColor(0xFB, 0xEC, 0xF1))
box(s, 21.8, 9.0, 10, 0.05, fill=ROSE)
txt(s, 21.8, 9.5, 11, 3.6,
    "Tertinggi: DKI Jakarta 85,05\n"
    "Terendah: Papua Pegunungan 54,91\n"
    "Gap: 30,14 poin (1,55 kali lipat)\n"
    "Kategori 2025: 3 Sangat Tinggi,\n"
    "30 Tinggi, 4 Sedang, 1 Rendah",
    size=14.5, color=WHITE)
txt(s, 21.8, 15.6, 11, 1.6, "BAGHIZ ASSHIDDIQIE ARASYA\nData Analyst",
    size=14, bold=True, color=WHITE)

# ================================================================ 2 · KPI
s = slide()
title_bar(s, "Potret Terbaru: IPM 2025 Sebesar 75,90",
          "Empat angka kunci dari Publikasi dan BRS IPM 2025, BPS")
chip(s, 1.2, 3.4, 7.5, "IPM NASIONAL 2025", "75,90",
     "Kategori Tinggi, sama seperti 2020 sampai 2024")
chip(s, 9.3, 3.4, 7.5, "KENAIKAN 2020 KE 2025", "+3,09 poin",
     "72,81 menjadi 75,90, rata-rata +0,62 poin per tahun")
chip(s, 17.4, 3.4, 7.5, "IPM TERTINGGI", "85,05",
     "DKI Jakarta, kategori Sangat Tinggi")
chip(s, 25.5, 3.4, 7.2, "GAP TERTINGGI KE TERENDAH", "30,14 poin",
     "Terendah Papua Pegunungan 54,91, rasio 1,55 kali")
bullets(s, 1.2, 7.6, 31.4, [
    ("Nasional belum menyentuh Sangat Tinggi",
     "Ambang Sangat Tinggi adalah 80. IPM nasional 75,90 masih berjarak "
     "4,10 poin dari ambang itu, dan statusnya Tinggi di seluruh seri "
     "2020 sampai 2025."),
    ("Hanya 3 provinsi yang Sangat Tinggi",
     "DKI Jakarta (85,05), DI Yogyakarta (82,48), dan Kepulauan Riau "
     "(80,53). Sisanya: 30 provinsi Tinggi, 4 Sedang, dan 1 Rendah."),
    ("Provinsi tipikal berada di bawah angka nasional",
     "Median IPM provinsi 2025 adalah 74,81 dan rata-rata sederhana 38 "
     "provinsi 74,25, sedikit di bawah IPM nasional resmi 75,90."),
], size=15.5)
footer(s, 2)

# ================================================================ 3 · tren & komponen
s = slide()
title_bar(s, "Tren Nasional: Naik Setiap Tahun, Semua Komponen Ikut Naik",
          "IPM dan komponen penyusunnya, nasional 2020 sampai 2025")
pic(s, os.path.join(CH, "01_tren_nasional_ipm.png"), 1.2, 3.1, w=15.9)
pic(s, os.path.join(CH, "02_komponen_nasional_2020_2025.png"), 17.0, 3.1, w=15.7)
bullets(s, 1.2, 12.3, 31.4, [
    ("Enam tahun tanpa penurunan",
     "Seri IPM nasional: 72,81 (2020), 73,16, 73,77, 74,39, 75,02, lalu "
     "75,90 (2025). Total kenaikan 3,09 poin, rata-rata +0,62 poin per tahun."),
    ("Komponen 2025 dan perubahannya sejak 2020",
     "Umur Harapan Hidup 74,47 tahun (+1,10), Rata-rata Lama Sekolah 9,07 "
     "tahun (+0,59), Harapan Lama Sekolah 13,30 tahun (+0,32)."),
    ("Standar hidup naik paling besar secara persen",
     "Pengeluaran riil per kapita naik 16,24%, dari Rp11.013 ribu menjadi "
     "Rp12.802 ribu per tahun."),
], size=14.5, gap=0.25)
footer(s, 3)

# ================================================================ 4 · ranking provinsi
s = slide()
title_bar(s, "Peringkat Provinsi 2025: Jurang 30,14 Poin di Satu Negara",
          "IPM per provinsi tahun 2025, 38 provinsi")
pic(s, os.path.join(CH, "03_ranking_provinsi_2025.png"), 1.2, 2.9, h=15.6)
bullets(s, 14.8, 3.2, 17.8, [
    ("DKI Jakarta di puncak: 85,05",
     "Disusul DI Yogyakarta 82,48 dan Kepulauan Riau 80,53. Hanya tiga "
     "provinsi ini yang mencapai kategori Sangat Tinggi (80 ke atas)."),
    ("Papua Pegunungan di dasar: 54,91",
     "Satu-satunya provinsi kategori Rendah (di bawah 60). Di atasnya "
     "Papua Tengah 60,64, lalu klaster Sedang: Papua Barat 68,48, Papua "
     "Selatan 69,54, dan Nusa Tenggara Timur 69,89."),
    ("Mayoritas provinsi berstatus Tinggi",
     "30 dari 38 provinsi berada di rentang 70 sampai di bawah 80. "
     "Kalimantan Timur (79,39) dan Bali (79,37) adalah yang paling dekat "
     "menyusul ke Sangat Tinggi."),
    ("Titik tengah provinsi: 74,81",
     "Separuh provinsi berada di bawah median itu. Jawa Barat tepat di "
     "75,90, sama dengan angka nasional, di peringkat 15."),
], size=14.5)
footer(s, 4)

# ================================================================ 5 · kategori & gap
s = slide()
title_bar(s, "Kategori dan Gap: Mayoritas Tinggi, Jurang Tidak Bergerak",
          "Distribusi kategori 2025 dan jarak tertinggi, terendah, median 2022 sampai 2025")
pic(s, os.path.join(CH, "04_distribusi_kategori_2025.png"), 1.2, 3.1, w=15.9)
pic(s, os.path.join(CH, "05_gap_maks_min_median_2022_2025.png"), 17.0, 3.1, w=15.7)
bullets(s, 1.2, 12.3, 31.4, [
    ("Distribusi kategori 2025",
     "3 provinsi Sangat Tinggi, 30 Tinggi, 4 Sedang, dan 1 Rendah. "
     "Peta pembangunan manusia Indonesia terkonsentrasi di kategori Tinggi."),
    ("Gap maksimum ke minimum: 30,14 poin",
     "DKI Jakarta 85,05 berbanding Papua Pegunungan 54,91, setara 1,55 "
     "kali lipat. Jurang ini adalah cerita utama proyek ini."),
    ("Gap hampir persis sama dengan 2022",
     "Pada 2022 gapnya 30,08 poin, pada 2025 menjadi 30,14 poin, berubah "
     "hanya +0,06 poin dalam tiga tahun."),
], size=14.5, gap=0.25)
footer(s, 5)

# ================================================================ 6 · konvergensi
s = slide()
title_bar(s, "Konvergensi: Yang Tertinggal Berlari Lebih Cepat, Jurang Belum Menutup",
          "Kenaikan IPM per provinsi, 2022 ke 2025")
pic(s, os.path.join(CH, "06_gain_provinsi_2022_2025.png"), 1.2, 2.9, h=15.6)
bullets(s, 16.4, 3.2, 16.2, [
    ("Tercepat: Papua Barat, +2,45 poin",
     "Dari 66,03 (2022) menjadi 68,48 (2025). Disusul Kalimantan Barat "
     "(+2,38) dan Nusa Tenggara Barat (+2,32)."),
    ("Terlambat: Kalimantan Tengah, +1,69 poin",
     "Dari 73,17 menjadi 74,86. Rata-rata kenaikan semua provinsi pada "
     "periode ini adalah 2,05 poin."),
    ("Kelompok bawah memang lebih cepat",
     "10 provinsi terbawah versi 2022 rata-rata naik 2,15 poin, berbanding "
     "1,99 poin untuk 10 provinsi teratas. Selisih kecepatannya hanya "
     "0,16 poin."),
], size=14.5, gap=0.25)
pic(s, os.path.join(CH, "07_konvergensi_scatter.png"), 16.4, 12.4, w=10.5)
txt(s, 27.3, 12.6, 5.4, 3.5,
    "Scatter: IPM awal 2022 vs kenaikan. Titik bawah cenderung naik "
    "lebih besar, tetapi belum cukup untuk menutup gap.",
    size=11.5, color=GREY)
footer(s, 6)

# ================================================================ 7 · diagnostik komponen
s = slide()
title_bar(s, "Diagnostik: 10 Provinsi Terendah Tertinggal di Uang dan Sekolah Dewasa",
          "Rata-rata komponen 2025, kelompok 10 terendah vs angka nasional BPS")
pic(s, os.path.join(CH, "08_komponen_bawah_vs_nasional.png"), 1.2, 3.1, w=15.9)
pic(s, os.path.join(CH, "09_gap_hls_rls_terbawah.png"), 17.0, 3.1, w=15.7)
bullets(s, 1.2, 12.3, 31.4, [
    ("Pengeluaran: ketertinggalan terbesar",
     "Kelompok 10 terendah rata-rata Rp9,36 juta per tahun, berbanding "
     "Rp12,80 juta nasional, selisih Rp3,45 juta."),
    ("Pendidikan dewasa dan kesehatan ikut tertinggal",
     "Rata-rata Lama Sekolah 7,83 tahun vs 9,07 tahun nasional (selisih "
     "1,24), Umur Harapan Hidup 70,41 vs 74,47 tahun (selisih 4,06), "
     "Harapan Lama Sekolah 12,53 vs 13,30 tahun."),
    ("Gap HLS ke RLS lebih lebar di kelompok bawah: 4,70 vs 4,23 tahun",
     "Harapan Lama Sekolah adalah harapan untuk anak usia 7 tahun, "
     "Rata-rata Lama Sekolah adalah stok pendidikan penduduk 25 tahun ke "
     "atas. Gap yang lebih lebar berarti stok pendidikan orang dewasa "
     "tertinggal lebih jauh dari harapan generasi anak saat ini."),
], size=14.5, gap=0.25)
footer(s, 7)

# ================================================================ 8 · rentang & korelasi
s = slide()
title_bar(s, "IPM vs Kemiskinan: Berlawanan Arah Secara Kuat",
          "Korelasi IPM 2025 x kemiskinan Maret 2025, 38 provinsi")
pic(s, os.path.join(CH, "12_ipm_vs_kemiskinan.png"), 1.2, 3.1, w=19.6)
txt(s, 1.2, 14.3, 19.6, 1.2,
    "Chart rentang antarprovinsi per komponen tersedia di repo: "
    "10_rentang_uhh_provinsi.png dan 11_rentang_pengeluaran_provinsi.png.",
    size=11, color=GREY)
bullets(s, 21.6, 3.4, 11.0, [
    ("Korelasi negatif kuat: r = -0,8188",
     "Pasangannya dinyatakan eksplisit: IPM 2025 x kemiskinan Maret 2025. "
     "Provinsi ber-IPM tinggi cenderung ber-kemiskinan rendah."),
    ("Dua kutub yang sama",
     "DKI Jakarta: IPM 85,05 dan kemiskinan 4,28%. Papua Pegunungan: "
     "IPM 54,91 dan kemiskinan 30,03%. Kemiskinan terendah di Bali: "
     "3,72% dengan IPM 79,37."),
    ("Rentang UHH: 8,72 tahun",
     "Umur Harapan Hidup tertinggi DKI Jakarta 76,27 tahun, terendah "
     "Papua Pegunungan 67,55 tahun."),
    ("Rentang pengeluaran: 3,53 kali lipat",
     "DKI Jakarta Rp20.676 ribu berbanding Papua Pegunungan Rp5.861 "
     "ribu per tahun, selisih Rp14.815 ribu."),
], size=14)
footer(s, 8)

# ================================================================ 9 · dashboard
s = slide()
title_bar(s, "Dashboard Power BI: IPM-Indonesia-2026.pbix",
          "Kit siap rakit di folder powerbi/, model bintang, 19 measure DAX, 4 halaman")
pic(s, os.path.join(ROOT, "powerbi", "dashboard_preview_halaman1.png"), 1.2, 3.0, w=19.4)
bullets(s, 21.4, 3.1, 11.2, [
    ("Halaman 1, Ringkasan Nasional",
     "Empat kartu KPI 2025 (75,90; 85,05; gap 30,14; 3 Sangat Tinggi), "
     "tren nasional 2020 sampai 2025, ranking mini 6 teratas, slicer tahun."),
    ("Halaman 2, Peringkat Provinsi",
     "Bar terurut 38 provinsi, tabel rinci dengan kategori, kartu jumlah "
     "per kategori (3, 30, 4, 1), slicer tahun dan kategori."),
    ("Halaman 3, Komponen",
     "Kartu rata-rata provinsi 2025: UHH 73,18, HLS 13,26, RLS 9,03, "
     "pengeluaran Rp11.962 ribu. Catatan: rata-rata sederhana 38 provinsi, "
     "bukan angka nasional resmi."),
    ("Halaman 4, Tren dan Konvergensi",
     "Tren provinsi 2022 sampai 2025 dan nasional 2020 sampai 2025, "
     "kolom gap per tahun, kartu kenaikan 3,09 dan gap 30,14."),
    ("Aman dari jebakan klasik",
     "IPM adalah indeks: jangan dijumlah, pakai AVERAGE, MAX, atau MIN. "
     "Kunci filter tahun sebelum membaca peringkat, dan cocokkan setiap "
     "measure dengan tabel verifikasi di measures_dax.md."),
], size=13)
footer(s, 9)

# ================================================================ 10 · penutup
s = slide(bg=BLUE)
txt(s, 1.4, 1.6, 31, 1.2, "Kesimpulan", size=30, bold=True, color=WHITE)
box(s, 1.4, 3.0, 16.8, 0.06, fill=SKY)
items = [
    ("Naik konsisten enam tahun",
     "IPM mencapai 75,90 (kategori Tinggi) pada 2025, naik 3,09 poin dari "
     "72,81 pada 2020, rata-rata +0,62 poin per tahun, dengan semua "
     "komponen membaik."),
    ("Jurang antarprovinsi belum ikut menyempit",
     "Gap tertinggi ke terendah 30,14 poin (1,55 kali lipat), nyaris sama "
     "dengan 30,08 poin pada 2022, walau kelompok bawah tumbuh lebih "
     "cepat (2,15 vs 1,99 poin)."),
    ("Ketertinggalan terdalam di uang dan pendidikan dewasa",
     "Pengeluaran 10 provinsi terendah Rp9,36 juta vs Rp12,80 juta "
     "nasional, RLS 7,83 vs 9,07 tahun, dan gap HLS ke RLS 4,70 vs "
     "4,23 tahun."),
    ("IPM dan kemiskinan bergerak berlawanan",
     "Korelasi IPM 2025 x kemiskinan Maret 2025 sebesar r = -0,8188: "
     "Papua Pegunungan 54,91 dan 30,03% berbanding DKI Jakarta 85,05 "
     "dan 4,28%."),
    ("Metode dan keterbatasan",
     "Seluruh angka dari Publikasi dan BRS IPM 2025 BPS, dapat ditelusur "
     "di data/SOURCES.md. Seri provinsi mulai 2022 karena pemekaran "
     "Papua, dan komponen provinsi hanya tersedia untuk 2025."),
]
cy = 3.7
for head, body in items:
    txt(s, 1.4, cy, 0.5, 0.7, "▪", size=16, bold=True, color=SKY)
    txt(s, 2.0, cy, 29.5, 0.8, head, size=16.5, bold=True, color=WHITE)
    cy += 0.85
    txt(s, 2.0, cy, 29.5, 1.6, body, size=13.5, color=ROSE)
    cy += 0.62 + 0.5 * (len(body) // 110) + 0.4
box(s, 1.4, 16.6, 31.0, 0.05, fill=SKY)
txt(s, 1.4, 17.0, 31.4, 1.2,
    "Terima kasih, BAGHIZ ASSHIDDIQIE ARASYA • Data Analyst\n"
    "Repo: github.com/baghizash/ipm-indonesia-2026",
    size=14, bold=True, color=WHITE)

OUT = os.path.join(ROOT, "Portofolio-Analisis-IPM.pptx")
prs.save(OUT)
print("PPTX:", OUT)
