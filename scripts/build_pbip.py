#!/usr/bin/env python3
"""Build the IPMIndonesia2026 PBIP package (validated pattern, cf. Kemiskinan2026).

Output: ~/workspace/ipm/pbip/IPMIndonesia2026/ + copy at ~/workspace/pbip/IPMIndonesia2026/
Validate: python3 ~/workspace/pbip/validate_pbip.py ~/workspace/ipm/pbip/IPMIndonesia2026
"""
import json, uuid, shutil
from pathlib import Path

NS = uuid.UUID('7a2d91c4-5e6f-4a8b-9c01-2d3e4f5a6b70')
def G(s): return str(uuid.uuid5(NS, s))

PROJ = 'IPMIndonesia2026'
PROOT = Path(__file__).resolve().parent.parent
ROOT = PROOT / 'pbip' / PROJ
KIT = PROOT / 'powerbi'
REP = ROOT / f'{PROJ}.Report'
SEM = ROOT / f'{PROJ}.SemanticModel'
DEF_R = REP / 'definition'
DEF_S = SEM / 'definition'

VC = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json'
PG = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json'

def W(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
def WJ(path, obj):
    W(path, json.dumps(obj, indent=2, ensure_ascii=False))

# ---------------------------------------------------------------- field refs
def col(e, p):  return {"Column": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}}
def mea(e, p):  return {"Measure": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}}
def agg(e, p, f=0): return {"Aggregation": {"Expression": {"SourceRef": {"Entity": e}}, "Function": f, "Property": p}}
def proj(field, e, p, native=None):
    return {"field": field, "queryRef": f"{e}.{p}", "nativeQueryRef": native or p}
def sortby(field, direction):
    return {"field": field, "direction": direction}

_fc = [0]
def catfilter(alias, e, p, values, numeric=False):
    _fc[0] += 1
    return {
        "name": f"flt{_fc[0]:014x}",
        "ordinal": _fc[0],
        "field": col(e, p),
        "type": "Categorical",
        "filter": {
            "Version": 2,
            "From": [{"Name": alias, "Entity": e, "Type": 0}],
            "Where": [{"Condition": {"In": {
                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": p}}],
                "Values": [[{"Literal": {"Value": f"'{v}'" if not numeric else f"{v}"}}] for v in values],
            }}}],
        },
        "isHiddenInViewMode": False,
        "isLockedInViewMode": False,
    }

def title_obj(text):
    return {"title": [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "text": {"expr": {"Literal": {"Value": f"'{text}'"}}},
        "bold": {"expr": {"Literal": {"Value": "true"}}},
    }}]}

def visual(name, x, y, w, h, vtype, qstate=None, title_text=None, filters=None,
           sorts=None, objects=None, z=0):
    v = {"$schema": VC, "name": name,
         "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
         "visual": {"visualType": vtype}}
    if qstate is not None:
        q = {"queryState": qstate}
        if sorts:
            q["sortDefinition"] = {"sort": sorts, "isDefaultSort": False}
        v["visual"]["query"] = q
    if objects is not None:
        v["visual"]["objects"] = objects
    if title_text:
        v["visual"]["visualContainerObjects"] = title_obj(title_text)
    if filters:
        v["filterConfig"] = {"filters": filters}
    return v

def textbox(name, x, y, w, h, text, size=14, bold=False, z=0):
    tr = {"value": text, "textStyle": {"fontFamily": "Segoe UI", "fontSize": size}}
    if bold:
        tr["textStyle"]["bold"] = True
    objects = {"general": [{"properties": {"paragraphs": [{
        "textRuns": [tr], "horizontalTextAlignment": "left"}]}}]}
    return visual(name, x, y, w, h, "textbox", objects=objects, z=z)

def slicer(name, x, y, w, h, e, p, z=0):
    return visual(name, x, y, w, h, "slicer",
                  qstate={"Values": {"projections": [proj(col(e, p), e, p)]}}, z=z)

# ------------------------------------------------------------------- TMDL
TABLES = {
    'dim_provinsi': [
        ('provinsi_id', 'int64', '0'), ('provinsi', 'string', None)],
    'dim_tahun': [
        ('tahun_id', 'int64', '0'), ('tahun', 'int64', '0'),
        ('kategori_nasional', 'string', None)],
    'fact_ipm_provinsi': [
        ('provinsi_id', 'int64', '0'), ('provinsi', 'string', None),
        ('tahun_id', 'int64', '0'), ('ipm', 'double', '0.00'),
        ('kategori', 'string', None)],
    'fact_ipm_nasional': [
        ('tahun_id', 'int64', '0'), ('ipm', 'double', '0.00'),
        ('uhh_tahun', 'double', '0.00'), ('hls_tahun', 'double', '0.00'),
        ('rls_tahun', 'double', '0.00'), ('pengeluaran_ribu_rp', 'int64', '#,##0')],
    'fact_komponen_provinsi': [
        ('provinsi_id', 'int64', '0'), ('provinsi', 'string', None),
        ('tahun_id', 'int64', '0'), ('uhh_tahun', 'double', '0.00'),
        ('hls_tahun', 'double', '0.00'), ('rls_tahun', 'double', '0.00'),
        ('pengeluaran_ribu_rp', 'int64', '#,##0'), ('ipm', 'double', '0.00'),
        ('kategori', 'string', None), ('pertumbuhan_persen', 'double', '0.00')],
}
SORTBY = {}
MTYPE = {'int64': 'Int64.Type', 'double': 'type number', 'string': 'type text', 'dateTime': 'type date'}

MEASURES = {
    'fact_ipm_provinsi': [
        ('IPM Terpilih', 'AVERAGE ( fact_ipm_provinsi[ipm] )', '0.00'),
        ('Jumlah Provinsi Sangat Tinggi', 'CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Sangat Tinggi" )', '0'),
        ('Jumlah Provinsi Sangat Tinggi 2025', 'CALCULATE ( [Jumlah Provinsi Sangat Tinggi], dim_tahun[tahun] = 2025 )', '0'),
        ('Jumlah Provinsi Tinggi 2025', 'CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Tinggi", dim_tahun[tahun] = 2025 )', '0'),
        ('Jumlah Provinsi Sedang 2025', 'CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Sedang", dim_tahun[tahun] = 2025 )', '0'),
        ('Jumlah Provinsi Rendah 2025', 'CALCULATE ( COUNTROWS ( fact_ipm_provinsi ), fact_ipm_provinsi[kategori] = "Rendah", dim_tahun[tahun] = 2025 )', '0'),
        ('IPM Tertinggi', 'MAX ( fact_ipm_provinsi[ipm] )', '0.00'),
        ('IPM Terendah', 'MIN ( fact_ipm_provinsi[ipm] )', '0.00'),
        ('Gap IPM', '[IPM Tertinggi] - [IPM Terendah]', '0.00'),
        ('IPM Tertinggi 2025', 'CALCULATE ( [IPM Tertinggi], dim_tahun[tahun] = 2025 )', '0.00'),
        ('Gap IPM 2025', 'CALCULATE ( [Gap IPM], dim_tahun[tahun] = 2025 )', '0.00'),
    ],
    'fact_ipm_nasional': [
        ('IPM Nasional', 'AVERAGE ( fact_ipm_nasional[ipm] )', '0.00'),
        ('IPM Nasional 2025', 'CALCULATE ( [IPM Nasional], dim_tahun[tahun] = 2025 )', '0.00'),
        ('IPM Nasional 2020', 'CALCULATE ( [IPM Nasional], dim_tahun[tahun] = 2020 )', '0.00'),
        ('Kenaikan IPM 2020 ke 2025', '[IPM Nasional 2025] - [IPM Nasional 2020]', '0.00'),
    ],
    'fact_komponen_provinsi': [
        ('Rata-rata UHH', 'AVERAGE ( fact_komponen_provinsi[uhh_tahun] )', '0.00'),
        ('Rata-rata RLS', 'AVERAGE ( fact_komponen_provinsi[rls_tahun] )', '0.00'),
        ('Rata-rata HLS', 'AVERAGE ( fact_komponen_provinsi[hls_tahun] )', '0.00'),
        ('Rata-rata Pengeluaran', 'AVERAGE ( fact_komponen_provinsi[pengeluaran_ribu_rp] )', '#,##0'),
    ],
}

RELATIONSHIPS = [
    ('fact_ipm_provinsi', 'provinsi_id', 'dim_provinsi', 'provinsi_id'),
    ('fact_ipm_provinsi', 'tahun_id', 'dim_tahun', 'tahun_id'),
    ('fact_ipm_nasional', 'tahun_id', 'dim_tahun', 'tahun_id'),
    ('fact_komponen_provinsi', 'provinsi_id', 'dim_provinsi', 'provinsi_id'),
    ('fact_komponen_provinsi', 'tahun_id', 'dim_tahun', 'tahun_id'),
]

def table_tmdl(name):
    cols = TABLES[name]
    out = [f'table {name}', f'\tlineageTag: {G("tab-" + name)}', '']
    for mname, dax, fmt in MEASURES.get(name, []):
        if '\n' in dax:
            body = '\n'.join('\t\t\t' + ln for ln in dax.split('\n'))
            out.append(f"\tmeasure '{mname}' = ```")
            out.append(body)
            out.append('\t\t\t```')
        else:
            out.append(f"\tmeasure '{mname}' =")
            out.append(f'\t\t\t{dax}')
        out.append(f'\t\tformatString: {fmt}')
        out.append(f'\t\tlineageTag: {G("mea-" + name + "-" + mname)}')
        out.append('')
    for cname, dtype, fmt in cols:
        out.append(f'\tcolumn {cname}')
        out.append(f'\t\tdataType: {dtype}')
        if fmt:
            out.append(f'\t\tformatString: {fmt}')
        out.append(f'\t\tlineageTag: {G("col-" + name + "-" + cname)}')
        if (name, cname) in SORTBY:
            out.append(f'\t\tsortByColumn: {SORTBY[(name, cname)]}')
        out.append('\t\tsummarizeBy: none')
        out.append(f'\t\tsourceColumn: {cname}')
        out.append('')
    pairs = ', '.join(f'{{"{c}", {MTYPE[t]}}}' for c, t, _ in cols)
    out.append(f'\tpartition {name} = m')
    out.append('\t\tmode: import')
    out.append('\t\tsource = ```')
    out.append('\t\t\t\tlet')
    out.append(f'\t\t\t\t\tSource = Csv.Document(File.Contents(FolderData & "\\{name}.csv"), [Delimiter = ",", Columns = {len(cols)}, Encoding = 65001, QuoteStyle = QuoteStyle.None]),')
    out.append('\t\t\t\t\tPromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),')
    out.append(f'\t\t\t\t\tChangedType = Table.TransformColumnTypes(PromotedHeaders, {{{pairs}}})')
    out.append('\t\t\t\tin')
    out.append('\t\t\t\t\tChangedType')
    out.append('\t\t\t\t```')
    return '\n'.join(out) + '\n'

def build_model():
    WJ(SEM / '.platform', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/platformProperties/1.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": PROJ},
        "config": {"version": "2.0", "logicalId": G('platform-sem')}})
    WJ(SEM / 'definition.pbism', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/2.0.0/schema.json",
        "version": "4.0", "settings": {}})
    W(DEF_S / 'database.tmdl', 'database\n\tcompatibilityLevel: 1600\n')
    refs = '\n'.join(f'ref table {t}' for t in TABLES)
    W(DEF_S / 'model.tmdl',
      f'model Model\n\tculture: en-US\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\n{refs}\n\nref expression FolderData\n')
    W(DEF_S / 'expressions.tmdl',
      'expression FolderData = ```\n'
      '\t\t"C:\\\\PowerBI\\\\IPM\\\\data" meta [IsParameterQuery = true, IsParameterQueryRequired = true, Type = "Text"]\n'
      '\t\t```\n'
      f'\tlineageTag: {G("expr-FolderData")}\n')
    rel = []
    for i, (ft, fc, tt, tc) in enumerate(RELATIONSHIPS):
        rel.append(f'relationship {G("rel-" + str(i))}')
        rel.append(f'\tfromColumn: {ft}.{fc}')
        rel.append(f'\ttoColumn: {tt}.{tc}')
        rel.append('\tcrossFilteringBehavior: oneDirection')
        rel.append('')
    W(DEF_S / 'relationships.tmdl', '\n'.join(rel))
    for t in TABLES:
        W(DEF_S / 'tables' / f'{t}.tmdl', table_tmdl(t))
    nodes = []
    for i, t in enumerate(TABLES):
        nodes.append({"location": {"x": (i % 3) * 300, "y": (i // 3) * 260},
                      "nodeIndex": t, "nodeLineageTag": G('tab-' + t),
                      "size": {"height": 200, "width": 234}, "zIndex": i})
    WJ(SEM / 'diagramLayout.json', {
        "version": "1.1.0",
        "diagrams": [{"ordinal": 0, "scrollPosition": {"x": 0, "y": 0}, "nodes": nodes,
                      "name": "All tables", "zoomValue": 100, "pinKeyFields": [],
                      "showExtraHeaderInfo": False, "hideKeyFieldsWhenCollapsed": False}],
        "selectedDiagram": "All tables", "defaultDiagram": "All tables"})

# ------------------------------------------------------------------ report
F_PROV = 'fact_ipm_provinsi'; F_NAS = 'fact_ipm_nasional'; F_KOMP = 'fact_komponen_provinsi'
D_PROV = 'dim_provinsi'; D_THN = 'dim_tahun'
Y2025 = lambda a='dt': catfilter(a, D_THN, 'tahun', [2025], numeric=True)

def build_report():
    WJ(REP / '.platform', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/platformProperties/1.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": PROJ},
        "config": {"version": "2.0", "logicalId": G('platform-rep')}})
    WJ(REP / 'definition.pbir', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{PROJ}.SemanticModel"}}})
    WJ(DEF_R / 'version.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "1.0.0"})
    WJ(DEF_R / 'report.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
        "themeCollection": {"baseTheme": {"name": "CY24SU10", "reportVersionAtImport": "5.60", "type": "SharedResources"}}})
    WJ(REP / 'StaticResources' / 'SharedResources' / 'BaseThemes' / 'CY24SU10.json', {
        "name": "CY24SU10",
        "dataColors": ["#2F5D8A", "#7FB0D9", "#D96C8A", "#8A7F76", "#2E2A26", "#5B84A6",
                       "#744EC2", "#D64550", "#197278", "#1AAB40", "#15C6F4", "#4092FF",
                       "#FF9B85", "#FFC36D", "#A0D8EF", "#5E4B8B"],
        "background": "#FAF6EF", "foreground": "#2E2A26", "tableAccent": "#2F5D8A"})

    pages = {}

    # ---- Page 1: Ringkasan Nasional
    p1 = []
    p1.append(textbox('v01Title', 0, 0, 900, 60, 'IPM Indonesia 2026: Ringkasan Nasional', 20, bold=True, z=0))
    p1.append(slicer('v02SlicerTahun', 930, 8, 330, 52, D_THN, 'tahun', z=1))
    cards = [(F_NAS, 'IPM Nasional 2025', 'IPM Nasional 2025'),
             (F_PROV, 'IPM Tertinggi 2025', 'IPM Tertinggi 2025 (DKI Jakarta)'),
             (F_PROV, 'Gap IPM 2025', 'Gap IPM 2025 (poin)'),
             (F_PROV, 'Jumlah Provinsi Sangat Tinggi 2025', 'Provinsi Sangat Tinggi 2025')]
    for i, (ent, m, t) in enumerate(cards):
        p1.append(visual(f'v{3+i:02d}Card', i * 320, 76, 300, 110, 'card',
                         qstate={"Values": {"projections": [proj(mea(ent, m), ent, m)]}},
                         title_text=t, z=2 + i))
    p1.append(visual('v07LineNasional', 0, 200, 620, 250, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(D_THN, 'tahun'), D_THN, 'tahun')]},
                             "Y": {"projections": [proj(mea(F_NAS, 'IPM Nasional'), F_NAS, 'IPM Nasional')]}},
                     title_text='IPM Nasional per Tahun, 2020 sampai 2025', z=6))
    p1.append(visual('v08BarTopProv', 640, 200, 620, 250, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi')]},
                             "Y": {"projections": [proj(mea(F_PROV, 'IPM Terpilih'), F_PROV, 'IPM Terpilih')]}},
                     title_text='IPM per Provinsi, 2025 (DKI Jakarta 85,05)',
                     filters=[Y2025()],
                     sorts=[sortby(mea(F_PROV, 'IPM Terpilih'), 'Descending')], z=7))
    p1.append(textbox('v09Metode', 0, 466, 1260, 60,
                      'Sumber: BPS, Publikasi IPM 2025 dan BRS IPM 2025 tanggal 5 November 2025. Seri nasional 2020 sampai 2025, seri provinsi 2022 sampai 2025 untuk 38 provinsi.', 12, z=8))
    pages['pg01Ringkasan'] = ('Ringkasan Nasional', p1)

    # ---- Page 2: Peringkat Provinsi
    p2 = []
    p2.append(textbox('v01Title', 0, 0, 640, 60, 'Peringkat Provinsi: Jurang 30,14 Poin di Satu Negara', 20, bold=True, z=0))
    p2.append(slicer('v02SlicerTahun', 660, 8, 290, 52, D_THN, 'tahun', z=1))
    p2.append(slicer('v03SlicerKategori', 970, 8, 290, 52, F_PROV, 'kategori', z=2))
    p2.append(visual('v04BarIPMProv', 0, 76, 620, 584, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi')]},
                             "Y": {"projections": [proj(mea(F_PROV, 'IPM Terpilih'), F_PROV, 'IPM Terpilih')]}},
                     title_text='IPM per Provinsi, 2025',
                     filters=[Y2025()],
                     sorts=[sortby(mea(F_PROV, 'IPM Terpilih'), 'Descending')], z=3))
    p2.append(visual('v05TableProv', 640, 76, 620, 360, 'tableEx',
                     qstate={"Values": {"projections": [
                         proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi'),
                         proj(mea(F_PROV, 'IPM Terpilih'), F_PROV, 'IPM Terpilih'),
                         proj(col(F_PROV, 'kategori'), F_PROV, 'kategori')]}},
                     title_text='Rincian Provinsi, 2025',
                     filters=[Y2025()],
                     sorts=[sortby(mea(F_PROV, 'IPM Terpilih'), 'Descending')], z=4))
    cards2 = [(F_PROV, 'Jumlah Provinsi Sangat Tinggi 2025', 'Sangat Tinggi 2025'),
              (F_PROV, 'Jumlah Provinsi Tinggi 2025', 'Tinggi 2025'),
              (F_PROV, 'Jumlah Provinsi Sedang 2025', 'Sedang 2025'),
              (F_PROV, 'Jumlah Provinsi Rendah 2025', 'Rendah 2025')]
    for i, (ent, m, t) in enumerate(cards2):
        p2.append(visual(f'v{6+i:02d}CardKat', 640 + (i % 2) * 320, 452 + (i // 2) * 104, 300, 92, 'card',
                         qstate={"Values": {"projections": [proj(mea(ent, m), ent, m)]}},
                         title_text=t, z=5 + i))
    pages['pg02Peringkat'] = ('Peringkat Provinsi', p2)

    # ---- Page 3: Komponen
    p3 = []
    p3.append(textbox('v01Title', 0, 0, 900, 60, 'Komponen IPM per Provinsi, 2025', 20, bold=True, z=0))
    p3.append(slicer('v02SlicerProvinsi', 930, 8, 330, 52, D_PROV, 'provinsi', z=1))
    cards3 = [(F_KOMP, 'Rata-rata UHH', 'Rata-rata UHH (tahun)'),
              (F_KOMP, 'Rata-rata HLS', 'Rata-rata HLS (tahun)'),
              (F_KOMP, 'Rata-rata RLS', 'Rata-rata RLS (tahun)'),
              (F_KOMP, 'Rata-rata Pengeluaran', 'Rata-rata Pengeluaran (ribu Rp)')]
    for i, (ent, m, t) in enumerate(cards3):
        p3.append(visual(f'v{3+i:02d}Card', i * 320, 76, 300, 110, 'card',
                         qstate={"Values": {"projections": [proj(mea(ent, m), ent, m)]}},
                         title_text=t, z=2 + i))
    p3.append(visual('v07BarUHH', 0, 200, 620, 220, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi')]},
                             "Y": {"projections": [proj(agg(F_KOMP, 'uhh_tahun', 1), F_KOMP, 'uhh_tahun', 'Average of uhh_tahun')]}},
                     title_text='Umur Harapan Hidup per Provinsi, 2025 (tahun)',
                     sorts=[sortby(agg(F_KOMP, 'uhh_tahun', 1), 'Descending')], z=6))
    p3.append(visual('v08BarRLS', 640, 200, 620, 220, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi')]},
                             "Y": {"projections": [proj(agg(F_KOMP, 'rls_tahun', 1), F_KOMP, 'rls_tahun', 'Average of rls_tahun')]}},
                     title_text='Rata-rata Lama Sekolah per Provinsi, 2025 (tahun)',
                     sorts=[sortby(agg(F_KOMP, 'rls_tahun', 1), 'Descending')], z=7))
    p3.append(visual('v09TableKomp', 0, 436, 1260, 224, 'tableEx',
                     qstate={"Values": {"projections": [
                         proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi'),
                         proj(agg(F_KOMP, 'uhh_tahun', 1), F_KOMP, 'uhh_tahun', 'Average of uhh_tahun'),
                         proj(agg(F_KOMP, 'hls_tahun', 1), F_KOMP, 'hls_tahun', 'Average of hls_tahun'),
                         proj(agg(F_KOMP, 'rls_tahun', 1), F_KOMP, 'rls_tahun', 'Average of rls_tahun'),
                         proj(agg(F_KOMP, 'pengeluaran_ribu_rp', 1), F_KOMP, 'pengeluaran_ribu_rp', 'Average of pengeluaran_ribu_rp'),
                         proj(mea(F_PROV, 'IPM Terpilih'), F_PROV, 'IPM Terpilih'),
                         proj(agg(F_KOMP, 'pertumbuhan_persen', 1), F_KOMP, 'pertumbuhan_persen', 'Average of pertumbuhan_persen')]}},

                     title_text='Tabel Komponen Lengkap 38 Provinsi, 2025',
                     filters=[Y2025('dt3')],
                     sorts=[sortby(mea(F_PROV, 'IPM Terpilih'), 'Descending')], z=8))
    pages['pg03Komponen'] = ('Komponen', p3)

    # ---- Page 4: Tren dan Konvergensi
    p4 = []
    p4.append(textbox('v01Title', 0, 0, 900, 60, 'Tren dan Konvergensi: Naik Bersama, Jarak Bertahan', 20, bold=True, z=0))
    p4.append(slicer('v02SlicerTahun', 930, 8, 330, 52, D_THN, 'tahun', z=1))
    p4.append(visual('v03LineProv', 0, 76, 620, 280, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(D_THN, 'tahun'), D_THN, 'tahun')]},
                             "Y": {"projections": [proj(mea(F_PROV, 'IPM Terpilih'), F_PROV, 'IPM Terpilih')]}},
                     title_text='Rata-rata IPM Provinsi per Tahun, 2022 sampai 2025', z=2))
    p4.append(visual('v04LineNas', 640, 76, 620, 280, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(D_THN, 'tahun'), D_THN, 'tahun')]},
                             "Y": {"projections": [proj(mea(F_NAS, 'IPM Nasional'), F_NAS, 'IPM Nasional')]}},
                     title_text='IPM Nasional per Tahun, 2020 sampai 2025', z=3))
    p4.append(visual('v05ColGap', 0, 372, 620, 220, 'clusteredColumnChart',
                     qstate={"Category": {"projections": [proj(col(D_THN, 'tahun'), D_THN, 'tahun')]},
                             "Y": {"projections": [proj(mea(F_PROV, 'Gap IPM'), F_PROV, 'Gap IPM')]}},
                     title_text='Gap IPM Antarprovinsi per Tahun (poin)', z=4))
    p4.append(visual('v06CardKenaikan', 640, 372, 300, 110, 'card',
                     qstate={"Values": {"projections": [proj(mea(F_NAS, 'Kenaikan IPM 2020 ke 2025'), F_NAS, 'Kenaikan IPM 2020 ke 2025')]}},
                     title_text='Kenaikan IPM 2020 ke 2025 (poin)', z=5))
    p4.append(visual('v07CardGap25', 960, 372, 300, 110, 'card',
                     qstate={"Values": {"projections": [proj(mea(F_PROV, 'Gap IPM 2025'), F_PROV, 'Gap IPM 2025')]}},
                     title_text='Gap IPM 2025 (poin)', z=6))
    p4.append(textbox('v08Catatan', 640, 498, 620, 94,
                      'Gap antarprovinsi sebesar 30,08 poin pada 2022 dan 30,14 poin pada 2025. Semua provinsi naik, tetapi disparitas belum menyempit.', 13, z=7))
    p4.append(textbox('v09Catatan2', 0, 608, 1260, 52,
                      'Catatan: seri provinsi dimulai 2022 karena pemekaran Papua. Seri nasional memakai metode baru BPS mulai 2020.', 12, z=8))
    pages['pg04TrenKonvergensi'] = ('Tren & Konvergensi', p4)

    order = list(pages)
    for pname, (disp, visuals) in pages.items():
        WJ(DEF_R / 'pages' / pname / 'page.json', {
            "$schema": PG, "name": pname, "displayName": disp,
            "displayOption": "FitToPage", "height": 720, "width": 1280})
        for v in visuals:
            WJ(DEF_R / 'pages' / pname / 'visuals' / v['name'] / 'visual.json', v)
    WJ(DEF_R / 'pages' / 'pages.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": order, "activePageName": order[0]})

README = """LANGKAH MEMBUKA PAKET PBIP: IPM Indonesia 2026
====================================================================

1. Ekstrak file ZIP ini ke folder lokal (mis. C:\\PowerBI\\IPM).
2. Buka file IPMIndonesia2026.pbip dengan Power BI Desktop.
3. Saat diminta parameter, klik Edit Parameters atau Transform Data,
   lalu arahkan FolderData ke folder "data" di dalam hasil ekstrak
   (folder berisi 5 file CSV kit).
4. Klik Refresh agar seluruh tabel termuat.
5. Cek cepat angka kunci (Halaman 1: Ringkasan Nasional):
   - Kartu IPM Nasional 2025 harus menunjukkan 75,90
   - Kartu IPM Tertinggi 2025 harus menunjukkan 85,05 (DKI Jakarta)
   - Kartu Gap IPM 2025 harus menunjukkan 30,14 poin
   - Kartu Provinsi Sangat Tinggi 2025 harus menunjukkan 3 provinsi
   - Halaman 2: jumlah kategori 2025 adalah Sangat Tinggi 3, Tinggi 30,
     Sedang 4, Rendah 1 (total 38 provinsi)
   - Halaman 3: rata-rata komponen provinsi 2025 adalah UHH 73,18 tahun,
     HLS 13,26 tahun, RLS 9,03 tahun, Pengeluaran 11.962 ribu Rp
6. Jika semua cocok, Save As menjadi IPM-Indonesia-2026.pbix.

Catatan sentuhan pertama (wajar terjadi):
- Slicer tahun mungkin tampil sebagai daftar (list), bukan slider.
  Itu normal untuk data tahun kategori.
- Visual peta tidak dipakai (diganti bar terurut) karena visual peta PBIR
  rawan error; peringkat provinsi tetap terbaca jelas dari bar.
- Rata-rata komponen pada Halaman 3 adalah rata-rata sederhana
  38 provinsi tahun 2025, bukan angka nasional resmi BPS. Angka nasional
  resmi 2025: UHH 74,47 tahun, HLS 13,30 tahun, RLS 9,07 tahun,
  Pengeluaran 12.802 ribu Rp.
- Seri provinsi hanya 2022 sampai 2025 karena pemekaran Papua; jangan
  mencari provinsi hasil pemekaran pada tahun sebelum 2022.
"""

# --------------------------------------------------------------------- main
def main():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    (ROOT / 'data').mkdir(parents=True)
    for f in sorted(KIT.glob('*.csv')):
        shutil.copy(f, ROOT / 'data' / f.name)
    WJ(ROOT / f'{PROJ}.pbip', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [{"report": {"path": f"{PROJ}.Report"}}],
        "settings": {"enableAutoRecovery": True}})
    W(ROOT / '.gitignore', '**/.pbi/localSettings.json\n**/.pbi/cache.abf\n')
    W(ROOT / 'README-LANGKAH.txt', README)
    build_model()
    build_report()
    dst = Path.home() / 'workspace' / 'pbip' / PROJ
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ROOT, dst)
    print('built', ROOT, '+ copy at', dst)

if __name__ == '__main__':
    main()
