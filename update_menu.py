import urllib.request
import csv

# Odkazy na tvé CSV tabulky
URL_DENNI = "https://docs.google.com/spreadsheets/d/e/2PACX-1vToihWTUNEtB_Weo_gKLbT0aq_JtHOYt6n5q5_DUzfc7Z5P5NFsyHjT_djPiwWMSLEFEptCNR20lWfN/pub?gid=0&single=true&output=csv"
URL_TYDENNI = "https://docs.google.com/spreadsheets/d/e/2PACX-1vToihWTUNEtB_Weo_gKLbT0aq_JtHOYt6n5q5_DUzfc7Z5P5NFsyHjT_djPiwWMSLEFEptCNR20lWfN/pub?gid=1864381089&single=true&output=csv"

def get_menu_html(url):
    response = urllib.request.urlopen(url)
    lines = response.read().decode('utf-8').splitlines()
    reader = csv.reader(lines)
    next(reader) # Přeskočit hlavičku

    items = []
    for row in reader:
        if len(row) >= 5:
            items.append({'kat': row[0], 'naz': row[1], 'pri': row[2], 'vah': row[3], 'cen': row[4]})

    # Seřadit polévky na konec
    items.sort(key=lambda x: 1 if "polé" in x['kat'].lower() else 0)

    html = ""
    current_kat = ""
    for i in items:
        if not i['naz']: continue
        if i['kat'] and i['kat'] != current_kat:
            current_kat = i['kat']
            html += f'<h2 class="category">{current_kat}</h2>'
        html += f'<div class="menu-item"><span class="item-name">{i["naz"]}</span>'
        if i['pri']: html += f'<span class="item-sub gray">{i["pri"]}</span>'
        if i['vah']: html += f'<span class="item-sub">{i["vah"]} g</span>'
        html += f'<span class="item-price">{i["cen"]} Kč</span></div>'
    return html

# Načtení dat a šablony
denni_html = get_menu_html(URL_DENNI)
tydenni_html = get_menu_html(URL_TYDENNI)

with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Výměna značek za hotové jídlo
final_html = template.replace('{{DENNI_MENU}}', denni_html).replace('{{TYDENNI_MENU}}', tydenni_html)

# Uložení jako index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
