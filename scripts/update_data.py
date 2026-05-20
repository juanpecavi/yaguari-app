import requests
import json
import re
from datetime import datetime

BASE_URL = 'https://ligauniversitaria.org.uy/detallefechas/api.php'
HEADERS = {
    'Referer': 'https://ligauniversitaria.org.uy/detallefechas/',
    'User-Agent': 'Mozilla/5.0'
}

# Temporada activa actual - actualizar al inicio de cada año
ACTIVE_SEASONS = [
    {'t': '113', 'serie': 'DIVISIONAL "D"', 'serie2': None},
]

def fetch(url, params=None):
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=15)
        return r.json()
    except Exception as e:
        print(f"  Error: {e}")
        return []

def get_partidos(t, serie):
    fechas = fetch(BASE_URL, {
        'action': 'cargarFechas', 'temporada': t,
        'deporte': 'FÚTBOL', 'torneo': 'Mayores Masculino', 'serie': serie
    })
    partidos = []
    for f in fechas:
        ps = fetch(BASE_URL, {
            'action': 'cargarPartidos', 'temporada': t,
            'deporte': 'FÚTBOL', 'torneo': 'Mayores Masculino',
            'serie': serie, 'fecha': f.get('fecha','')
        })
        yag = [p for p in ps if 'YAGUARI' in (p.get('Locatario','')+p.get('Visitante',''))]
        for p in yag:
            p['_fecha'] = f.get('fecha','')
        partidos.extend(yag)
    return partidos

def main():
    print(f"=== Actualización {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    changed = False

    for season in ACTIVE_SEASONS:
        t = season['t']
        serie = season['serie']
        print(f"\nTemporada {t} ({serie}):")

        # Fetch primera rueda
        p1_new = get_partidos(t, serie)
        print(f"  1ª rueda: {len(p1_new)} partidos")

        # Find and update P1 in HTML
        p1_match = re.search(r'const P1 = (\{.*?\});', html, re.DOTALL)
        if p1_match:
            p1 = json.loads(p1_match.group(1))
            if json.dumps(p1.get(t,[]), ensure_ascii=False) != json.dumps(p1_new, ensure_ascii=False):
                p1[t] = p1_new
                new_p1 = f'const P1 = {json.dumps(p1, ensure_ascii=True, separators=(",",":"))};'
                html = html.replace(p1_match.group(0), new_p1)
                print(f"  P1 actualizado")
                changed = True
            else:
                print(f"  P1 sin cambios")

        # Fetch segunda rueda si existe
        if season.get('serie2'):
            p2_new = get_partidos(t, season['serie2'])
            print(f"  2ª rueda: {len(p2_new)} partidos")
            p2_match = re.search(r'const P2 = (\{.*?\});', html, re.DOTALL)
            if p2_match:
                p2 = json.loads(p2_match.group(1))
                if json.dumps(p2.get(t,[]), ensure_ascii=False) != json.dumps(p2_new, ensure_ascii=False):
                    p2[t] = p2_new
                    new_p2 = f'const P2 = {json.dumps(p2, ensure_ascii=True, separators=(",",":"))};'
                    html = html.replace(p2_match.group(0), new_p2)
                    print(f"  P2 actualizado")
                    changed = True

    if changed:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n✓ index.html actualizado")
    else:
        print(f"\n✓ Sin cambios")

if __name__ == '__main__':
    main()
