import urllib.request
import csv

# Odkazy na tvé CSV tabulky (ujisti se, že jsou v tabulce publikované jako CSV!)
URL_DENNI = "https://docs.google.com/spreadsheets/d/e/2PACX-1vToihWTUNEtB_Weo_gKLbT0aq_JtHOYt6n5q5_DUzfc7Z5P5NFsyHjT_djPiwWMSLEFEptCNR20lWfN/pub?gid=0&single=true&output=csv"
URL_TYDENNI = "https://docs.google.com/spreadsheets/d/e/2PACX-1vToihWTUNEtB_Weo_gKLbT0aq_JtHOYt6n5q5_DUzfc7Z5P5NFsyHjT_djPiwWMSLEFEptCNR20lWfN/pub?gid=1864381089&single=true&output=csv"

def get_menu_html(url):
    try:
        response = urllib.request.urlopen(url)
        lines = response.read().decode('utf-8').splitlines()
        reader = csv.reader(lines)
        next(reader) # Přeskočit hlavičku

        items = []
        for row in reader:
            # Snížil jsem podmínku na 3 sloupce, aby to nepadalo, když zapomeneš vyplnit váhu
            if len(row) >= 3:
                items.append({
                    'kat': row[0] if len(row) > 0 else "",
                    'naz': row[1] if len(row) > 1 else "",
                    'pri': row[2] if len(row) > 2 else "",
                    'vah': row[3] if len(row) > 3 else "",
                    'cen': row[4] if len(row) > 4 else ""
                })

        if not items:
            return "<p>Momentálně nemáme žádná data.</p>"

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
            if i['pri']: html += f'<span class="item-sub">{i["pri"]}</span>'
            if i['vah']: html += f'<span class="item-sub gray">{i["vah"]} g</span>'
            if i['cen']: html += f'<span class="item-price">{i["cen"]} Kč</span></div>'

        return html
    except Exception as e:
        return f"<p>Chyba při načítání dat: {e}</p>"

# Načtení dat a šablony
denni_html = get_menu_html(URL_DENNI)
tydenni_html = get_menu_html(URL_TYDENNI)

try:
    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Nahrazení značek v šabloně
    final_html = template.replace('{{DENNI_MENU}}', denni_html)
    final_html = final_html.replace('{{TYDENNI_MENU}}', tydenni_html)

    # ULOŽENÍ do index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    print("Úspěšně aktualizováno!")

except FileNotFoundError:
    print("Chyba: Soubor template.html nebyl nalezen!")
