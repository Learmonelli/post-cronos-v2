"""Genera datos 100% sinteticos para la demo publica (sin menores ni dibujos reales).

Salida:
  data.sample.js      -> window.DATA (mismo esquema que generate_data.py)
  resumen.sample.js   -> window.RESUMEN (mismo esquema que analisis_tendencias.py)
  sample/dibujo_XX.svg -> ilustraciones abstractas generadas por codigo

Uso: python scripts/make_sample_data.py
"""
import json
import os
import random

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SAMPLE_DIR = os.path.join(ROOT, 'sample')
os.makedirs(SAMPLE_DIR, exist_ok=True)

rnd = random.Random(2060)  # semilla fija: salida reproducible

COLEGIOS = ['Colegio Ejemplo A', 'Colegio Ejemplo B', 'Colegio Ejemplo C']
BARRIOS = ['Barrio Centro', 'Barrio Norte', 'Barrio Sur', 'Barrio Oeste']
GENEROS = ['Femenino', 'Masculino', 'No binario', 'No responder']
EJES = ['Tecnologia', 'Mobiliario', 'Moda', 'Educacion', 'Salud', 'Comunicacion', 'Herramientas']

TEXTOS = {
    'Tecnologia': ('Una ciudad con edificios cubiertos de paneles solares y drones que reparten alimentos.',
                   'Calles con energia limpia y transporte autonomo.'),
    'Mobiliario': ('Bancos que se transforman en refugios y plazas con sombra automatica.',
                   'Muebles urbanos que se adaptan al clima.'),
    'Moda': ('Ropa que cambia de color segun la temperatura y se fabrica con material reciclado.',
             'Indumentaria sustentable para todas las edades.'),
    'Educacion': ('Escuelas al aire libre con aulas conectadas a bosques urbanos.',
                  'Aprender explorando la ciudad.'),
    'Salud': ('Parques con estaciones de chequeo medico gratuitas y huertas comunitarias.',
              'Una ciudad que cuida a su gente.'),
    'Comunicacion': ('Pantallas en las plazas donde los vecinos comparten ideas en tiempo real.',
                     'Ciudad conectada y participativa.'),
    'Herramientas': ('Talleres abiertos donde se reparan objetos en lugar de tirarlos.',
                     'Cultura de reparar y reutilizar.'),
}

PALETAS = [
    ('#1b2a49', '#f2c14e', '#6fb1a0'),
    ('#2d1b4e', '#ff8a5b', '#8be0c6'),
    ('#0f3d3e', '#f7d488', '#e07a5f'),
    ('#3a1c3f', '#9ad1d4', '#f4a259'),
]


def svg(idx, ejes):
    """Dibujo abstracto: cielo, sol/luna, edificios y arboles con formas aleatorias."""
    bg, accent, green = PALETAS[idx % len(PALETAS)]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 520" role="img" '
             f'aria-label="Ilustracion abstracta de ejemplo {idx + 1}">',
             f'<rect width="400" height="520" fill="{bg}"/>',
             f'<circle cx="{rnd.randint(70, 330)}" cy="{rnd.randint(60, 120)}" r="{rnd.randint(28, 44)}" fill="{accent}" opacity="0.9"/>']
    x = 10
    while x < 380:
        w, h = rnd.randint(36, 70), rnd.randint(120, 300)
        parts.append(f'<rect x="{x}" y="{520 - h - 60}" width="{w}" height="{h}" rx="6" fill="{accent}" opacity="0.{rnd.randint(35, 70)}"/>')
        for wy in range(520 - h - 40, 440, 28):
            parts.append(f'<rect x="{x + 8}" y="{wy}" width="{max(w - 16, 6)}" height="8" rx="2" fill="{bg}" opacity="0.7"/>')
        x += w + rnd.randint(4, 14)
    parts.append(f'<rect y="460" width="400" height="60" fill="{green}"/>')
    for tx in range(20, 400, rnd.randint(55, 80)):
        parts.append(f'<circle cx="{tx}" cy="{450}" r="{rnd.randint(14, 22)}" fill="{green}" stroke="{bg}" stroke-width="3"/>')
    parts.append(f'<text x="200" y="505" text-anchor="middle" font-family="sans-serif" font-size="14" fill="{bg}">'
                 f'Ilustracion de ejemplo · {" + ".join(ejes)}</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


data = []
for i in range(12):
    ejes = rnd.sample(EJES, rnd.choice([1, 1, 2]))
    interp_base, diseno_base = TEXTOS[ejes[0]]
    fname = f'dibujo_{i + 1:02d}.svg'
    with open(os.path.join(SAMPLE_DIR, fname), 'w', encoding='utf-8') as f:
        f.write(svg(i, ejes))
    data.append({
        'id': f'ejemplo_{i + 1:03d}',
        'edad': rnd.randint(9, 17),
        'genero': rnd.choice(GENEROS),
        'ciudad_barrio': rnd.choice(BARRIOS),
        'colegio': rnd.choice(COLEGIOS),
        'eje': ', '.join(ejes),
        'img': f'sample/{fname}',
        'interp': f'[Dato de ejemplo] {interp_base}',
        'diseno': f'[Dato de ejemplo] {diseno_base}',
    })

with open(os.path.join(ROOT, 'data.sample.js'), 'w', encoding='utf-8') as f:
    f.write('// DATOS SINTETICOS DE DEMO (generados por scripts/make_sample_data.py)\n')
    f.write('// No contienen personas, colegios ni dibujos reales.\n')
    f.write('window.DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')

resumen = {
    'resumen_general': '[Ejemplo sintetico] En los datos de demo predominan visiones de una ciudad tecnologica '
                       'pero integrada con la naturaleza, con foco en sostenibilidad y participacion vecinal.',
    'tendencias': [
        {'tema': 'Tecnologia y naturaleza', 'detalle': 'Los dibujos de ejemplo combinan paneles solares, '
         'arboles y transporte autonomo.', 'ejemplos': [d['id'] for d in data[:2]]},
        {'tema': 'Espacios comunitarios', 'detalle': 'Plazas, talleres y escuelas abiertas aparecen como '
         'lugares de encuentro.', 'ejemplos': [d['id'] for d in data[2:4]]},
    ],
    'insight_por_eje': {e: f'[Ejemplo] Observacion ficticia sobre {e}.' for e in EJES},
    'recomendaciones': ['[Ejemplo] Sumar mas colegios y tandas de encuestas.',
                        '[Ejemplo] Cruzar ejes tematicos con rangos de edad.'],
}
with open(os.path.join(ROOT, 'resumen.sample.js'), 'w', encoding='utf-8') as f:
    f.write('// RESUMEN SINTETICO DE DEMO (formato igual a analisis_tendencias.py)\n')
    f.write('window.RESUMEN = ' + json.dumps(resumen, ensure_ascii=False, indent=2) + ';\n')

print(f'OK - {len(data)} registros sinteticos y {len(data)} SVG en {SAMPLE_DIR}')
