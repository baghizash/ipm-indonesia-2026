-- Query SQL Analisis IPM Indonesia 2026
-- Dialek standar / SQLite. Nama tabel sama dengan nama file CSV tanpa .csv:
-- ipm_nasional, ipm_provinsi, komponen_provinsi_2025.
-- Semua query mereproduksi temuan utama di findings.json dari ketiga CSV itu.

-- 1. Tren nasional: IPM 2020 vs 2025, gain total dan rata-rata per tahun
SELECT
    MAX(CASE WHEN tahun = 2025 THEN ipm END) - MAX(CASE WHEN tahun = 2020 THEN ipm END) AS gain_total_poin,
    (MAX(CASE WHEN tahun = 2025 THEN ipm END) - MAX(CASE WHEN tahun = 2020 THEN ipm END)) / 5.0 AS gain_rata_rata_per_tahun,
    MAX(CASE WHEN tahun = 2020 THEN ipm END) AS ipm_2020,
    MAX(CASE WHEN tahun = 2025 THEN ipm END) AS ipm_2025
FROM ipm_nasional;

-- 2. Komponen nasional 2020 vs 2025 dan selisihnya (UHH, HLS, RLS, pengeluaran)
SELECT
    MAX(CASE WHEN tahun = 2025 THEN uhh_tahun END) - MAX(CASE WHEN tahun = 2020 THEN uhh_tahun END) AS delta_uhh,
    MAX(CASE WHEN tahun = 2025 THEN hls_tahun END) - MAX(CASE WHEN tahun = 2020 THEN hls_tahun END) AS delta_hls,
    MAX(CASE WHEN tahun = 2025 THEN rls_tahun END) - MAX(CASE WHEN tahun = 2020 THEN rls_tahun END) AS delta_rls,
    MAX(CASE WHEN tahun = 2025 THEN pengeluaran_ribu_rp END) - MAX(CASE WHEN tahun = 2020 THEN pengeluaran_ribu_rp END) AS delta_pengeluaran_ribu_rp
FROM ipm_nasional;

-- 3. Ranking IPM provinsi 2025 dari tertinggi ke terendah, termasuk gap ke peringkat pertama
SELECT
    provinsi,
    ipm,
    kategori,
    ROUND(MAX(ipm) OVER () - ipm, 2) AS selisih_ke_tertinggi_poin
FROM ipm_provinsi
WHERE tahun = 2025
ORDER BY ipm DESC;

-- 4. Jumlah provinsi per kategori pada 2025 dan daftar provinsi Sangat Tinggi (IPM 80 ke atas)
SELECT kategori, COUNT(*) AS jumlah_provinsi
FROM ipm_provinsi
WHERE tahun = 2025
GROUP BY kategori
ORDER BY MIN(ipm);

SELECT provinsi, ipm
FROM ipm_provinsi
WHERE tahun = 2025 AND ipm >= 80
ORDER BY ipm DESC;

-- 5. Gap maksimum-minimum dan median pendekatan per tahun 2022-2025
-- Catatan: SQLite tidak punya fungsi MEDIAN bawaan, jadi query ini memberi maks, min, gap, dan rata-rata.
SELECT
    tahun,
    MAX(ipm) AS ipm_maks,
    MIN(ipm) AS ipm_min,
    ROUND(MAX(ipm) - MIN(ipm), 2) AS gap_poin,
    ROUND(AVG(ipm), 2) AS rata_rata_ipm
FROM ipm_provinsi
GROUP BY tahun
ORDER BY tahun;

-- 6. Gain per provinsi 2022 ke 2025, terurut dari tercepat (konvergensi)
SELECT
    a.provinsi,
    a.ipm AS ipm_2022,
    b.ipm AS ipm_2025,
    ROUND(b.ipm - a.ipm, 2) AS gain_poin
FROM ipm_provinsi a
JOIN ipm_provinsi b ON b.provinsi = a.provinsi AND b.tahun = 2025
WHERE a.tahun = 2022
ORDER BY gain_poin DESC;

-- 7. Diagnostik komponen 2025: rata-rata 10 provinsi IPM terendah vs rata-rata semua provinsi
SELECT
    '10 terendah' AS kelompok,
    ROUND(AVG(uhh_tahun), 2) AS rata_uhh,
    ROUND(AVG(hls_tahun), 2) AS rata_hls,
    ROUND(AVG(rls_tahun), 2) AS rata_rls,
    ROUND(AVG(hls_tahun - rls_tahun), 2) AS gap_hls_rls,
    ROUND(AVG(pengeluaran_ribu_rp), 2) AS rata_pengeluaran_ribu_rp
FROM (
    SELECT * FROM komponen_provinsi_2025 ORDER BY ipm ASC LIMIT 10
)
UNION ALL
SELECT
    'Semua provinsi',
    ROUND(AVG(uhh_tahun), 2),
    ROUND(AVG(hls_tahun), 2),
    ROUND(AVG(rls_tahun), 2),
    ROUND(AVG(hls_tahun - rls_tahun), 2),
    ROUND(AVG(pengeluaran_ribu_rp), 2)
FROM komponen_provinsi_2025;

-- 8. Rentang UHH dan pengeluaran antarprovinsi pada 2025
SELECT
    MAX(uhh_tahun) - MIN(uhh_tahun) AS rentang_uhh_tahun,
    MAX(pengeluaran_ribu_rp) AS pengeluaran_maks_ribu_rp,
    MIN(pengeluaran_ribu_rp) AS pengeluaran_min_ribu_rp,
    ROUND(MAX(pengeluaran_ribu_rp) * 1.0 / MIN(pengeluaran_ribu_rp), 3) AS rasio_pengeluaran_maks_min
FROM komponen_provinsi_2025;

SELECT provinsi, uhh_tahun, pengeluaran_ribu_rp, ipm
FROM komponen_provinsi_2025
WHERE uhh_tahun = (SELECT MAX(uhh_tahun) FROM komponen_provinsi_2025)
   OR uhh_tahun = (SELECT MIN(uhh_tahun) FROM komponen_provinsi_2025)
   OR pengeluaran_ribu_rp = (SELECT MAX(pengeluaran_ribu_rp) FROM komponen_provinsi_2025)
   OR pengeluaran_ribu_rp = (SELECT MIN(pengeluaran_ribu_rp) FROM komponen_provinsi_2025)
ORDER BY ipm DESC;
