# =============================================================================
#  CAMPAIGN ANALYZER
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

# Colores que usaremos en toda la aplicación
AZUL_OSCURO = "#0B1F4B"
AZUL_ELECTRICO = "#2F6BFF"
VIOLETA = "#7B5CFF"
GRIS_SUAVE = "#C9D2E3"
VERDE = "#12A150"
AMARILLO = "#E8A317"
ROJO = "#E5484D"

# Datos de demostración pedidos en el enunciado
DATOS_DEMO = [
    {"nombre": "Campaña Primavera", "impresiones": 5000, "clics": 100},
    {"nombre": "Campaña Verano", "impresiones": 10000, "clics": 400},
    {"nombre": "Campaña Invierno", "impresiones": 8000, "clics": 40},
]


# -----------------------------------------------------------------------------
# 2. ESTILOS VISUALES (CSS)
#    Streamlit permite inyectar CSS para personalizar el diseño.
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, .stTextInput, .stButton {
        font-family: 'Inter', sans-serif;
    }
    .stApp { background-color: #F5F7FB; }
    .block-container { padding-top: 2rem; max-width: 1200px; }

    /* Encabezado principal */
    .encabezado {
        background: linear-gradient(120deg, #0B1F4B 0%, #1B3A8A 60%, #7B5CFF 100%);
        border-radius: 20px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
    }
    .encabezado h1 {
        margin: 0; font-size: 2.1rem; font-weight: 800;
        letter-spacing: 0.06em; color: white;
    }
    .encabezado p { margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.85; }

    /* Tarjetas de indicadores */
    .tarjeta {
        background: white;
        border-radius: 16px;
        padding: 18px 20px;
        border: 1px solid #E3E8F2;
        box-shadow: 0 2px 10px rgba(11, 31, 75, 0.05);
        height: 100%;
    }
    .tarjeta .etiqueta {
        font-size: 0.78rem; font-weight: 600; color: #6B7A99;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .tarjeta .valor {
        font-size: 1.7rem; font-weight: 800; color: #0B1F4B;
        margin-top: 6px; line-height: 1.2; word-break: break-word;
    }
    .tarjeta .valor.pequeno { font-size: 1.15rem; }
    .tarjeta .detalle { font-size: 0.85rem; color: #2F6BFF; margin-top: 4px; }

    /* Bloque del resultado del análisis */
    .resultado {
        background: white;
        border-left: 6px solid #7B5CFF;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 2px 10px rgba(11, 31, 75, 0.06);
        margin: 20px 0;
        font-size: 1.1rem;
        color: #0B1F4B;
    }
    .resultado b { color: #7B5CFF; }

    /* Etiquetas de clasificación */
    .badge {
        display: inline-block; padding: 3px 12px; border-radius: 999px;
        font-size: 0.8rem; font-weight: 700; color: white;
    }
    .badge.alto  { background: #12A150; }
    .badge.medio { background: #E8A317; }
    .badge.bajo  { background: #E5484D; }

    /* Tarjeta de campaña individual */
    .campana {
        background: white; border-radius: 14px; padding: 14px 18px;
        border: 1px solid #E3E8F2; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
        flex-wrap: wrap; gap: 8px;
    }
    .campana .nombre { font-weight: 700; color: #0B1F4B; }
    .campana .datos { color: #6B7A99; font-size: 0.9rem; }

    /* Botones */
    .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
        border-radius: 10px; font-weight: 600;
    }
    .stFormSubmitButton > button {
        background: #2F6BFF; color: white; border: none;
    }
    .stFormSubmitButton > button:hover { background: #1B3A8A; color: white; }

    /* Pestañas */
    .stTabs [data-baseweb="tab"] { font-weight: 600; }

    /* Ajustes para celulares */
    @media (max-width: 640px) {
        .encabezado h1 { font-size: 1.5rem; }
        .tarjeta .valor { font-size: 1.35rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# 3. MEMORIA DE LA SESIÓN
#    st.session_state guarda datos mientras la página esté abierta.
#    Aquí guardamos la lista de campañas (cada campaña es un diccionario).
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
    # while: repetimos la revisión hasta llegar al final del texto
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
    """
    Valida los datos del formulario.
    Devuelve una lista de errores (vacía si todo está bien).
    """
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
        errores.append("Las impresiones deben ser un número entero (sin decimales, letras ni signos).")
    elif int(impresiones_texto) <= 0:
        errores.append("Las impresiones deben ser mayores que cero.")
    else:
        impresiones_ok = True

    # --- Validación de clics ---
    clics_ok = False
    if clics_texto == "":
        errores.append("Debes ingresar el número de clics.")
    elif not es_entero_valido(clics_texto):
        errores.append("Los clics deben ser un número entero mayor o igual a cero (sin decimales, letras ni signos).")
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
    """
    Recorre TODAS las campañas con un ciclo FOR para sumar
    impresiones, clics y CTR, y así obtener los indicadores generales.
    """
    total_impresiones = 0
    total_clics = 0
    suma_ctr = 0

    for campana in campanas:
        total_impresiones = total_impresiones + campana["impresiones"]
        total_clics = total_clics + campana["clics"]
        suma_ctr = suma_ctr + campana["ctr"]

    # if / else: el promedio solo existe si hay campañas
    if len(campanas) > 0:
        ctr_promedio = suma_ctr / len(campanas)
    else:
        ctr_promedio = 0.0

    return total_impresiones, total_clics, ctr_promedio


def buscar_mejores(campanas):
    """
    Encuentra la(s) campaña(s) con el CTR más alto.
    Si hay empate, devuelve todas las campañas empatadas.
    """
    mejores = []
    ctr_maximo = -1

    # for: comparamos cada campaña con el mejor CTR encontrado hasta ahora
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
    """
    Ordena las campañas de mayor a menor CTR.
    Usamos el método de la burbuja con dos ciclos FOR
    para que se vea claramente cómo funciona el ordenamiento.
    """
    lista = campanas.copy()
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j]["ctr"] < lista[j + 1]["ctr"]:
                # Intercambiamos las dos campañas
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def construir_tabla(campanas):
    """Construye la tabla comparativa recorriendo las campañas con FOR."""
    filas = []
    posicion = 1
    for campana in ordenar_por_ctr(campanas):
        # if / elif / else para poner un ícono según la clasificación
        if campana["clasificacion"] == "ALTO":
            icono = "🟢 ALTO"
        elif campana["clasificacion"] == "MEDIO":
            icono = "🟡 MEDIO"
        else:
            icono = "🔴 BAJO"

        filas.append({
            "Posición": posicion,
            "Campaña": campana["nombre"],
            "Impresiones": campana["impresiones"],
            "Clics": campana["clics"],
            "CTR (%)": round(campana["ctr"], 2),
            "Clasificación": icono,
        })
        posicion = posicion + 1

    return pd.DataFrame(filas)


def color_clasificacion(clasificacion):
    """Devuelve el color correspondiente a cada clasificación."""
    if clasificacion == "ALTO":
        return VERDE
    elif clasificacion == "MEDIO":
        return AMARILLO
    else:
        return ROJO


def texto_mejores(mejores, ctr_maximo):
    """Arma la frase del resultado del análisis, contemplando empates."""
    if len(mejores) == 1:
        return (
            f"La campaña con mejor rendimiento es <b>{mejores[0]['nombre']}</b>, "
            f"con un CTR de <b>{ctr_maximo:.2f}%</b>."
        )
    else:
        # for: juntamos los nombres de todas las campañas empatadas
        nombres = []
        for campana in mejores:
            nombres.append(f"<b>{campana['nombre']}</b>")
        lista_nombres = ", ".join(nombres[:-1]) + " y " + nombres[-1]
        return (
            f"Hay un empate en el mejor rendimiento: {lista_nombres}, "
            f"todas con un CTR de <b>{ctr_maximo:.2f}%</b>."
        )


def formato_numero(numero):
    """Escribe un número con puntos de miles, por ejemplo: 10000 -> 10.000."""
    return f"{numero:,}".replace(",", ".")


def guardar_mensaje(tipo, texto):
    """Guarda un mensaje para mostrarlo después de recargar la página."""
    st.session_state.mensaje = (tipo, texto)


def estilo_grafica(figura, titulo):
    """Aplica el mismo estilo limpio a todas las gráficas."""
    figura.update_layout(
        title=dict(text=titulo, font=dict(size=16, color=AZUL_OSCURO)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", color=AZUL_OSCURO),
        margin=dict(l=20, r=20, t=60, b=20),
        height=400,
        legend=dict(orientation="h", y=-0.15),
    )
    figura.update_yaxes(gridcolor="#EEF1F7")
    return figura


# =============================================================================
# 5. INTERFAZ DE USUARIO
# =============================================================================

# --- Encabezado ---
st.markdown(
    """
    <div class="encabezado">
        <h1>📊 CAMPAIGN ANALYZER</h1>
        <p>Analiza, compara y optimiza tus campañas digitales.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Mensaje pendiente de una acción anterior (agregar, eliminar, etc.) ---
if st.session_state.mensaje is not None:
    tipo, texto = st.session_state.mensaje
    if tipo == "exito":
        st.success(texto)
    elif tipo == "aviso":
        st.warning(texto)
    else:
        st.info(texto)
    st.session_state.mensaje = None

campanas = st.session_state.campanas

# Pestañas de navegación
tab_dashboard, tab_registro, tab_comparador, tab_graficas, tab_gestion = st.tabs(
    ["🏠 Dashboard", "➕ Registrar campaña", "📋 Comparador", "📈 Gráficas", "⚙️ Gestión"]
)


# -----------------------------------------------------------------------------
# A. DASHBOARD PRINCIPAL
# -----------------------------------------------------------------------------
with tab_dashboard:
    total_impresiones, total_clics, ctr_promedio = calcular_resumen(campanas)

    # Nombre de la mejor campaña para la tarjeta
    if len(campanas) > 0:
        mejores, ctr_maximo = buscar_mejores(campanas)
        if len(mejores) == 1:
            nombre_mejor = mejores[0]["nombre"]
        else:
            nombre_mejor = f"Empate ({len(mejores)} campañas)"
        detalle_mejor = f"CTR {ctr_maximo:.2f}%"
    else:
        nombre_mejor = "—"
        detalle_mejor = "Sin datos"

    # Lista de tarjetas: (etiqueta, valor, detalle)
    tarjetas = [
        ("Campañas registradas", f"{len(campanas)}", "en esta sesión"),
        ("Total impresiones", formato_numero(total_impresiones), "veces vistas"),
        ("Total clics", formato_numero(total_clics), "interacciones"),
        ("CTR promedio", f"{ctr_promedio:.2f}%", "entre todas las campañas"),
        ("Mejor campaña", nombre_mejor, detalle_mejor),
    ]

    # for: dibujamos una tarjeta en cada columna
    columnas = st.columns(5)
    for i in range(len(tarjetas)):
        etiqueta, valor, detalle = tarjetas[i]
        clase_valor = "valor pequeno" if i == 4 else "valor"
        columnas[i].markdown(
            f"""
            <div class="tarjeta">
                <div class="etiqueta">{etiqueta}</div>
                <div class="{clase_valor}">{valor}</div>
                <div class="detalle">{detalle}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # F. Resultado del análisis
    if len(campanas) > 0:
        st.markdown(
            f'<div class="resultado">🏆 {texto_mejores(mejores, ctr_maximo)}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("#### Campañas registradas")
        # for: mostramos cada campaña con su etiqueta de clasificación
        for campana in campanas:
            clase = campana["clasificacion"].lower()
            st.markdown(
                f"""
                <div class="campana">
                    <div>
                        <div class="nombre">{campana['nombre']}</div>
                        <div class="datos">{formato_numero(campana['impresiones'])} impresiones · {formato_numero(campana['clics'])} clics · CTR {campana['ctr']:.2f}%</div>
                    </div>
                    <span class="badge {clase}">{campana['clasificacion']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info(
            "Aún no hay campañas. Ve a **➕ Registrar campaña** para agregar una, "
            "o carga los datos de demostración."
        )
        if st.button("Cargar datos de demostración", key="demo_dashboard", type="primary"):
            for dato in DATOS_DEMO:
                st.session_state.campanas.append(
                    crear_campana(dato["nombre"], dato["impresiones"], dato["clics"])
                )
            guardar_mensaje("exito", "Se cargaron las 3 campañas de demostración.")
            st.rerun()

    # Leyenda de la clasificación
    st.caption(
        "Criterios de clasificación (definidos para este ejercicio académico): "
        "🟢 ALTO: CTR ≥ 3% · 🟡 MEDIO: 1% ≤ CTR < 3% · 🔴 BAJO: CTR < 1%"
    )


# -----------------------------------------------------------------------------
# B. REGISTRO DE CAMPAÑAS
# -----------------------------------------------------------------------------
with tab_registro:
    st.subheader("Registrar una nueva campaña")
    st.write("Ingresa los datos y el CTR se calculará automáticamente.")

    with st.form("formulario_campana", clear_on_submit=False):
        nombre = st.text_input("Nombre de la campaña", placeholder="Ej: Campaña Otoño")
        col1, col2 = st.columns(2)
        impresiones_texto = col1.text_input("Número de impresiones", placeholder="Ej: 5000")
        clics_texto = col2.text_input("Número de clics", placeholder="Ej: 120")
        enviado = st.form_submit_button("Agregar campaña", width="stretch")

    if enviado:
        # Quitamos espacios al inicio y al final
        nombre = nombre.strip()
        impresiones_texto = impresiones_texto.strip()
        clics_texto = clics_texto.strip()

        errores = validar_campana(nombre, impresiones_texto, clics_texto)

        if len(errores) > 0:
            # for: mostramos cada error encontrado
            for error in errores:
                st.error("⚠️ " + error)
        else:
            nueva = crear_campana(nombre, int(impresiones_texto), int(clics_texto))
            st.session_state.campanas.append(nueva)
            guardar_mensaje(
                "exito",
                f"✅ «{nueva['nombre']}» agregada. CTR: {nueva['ctr']:.2f}% → {nueva['clasificacion']}",
            )
            st.rerun()

    st.divider()
    st.markdown("**¿Quieres probar rápido?** Carga las campañas de ejemplo (Primavera, Verano e Invierno).")
    if st.button("Cargar datos de demostración", key="demo_registro"):
        agregadas = 0
        # for: recorremos los datos de ejemplo
        for dato in DATOS_DEMO:
            # if: solo agregamos las que no existan todavía
            if buscar_campana(dato["nombre"]) == -1:
                st.session_state.campanas.append(
                    crear_campana(dato["nombre"], dato["impresiones"], dato["clics"])
                )
                agregadas = agregadas + 1

        if agregadas > 0:
            guardar_mensaje("exito", f"Se cargaron {agregadas} campaña(s) de demostración.")
        else:
            guardar_mensaje("aviso", "Las campañas de demostración ya estaban registradas.")
        st.rerun()


# -----------------------------------------------------------------------------
# D. COMPARADOR DE CAMPAÑAS
# -----------------------------------------------------------------------------
with tab_comparador:
    st.subheader("Tabla comparativa")

    if len(campanas) == 0:
        st.info("Registra al menos una campaña para ver la comparación.")
    else:
        st.write("Campañas ordenadas por CTR, de mayor a menor.")
        tabla = construir_tabla(campanas)
        st.dataframe(
            tabla,
            hide_index=True,
            width="stretch",
            column_config={
                "Impresiones": st.column_config.NumberColumn(format="localized"),
                "Clics": st.column_config.NumberColumn(format="localized"),
                "CTR (%)": st.column_config.NumberColumn(format="%.2f %%"),
            },
        )

        mejores, ctr_maximo = buscar_mejores(campanas)
        st.markdown(
            f'<div class="resultado">🏆 {texto_mejores(mejores, ctr_maximo)}</div>',
            unsafe_allow_html=True,
        )

        # Conteo por clasificación usando for + if / elif / else
        altos, medios, bajos = 0, 0, 0
        for campana in campanas:
            if campana["clasificacion"] == "ALTO":
                altos = altos + 1
            elif campana["clasificacion"] == "MEDIO":
                medios = medios + 1
            else:
                bajos = bajos + 1

        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 Rendimiento ALTO", altos)
        c2.metric("🟡 Rendimiento MEDIO", medios)
        c3.metric("🔴 Rendimiento BAJO", bajos)


# -----------------------------------------------------------------------------
# E. GRÁFICAS
# -----------------------------------------------------------------------------
with tab_graficas:
    if len(campanas) == 0:
        st.info("Registra campañas para ver las gráficas.")
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

        # --- Gráfica 1: CTR por campaña (color según clasificación) ---
        fig_ctr = go.Figure(
            go.Bar(
                x=nombres,
                y=ctrs,
                marker_color=colores,
                text=[f"{c:.2f}%" for c in ctrs],
                textposition="outside",
                hovertemplate="%{x}<br>CTR: %{y:.2f}%<extra></extra>",
            )
        )
        # Líneas de referencia de los umbrales 1% y 3%
        fig_ctr.add_hline(y=3, line_dash="dash", line_color=VERDE,
                          annotation_text="ALTO (3%)", annotation_position="top left")
        fig_ctr.add_hline(y=1, line_dash="dash", line_color=AMARILLO,
                          annotation_text="MEDIO (1%)", annotation_position="top left")
        estilo_grafica(fig_ctr, "1. CTR por campaña")
        fig_ctr.update_yaxes(title="CTR (%)", range=[0, max(max(ctrs), 3) * 1.25])
        st.plotly_chart(fig_ctr, width="stretch")
        st.caption("Verde = ALTO · Amarillo = MEDIO · Rojo = BAJO")

        # --- Gráfica 2: Impresiones frente a clics ---
        fig_ic = go.Figure()
        fig_ic.add_trace(go.Bar(name="Impresiones", x=nombres, y=impresiones,
                                marker_color=AZUL_OSCURO))
        fig_ic.add_trace(go.Bar(name="Clics", x=nombres, y=clics,
                                marker_color=AZUL_ELECTRICO))
        estilo_grafica(fig_ic, "2. Impresiones frente a clics")
        fig_ic.update_layout(barmode="group")
        fig_ic.update_yaxes(title="Cantidad")
        st.plotly_chart(fig_ic, width="stretch")

        # --- Gráfica 3: Ranking que resalta la campaña con mayor CTR ---
        nombres_mejores = []
        for campana in mejores:
            nombres_mejores.append(campana["nombre"])

        colores_ranking = []
        for nombre in nombres:
            if nombre in nombres_mejores:
                colores_ranking.append(VIOLETA)   # La(s) mejor(es) en violeta
            else:
                colores_ranking.append(GRIS_SUAVE)

        # Invertimos el orden para que la mejor quede arriba
        fig_rank = go.Figure(
            go.Bar(
                x=ctrs[::-1],
                y=nombres[::-1],
                orientation="h",
                marker_color=colores_ranking[::-1],
                text=[f"{c:.2f}%" for c in ctrs[::-1]],
                textposition="outside",
                hovertemplate="%{y}<br>CTR: %{x:.2f}%<extra></extra>",
            )
        )
        estilo_grafica(fig_rank, "3. Ranking de CTR: la campaña ganadora en violeta")
        fig_rank.update_xaxes(title="CTR (%)", range=[0, max(ctrs) * 1.25], gridcolor="#EEF1F7")
        fig_rank.update_layout(height=max(300, 70 * len(nombres) + 120))
        st.plotly_chart(fig_rank, width="stretch")


# -----------------------------------------------------------------------------
# G. GESTIÓN DE CAMPAÑAS
# -----------------------------------------------------------------------------
with tab_gestion:
    st.subheader("Gestión de campañas")

    if len(campanas) == 0:
        st.info("No hay campañas registradas.")
    else:
        col_a, col_b = st.columns(2)

        # --- Eliminar una campaña ---
        with col_a:
            st.markdown("**Eliminar una campaña**")
            nombres_lista = []
            for campana in campanas:
                nombres_lista.append(campana["nombre"])
            seleccion = st.selectbox("Selecciona la campaña", nombres_lista)
            if st.button("🗑️ Eliminar campaña", width="stretch"):
                indice = buscar_campana(seleccion)
                if indice != -1:
                    st.session_state.campanas.pop(indice)
                    guardar_mensaje("exito", f"Se eliminó «{seleccion}».")
                else:
                    guardar_mensaje("aviso", "No se encontró la campaña.")
                st.rerun()

        # --- Limpiar todos los registros ---
        with col_b:
            st.markdown("**Limpiar todos los registros**")
            confirmar = st.checkbox("Confirmo que quiero borrar todas las campañas")
            if st.button("🧹 Limpiar todo", width="stretch", disabled=not confirmar):
                st.session_state.campanas = []
                guardar_mensaje("exito", "Se borraron todas las campañas.")
                st.rerun()

        st.divider()

        # --- Descargar resultados en CSV ---
        st.markdown("**Descargar resultados**")
        tabla = construir_tabla(campanas)
        # utf-8-sig hace que Excel muestre bien las tildes y la ñ
        csv = tabla.to_csv(index=False, sep=";").encode("utf-8-sig")
        st.download_button(
            "⬇️ Descargar CSV",
            data=csv,
            file_name="resultados_campanas.csv",
            mime="text/csv",
            type="primary",
        )

st.markdown("---")
st.caption("CAMPAIGN ANALYZER · Proyecto académico en Python + Streamlit")
