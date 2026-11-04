# 📊 CAMPAIGN ANALYZER

**Analiza, compara y optimiza tus campañas digitales.**

Aplicación web hecha en Python con Streamlit para registrar campañas publicitarias, calcular su CTR, clasificar su rendimiento y compararlas para encontrar la mejor.

Proyecto académico para demostrar el uso de estructuras de decisión (`if`, `elif`, `else`) y de repetición (`for`, `while`) en Python.

---

## ✨ Funcionalidades

| Sección | Qué hace |
|---|---|
| 🏠 **Dashboard** | Tarjetas con el total de campañas, impresiones, clics, el CTR promedio y la mejor campaña. Muestra el resultado del análisis. |
| ➕ **Registrar campaña** | Formulario con validaciones y botón para cargar los datos de demostración. |
| 📋 **Comparador** | Tabla ordenada por CTR (de mayor a menor) y conteo por clasificación. |
| 📈 **Gráficas** | CTR por campaña, impresiones frente a clics y un ranking que resalta la campaña ganadora. |
| ⚙️ **Gestión** | Eliminar una campaña, limpiar todo y descargar los resultados en CSV. |

**Fórmula:** `CTR = (Clics / Impresiones) * 100`

**Clasificación** (criterios de referencia del ejercicio):

- 🟢 **ALTO:** CTR ≥ 3%
- 🟡 **MEDIO:** 1% ≤ CTR < 3%
- 🔴 **BAJO:** CTR < 1%

---

## 🧠 Dónde están las estructuras de control en `app.py`

| Estructura | Función o bloque | Para qué se usa |
|---|---|---|
| `if / elif / else` | `clasificar_ctr()` | Clasifica el CTR en ALTO, MEDIO o BAJO. |
| `if / elif / else` | `validar_campana()` | Valida el nombre, las impresiones y los clics. |
| `while` | `es_entero_valido()` | Revisa carácter por carácter que el texto sea un número entero. |
| `while` | `buscar_campana()` | Busca una campaña por nombre (evita duplicados y sirve para eliminar). |
| `for` | `calcular_resumen()` | Suma impresiones, clics y CTR para los indicadores. |
| `for` + `if / elif / else` | `buscar_mejores()` | Encuentra la campaña con mayor CTR y detecta los empates. |
| `for` (doble) | `ordenar_por_ctr()` | Ordena las campañas de mayor a menor CTR (método burbuja). |
| `for` | `construir_tabla()` | Arma la tabla comparativa. |

---

## 💻 Cómo ejecutarlo en tu computador

1. Instala **Python 3.10 o superior** desde <https://www.python.org/downloads/> (en Windows, marca la casilla *"Add Python to PATH"*).
2. Abre una terminal dentro de la carpeta del proyecto.
3. Instala las librerías:

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   streamlit run app.py
   ```

5. Se abrirá el navegador en `http://localhost:8501`. Para detenerla, presiona `Ctrl + C` en la terminal.

**Prueba rápida:** pulsa **"Cargar datos de demostración"**. Debes ver:

| Campaña | Impresiones | Clics | CTR | Clasificación |
|---|---|---|---|---|
| Campaña Verano | 10000 | 400 | 4.00% | ALTO |
| Campaña Primavera | 5000 | 100 | 2.00% | MEDIO |
| Campaña Invierno | 8000 | 40 | 0.50% | BAJO |

Resultado: *"La campaña con mejor rendimiento es Campaña Verano, con un CTR de 4.00%"*.

---

## 🐙 Cómo subirlo a GitHub (sin usar comandos)

1. Crea una cuenta en <https://github.com> si no tienes una.
2. Arriba a la derecha, haz clic en **+ → New repository**.
3. Ponle un nombre, por ejemplo `campaign-analyzer`, elige **Public** y haz clic en **Create repository**.
4. En la página del repositorio, haz clic en **"uploading an existing file"**.
5. Arrastra `app.py`, `requirements.txt` y `README.md`.
6. Escribe un mensaje, por ejemplo *"Primera versión"*, y haz clic en **Commit changes**.
7. *(Opcional, para el tema de colores)* Haz clic en **Add file → Create new file**, escribe como nombre `.streamlit/config.toml` (la barra crea la carpeta), pega el contenido del archivo `config.toml` y haz clic en **Commit changes**.

### Alternativa con comandos (Git)

```bash
git init
git add .
git commit -m "Primera versión de Campaign Analyzer"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/campaign-analyzer.git
git push -u origin main
```

---

## 🚀 Cómo publicarlo en Streamlit Community Cloud

1. Entra a <https://share.streamlit.io> e inicia sesión con tu cuenta de **GitHub**.
2. Autoriza a Streamlit para que pueda ver tus repositorios.
3. Haz clic en **Create app** (o **New app**) y elige la opción para desplegar desde un repositorio de GitHub.
4. Completa:
   - **Repository:** `TU_USUARIO/campaign-analyzer`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL** *(opcional)*: un nombre fácil, por ejemplo `campaign-analyzer-tunombre`
5. Haz clic en **Deploy**. La primera vez tarda uno o dos minutos mientras instala las librerías.
6. Copia el enlace (algo como `https://campaign-analyzer-tunombre.streamlit.app`) y compártelo con tu profesor.

Cada vez que actualices un archivo en GitHub, la aplicación publicada se actualiza sola.

> **Nota:** en el plan gratuito, si nadie abre la app durante varios días, se "duerme". Al abrirla aparece un botón para despertarla y tarda unos segundos en cargar. Conviene abrirla tú misma antes de enviar el enlace.

> **Nota:** los datos se guardan solo durante la sesión. Si se recarga la página, las campañas se borran (por eso existe el botón de datos de demostración).

---

## 📁 Estructura del proyecto

```
campaign-analyzer/
├── app.py                 # Código principal
├── requirements.txt       # Librerías necesarias
├── README.md              # Este archivo
└── .streamlit/
    └── config.toml        # Tema de colores (opcional)
```
