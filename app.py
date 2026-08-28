import streamlit as st
import sqlite3
import time
import random

# --- CONFIGURACI脫N DE LA BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect("zafirox_users.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            saldo REAL,
            retiros_solicitados REAL
        )
    '''''')
    # Verificar si existe el usuario Lud337, si no, crearlo con saldo inicial
    cursor.execute("SELECT * FROM usuarios WHERE username = ?", ("Lud337",))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (saldo, retiros_solicitados, username) VALUES (?, ?, ?)", (27.40, 0.0, "Lud337"))
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

def get_saldo(username):
    cursor.execute("SELECT saldo FROM usuarios WHERE username = ?", (username,))
    row = cursor.fetchone()
    return row[0] if row else 0.0

def update_saldo(username, nuevo_saldo):
    cursor.execute("UPDATE usuarios SET saldo = ? WHERE username = ?", (nuevo_saldo, username))
    conn.commit()

# --- ESTADO DE SESI脫N ---
if "usuario_activo" not in st.session_state:
    st.session_state.usuario_activo = "Lud337"

usuario = st.session_state.usuario_activo
saldo_actual = get_saldo(usuario)

# --- MEN脷 LATERAL ---
st.sidebar.title(f"Hola, {usuario} 馃憢")
st.sidebar.markdown(f"**Tu Saldo (Monedas):**")
st.sidebar.markdown(f"# 馃拵 {saldo_actual:.2f}")

menu_seleccionado = st.sidebar.selectbox(
    "Men煤",
    [
        "Ruleta de la Suerte",
        "Caja Misteriosa",
        "Caza de Gemas (Nuevo)",
        "Ver Videos Premiados",
        "Invitar Amigos",
        "Solicitar Retiro",
    ],
)

# --- VISTA: VER VIDEOS PREMIADOS ---
if menu_seleccionado == "Ver Videos Premiados":
    st.subheader("馃摵 Ver Videos Premiados")
    st.write("Mira el contenido patrocinado y completa el contador para recibir tus recompensas autom谩ticas en tu saldo.")

    st.info("馃挕 Haz clic en el bot贸n inferior para iniciar el video publicitario patrocinado.")

    if "viendo_video" not in st.session_state:
        st.session_state.viendo_video = False

    if not st.session_state.viendo_video:
        if st.button("鈻讹笍 Iniciar Video Premiado"):
            st.session_state.viendo_video = True
            st.rerun()

    if st.session_state.viendo_video:
        barra_progreso = st.progress(0)
        estado_texto = st.empty()

        tiempo_total = 10  # Segundos del anuncio
        for segundos in range(tiempo_total):
            porcentaje = int(((segundos + 1) / tiempo_total) * 100)
            barra_progreso.progress(porcentaje)
            estado_texto.text(f"Reproduciendo anuncio publicitario masivo... {tiempo_total - segundos} segundos restantes")
            time.sleep(1)

        barra_progreso.empty()
        estado_texto.empty()

        # Otorgar recompensa
        recompensa = 2.50
        nuevo_saldo = get_saldo(usuario) + recompensa
        update_saldo(usuario, nuevo_saldo)
        st.session_state.viendo_video = False

        st.success(f"隆Felicidades {usuario}! Has ganado 馃拵 {recompensa:.2f} monedas.")
        st.rerun()

# --- VISTA: RULETA DE LA SUERTE ---
elif menu_seleccionado == "Ruleta de la Suerte":
    st.subheader("馃帯 Ruleta de la Suerte")
    st.write("隆Gira la ruleta por un costo de 1.00 馃拵 y gana recompensas incre铆bles!")
    
    if st.button("Girar Ruleta (Costo: 1.00 馃拵)"):
        saldo_actual = get_saldo(usuario)
        if saldo_actual >= 1.00:
            # Descontar costo y dar premio aleatorio
            premio = random.choice([0.50, 1.50, 3.00, 5.00, 10.00])
            nuevo_saldo = saldo_actual - 1.00 + premio
            update_saldo(usuario, nuevo_saldo)
            st.success(f"隆La ruleta gir贸 y ganaste 馃拵 {premio:.2f} monedas!")
            st.rerun()
        else:
            st.error("No tienes suficientes monedas para girar la ruleta.")

# --- VISTA: CAJA MISTERIOSA ---
elif menu_seleccionado == "Caja Misteriosa":
    st.subheader("馃巵 Caja Misteriosa")
    st.write("Abre una caja secreta patrocinada. Algunas tienen bonos sorpresa y otras est谩n vac铆as.")
    if st.button("Abrir Caja Misteriosa"):
        premio_caja = random.choice([0.0, 2.0, 4.0, 8.0])
        nuevo_saldo = get_saldo(usuario) + premio_caja
        update_saldo(usuario, nuevo_saldo)
        if premio_caja > 0:
            st.success(f"隆Sorpresa! La caja conten铆a 馃拵 {premio_caja:.2f} monedas.")
        else:
            st.warning("Oh no, la caja estaba vac铆a. 隆Sigue intentando con los videos premiados!")
        st.rerun()

# --- VISTA: CAZA DE GEMAS ---
elif menu_seleccionado == "Caza de Gemas (Nuevo)":
    st.subheader("馃拵 Caza de Gemas (Nuevo)")
    st.write("Selecciona una de las 3 rocas ocultas para encontrar gemas ocultas.")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Roca A"):
            gema = random.choice([1.0, 3.0])
            update_saldo(usuario, get_saldo(usuario) + gema)
            st.success(f"隆Encontraste 馃拵 {gema} en la Roca A!")
            st.rerun()
    with col2:
        if st.button("Roca B"):
            gema = random.choice([0.5, 5.0])
            update_saldo(usuario, get_saldo(usuario) + gema)
            st.success(f"隆Encontraste 馃拵 {gema} en la Roca B!")
            st.rerun()
    with col3:
        if st.button("Roca C"):
            gema = random.choice([2.0, 4.0])
            update_saldo(usuario, get_saldo(usuario) + gema)
            st.success(f"隆Encontraste 馃拵 {gema} en la Roca C!")
            st.rerun()

# --- VISTA: INVITAR AMIGOS ---
elif menu_seleccionado == "Invitar Amigos":
    st.subheader("馃懃 Invitar Amigos")
    st.write("Comparte tu enlace de referido para ganar 5.00 monedas por cada amigo que se registre en ZafiroX.")
    st.code(f"https://zafirox-minijuegos.streamlit.app/?ref={usuario}")
    st.info("Cada visualizaci贸n de video de tus referidos te otorga una comisi贸n del 10%.")

# --- VISTA: SOLICITAR RETIRO (CUENTAS REALES) ---
elif menu_seleccionado == "Solicitar Retiro":
    st.subheader("馃捀 Solicitar Retiro a Cuentas Reales")
    st.write("Convierte tus monedas acumuladas en dinero real y ret铆ralo a tu m茅todo de pago preferido.")
    
    saldo_disp = get_saldo(usuario)
    tasa_conversion = 0.10  # 1 Moneda/Diamante = $0.10 USD (o moneda local)
    dinero_estimado = saldo_disp * tasa_conversion

    st.markdown(f"### Saldo Disponible: **馃拵 {saldo_disp:.2f} monedas**")
    st.markdown(f"### Equivalente en Dinero Real: **$ {dinero_estimado:.2f} USD**")
    
    st.markdown("---")
    
    metodo_pago = st.selectbox("Selecciona tu M茅todo de Retiro", ["PayPal", "Nequi", "Daviplata", "PSE (Transferencia Bancaria)"])
    
    # Campos din谩micos seg煤n el m茅todo
    cuenta_destino = ""
    if metodo_pago == "PayPal":
        cuenta_destino = st.text_input("Correo electr贸nico asociado a PayPal")
    elif metodo_pago in ["Nequi", "Daviplata"]:
        cuenta_destino = st.text_input(f"N煤mero de celular registrado en {metodo_pago}")
    else:
        banco = st.selectbox("Selecciona tu Banco", ["Bancolombia", "Davivienda", "BBVA", "Banco de Bogot谩", "Nu Colombia"])
        tipo_cuenta = st.selectbox("Tipo de Cuenta", ["Ahorros", "Corriente"])
        num_cuenta = st.text_input("N煤mero de Cuenta Bancaria")
        cuenta_destino = f"{banco} - {tipo_cuenta} - {num_cuenta}"

    minimo_retiro = 20.00  # M铆nimo en monedas

    if st.button("Confirmar Solicitud de Retiro"):
        if saldo_disp < minimo_retiro:
            st.error(f"鉂� Saldo insuficiente. El m铆nimo requerido para retirar es de **{minimo_retiro} monedas** (Tienes {saldo_disp:.2f}).")
        elif not cuenta_destino.strip():
            st.error(f"鉂� Por favor ingresa los datos correctos para tu cuenta de {metodo_pago}.")
        else:
            # Procesar retiro (descontar del saldo)
            nuevo_saldo_post_retiro = saldo_disp - minimo_retiro
            update_saldo(usuario, nuevo_saldo_post_retiro)
            
            st.success(f"馃帀 隆Solicitud de retiro enviada con 茅xito!")
            st.info(f"Se ha procesado el env铆o de **$ {minimo_retiro * tasa_conversion:.2f} USD** hacia tu cuenta de **{metodo_pago}** ({cuenta_destino}). El dinero se ver谩 reflejado en un plazo de 24 a 48 horas h谩biles.")
            st.rerun()
