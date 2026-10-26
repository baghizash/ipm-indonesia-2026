# -*- coding: utf-8 -*-
"""
Modul pembelajaran Analisis IPM Indonesia 2026.
Landscape A4, gaya pro pemula, Bahasa Indonesia sederhana, banyak visual.
Angka dibaca dari findings.json. Output: Modul-Analisis-IPM.pdf
Tanpa em dash di semua teks.
"""
import json
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (Image, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = os.path.join(ROOT, "charts")
F = json.load(open(os.path.join(ROOT, "findings.json")))

BLUE = colors.HexColor("#2F5D8A"); SKY = colors.HexColor("#7FB0D9")
PINK = colors.HexColor("#D96C8A"); ROSE = colors.HexColor("#E9B7C6")
OAT = colors.HexColor("#FAF6EF")
SLATE = colors.HexColor("#2E2A26"); GREY = colors.HexColor("#8A7F76")
LIGHT = colors.HexColor("#EAF1F7"); PINKBG = colors.HexColor("#FDF0F4")
WHITE = colors.white

W, H = landscape(A4)  # 29.7 x 21 cm

H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=25, leading=31,
                    textColor=BLUE, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=16.5, leading=21,
                    textColor=BLUE, spaceBefore=4, spaceAfter=5)
BODY = ParagraphStyle("BODY", fontName="Helvetica", fontSize=11.5, leading=16,
                      textColor=SLATE, spaceAfter=6)
SMALL = ParagraphStyle("SMALL", fontName="Helvetica", fontSize=9.5, leading=13,
                       textColor=GREY)
CALLOUT = ParagraphStyle("CALLOUT", fontName="Helvetica", fontSize=11.5,
                         leading=16, textColor=SLATE)
BOLD = ParagraphStyle("BOLD", parent=BODY, fontName="Helvetica-Bold")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLUE)
    canvas.rect(0, 0, W, 0.85 * cm, stroke=0, fill=1)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(1.4 * cm, 0.32 * cm,
                      "Modul Analisis IPM Indonesia 2026, Data: BPS (Publikasi IPM 2025 dan BRS IPM 2025)")
    canvas.drawRightString(W - 1.4 * cm, 0.32 * cm, f"Halaman {doc.page}")
    canvas.restoreState()


def img(name, w):
    from PIL import Image as PILImage
    p = os.path.join(CH, name)
    iw, ih = PILImage.open(p).size
    return Image(p, width=w, height=w * ih / iw)


def side_by_side(left, right, w_each=13.1 * cm):
    t = Table([[img(left, w_each), img(right, w_each)]],
              colWidths=[(W - 2.8 * cm) / 2] * 2)
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def callout(text, bg=LIGHT, bar=PINK):
    t = Table([[Paragraph(text, CALLOUT)]], colWidths=[W - 3.4 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def kpi_table():
    data = [[Paragraph("<b>IPM Nasional<br/>2025</b>", SMALL),
             Paragraph("<b>Kenaikan<br/>2020 ke 2025</b>", SMALL),
             Paragraph("<b>IPM Tertinggi<br/>2025</b>", SMALL),
             Paragraph("<b>Gap Tertinggi ke<br/>Terendah 2025</b>", SMALL)],
            [Paragraph("<b><font size=17 color='#2F5D8A'>75,90</font></b>", BODY),
             Paragraph("<b><font size=17 color='#2F5D8A'>+3,09 poin</font></b>", BODY),
             Paragraph("<b><font size=17 color='#2F5D8A'>85,05</font></b>", BODY),
             Paragraph("<b><font size=17 color='#2F5D8A'>30,14 poin</font></b>", BODY)],
            [Paragraph("Kategori Tinggi", SMALL),
             Paragraph("Dari 72,81, rata-rata +0,62 per tahun", SMALL),
             Paragraph("DKI Jakarta", SMALL),
             Paragraph("Terendah Papua Pegunungan 54,91", SMALL)]]
    t = Table(data, colWidths=[(W - 2.8 * cm) / 4] * 4)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#D8E2EC")),
        ("LINEABOVE", (0, 0), (-1, 0), 3, PINK),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


story = []

# ---------------------------------------------------------------- sampul isi
story.append(Spacer(1, 1.1 * cm))
story.append(Paragraph("Memahami Indeks Pembangunan Manusia Indonesia", H1))
story.append(Paragraph(
    "Modul belajar analisis data untuk pemula: membaca angka IPM resmi BPS "
    "dari 2020 sampai 2025, memahami tiga dimensi dan empat komponen "
    "penyusunnya, membaca peringkat 38 provinsi, lalu merakitnya menjadi "
    "dashboard Power BI.", BODY))
story.append(kpi_table())
story.append(Spacer(1, 0.5 * cm))
story.append(callout(
    "<b>Gambaran besarnya:</b> pada 2025, IPM Indonesia adalah 75,90 dan "
    "masuk kategori Tinggi. Angkanya naik 3,09 poin dalam lima tahun. "
    "Tetapi provinsi tertinggi, DKI Jakarta (85,05), berjarak 30,14 poin "
    "dari provinsi terendah, Papua Pegunungan (54,91). Modul ini membedah "
    "kedua sisi cerita itu."))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph(
    "<b>Cara memakai modul ini:</b> baca berurutan. Setiap bab punya "
    "grafik utama, penjelasan dengan bahasa sehari-hari, dan kotak "
    "<i>Analogi</i> atau <i>Catatan Analis</i>. Di akhir ada bab cara "
    "membaca dan merakit dashboard Power BI, latihan singkat, dan "
    "glosarium istilah.", BODY))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 1
story.append(Paragraph("Bab 1: Apa Itu IPM dan Tiga Dimensinya?", H2))
story.append(Paragraph(
    "<b>Indeks Pembangunan Manusia (IPM)</b> adalah satu angka ringkasan "
    "dari 0 sampai 100 yang menjawab pertanyaan sederhana: seberapa maju "
    "kualitas hidup manusia di suatu wilayah? BPS menyusunnya dari "
    "<b>tiga dimensi</b>. Pertama, kesehatan, diukur dengan Umur Harapan "
    "Hidup (UHH). Kedua, pendidikan, diukur dengan Harapan Lama Sekolah "
    "(HLS) dan Rata-rata Lama Sekolah (RLS). Ketiga, standar hidup layak, "
    "diukur dengan pengeluaran riil per kapita yang disesuaikan. Ketiga "
    "dimensi digabung dengan rata-rata ukur (geometrik), sedangkan indeks "
    "pendidikan adalah rata-rata hitung indeks HLS dan indeks RLS.", BODY))
story.append(img("02_komponen_nasional_2020_2025.png", 19.5 * cm))
story.append(callout(
    "<b>Kategori IPM menurut BPS:</b> Rendah bila IPM di bawah 60, Sedang "
    "bila 60 sampai di bawah 70, Tinggi bila 70 sampai di bawah 80, dan "
    "Sangat Tinggi bila 80 ke atas. Indonesia pada 2025 berada di "
    "kategori Tinggi dengan 75,90.",
    bar=SKY))
story.append(Paragraph(
    "Perhatikan perbedaan HLS dan RLS, karena dua istilah ini paling "
    "sering tertukar. HLS adalah harapan: berapa tahun seorang anak usia "
    "7 tahun diperkirakan akan bersekolah ke depan. RLS adalah stok: "
    "berapa tahun rata-rata pendidikan yang sudah ditempuh penduduk usia "
    "25 tahun ke atas. HLS membaca masa depan, RLS membaca masa lalu "
    "yang menumpuk.", BODY))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 2
story.append(Paragraph("Bab 2: Tren Nasional 2020 sampai 2025", H2))
story.append(img("01_tren_nasional_ipm.png", 20.5 * cm))
story.append(Paragraph(
    "IPM nasional naik setiap tahun tanpa satu pun penurunan: 72,81 "
    "(2020), 73,16 (2021), 73,77 (2022), 74,39 (2023), 75,02 (2024), dan "
    "75,90 (2025). Total kenaikan 3,09 poin dalam lima tahun, atau "
    "rata-rata +0,62 poin per tahun. Statusnya tetap kategori Tinggi di "
    "seluruh seri.", BODY))
story.append(callout(
    "<b>Semua komponen ikut naik:</b> UHH dari 73,37 menjadi 74,47 tahun "
    "(+1,10), RLS dari 8,48 menjadi 9,07 tahun (+0,59), HLS dari 12,98 "
    "menjadi 13,30 tahun (+0,32), dan pengeluaran riil dari Rp11.013 "
    "ribu menjadi Rp12.802 ribu per tahun (+16,24%). Jadi kenaikan IPM "
    "bukan ditopang satu komponen saja."))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 3
story.append(Paragraph("Bab 3: Peringkat 38 Provinsi pada 2025", H2))
story.append(img("03_ranking_provinsi_2025.png", 10.5 * cm))
story.append(Paragraph(
    "Provinsi tertinggi adalah DKI Jakarta (85,05), disusul DI Yogyakarta "
    "(82,48) dan Kepulauan Riau (80,53). Ketiganya adalah satu-satunya "
    "provinsi kategori Sangat Tinggi. Di ujung bawah ada Papua "
    "Pegunungan (54,91, kategori Rendah), Papua Tengah (60,64), Papua "
    "Barat (68,48), Papua Selatan (69,54), dan Nusa Tenggara Timur "
    "(69,89). Median IPM provinsi adalah 74,81, artinya separuh provinsi "
    "berada di bawah angka itu.", BODY))
story.append(PageBreak())
story.append(Paragraph("Bab 3 (lanjutan): Kategori dan Gap Antarprovinsi", H2))
story.append(side_by_side("04_distribusi_kategori_2025.png",
                          "05_gap_maks_min_median_2022_2025.png"))
story.append(Paragraph(
    "Distribusi kategori 2025: 3 provinsi Sangat Tinggi, 30 Tinggi, "
    "4 Sedang, dan 1 Rendah. Mayoritas provinsi sudah Tinggi, tetapi "
    "jarak antara puncak dan dasar hampir tidak berubah: gap maksimum "
    "ke minimum adalah 30,08 poin pada 2022 dan 30,14 poin pada 2025, "
    "berubah hanya +0,06 poin. Sebagai rasio, IPM tertinggi adalah 1,55 "
    "kali IPM terendah.", BODY))
story.append(callout(
    "<b>Analogi:</b> bayangkan dua pelari yang sama-sama berlari lebih "
    "cepat dari tahun lalu. Bila pelari depan juga mempercepat langkah, "
    "jarak di antara mereka tidak menutup. Itulah yang terjadi pada gap "
    "IPM, dan bab berikutnya menunjukkan buktinya.",
    bar=SKY))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 4
story.append(Paragraph("Bab 4: Konvergensi, Siapa Mengejar dan Siapa Tertinggal?", H2))
story.append(img("06_gain_provinsi_2022_2025.png", 10.5 * cm))
story.append(Paragraph(
    "Seri provinsi yang sebanding tersedia untuk 2022 sampai 2025 "
    "(seri tidak diperpanjang ke sebelum 2022 karena pemekaran provinsi "
    "Papua). Kenaikan tercepat pada periode ini dicapai Papua Barat: "
    "+2,45 poin, dari 66,03 menjadi 68,48. Kenaikan terlambat adalah "
    "Kalimantan Tengah: +1,69 poin, dari 73,17 menjadi 74,86. Rata-rata "
    "kenaikan semua provinsi adalah 2,05 poin.", BODY))
story.append(PageBreak())
story.append(Paragraph("Bab 4 (lanjutan): Kelompok Bawah Lebih Cepat, Gap Tetap", H2))
story.append(img("07_konvergensi_scatter.png", 20 * cm))
story.append(Paragraph(
    "Kelompok 10 provinsi terbawah versi 2022 (Papua Pegunungan, Papua "
    "Tengah, Papua Barat, Papua Selatan, Nusa Tenggara Timur, Papua "
    "Barat Daya, Sulawesi Barat, Kalimantan Barat, Maluku Utara, dan "
    "Gorontalo) rata-rata naik 2,15 poin. Kelompok 10 provinsi teratas "
    "rata-rata naik 1,99 poin. Kelompok bawah memang tumbuh lebih cepat, "
    "tetapi selisih kecepatannya hanya 0,16 poin.", BODY))
story.append(callout(
    "<b>Catatan Analis:</b> gap maksimum ke minimum ditentukan oleh dua "
    "provinsi ekstrem, bukan oleh rata-rata kelompok. DKI Jakarta naik "
    "+2,28 poin dan Papua Pegunungan naik +2,22 poin pada 2022 sampai "
    "2025, selisihnya +0,06 poin, persis sama dengan perubahan gap dari "
    "30,08 menjadi 30,14 poin."))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 5
story.append(Paragraph("Bab 5: Diagnostik Komponen, Tertinggal di Bagian Mana?", H2))
story.append(side_by_side("08_komponen_bawah_vs_nasional.png",
                          "09_gap_hls_rls_terbawah.png"))
story.append(Paragraph(
    "Bandingkan rata-rata komponen 2025 kelompok 10 provinsi IPM "
    "terendah dengan angka nasional BPS. Pengeluaran: Rp9,36 juta vs "
    "Rp12,80 juta per tahun (selisih Rp3,45 juta, ketertinggalan "
    "terbesar). Rata-rata Lama Sekolah: 7,83 vs 9,07 tahun (selisih "
    "1,24 tahun). Umur Harapan Hidup: 70,41 vs 74,47 tahun (selisih "
    "4,06 tahun). Harapan Lama Sekolah: 12,53 vs 13,30 tahun (selisih "
    "0,77 tahun).", BODY))
story.append(callout(
    "<b>Membaca gap HLS ke RLS:</b> di kelompok 10 terendah, gapnya "
    "4,70 tahun, lebih lebar dari gap nasional 4,23 tahun (selisih "
    "0,47 tahun). Artinya stok pendidikan orang dewasa di kelompok "
    "bawah tertinggal lebih jauh dari harapan generasi anak saat ini. "
    "Sekolah anak membaik, tetapi mengejar ketertinggalan orang dewasa "
    "membutuhkan program tersendiri, misalnya pendidikan kesetaraan.",
    bg=PINKBG))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 6
story.append(Paragraph("Bab 6: IPM vs Kemiskinan, Dua Angka yang Saling Menjelaskan", H2))
story.append(img("12_ipm_vs_kemiskinan.png", 20.5 * cm))
story.append(Paragraph(
    "Pasangan tahunnya dinyatakan eksplisit: <b>IPM 2025 x kemiskinan "
    "Maret 2025</b>, untuk 38 provinsi. Korelasi Pearson keduanya adalah "
    "<b>r = -0,8188</b>, negatif dan kuat. Tanda negatif berarti arahnya "
    "berlawanan: provinsi dengan IPM lebih tinggi cenderung memiliki "
    "persentase penduduk miskin lebih rendah. Contohnya DKI Jakarta "
    "(IPM 85,05, kemiskinan 4,28%) dan Bali (IPM 79,37, kemiskinan "
    "terendah 3,72%), berbanding Papua Pegunungan (IPM 54,91, "
    "kemiskinan 30,03%).", BODY))
story.append(callout(
    "<b>Hati-hati menafsirkan korelasi:</b> korelasi kuat bukan bukti "
    "sebab akibat. IPM dan kemiskinan sama-sama dipengaruhi pengeluaran "
    "rumah tangga, pendidikan, dan layanan kesehatan. Nilai korelasi di "
    "sini dipakai sebagai cek konsistensi dua statistik resmi, bukan "
    "sebagai klaim penyebab."))
story.append(PageBreak())
story.append(Paragraph("Bab 6 (lanjutan): Rentang Komponen Antarprovinsi", H2))
story.append(Paragraph(
    "Dua chart di bawah menunjukkan sebaran Umur Harapan Hidup (kiri) "
    "dan pengeluaran (kanan) di semua provinsi pada 2025. Rentang UHH "
    "adalah 8,72 tahun, dari Papua Pegunungan 67,55 tahun sampai DKI "
    "Jakarta 76,27 tahun. Rentang pengeluaran jauh lebih lebar secara "
    "rasio: DKI Jakarta Rp20.676 ribu berbanding Papua Pegunungan "
    "Rp5.861 ribu per tahun, selisih Rp14.815 ribu atau 3,53 kali lipat.", BODY))
story.append(side_by_side("10_rentang_uhh_provinsi.png",
                          "11_rentang_pengeluaran_provinsi.png"))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 7
story.append(Paragraph("Bab 7: Membaca dan Merakit Dashboard Power BI", H2))
story.append(Paragraph(
    "<b>Cara membaca dashboard:</b> mulai dari Halaman 1 untuk kartu "
    "KPI dan tren nasional, lalu pakai slicer tahun untuk memeriksa "
    "peringkat provinsi di Halaman 2, komponen di Halaman 3, dan gap "
    "antarprovinsi di Halaman 4. Selalu periksa tahun yang aktif di "
    "slicer sebelum mengutip angka.", BODY))
story.append(Image(os.path.join(ROOT, "powerbi", "dashboard_preview_halaman1.png"),
                   width=16 * cm, height=16 * cm * 0.5625))
story.append(Paragraph(
    "Folder <b>powerbi/</b> berisi kit siap rakit menjadi file "
    "<b>IPM-Indonesia-2026.pbix</b> dengan model bintang (star schema): "
    "tiga tabel fakta dihubungkan ke dimensi tahun dan dimensi provinsi.", BODY))
story.append(Paragraph(
    "<b>Langkah singkat:</b> (1) muat 5 CSV dari folder powerbi; "
    "(2) buat relasi sesuai build_guide.md lewat tahun_id dan "
    "provinsi_id; (3) sembunyikan kolom kunci pada tabel fakta; "
    "(4) buat 19 measure dari measures_dax.md dan cocokkan dengan "
    "tabel verifikasinya (IPM Nasional 2025 harus 75,90, Gap IPM 2025 "
    "harus 30,14); (5) susun 4 halaman mengikuti dashboard_layout.md, "
    "atur format 2 desimal, lalu simpan sebagai "
    "IPM-Indonesia-2026.pbix.", BODY))
story.append(callout(
    "<b>Tiga jebakan pemula:</b> jangan menjumlahkan IPM (indeks, pakai "
    "AVERAGE, MAX, atau MIN); selalu kunci filter tahun sebelum membaca "
    "peringkat, karena fact IPM provinsi berisi 4 tahun; dan jangan "
    "menyamakan rata-rata komponen 38 provinsi dengan angka nasional "
    "resmi BPS, karena agregasi BPS memakai pembobotan penduduk.",
    bg=PINKBG))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 8
story.append(Paragraph("Bab 8: SQL dan Notebook, Mengolahnya Sendiri", H2))
story.append(Paragraph(
    "File <b>sql/queries.sql</b> berisi kueri analitis atas CSV "
    "kompilasi: tren nasional 2020 vs 2025, selisih komponen, ranking "
    "provinsi 2025 beserta selisih ke peringkat pertama, jumlah provinsi "
    "per kategori, gap maksimum ke minimum per tahun, gain per provinsi "
    "2022 ke 2025, diagnostik komponen 10 provinsi terendah, dan "
    "rentang UHH serta pengeluaran. Notebook <b>analysis.ipynb</b> "
    "mereproduksi seluruh angka temuan dari CSV yang sama, sehingga "
    "semua klaim di modul ini bisa kamu periksa ulang baris demi baris.", BODY))
story.append(Paragraph("<b>Latihan dan kuis singkat:</b>", BOLD))
story.append(Paragraph(
    "1. Provinsi mana yang kenaikannya tercepat pada 2022 sampai 2025, "
    "dan berapa poin kenaikannya?<br/>"
    "2. Berapa median IPM provinsi pada 2025, dan apa artinya?<br/>"
    "3. Sebuah provinsi memiliki IPM 68,48. Masuk kategori apa provinsi "
    "itu menurut ambang BPS?<br/>"
    "4. Hitung selisih pengeluaran rata-rata kelompok 10 provinsi "
    "terendah (Rp9.356 ribu) terhadap angka nasional (Rp12.802 ribu).<br/>"
    "5. Jelaskan dengan bahasamu sendiri: mengapa gap maksimum ke "
    "minimum bisa tetap, padahal kelompok provinsi terbawah tumbuh "
    "lebih cepat dari kelompok teratas?", BODY))
story.append(callout(
    "<b>Kunci singkat:</b> (1) Papua Barat, +2,45 poin (66,03 menjadi "
    "68,48). (2) 74,81, artinya separuh dari 38 provinsi memiliki IPM "
    "di bawah angka itu. (3) Sedang, karena berada di rentang 60 sampai "
    "di bawah 70. (4) Rp3.446 ribu, sekitar Rp3,45 juta per tahun. "
    "(5) Karena gap ditentukan dua provinsi ekstrem: DKI Jakarta naik "
    "+2,28 poin dan Papua Pegunungan +2,22 poin, jadi jarak keduanya "
    "justru melebar 0,06 poin walau rata-rata kelompok bawah tumbuh "
    "lebih cepat (2,15 vs 1,99 poin).", bg=PINKBG))
story.append(PageBreak())

# ---------------------------------------------------------------- glosarium
story.append(Paragraph("Glosarium dan Sumber", H2))
story.append(Paragraph(
    "<b>IPM</b>: Indeks Pembangunan Manusia, indeks 0 sampai 100 dari "
    "tiga dimensi: kesehatan, pendidikan, standar hidup layak. "
    "<b>UHH</b>: Umur Harapan Hidup, perkiraan lama hidup bayi baru "
    "lahir. <b>HLS</b>: Harapan Lama Sekolah, perkiraan lama sekolah "
    "anak usia 7 tahun ke depan. <b>RLS</b>: Rata-rata Lama Sekolah "
    "penduduk usia 25 tahun ke atas. <b>Pengeluaran disesuaikan</b>: "
    "pengeluaran riil per kapita per tahun dengan harga konstan dan "
    "paritas daya beli, dalam ribu rupiah. <b>Gap</b>: selisih antara "
    "nilai tertinggi dan terendah. <b>Konvergensi</b>: keadaan ketika "
    "kelompok tertinggal tumbuh lebih cepat sehingga jarak menyempit. "
    "<b>Korelasi Pearson (r)</b>: ukuran kekuatan hubungan linear dua "
    "variabel, dari -1 sampai 1. <b>Median</b>: nilai tengah setelah "
    "data diurutkan. <b>BRS</b>: Berita Resmi Statistik, format rilis "
    "resmi BPS. <b>Star schema</b>: pola model Power BI dengan tabel "
    "fakta di tengah dan tabel dimensi di sekelilingnya. <b>Measure "
    "DAX</b>: rumus hitung di Power BI yang hasilnya mengikuti filter "
    "yang aktif.", BODY))
story.append(Paragraph(
    "<b>Sumber data:</b> seluruh angka dikompilasi dari BPS. Seri "
    "nasional 2020 sampai 2025 dari BRS IPM 2025 (No. 104/11/Th. XXVIII, "
    "5 November 2025, Tabel 1 dan Gambar 1). IPM provinsi 2022 sampai "
    "2025 dan komponen per provinsi 2025 dari publikasi tahunan BPS "
    "Indeks Pembangunan Manusia 2025 (Volume 20, 2026, Katalog "
    "4102002, Lampiran 1 dan Lampiran 3). Angka IPM 2025 per provinsi "
    "pada kedua lampiran itu identik untuk 38 dari 38 provinsi. Data "
    "kemiskinan untuk korelasi adalah persentase penduduk miskin per "
    "provinsi periode Maret 2025 dari BRS Profil Kemiskinan BPS, "
    "sehingga pasangan korelasinya adalah IPM 2025 x kemiskinan Maret "
    "2025. Rincian per angka ada di data/SOURCES.md pada repo. Catatan "
    "cakupan: seri provinsi dimulai 2022 karena pemekaran Papua, dan "
    "komponen per provinsi hanya tersedia untuk 2025.", BODY))
story.append(Spacer(1, 0.5 * cm))
story.append(callout(
    "<b>Penutup:</b> angka IPM bukan sekadar statistik, ia adalah "
    "ringkasan harapan hidup, tahun-tahun sekolah, dan daya beli "
    "ratusan juta orang. Tugas analis adalah membacanya dengan jujur: "
    "merayakan kenaikan ke 75,90 sambil tetap menunjuk jurang 30,14 "
    "poin, ketertinggalan pengeluaran dan pendidikan dewasa, dan gap "
    "yang belum menutup. Selamat, kamu baru saja membaca satu laporan "
    "pembangunan manusia utuh seperti analis sungguhan.",
    bg=PINKBG))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph(
    "Disusun oleh BAGHIZ ASSHIDDIQIE ARASYA, Data Analyst. "
    "Repo: github.com/baghizash/ipm-indonesia-2026", SMALL))

doc = SimpleDocTemplate(os.path.join(ROOT, "Modul-Analisis-IPM.pdf"),
                        pagesize=landscape(A4), leftMargin=1.4 * cm,
                        rightMargin=1.4 * cm, topMargin=1.2 * cm,
                        bottomMargin=1.3 * cm,
                        title="Modul Analisis IPM Indonesia 2026",
                        author="Baghiz Asshiddiqie Arasya")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF modul tertulis")
