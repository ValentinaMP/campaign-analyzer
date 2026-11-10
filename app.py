# =============================================================================
#  CAMPAIGN ANALYZER  ·  versión 2.0
#  Analiza, compara y optimiza tus campañas digitales.
#
#  Proyecto académico: demuestra el uso de las estructuras de decisión
#  (if, elif, else) y de repetición (for, while) en Python.
#
#  Para ejecutar:  streamlit run app.py
# =============================================================================

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Campaign Analyzer",
    page_icon="📊",
    layout="wide",
)

# Paleta de colores de la aplicación
AZUL_OSCURO = "#0B1F4B"
AZUL_ELECTRICO = "#2F6BFF"
VIOLETA = "#7B5CFF"
CIAN = "#22C3EE"
GRIS_SUAVE = "#D5DCEA"
GRIS_TEXTO = "#6B7A99"
VERDE = "#16A34A"
AMARILLO = "#F59E0B"
ROJO = "#EF4444"

# Datos de demostración pedidos en el enunciado
DATOS_DEMO = [
    {"nombre": "Campaña Primavera", "impresiones": 5000, "clics": 100},
    {"nombre": "Campaña Verano", "impresiones": 10000, "clics": 400},
    {"nombre": "Campaña Invierno", "impresiones": 8000, "clics": 40},
]


# -----------------------------------------------------------------------------
# 2. ESTILOS VISUALES (CSS)
#    Streamlit permite agregar CSS para personalizar el diseño.
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, .stApp, .stMarkdown, p, label, input, button, textarea, h1, h2, h3, h4, .hero h1, td, th, li,
.kpi, .ganador, .campana, .caja, .tip, .tabla, .vacio, .seccion, .seccion-sub, .hero {
    font-family: 'Plus Jakarta Sans', 'Source Sans', 'Source Sans Pro', sans-serif !important;
}
.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(123,92,255,0.10) 0, transparent 35%),
        radial-gradient(circle at 100% 20%, rgba(47,107,255,0.10) 0, transparent 30%),
        #F4F6FB;
}
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1220px; }
header[data-testid="stHeader"] { background: transparent; }

/* ---------- Encabezado (hero) ---------- */
.hero {
    position: relative; overflow: hidden;
    background: linear-gradient(125deg, #0B1F4B 0%, #16307A 45%, #4B3FD8 80%, #7B5CFF 100%);
    border-radius: 28px; padding: 36px 40px 30px 40px; color: white;
    box-shadow: 0 20px 45px rgba(27, 47, 120, 0.28);
    margin-bottom: 26px;
}
.hero .burbuja { position: absolute; border-radius: 50%; filter: blur(2px); opacity: 0.55; }
.hero .b1 { width: 260px; height: 260px; right: -60px; top: -90px;
            background: radial-gradient(circle, #22C3EE 0%, transparent 70%); }
.hero .b2 { width: 200px; height: 200px; right: 180px; bottom: -110px;
            background: radial-gradient(circle, #B49CFF 0%, transparent 70%); }
.hero .pastilla {
    display: inline-block; background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.25); border-radius: 999px;
    padding: 5px 14px; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em;
}
.hero h1 {
    margin: 14px 0 4px 0; font-size: 2.7rem; font-weight: 800; color: white !important;
    letter-spacing: 0.02em; line-height: 1.1; padding: 0;
}
.hero h1 span { background: linear-gradient(90deg, #8FE9FF, #C9B8FF);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p.sub { margin: 0; font-size: 1.1rem; opacity: 0.88; }
.hero .mini { display: flex; gap: 12px; margin-top: 22px; flex-wrap: wrap; position: relative; }
.hero .mini div {
    background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.18);
    border-radius: 14px; padding: 8px 14px; font-size: 0.85rem;
}
.hero .mini b { font-size: 1rem; }

/* ---------- Tarjetas de indicadores (KPI) ---------- */
.kpi {
    background: white; border-radius: 20px; padding: 18px 18px 16px 18px;
    border: 1px solid #E6EAF3; box-shadow: 0 6px 18px rgba(11,31,75,0.06);
    height: 100%; position: relative; overflow: hidden;
}
.kpi::before {
    content: ""; position: absolute; left: 0; top: 0; right: 0; height: 4px;
    background: var(--color);
}
.kpi .icono {
    width: 42px; height: 42px; border-radius: 13px; display: flex;
    align-items: center; justify-content: center; font-size: 1.3rem;
    background: var(--fondo); margin-bottom: 12px;
}
.kpi .etiqueta { font-size: 0.74rem; font-weight: 700; color: #6B7A99;
                 text-transform: uppercase; letter-spacing: 0.06em; }
.kpi .valor { font-size: 1.75rem; font-weight: 800; color: #0B1F4B;
              margin-top: 2px; line-height: 1.2; word-break: break-word; }
.kpi .valor.pequeno { font-size: 1.12rem; padding-top: 4px; }
.kpi .detalle { font-size: 0.8rem; color: #6B7A99; margin-top: 4px; }

/* ---------- Tarjeta de la campaña ganadora ---------- */
.ganador {
    background: linear-gradient(120deg, #7B5CFF 0%, #2F6BFF 100%);
    border-radius: 24px; padding: 24px 28px; color: white;
    box-shadow: 0 16px 34px rgba(91, 80, 255, 0.30);
    display: flex; align-items: center; gap: 22px; flex-wrap: wrap;
    margin: 22px 0 8px 0;
}
.ganador .trofeo {
    font-size: 2.6rem; width: 76px; height: 76px; border-radius: 22px;
    background: rgba(255,255,255,0.18); display: flex; align-items: center; justify-content: center;
}
.ganador .texto { flex: 1; min-width: 220px; }
.ganador .titulo { font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em;
                   text-transform: uppercase; opacity: 0.85; }
.ganador .frase { font-size: 1.18rem; margin-top: 4px; line-height: 1.45; }
.ganador .frase b { font-weight: 800; }
.ganador .cifra { text-align: center; background: rgba(255,255,255,0.16);
                  border-radius: 18px; padding: 10px 20px; }
.ganador .cifra .num { font-size: 2rem; font-weight: 800; line-height: 1.1; }
.ganador .cifra .lbl { font-size: 0.75rem; opacity: 0.85; }

/* ---------- Títulos de sección ---------- */
.seccion { font-size: 1.25rem; font-weight: 800; color: #0B1F4B; margin: 26px 0 4px 0; }
.seccion-sub { font-size: 0.9rem; color: #6B7A99; margin-bottom: 14px; }

/* ---------- Tarjeta de campaña con barra de progreso ---------- */
.campana {
    background: white; border-radius: 18px; padding: 16px 20px; margin-bottom: 12px;
    border: 1px solid #E6EAF3; box-shadow: 0 4px 12px rgba(11,31,75,0.04);
}
.campana .fila { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
.campana .izq { display: flex; align-items: center; gap: 12px; }
.campana .medalla { font-size: 1.5rem; width: 40px; text-align: center; font-weight: 800; color: #6B7A99; }
.campana .nombre { font-weight: 700; color: #0B1F4B; font-size: 1.02rem; }
.campana .datos { color: #6B7A99; font-size: 0.85rem; }
.campana .der { display: flex; align-items: center; gap: 12px; }
.campana .ctr { font-weight: 800; font-size: 1.25rem; color: #0B1F4B; }
.barra { height: 9px; background: #EEF1F8; border-radius: 99px; margin-top: 12px; overflow: hidden; }
.barra div { height: 100%; border-radius: 99px; }

/* ---------- Etiquetas de clasificación ---------- */
.badge { display: inline-block; padding: 4px 12px; border-radius: 999px;
         font-size: 0.75rem; font-weight: 800; letter-spacing: 0.04em; }
.badge.alto  { background: #DCFCE7; color: #15803D; }
.badge.medio { background: #FEF3C7; color: #B45309; }
.badge.bajo  { background: #FEE2E2; color: #B91C1C; }

/* ---------- Tarjetas genéricas ---------- */
.caja {
    background: white; border-radius: 20px; padding: 20px 22px;
    border: 1px solid #E6EAF3; box-shadow: 0 6px 18px rgba(11,31,75,0.05); margin-bottom: 14px;
}
.caja h4 { margin: 0 0 10px 0; color: #0B1F4B; font-weight: 800; font-size: 1.02rem; }
.caja p, .caja li { color: #42506E; font-size: 0.92rem; line-height: 1.55; }
.formula {
    background: linear-gradient(120deg, #EEF2FF, #F3EEFF); border-radius: 14px;
    padding: 12px 16px; font-weight: 700; color: #3B2FB8; text-align: center; font-size: 1.02rem;
}
.regla { display: flex; align-items: center; gap: 10px; margin: 8px 0; color: #42506E; font-size: 0.9rem; }

/* ---------- Recomendaciones ---------- */
.tip {
    display: flex; gap: 14px; align-items: flex-start; background: white; border-radius: 16px;
    padding: 14px 18px; margin-bottom: 10px; border: 1px solid #E6EAF3; border-left: 5px solid var(--color);
}
.tip .ico { font-size: 1.4rem; }
.tip .t { font-weight: 700; color: #0B1F4B; }
.tip .d { color: #586689; font-size: 0.88rem; }

/* ---------- Tabla comparativa ---------- */
.tabla { width: 100%; border-collapse: separate; border-spacing: 0 8px; }
.tabla th { text-align: left; font-size: 0.74rem; color: #6B7A99; text-transform: uppercase;
            letter-spacing: 0.06em; padding: 0 14px; font-weight: 700; }
.tabla td { background: white; padding: 14px; color: #0B1F4B; font-size: 0.95rem;
            border-top: 1px solid #E6EAF3; border-bottom: 1px solid #E6EAF3; }
.tabla td:first-child { border-left: 1px solid #E6EAF3; border-radius: 14px 0 0 14px; font-size: 1.3rem; text-align: center; width: 56px; }
.tabla td:last-child { border-right: 1px solid #E6EAF3; border-radius: 0 14px 14px 0; }
.tabla tr.top td { background: #F5F2FF; }
.tabla th { border: none !important; background: transparent !important; }
.tabla td { border-left: none; border-right: none; }
.tabla tr { border: none !important; background: transparent !important; }
.tabla { border: none !important; }
.mini-barra { height: 7px; background: #EEF1F8; border-radius: 99px; width: 110px; display: inline-block;
              vertical-align: middle; margin-left: 8px; overflow: hidden; }
.mini-barra div { height: 100%; border-radius: 99px; }

/* ---------- Estado vacío ---------- */
.vacio { text-align: center; background: white; border: 2px dashed #D5DCEA; border-radius: 24px;
         padding: 38px 20px; margin: 10px 0 16px 0; }
.vacio .grande { font-size: 3rem; }
.vacio h3 { color: #0B1F4B; margin: 8px 0 4px 0; font-weight: 800; }
.vacio p { color: #6B7A99; margin: 0; }

/* ---------- Pestañas ---------- */
[data-testid="stTabs"] [role="tablist"] {
    gap: 6px; background: white; padding: 6px; border-radius: 16px; border: 1px solid #E6EAF3;
    box-shadow: 0 4px 12px rgba(11,31,75,0.04); margin-bottom: 8px; width: fit-content; max-width: 100%;
}
[data-testid="stTab"] {
    border-radius: 12px !important; padding: 10px 18px !important; height: auto !important;
    border-bottom: none !important;
}
[data-testid="stTab"] p { font-weight: 700 !important; font-size: 0.95rem !important; }
[data-testid="stTab"]:hover { background: #F1F4FB; }
[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(120deg, #2F6BFF, #7B5CFF) !important;
    box-shadow: 0 6px 14px rgba(79, 90, 255, 0.28);
}
[data-testid="stTab"][aria-selected="true"] p { color: white !important; }
[data-testid="stTab"]::after, [data-testid="stTab"]::before { display: none !important; }

/* ---------- Botones y formularios ---------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    border-radius: 12px; font-weight: 700; padding: 0.55rem 1.1rem;
}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"], .stFormSubmitButton > button {
    background: linear-gradient(120deg, #2F6BFF, #7B5CFF); border: none; color: white;
    box-shadow: 0 8px 18px rgba(79, 90, 255, 0.28);
}
[data-testid="stForm"] {
    background: white; border-radius: 22px; border: 1px solid #E6EAF3;
    box-shadow: 0 6px 18px rgba(11,31,75,0.05); padding: 22px;
}
[data-testid="stPlotlyChart"] {
    background: white; border-radius: 20px; border: 1px solid #E6EAF3;
    box-shadow: 0 6px 18px rgba(11,31,75,0.05); padding: 8px; overflow: hidden;
}

.pie { text-align: center; color: #8A97B5; font-size: 0.82rem; margin-top: 30px; }

/* ---------- Celulares ---------- */
@media (max-width: 640px) {
    .hero { padding: 26px 22px; border-radius: 22px; }
    .hero h1 { font-size: 1.75rem; }
    .kpi .valor { font-size: 1.4rem; }
    .ganador { padding: 20px; }
}
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 3. MEMORIA DE LA SESIÓN
#    st.session_state guarda los datos mientras la página esté abierta.
# -----------------------------------------------------------------------------
if "campanas" not in st.session_state:
    st.session_state.campanas = []

if "mensaje" not in st.session_state:
    st.session_state.mensaje = None  # Mensaje que se muestra tras una acción


# =============================================================================
# 4. FUNCIONES DE LÓGICA (aquí están if / elif / else / while / for)
# =============================================================================

def calcular_ctr(clics, impresiones):
    """Calcula el CTR con la fórmula: (Clics / Impresiones) * 100."""
    # if / else: evitamos dividir entre cero
    if impresiones > 0:
        return (clics / impresiones) * 100
    else:
        return 0.0


def clasificar_ctr(ctr):
    """Clasifica el rendimiento usando if / elif / else."""
    if ctr >= 3:
        return "ALTO"
    elif ctr >= 1:
        # Si llegamos aquí, ya sabemos que el CTR es menor que 3
        return "MEDIO"
    else:
        return "BAJO"


def es_entero_valido(texto):
    """
    Revisa, carácter por carácter, que el texto solo tenga dígitos (0-9).
    Usamos un ciclo WHILE: avanzamos mientras los caracteres sean válidos.
    """
    if texto == "":
        return False

    posicion = 0
    while posicion < len(texto):
        caracter = texto[posicion]
        if caracter not in "0123456789":
            return False  # Encontramos algo que no es un dígito
        posicion = posicion + 1

    return True


def buscar_campana(nombre):
    """
    Busca una campaña por nombre (sin importar mayúsculas).
    Devuelve su posición en la lista, o -1 si no existe.
    Usamos WHILE porque nos detenemos apenas la encontramos.
    """
    campanas = st.session_state.campanas
    indice = 0
    while indice < len(campanas):
        if campanas[indice]["nombre"].lower() == nombre.lower():
            return indice
        indice = indice + 1
    return -1


def validar_campana(nombre, impresiones_texto, clics_texto):
    """Valida los datos del formulario. Devuelve una lista de errores."""
    errores = []

    # --- Validación del nombre ---
    if nombre == "":
        errores.append("El nombre de la campaña no puede estar vacío.")
    elif buscar_campana(nombre) != -1:
        errores.append(f"Ya existe una campaña llamada «{nombre}». Usa otro nombre.")

    # --- Validación de impresiones ---
    impresiones_ok = False
    if impresiones_texto == "":
        errores.append("Debes ingresar el número de impresiones.")
    elif not es_entero_valido(impresiones_texto):
        errores.append("Las impresiones deben ser un número entero (sin puntos, decimales, letras ni signos).")
    elif int(impresiones_texto) <= 0:
        errores.append("Las impresiones deben ser mayores que cero.")
    else:
        impresiones_ok = True

    # --- Validación de clics ---
    clics_ok = False
    if clics_texto == "":
        errores.append("Debes ingresar el número de clics.")
    elif not es_entero_valido(clics_texto):
        errores.append("Los clics deben ser un número entero mayor o igual a cero (sin puntos, decimales, letras ni signos).")
    else:
        clics_ok = True

    # --- Los clics no pueden superar las impresiones ---
    if impresiones_ok and clics_ok:
        if int(clics_texto) > int(impresiones_texto):
            errores.append("Los clics no pueden ser mayores que las impresiones.")

    return errores


def crear_campana(nombre, impresiones, clics):
    """Arma el diccionario de una campaña con su CTR y clasificación."""
    ctr = calcular_ctr(clics, impresiones)
    return {
        "nombre": nombre,
        "impresiones": impresiones,
        "clics": clics,
        "ctr": ctr,
        "clasificacion": clasificar_ctr(ctr),
    }


def calcular_resumen(campanas):
    """Recorre las campañas con FOR para obtener los totales y el CTR promedio."""
    total_impresiones = 0
    total_clics = 0
    suma_ctr = 0

    for campana in campanas:
        total_impresiones = total_impresiones + campana["impresiones"]
        total_clics = total_clics + campana["clics"]
        suma_ctr = suma_ctr + campana["ctr"]

    if len(campanas) > 0:
        ctr_promedio = suma_ctr / len(campanas)
    else:
        ctr_promedio = 0.0

    return total_impresiones, total_clics, ctr_promedio


def buscar_mejores(campanas):
    """Encuentra la(s) campaña(s) con el CTR más alto, incluyendo empates."""
    mejores = []
    ctr_maximo = -1

    for campana in campanas:
        ctr = round(campana["ctr"], 2)  # Redondeamos a 2 decimales para comparar
        if ctr > ctr_maximo:
            ctr_maximo = ctr
            mejores = [campana]          # Nueva mejor campaña
        elif ctr == ctr_maximo:
            mejores.append(campana)      # Empate: la agregamos también
        else:
            pass                         # Es menor: no hacemos nada

    return mejores, ctr_maximo


def ordenar_por_ctr(campanas):
    """Ordena de mayor a menor CTR con el método de la burbuja (dos ciclos FOR)."""
    lista = campanas.copy()
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j]["ctr"] < lista[j + 1]["ctr"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def contar_clasificaciones(campanas):
    """Cuenta cuántas campañas hay de cada tipo con FOR + if / elif / else."""
    altos, medios, bajos = 0, 0, 0
    for campana in campanas:
        if campana["clasificacion"] == "ALTO":
            altos = altos + 1
        elif campana["clasificacion"] == "MEDIO":
            medios = medios + 1
        else:
            bajos = bajos + 1
    return altos, medios, bajos


def medalla(posicion):
    """Devuelve una medalla según la posición en el ranking."""
    if posicion == 1:
        return "🥇"
    elif posicion == 2:
        return "🥈"
    elif posicion == 3:
        return "🥉"
    else:
        return f"#{posicion}"


def color_clasificacion(clasificacion):
    """Devuelve el color correspondiente a cada clasificación."""
    if clasificacion == "ALTO":
        return VERDE
    elif clasificacion == "MEDIO":
        return AMARILLO
    else:
        return ROJO


def recomendacion(campana, ctr_promedio):
    """Genera un consejo para cada campaña según su clasificación."""
    diferencia = campana["ctr"] - ctr_promedio
    if diferencia >= 0:
        comparacion = f"{diferencia:.2f} puntos por encima del promedio"
    else:
        comparacion = f"{abs(diferencia):.2f} puntos por debajo del promedio"

    if campana["clasificacion"] == "ALTO":
        return "🚀", VERDE, "Excelente rendimiento", f"Está {comparacion}. Mantén la estrategia y considera aumentar su inversión."
    elif campana["clasificacion"] == "MEDIO":
        return "🛠️", AMARILLO, "Rendimiento aceptable", f"Está {comparacion}. Prueba nuevos textos, imágenes o llamados a la acción."
    else:
        return "⚠️", ROJO, "Necesita mejorar", f"Está {comparacion}. Revisa la segmentación del público y el mensaje del anuncio."


def construir_tabla(campanas):
    """Construye la tabla de datos (para el CSV) recorriendo las campañas con FOR."""
    filas = []
    posicion = 1
    for campana in ordenar_por_ctr(campanas):
        filas.append({
            "Posición": posicion,
            "Campaña": campana["nombre"],
            "Impresiones": campana["impresiones"],
            "Clics": campana["clics"],
            "CTR (%)": round(campana["ctr"], 2),
            "Clasificación": campana["clasificacion"],
        })
        posicion = posicion + 1
    return pd.DataFrame(filas)


def formato_numero(numero):
    """Escribe un número con puntos de miles, por ejemplo: 10000 -> 10.000."""
    return f"{numero:,}".replace(",", ".")


def texto_mejores(mejores, ctr_maximo):
    """Arma la frase del resultado del análisis, contemplando empates."""
    if len(mejores) == 1:
        return (
            f"La campaña con mejor rendimiento es <b>{mejores[0]['nombre']}</b>, "
            f"con un CTR de <b>{ctr_maximo:.2f}%</b>."
        )
    else:
        nombres = []
        for campana in mejores:
            nombres.append(f"<b>{campana['nombre']}</b>")
        lista_nombres = ", ".join(nombres[:-1]) + " y " + nombres[-1]
        return (
            f"Hay un empate en el mejor rendimiento: {lista_nombres}, "
            f"todas con un CTR de <b>{ctr_maximo:.2f}%</b>."
        )


def mostrar_html(codigo):
    """
    Muestra un bloque HTML. Quitamos los espacios del inicio de cada línea
    porque Markdown interpreta las líneas con sangría como código.
    """
    lineas = []
    for linea in codigo.split("\n"):
        lineas.append(linea.strip())
    st.markdown("".join(lineas), unsafe_allow_html=True)


def guardar_mensaje(tipo, texto):
    """Guarda un mensaje para mostrarlo después de recargar la página."""
    st.session_state.mensaje = (tipo, texto)


def cargar_demo():
    """Agrega las campañas de ejemplo que todavía no existan."""
    agregadas = 0
    for dato in DATOS_DEMO:
        if buscar_campana(dato["nombre"]) == -1:
            st.session_state.campanas.append(
                crear_campana(dato["nombre"], dato["impresiones"], dato["clics"])
            )
            agregadas = agregadas + 1

    if agregadas > 0:
        guardar_mensaje("exito", f"✨ Se cargaron {agregadas} campaña(s) de demostración.")
    else:
        guardar_mensaje("aviso", "Las campañas de demostración ya estaban registradas.")


def estilo_grafica(figura, titulo, alto=400):
    """Aplica el mismo estilo limpio a todas las gráficas."""
    figura.update_layout(
        title=dict(text=f"<b>{titulo}</b>", font=dict(size=16, color=AZUL_OSCURO), x=0.02),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=AZUL_OSCURO),
        margin=dict(l=20, r=20, t=64, b=20),
        height=alto,
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
        hoverlabel=dict(bgcolor="white", font_size=13),
    )
    figura.update_xaxes(showgrid=False)
    figura.update_yaxes(gridcolor="#EEF1F7", zeroline=False)
    return figura


CONFIG_GRAFICA = {"displayModeBar": False}


# --- Gráficas reutilizables --------------------------------------------------

def grafica_donut(campanas):
    """Gráfica de dona con la distribución de clasificaciones."""
    altos, medios, bajos = contar_clasificaciones(campanas)
    figura = go.Figure(
        go.Pie(
            labels=["ALTO", "MEDIO", "BAJO"],
            values=[altos, medios, bajos],
            hole=0.62,
            marker=dict(colors=[VERDE, AMARILLO, ROJO], line=dict(color="white", width=3)),
            textinfo="value",
            textfont=dict(size=15, color="white"),
            sort=False,
            hovertemplate="%{label}: %{value} campaña(s)<extra></extra>",
        )
    )
    figura.add_annotation(text=f"<b>{len(campanas)}</b><br><span style='font-size:12px'>campañas</span>",
                          showarrow=False, font=dict(size=24, color=AZUL_OSCURO))
    return estilo_grafica(figura, "Distribución del rendimiento", 340)


def grafica_velocimetro(ctr_promedio, ctr_maximo):
    """Velocímetro que muestra el CTR promedio frente a los rangos."""
    tope = max(5, ctr_maximo * 1.2)
    figura = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(ctr_promedio, 2),
            number=dict(suffix="%", font=dict(size=40, color=AZUL_OSCURO)),
            gauge=dict(
                axis=dict(range=[0, tope], ticksuffix="%", tickcolor=GRIS_TEXTO),
                bar=dict(color=AZUL_OSCURO, thickness=0.28),
                bgcolor="white",
                borderwidth=0,
                steps=[
                    dict(range=[0, 1], color="#FECACA"),
                    dict(range=[1, 3], color="#FDE68A"),
                    dict(range=[3, tope], color="#BBF7D0"),
                ],
            ),
        )
    )
    estilo_grafica(figura, "CTR promedio", 340)
    figura.update_layout(margin=dict(l=45, r=45, t=80, b=20))
    return figura


# =============================================================================
# 5. INTERFAZ DE USUARIO
# =============================================================================

campanas = st.session_state.campanas
total_impresiones, total_clics, ctr_promedio = calcular_resumen(campanas)

# --- Encabezado (hero) ---
mostrar_html(
    f"""
    <div class="hero">
        <div class="burbuja b1"></div><div class="burbuja b2"></div>
        <span class="pastilla">📊 PROYECTO ACADÉMICO · PYTHON + STREAMLIT</span>
        <h1>CAMPAIGN <span>ANALYZER</span></h1>
        <p class="sub">Analiza, compara y optimiza tus campañas digitales.</p>
        <div class="mini">
            <div>🧮 <b>CTR</b> = (Clics ÷ Impresiones) × 100</div>
            <div>📁 <b>{len(campanas)}</b> campañas en esta sesión</div>
            <div>🟢 ALTO ≥ 3% · 🟡 MEDIO 1–3% · 🔴 BAJO &lt; 1%</div>
        </div>
    </div>
    """
)

# --- Mensaje pendiente de una acción anterior ---
if st.session_state.mensaje is not None:
    tipo, texto = st.session_state.mensaje
    if tipo == "exito":
        st.success(texto)
    elif tipo == "aviso":
        st.warning(texto)
    else:
        st.info(texto)
    st.session_state.mensaje = None

# Pestañas de navegación
tab_dashboard, tab_registro, tab_comparador, tab_graficas, tab_gestion = st.tabs(
    ["🏠 Dashboard", "➕ Registrar", "📋 Comparador", "📈 Gráficas", "⚙️ Gestión"]
)


# -----------------------------------------------------------------------------
# A. DASHBOARD PRINCIPAL
# -----------------------------------------------------------------------------
with tab_dashboard:
    if len(campanas) > 0:
        mejores, ctr_maximo = buscar_mejores(campanas)
        if len(mejores) == 1:
            nombre_mejor = mejores[0]["nombre"]
        else:
            nombre_mejor = f"Empate ({len(mejores)})"
        detalle_mejor = f"CTR de {ctr_maximo:.2f}%"
    else:
        mejores, ctr_maximo = [], 0
        nombre_mejor = "—"
        detalle_mejor = "Sin datos todavía"

    # Lista de tarjetas: (ícono, color, fondo, etiqueta, valor, detalle)
    tarjetas = [
        ("📁", AZUL_ELECTRICO, "#E8EFFF", "Campañas", f"{len(campanas)}", "registradas en la sesión"),
        ("👁️", CIAN, "#E3F8FD", "Impresiones", formato_numero(total_impresiones), "veces que se vio el anuncio"),
        ("🖱️", VIOLETA, "#EFEBFF", "Clics", formato_numero(total_clics), "interacciones totales"),
        ("🎯", AMARILLO, "#FEF3C7", "CTR promedio", f"{ctr_promedio:.2f}%", "entre todas las campañas"),
        ("🏆", VERDE, "#DCFCE7", "Mejor campaña", nombre_mejor, detalle_mejor),
    ]

    columnas = st.columns(5)
    for i in range(len(tarjetas)):
        icono, color, fondo, etiqueta, valor, detalle = tarjetas[i]
        if i == 4:
            clase_valor = "valor pequeno"
        else:
            clase_valor = "valor"
        with columnas[i]:
            mostrar_html(
                f"""
                <div class="kpi" style="--color:{color}; --fondo:{fondo};">
                    <div class="icono">{icono}</div>
                    <div class="etiqueta">{etiqueta}</div>
                    <div class="{clase_valor}">{valor}</div>
                    <div class="detalle">{detalle}</div>
                </div>
                """
            )

    if len(campanas) > 0:
        # F. Resultado del análisis (tarjeta ganadora)
        mostrar_html(
            f"""
            <div class="ganador">
                <div class="trofeo">🏆</div>
                <div class="texto">
                    <div class="titulo">Resultado del análisis</div>
                    <div class="frase">{texto_mejores(mejores, ctr_maximo)}</div>
                </div>
                <div class="cifra"><div class="num">{ctr_maximo:.2f}%</div><div class="lbl">CTR más alto</div></div>
            </div>
            """
        )

        col_izq, col_der = st.columns([3, 2])

        # Ranking de campañas con barra de progreso
        with col_izq:
            mostrar_html('<div class="seccion">Ranking de campañas</div>'
                         '<div class="seccion-sub">Ordenadas de mayor a menor CTR.</div>')
            ordenadas = ordenar_por_ctr(campanas)
            posicion = 1
            for campana in ordenadas:
                clase = campana["clasificacion"].lower()
                color = color_clasificacion(campana["clasificacion"])
                if ctr_maximo > 0:
                    ancho = campana["ctr"] / ctr_maximo * 100
                else:
                    ancho = 0
                mostrar_html(
                    f"""
                    <div class="campana">
                        <div class="fila">
                            <div class="izq">
                                <div class="medalla">{medalla(posicion)}</div>
                                <div>
                                    <div class="nombre">{campana['nombre']}</div>
                                    <div class="datos">{formato_numero(campana['impresiones'])} impresiones · {formato_numero(campana['clics'])} clics</div>
                                </div>
                            </div>
                            <div class="der">
                                <span class="ctr">{campana['ctr']:.2f}%</span>
                                <span class="badge {clase}">{campana['clasificacion']}</span>
                            </div>
                        </div>
                        <div class="barra"><div style="width:{ancho:.1f}%; background:linear-gradient(90deg, {color}, {color}CC);"></div></div>
                    </div>
                    """
                )
                posicion = posicion + 1

        # Gráficas resumen
        with col_der:
            mostrar_html('<div class="seccion">Vista rápida</div>'
                         '<div class="seccion-sub">Cómo se reparte el rendimiento.</div>')
            st.plotly_chart(grafica_donut(campanas), width="stretch", config=CONFIG_GRAFICA, key="donut_dashboard")
            st.plotly_chart(grafica_velocimetro(ctr_promedio, ctr_maximo), width="stretch", config=CONFIG_GRAFICA, key="gauge_dashboard")

        # Recomendaciones automáticas
        mostrar_html('<div class="seccion">💡 Recomendaciones</div>'
                     '<div class="seccion-sub">Sugerencias automáticas según la clasificación de cada campaña.</div>')
        for campana in ordenar_por_ctr(campanas):
            icono, color, titulo, descripcion = recomendacion(campana, ctr_promedio)
            mostrar_html(
                f"""
                <div class="tip" style="--color:{color};">
                    <div class="ico">{icono}</div>
                    <div><div class="t">{campana['nombre']} · {titulo}</div><div class="d">{descripcion}</div></div>
                </div>
                """
            )
    else:
        mostrar_html(
            """
            <div class="vacio">
                <div class="grande">🚀</div>
                <h3>¡Empecemos a analizar!</h3>
                <p>Registra tu primera campaña en la pestaña <b>➕ Registrar</b> o carga los datos de ejemplo.</p>
            </div>
            """
        )
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("✨ Cargar datos de demostración", key="demo_dashboard", type="primary", width="stretch"):
                cargar_demo()
                st.rerun()


# -----------------------------------------------------------------------------
# B. REGISTRO DE CAMPAÑAS
# -----------------------------------------------------------------------------
with tab_registro:
    col_form, col_guia = st.columns([3, 2])

    with col_form:
        mostrar_html('<div class="seccion">Registrar una nueva campaña</div>'
                     '<div class="seccion-sub">Ingresa los datos y el CTR se calculará automáticamente.</div>')

        with st.form("formulario_campana", clear_on_submit=False):
            nombre = st.text_input("📝 Nombre de la campaña", placeholder="Ej: Campaña Otoño")
            col1, col2 = st.columns(2)
            impresiones_texto = col1.text_input("👁️ Número de impresiones", placeholder="Ej: 5000")
            clics_texto = col2.text_input("🖱️ Número de clics", placeholder="Ej: 120")
            enviado = st.form_submit_button("➕ Agregar campaña", width="stretch")

        if enviado:
            nombre = nombre.strip()
            impresiones_texto = impresiones_texto.strip()
            clics_texto = clics_texto.strip()

            errores = validar_campana(nombre, impresiones_texto, clics_texto)

            if len(errores) > 0:
                for error in errores:
                    st.error("⚠️ " + error)
            else:
                nueva = crear_campana(nombre, int(impresiones_texto), int(clics_texto))
                st.session_state.campanas.append(nueva)
                guardar_mensaje(
                    "exito",
                    f"✅ «{nueva['nombre']}» agregada · CTR {nueva['ctr']:.2f}% → {nueva['clasificacion']}",
                )
                st.rerun()

        st.write("")
        if st.button("✨ Cargar datos de demostración", key="demo_registro", type="primary"):
            cargar_demo()
            st.rerun()

    with col_guia:
        mostrar_html(
            """
            <div class="caja" style="margin-top:26px;">
                <h4>🧮 ¿Cómo se calcula?</h4>
                <div class="formula">CTR = (Clics ÷ Impresiones) × 100</div>
                <p style="margin-top:10px;">El CTR indica qué porcentaje de las personas que vieron el anuncio hicieron clic.</p>
            </div>
            <div class="caja">
                <h4>🏷️ Clasificación</h4>
                <div class="regla"><span class="badge alto">ALTO</span> CTR igual o mayor a 3%</div>
                <div class="regla"><span class="badge medio">MEDIO</span> CTR entre 1% y menos de 3%</div>
                <div class="regla"><span class="badge bajo">BAJO</span> CTR menor a 1%</div>
            </div>
            <div class="caja">
                <h4>✅ Reglas de validación</h4>
                <ul style="margin:0; padding-left:18px;">
                    <li>El nombre no puede estar vacío ni repetirse.</li>
                    <li>Impresiones: número entero mayor que cero.</li>
                    <li>Clics: número entero mayor o igual a cero.</li>
                    <li>Los clics no pueden superar las impresiones.</li>
                    <li>Escribe los números sin puntos (5000, no 5.000).</li>
                </ul>
            </div>
            """
        )


# -----------------------------------------------------------------------------
# D. COMPARADOR DE CAMPAÑAS
# -----------------------------------------------------------------------------
with tab_comparador:
    mostrar_html('<div class="seccion">Tabla comparativa</div>'
                 '<div class="seccion-sub">Todas las campañas ordenadas por CTR, de mayor a menor.</div>')

    if len(campanas) == 0:
        mostrar_html('<div class="vacio"><div class="grande">📋</div><h3>Sin campañas para comparar</h3>'
                     '<p>Registra al menos una campaña para ver la comparación.</p></div>')
    else:
        mejores, ctr_maximo = buscar_mejores(campanas)

        # for: construimos cada fila de la tabla en HTML
        filas_html = ""
        posicion = 1
        for campana in ordenar_por_ctr(campanas):
            clase = campana["clasificacion"].lower()
            color = color_clasificacion(campana["clasificacion"])
            if ctr_maximo > 0:
                ancho = campana["ctr"] / ctr_maximo * 100
            else:
                ancho = 0
            if posicion == 1:
                clase_fila = "top"
            else:
                clase_fila = ""
            filas_html += (
                f'<tr class="{clase_fila}">'
                f"<td>{medalla(posicion)}</td>"
                f"<td><b>{campana['nombre']}</b></td>"
                f"<td>{formato_numero(campana['impresiones'])}</td>"
                f"<td>{formato_numero(campana['clics'])}</td>"
                f"<td><b>{campana['ctr']:.2f}%</b>"
                f'<span class="mini-barra"><div style="width:{ancho:.1f}%; background:{color};"></div></span></td>'
                f'<td><span class="badge {clase}">{campana["clasificacion"]}</span></td>'
                "</tr>"
            )
            posicion = posicion + 1

        mostrar_html(
            '<div style="overflow-x:auto;"><table class="tabla">'
            "<tr><th>#</th><th>Campaña</th><th>Impresiones</th><th>Clics</th><th>CTR</th><th>Clasificación</th></tr>"
            f"{filas_html}</table></div>"
        )

        mostrar_html(
            f"""
            <div class="ganador">
                <div class="trofeo">🏆</div>
                <div class="texto">
                    <div class="titulo">Resultado del análisis</div>
                    <div class="frase">{texto_mejores(mejores, ctr_maximo)}</div>
                </div>
            </div>
            """
        )

        altos, medios, bajos = contar_clasificaciones(campanas)
        conteo = [
            ("🟢", "Rendimiento ALTO", altos, VERDE, "#DCFCE7"),
            ("🟡", "Rendimiento MEDIO", medios, AMARILLO, "#FEF3C7"),
            ("🔴", "Rendimiento BAJO", bajos, ROJO, "#FEE2E2"),
        ]
        columnas = st.columns(3)
        for i in range(3):
            icono, etiqueta, cantidad, color, fondo = conteo[i]
            with columnas[i]:
                mostrar_html(
                    f"""
                    <div class="kpi" style="--color:{color}; --fondo:{fondo}; margin-top:14px;">
                        <div class="icono">{icono}</div>
                        <div class="etiqueta">{etiqueta}</div>
                        <div class="valor">{cantidad}</div>
                        <div class="detalle">campaña(s)</div>
                    </div>
                    """
                )

        with st.expander("Ver los datos en formato de tabla"):
            st.dataframe(construir_tabla(campanas), hide_index=True, width="stretch")


# -----------------------------------------------------------------------------
# E. GRÁFICAS
# -----------------------------------------------------------------------------
with tab_graficas:
    if len(campanas) == 0:
        mostrar_html('<div class="vacio"><div class="grande">📈</div><h3>Aún no hay gráficas</h3>'
                     '<p>Registra campañas para ver las visualizaciones.</p></div>')
    else:
        ordenadas = ordenar_por_ctr(campanas)
        mejores, ctr_maximo = buscar_mejores(campanas)

        # for: preparamos las listas de datos para las gráficas
        nombres, ctrs, colores, impresiones, clics = [], [], [], [], []
        for campana in ordenadas:
            nombres.append(campana["nombre"])
            ctrs.append(round(campana["ctr"], 2))
            colores.append(color_clasificacion(campana["clasificacion"]))
            impresiones.append(campana["impresiones"])
            clics.append(campana["clics"])

        tope = max(max(ctrs), 3) * 1.25

        # --- Gráfica 1: CTR por campaña con zonas de clasificación ---
        fig_ctr = go.Figure()
        fig_ctr.add_hrect(y0=0, y1=1, fillcolor=ROJO, opacity=0.07, line_width=0)
        fig_ctr.add_hrect(y0=1, y1=3, fillcolor=AMARILLO, opacity=0.08, line_width=0)
        fig_ctr.add_hrect(y0=3, y1=tope, fillcolor=VERDE, opacity=0.07, line_width=0)
        fig_ctr.add_trace(
            go.Bar(
                x=nombres, y=ctrs, marker=dict(color=colores, cornerradius=10),
                text=[f"<b>{c:.2f}%</b>" for c in ctrs], textposition="outside",
                hovertemplate="%{x}<br>CTR: %{y:.2f}%<extra></extra>", width=0.55,
            )
        )
        fig_ctr.add_hline(y=3, line_dash="dot", line_color=VERDE,
                          annotation_text="ALTO desde 3%", annotation_position="top left")
        fig_ctr.add_hline(y=1, line_dash="dot", line_color=AMARILLO,
                          annotation_text="MEDIO desde 1%", annotation_position="top left")
        estilo_grafica(fig_ctr, "1. CTR por campaña", 420)
        fig_ctr.update_yaxes(title="CTR (%)", range=[0, tope])
        st.plotly_chart(fig_ctr, width="stretch", config=CONFIG_GRAFICA)

        col_a, col_b = st.columns(2)

        # --- Gráfica 2: Impresiones frente a clics ---
        with col_a:
            fig_ic = go.Figure()
            fig_ic.add_trace(go.Bar(name="Impresiones", x=nombres, y=impresiones,
                                    marker=dict(color=AZUL_OSCURO, cornerradius=8),
                                    text=[formato_numero(v) for v in impresiones], textposition="outside"))
            fig_ic.add_trace(go.Bar(name="Clics", x=nombres, y=clics,
                                    marker=dict(color=CIAN, cornerradius=8),
                                    text=[formato_numero(v) for v in clics], textposition="outside"))
            estilo_grafica(fig_ic, "2. Impresiones frente a clics", 400)
            fig_ic.update_layout(barmode="group", bargap=0.3)
            fig_ic.update_yaxes(range=[0, max(impresiones) * 1.18])
            st.plotly_chart(fig_ic, width="stretch", config=CONFIG_GRAFICA)

        # --- Gráfica 3: Burbujas (tamaño = CTR) ---
        with col_b:
            tamanos = []
            for c in ctrs:
                tamanos.append(18 + c * 10)
            fig_bub = go.Figure(
                go.Scatter(
                    x=impresiones, y=clics, mode="markers+text", text=nombres,
                    textposition="top center",
                    marker=dict(size=tamanos, color=colores, opacity=0.85,
                                line=dict(color="white", width=2)),
                    customdata=ctrs,
                    hovertemplate="%{text}<br>Impresiones: %{x:,}<br>Clics: %{y:,}<br>CTR: %{customdata:.2f}%<extra></extra>",
                )
            )
            estilo_grafica(fig_bub, "3. Mapa de burbujas (tamaño = CTR)", 400)
            fig_bub.update_xaxes(title="Impresiones", showgrid=True, gridcolor="#EEF1F7",
                                 range=[0, max(impresiones) * 1.2])
            fig_bub.update_yaxes(title="Clics", range=[0, max(clics) * 1.3])
            st.plotly_chart(fig_bub, width="stretch", config=CONFIG_GRAFICA)

        # --- Gráfica 4: Ranking que resalta la campaña ganadora ---
        nombres_mejores = []
        for campana in mejores:
            nombres_mejores.append(campana["nombre"])

        colores_ranking = []
        for nombre in nombres:
            if nombre in nombres_mejores:
                colores_ranking.append(VIOLETA)
            else:
                colores_ranking.append(GRIS_SUAVE)

        etiquetas = []
        for i in range(len(nombres)):
            etiquetas.append(f"{medalla(i + 1)}  {nombres[i]}")

        fig_rank = go.Figure(
            go.Bar(
                x=ctrs[::-1], y=etiquetas[::-1], orientation="h",
                marker=dict(color=colores_ranking[::-1], cornerradius=10),
                text=[f"<b>{c:.2f}%</b>" for c in ctrs[::-1]], textposition="outside",
                hovertemplate="%{y}<br>CTR: %{x:.2f}%<extra></extra>",
            )
        )
        estilo_grafica(fig_rank, "4. Ranking de CTR · la campaña ganadora en violeta",
                       max(320, 70 * len(nombres) + 130))
        fig_rank.update_xaxes(title="CTR (%)", range=[0, max(ctrs) * 1.25], showgrid=True, gridcolor="#EEF1F7")
        st.plotly_chart(fig_rank, width="stretch", config=CONFIG_GRAFICA)

        col_c, col_d = st.columns(2)
        with col_c:
            st.plotly_chart(grafica_donut(campanas), width="stretch", config=CONFIG_GRAFICA, key="donut_graficas")
        with col_d:
            st.plotly_chart(grafica_velocimetro(ctr_promedio, ctr_maximo), width="stretch", config=CONFIG_GRAFICA, key="gauge_graficas")


# -----------------------------------------------------------------------------
# G. GESTIÓN DE CAMPAÑAS
# -----------------------------------------------------------------------------
with tab_gestion:
    mostrar_html('<div class="seccion">Gestión de campañas</div>'
                 '<div class="seccion-sub">Elimina registros o descarga los resultados.</div>')

    if len(campanas) == 0:
        mostrar_html('<div class="vacio"><div class="grande">🗂️</div><h3>No hay campañas registradas</h3>'
                     '<p>Cuando agregues campañas podrás gestionarlas aquí.</p></div>')
    else:
        col_a, col_b, col_c = st.columns(3)

        # --- Eliminar una campaña ---
        with col_a:
            with st.container(border=True):
                st.markdown("**🗑️ Eliminar una campaña**")
                nombres_lista = []
                for campana in campanas:
                    nombres_lista.append(campana["nombre"])
                seleccion = st.selectbox("Selecciona la campaña", nombres_lista)
                if st.button("Eliminar campaña", width="stretch"):
                    indice = buscar_campana(seleccion)
                    if indice != -1:
                        st.session_state.campanas.pop(indice)
                        guardar_mensaje("exito", f"Se eliminó «{seleccion}».")
                    else:
                        guardar_mensaje("aviso", "No se encontró la campaña.")
                    st.rerun()

        # --- Limpiar todos los registros ---
        with col_b:
            with st.container(border=True):
                st.markdown("**🧹 Limpiar todos los registros**")
                confirmar = st.checkbox("Confirmo que quiero borrar todas las campañas")
                if st.button("Limpiar todo", width="stretch", disabled=not confirmar):
                    st.session_state.campanas = []
                    guardar_mensaje("exito", "Se borraron todas las campañas.")
                    st.rerun()

        # --- Descargar resultados en CSV ---
        with col_c:
            with st.container(border=True):
                st.markdown("**⬇️ Descargar resultados**")
                st.caption("Archivo CSV compatible con Excel, ordenado por CTR.")
                tabla = construir_tabla(campanas)
                # utf-8-sig hace que Excel muestre bien las tildes y la ñ
                csv = tabla.to_csv(index=False, sep=";").encode("utf-8-sig")
                st.download_button(
                    "Descargar CSV",
                    data=csv,
                    file_name="resultados_campanas.csv",
                    mime="text/csv",
                    type="primary",
                    width="stretch",
                )

mostrar_html('<div class="pie">CAMPAIGN ANALYZER · Proyecto académico en Python + Streamlit</div>')
