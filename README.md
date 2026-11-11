# Post-Cronos: Córdoba 2060

Plataforma participativa donde niños y adolescentes imaginan y dibujan Córdoba en 2060. Cada ficha (dibujo + formulario escrito a mano) se escanea, se interpreta con IA generativa, se guarda en un data warehouse y se explora en un dashboard y una galería web.

> **Esta demo usa datos 100% sintéticos.** Los participantes reales son menores de edad, por eso los dibujos, nombres, colegios y barrios reales no forman parte de este repositorio. Las ilustraciones son SVG abstractos generados por código (`scripts/make_sample_data.py`).

## Arquitectura

```
Ficha escaneada (JPG)
        │
        ▼
Cloud Storage ──► Vertex AI (Gemini 2.5 Flash-Lite) ──► BigQuery (tabla `encuestas`)
   ▲                 extrae edad, género, ejes,                │
   │                 interpreta el dibujo y transcribe         ▼
Cloud Run (FastAPI)  el texto literal                generate_data.py ──► data.js
POST /api/upload                                       analisis_tendencias.py ──► resumen (Gemini)
                                                                │
                                                                ▼
                                              index.html (GitHub Pages): dashboard + galería
```

| Capa | Tecnología |
|---|---|
| Almacenamiento de imágenes | Google Cloud Storage |
| Extracción y análisis con IA | Vertex AI, Gemini 2.5 Flash-Lite (visión + JSON estructurado) |
| Data warehouse | BigQuery |
| API de subida | FastAPI en Cloud Run (validación JPG ≤ 10 MB, rate limit por IP, concurrencia limitada) |
| Frontend | HTML/CSS/JS estático, Chart.js |

## Estructura

```
index.html                  Dashboard (gráficos, tendencias IA) + galería con filtros
data.sample.js              Datos sintéticos de demo
resumen.sample.js           Resumen de tendencias sintético
sample/                     Ilustraciones SVG de ejemplo
backend/                    API FastAPI + Dockerfile + deploy.ps1 (Cloud Run)
scripts/
  process_with_gemini.py    Lote: imágenes en GCS -> Gemini -> BigQuery
  generate_data.py          BigQuery -> data.local.js
  analisis_tendencias.py    BigQuery -> Gemini -> resumen.local.js
  make_sample_data.py       Regenera los datos sintéticos
esquema_encuesta.json       Esquema de una encuesta
```

## Probar la demo

```bash
python -m http.server 8000 --bind 127.0.0.1
# abrir http://127.0.0.1:8000
```

## Usarlo con datos propios

Los scripts leen la configuración del entorno y usan Application Default Credentials. No hay claves en el repo.

```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT=<tu-proyecto>
export BUCKET=<tu-bucket>

python scripts/process_with_gemini.py     # procesa una carpeta de fichas
python scripts/generate_data.py           # escribe data.local.js
python scripts/analisis_tendencias.py     # escribe resumen.local.js
```

`data.local.js` y `resumen.local.js` reemplazan a los archivos `sample` en el navegador y están en `.gitignore`, para que datos reales no se commiteen por accidente.

### Backend de subida

```powershell
cd backend
./deploy.ps1 -ProjectId <tu-proyecto> -AllowedOrigins "https://<tu-usuario>.github.io"
```

Endpoints: `GET /health`, `GET /api/data`, `GET /api/img/{path}`, `POST /api/upload`. En el frontend se configura con `window.POST_CRONOS_API`.

## Decisiones de diseño

- **Transcripción literal.** El prompt exige copiar palabra por palabra lo que escribió cada participante; la interpretación de la IA va en un campo aparte.
- **Género y ejes por marca física.** Gemini lee las casillas tildadas del formulario en lugar de inferir por nombre o dibujo.
- **Privacidad por defecto.** Datos reales en archivos `*.local.js` ignorados por git, y CORS restringible por variable de entorno.

## Autor

Leandro Armonelli Fiedler · [LinkedIn](https://linkedin.com/in/leandro-armonelli-1529a1208)
