import random
import sqlite3
import time
import streamlit as st

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---


def init_db():
  conn = sqlite3.connect("zafirox_users.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            saldo REAL,
            retiros_solicitados REAL
        )
    """)
  cursor.execute("SELECT * FROM usuarios WHERE username = ?", ("Lud337",))
  if not cursor.fetchone():
    cursor.execute(
        "INSERT INTO usuarios (saldo, retiros_solicitados, username) VALUES"
        " (?, ?, ?)",
        (27.40, 0.0, "Lud337"),
    )
  conn.commit()
  return conn, cursor


conn, cursor = init_db()


def get_saldo(username):
  cursor.execute("SELECT saldo FROM usuarios WHERE username = ?", (username,))
  row = cursor.fetchone()
  return row[0] if row else 0.0


def update_saldo(username, nuevo_saldo):
  cursor.execute(
      "UPDATE usuarios SET saldo = ? WHERE username = ?", (nuevo_saldo, username)
  )
  conn.commit()


# --- ESTADO DE SESIÓN ---
if "usuario_activo" not in st.session_state:
  st.session_state.usuario_activo = "Lud337"

usuario = st.session_state.usuario_activo
saldo_actual = get_saldo(usuario)

# --- MENÚ LATERAL ---
st.sidebar.title(f"Hola, {usuario} 👋")
st.sidebar.markdown(f"**Tu Saldo (Monedas):**")
st.sidebar.markdown(f"# 💎 {saldo_actual:.2f}")

menu_seleccionado = st.sidebar.selectbox(
    "Menú",
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
  st.subheader("📺 Ver Videos Premiados")
  st.write(
      "Mira el contenido patrocinado y completa el contador para recibir tus"
      " recompensas automáticas en tu saldo."
  )

  st.info(
      "💡 Haz clic en el botón inferior para iniciar el video publicitario"
      " patrocinado."
  )

  if "viendo_video" not in st.session_state:
    st.session_state.viendo_video = False

  if not st.session_state.viendo_video:
    if st.button("▶️ Iniciar Video Premiado"):
      st.session_state.viendo_video = True
      st.rerun()

  if st.session_state.viendo_video:
    barra_progreso = st.progress(0)
    estado_texto = st.empty()

    tiempo_total = 10
    for segundos in range(tiempo_total):
      porcentaje = int(((segundos + 1) / tiempo_total) * 100)
      barra_progreso.progress(porcentaje)
      estado_texto.text(
          "Reproduciendo anuncio publicitario masivo..."
          f" {tiempo_total - segundos} segundos restantes"
      )
      time.sleep(1)

    barra_progreso.empty()
    estado_texto.empty()

    recompensa = 2.50
    nuevo_saldo = get_saldo(usuario) + recompensa
    update_saldo(usuario, nuevo_saldo)
    st.session_state.viendo_video = False

    st.success(
        f"¡Felicidades {usuario}! Has ganado 💎 {recompensa:.2f} monedas."
    )
    st.rerun()

# --- VISTA: RULETA DE LA SUERTE ---
elif menu_seleccionado == "Ruleta de la Suerte":
  st.subheader("🎡 Ruleta de la Suerte")
  st.write(
      "¡Gira la ruleta por un costo de 1.00 💎 y gana recompensas increíbles!"
  )

  if st.button("Girar Ruleta (Costo: 1.00 💎)"):
    saldo_actual = get_saldo(usuario)
    if saldo_actual >= 1.00:
      premio = random.choice([0.50, 1.50, 3.00, 5.00, 10.00])
      nuevo_saldo = saldo_actual - 1.00 + premio
      update_saldo(usuario, nuevo_saldo)
      st.success(f"¡La ruleta giró y ganaste 💎 {premio:.2f} monedas!")
      st.rerun()
    else:
      st.error("No tienes suficientes monedas para girar la ruleta.")

# --- VISTA: CAJA MISTERIOSA ---
elif menu_seleccionado == "Caja Misteriosa":
  st.subheader("🎁 Caja Misteriosa")
  st.write(
      "Abre una caja secreta patrocinada. Algunas tienen bonos sorpresa y"
      " otras están vacías."
  )
  if st.button("Abrir Caja Misteriosa"):
    premio_caja = random.choice([0.0, 2.0, 4.0, 8.0])
    nuevo_saldo = get_saldo(usuario) + premio_caja
    update_saldo(usuario, nuevo_saldo)
    if premio_caja > 0:
      st.success(f"¡Sorpresa! La caja contenía 💎 {premio_caja:.2f} monedas.")
    else:
      st.warning(
          "Oh no, la caja estaba vacía. ¡Sigue intentando con los videos"
          " premiados!"
      )
    st.rerun()

# --- VISTA: CAZA DE GEMAS ---
elif menu_seleccionado == "Caza de Gemas (Nuevo)":
  st.subheader("💎 Caza de Gemas (Nuevo)")
  st.write(
      "Selecciona una de las 3 rocas ocultas para encontrar gemas ocultas."
  )
  col1, col2, col3 = st.columns(3)

  with col1:
    if st.button("Roca A"):
      gema = random.choice([1.0, 3.0])
      update_saldo(usuario, get_saldo(usuario) + gema)
      st.success(f"¡Encontraste 💎 {gema} en la Roca A!")
      st.rerun()
  with col2:
    if st.button("Roca B"):
      gema = random.choice([0.5, 5.0])
      update_saldo(usuario, get_saldo(usuario) + gema)
      st.success(f"¡Encontraste 💎 {gema} en la Roca B!")
      st.rerun()
  with col3:
    if st.button("Roca C"):
      gema = random.choice([2.0, 4.0])
      update_saldo(usuario, get_saldo(usuario) + gema)
      st.success(f"¡Encontraste 💎 {gema} en la Roca C!")
      st.rerun()

# --- VISTA: INVITAR AMIGOS ---
elif menu_seleccionado == "Invitar Amigos":
  st.subheader("👥 Invitar Amigos")
  st.write(
      "Comparte tu enlace de referido para ganar 5.00 monedas por cada amigo"
      " que se registre en ZafiroX."
  )
  st.code(f"https://zafirox-minijuegos.streamlit.app/?ref={usuario}")
  st.info(
      "Cada visualización de video de tus referidos te otorga una comisión del"
      " 10%."
  )

# --- VISTA: SOLICITAR RETIRO (CUENTAS REALES) ---
elif menu_seleccionado == "Solicitar Retiro":
  st.subheader("💸 Solicitar Retiro a Cuentas Reales")
  st.write(
      "Convierte tus monedas acumuladas en dinero real y retíralo a tu método de"
      " pago preferido."
  )

  saldo_disp = get_saldo(usuario)
  tasa_conversion = 0.10
  dinero_estimado = saldo_disp * tasa_conversion

  st.markdown(f"### Saldo Disponible: **💎 {saldo_disp:.2f} monedas**")
  st.markdown(f"### Equivalente en Dinero Real: **$ {dinero_estimado:.2f} USD**")

  st.markdown("---")

  metodo_pago = st.selectbox(
      "Selecciona tu Método de Retiro",
      ["PayPal", "Nequi", "Daviplata", "PSE (Transferencia Bancaria)"],
  )

  cuenta_destino = ""
  if metodo_pago == "PayPal":
    cuenta_destino = st.text_input("Correo electrónico asociado a PayPal")
  elif metodo_pago in ["Nequi", "Daviplata"]:
    cuenta_destino = st.text_input(
        f"Número de celular registrado en {metodo_pago}"
    )
  else:
    banco = st.selectbox(
        "Selecciona tu Banco",
        ["Bancolombia", "Davivienda", "BBVA", "Banco de Bogotá", "Nu Colombia"],
    )
    tipo_cuenta = st.selectbox("Tipo de Cuenta", ["Ahorros", "Corriente"])
    num_cuenta = st.text_input("Número de Cuenta Bancaria")
    cuenta_destino = f"{banco} - {tipo_cuenta} - {num_cuenta}"

  minimo_retiro = 20.00

  if st.button("Confirmar Solicitud de Retiro"):
    if saldo_disp < minimo_retiro:
      st.error(
          f"❌ Saldo insuficiente. El mínimo requerido para retirar es de"
          f" **{minimo_retiro} monedas** (Tienes {saldo_disp:.2f})."
      )
    elif not cuenta_destino.strip():
      st.error(
          f"❌ Por favor ingresa los datos correctos para tu cuenta de"
          f" {metodo_pago}."
      )
    else:
      nuevo_saldo_post_retiro = saldo_disp - minimo_retiro
      update_saldo(usuario, nuevo_saldo_post_retiro)

      st.success("🎉 ¡Solicitud de retiro enviada con éxito!")
      st.info(
          "Se ha procesado el envío de"
          f" **$ {minimo_retiro * tasa_conversion:.2f} USD** hacia tu cuenta"
          f" de **{metodo_pago}** ({cuenta_destino}). El dinero se verá"
          " reflejado en un plazo de 24 a 48 horas hábiles."
      )
      st.rerun()
