import os
import sys
sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)
import json

from google.cloud import bigquery

# Credenciales: Application Default Credentials (gcloud auth application-default login)
PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
TABLE_ID = f'{PROJECT}.post_cronos.encuestas'
# data.local.js esta en .gitignore: los datos reales de menores nunca se commitean
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data.local.js')

bq = bigquery.Client(project=PROJECT)

rows = bq.query(f'''
    SELECT id_encuesta, edad, genero, colegio, ciudad_barrio, eje,
           url_imagen_dibujo, descripcion_audio_o_ia, descripcion_final_texto
    FROM `{TABLE_ID}`
    ORDER BY id_encuesta
''').result()

data = []
for r in rows:
    data.append({
        'id': r.id_encuesta,
        'edad': r.edad,
        'genero': r.genero,
        'ciudad_barrio': r.ciudad_barrio,
        'colegio': r.colegio,
        'eje': r.eje,
        'img': r.url_imagen_dibujo,
        'interp': r.descripcion_audio_o_ia,
        'diseno': r.descripcion_final_texto,
    })

js = '// GENERADO AUTOMATICAMENTE por generate_data.py\n'
js += '// Ejecutar: python scripts/generate_data.py\n'
js += 'window.DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n'

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(js)

print(f'OK - {len(data)} registros escritos en {OUTPUT}')
