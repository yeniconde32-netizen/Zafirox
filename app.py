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
        (28.90, 0.0, "Lud337"),
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

# --- MENÚ LATERAL CON ESTILO VISUAL ---
st.sidebar.title(f"🎮 ZafiroX Hub")
st.sidebar.markdown(f"**Usuario:** {usuario} 👋")
st.sidebar.markdown(f"### Tu Saldo:")
st.sidebar.markdown(f"# 💎 {saldo_actual:.2f}")
st.sidebar.markdown("---")

menu_seleccionado = st.sidebar.selectbox(
    "Menú Principal",
    [
        "🎰 Tragamonedas Zafiro",
        "🎴 Memoria de Gemas",
        "⛏️ Caza de Gemas",
        "🎡 Ruleta de la Suerte",
        "🎁 Caja Misteriosa",
        "📺 Ver Videos Premiados",
        "👥 Invitar Amigos",
        "💸 Solicitar Retiro",
    ],
)

# --- JUEGO 1: TRAGAMONEDAS ZAFIRO ---
if menu_seleccionado == "🎰 Tragamonedas Zafiro":
  st.title("🎰 Tragamonedas Zafiro")
  st.write(
      "¡Gira los rodillos mágicos! Si logras alinear símbolos iguales, ganas"
      " recompensas masivas."
  )

  col_img1, col_img2, col_img3 = st.columns(3)
  with col_img2:
    st.image(
        "https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=300&auto=format&fit=crop&q=80",
        caption="¡Premio Mayor!",
        use_container_width=True,
    )

  st.info("🪙 Costo por giro: **1.50 💎**")

  if st.button("🚀 ¡Girar Tragamonedas Ahora!"):
    saldo_disp = get_saldo(usuario)
    if saldo_disp >= 1.50:
      simbolos = ["💎", "🍋", "⭐", "7️⃣", "🍒"]
      r1 = random.choice(simbolos)
      r2 = random.choice(simbolos)
      r3 = random.choice(simbolos)

      st.markdown(f"### Resultado: [ {r1} ] [ {r2} ] [ {r3} ]")

      premio = 0.0
      if r1 == r2 == r3:
        premio = 15.0  # ¡Jackpot!
        st.success(
            f"🎉 ¡JACKPOT! ¡Los tres símbolos coincidieron! Ganaste 💎 {premio}"
            " monedas."
        )
      elif r1 == r2 or r2 == r3 or r1 == r3:
        premio = 3.0  # Par ganador
        st.success(f"✨ ¡Bien! Dos símbolos iguales. Ganaste 💎 {premio} monedas.")
      else:
        st.warning(
            "😢 Casi lo logras, prueba suerte otra vez con los videos"
            " premiados."
        )

      nuevo_saldo = saldo_disp - 1.50 + premio
      update_saldo(usuario, nuevo_saldo)
      time.sleep(1.5)
      st.rerun()
    else:
      st.error(
          "❌ No tienes suficientes monedas. Ve a ver videos premiados para"
          " recargar."
      )

# --- JUEGO 2: MEMORIA DE GEMAS ---
elif menu_seleccionado == "🎴 Memoria de Gemas":
  st.title("🎴 Memoria de Gemas")
  st.write(
      "Elige una de las 3 cartas ocultas. Encuentra la carta dorada para triplicar"
      " tu apuesta."
  )

  st.info("🎟️ Costo de participación: **1.00 💎**")

  c1, c2, c3 = st.columns(3)
  saldo_disp = get_saldo(usuario)

  if saldo_disp >= 1.00:
    with c1:
      if st.button("🎴 Carta 1"):
        resultado_memoria(usuario, 1)
    with c2:
      if st.button("🎴 Carta 2"):
        resultado_memoria(usuario, 2)
    with c3:
      if st.button("🎴 Carta 3"):
        resultado_memoria(usuario, 3)
  else:
    st.error("❌ Saldo insuficiente para jugar a la Memoria de Gemas.")


def resultado_memoria(user, eleccion):
  ganadora = random.randint(1, 3)
  saldo_actual = get_saldo(user)
  if eleccion == ganadora:
    premio = 4.0
    update_saldo(user, saldo_actual - 1.0 + premio)
    st.success(
        f"🎉 ¡Adivinaste la carta ganadora (#{ganadora})! Ganaste 💎 {premio}"
        " monedas."
    )
  else:
    update_saldo(user, saldo_actual - 1.0)
    st.error(
        f"❌ Era la carta #{ganadora}. Perdiste 1.00 moneda. ¡Inténtalo de"
        " nuevo!"
    )
  time.sleep(1)
  st.rerun()


# --- JUEGO 3: CAZA DE GEMAS ---
elif menu_seleccionado == "⛏️ Caza de Gemas":
  st.title("⛏️ Caza de Gemas (Mina Subterránea)")
  st.write(
      "Selecciona una roca misteriosa para extraer gemas ocultas de la mina."
  )

  col1, col2, col3 = st.columns(3)
  with col1:
    if st.button("🪨 Roca A"):
      gema = random.choice([0.5, 2.5, 5.0])
      update_saldo(usuario, get_saldo(usuario) + gema)
      st.success(f"💎 ¡Exquisitos cristales encontrados! Ganaste {gema} monedas.")
      st.rerun()
  with col2:
    if st.button("🪨 Roca B"):
      gema = random.choice([1.0, 3.0, 6.0])
      update_saldo(usuario, get_saldo(usuario) + gema)
      st.success(f"💎 ¡Veta rica encontrada! Ganaste {gema} monedas.")
      st.rerun()
  with col3:
    if st.button("🪨 Roca C"):
      gema = random.choice([0.0, 2.0, 4.0])
      update_saldo(usuario, get_saldo(usuario) + gema)
      if gema > 0:
        st.success(f"💎 ¡Gema descubierta! Ganaste {gema} monedas.")
      else:
        st.warning("💨 ¡Roca vacía! Sigue cavando.")
      st.rerun()

# --- RULETA DE LA SUERTE ---
elif menu_seleccionado == "🎡 Ruleta de la Suerte":
  st.title("🎡 Ruleta de la Suerte")
  st.write("¡Gira la ruleta por un costo de 1.00 💎 y gana premios sorpresa!")

  if st.button("Girar Ruleta (Costo: 1.00 💎)"):
    saldo_actual = get_saldo(usuario)
    if saldo_actual >= 1.00:
      premio = random.choice([0.50, 2.00, 4.00, 8.00, 12.00])
      nuevo_saldo = saldo_actual - 1.00 + premio
      update_saldo(usuario, nuevo_saldo)
      st.success(f"🎉 ¡La ruleta giró y ganaste 💎 {premio:.2f} monedas!")
      st.rerun()
    else:
      st.error("No tienes suficientes monedas para girar la ruleta.")

# --- CAJA MISTERIOSA ---
elif menu_seleccionado == "🎁 Caja Misteriosa":
  st.title("🎁 Caja Misteriosa")
  st.write(
      "Abre una caja secreta patrocinada. Algunas tienen bonos sorpresa y"
      " otras están vacías."
  )
  if st.button("Abrir Caja Misteriosa"):
    premio_caja = random.choice([0.0, 2.5, 5.0, 10.0])
    nuevo_saldo = get_saldo(usuario) + premio_caja
    update_saldo(usuario, nuevo_saldo)
    if premio_caja > 0:
      st.success(f"🎁 ¡Sorpresa! La caja contenía 💎 {premio_caja:.2f} monedas.")
    else:
      st.warning(
          "Oh no, la caja estaba vacía. ¡Sigue intentando con los videos"
          " premiados!"
      )
    st.rerun()

# --- VIDEOS PREMIADOS ---
elif menu_seleccionado == "📺 Ver Videos Premiados":
  st.title("📺 Ver Videos Premiados")
  st.write(
      "Mira el contenido patrocinado y completa el contador para recibir"
      " recompensas automáticas."
  )

  if "viendo_video" not in st.session_state:
    st.session_state.viendo_video = False

  if not st.session_state.viendo_video:
    if st.button("▶️ Iniciar Video Premiado (+2.50 💎)"):
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

# --- INVITAR AMIGOS ---
elif menu_seleccionado == "Invitar Amigos":
  st.title("👥 Invitar Amigos")
  st.write(
      "Comparte tu enlace de referido para ganar 5.00 monedas por cada amigo"
      " que se registre."
  )
  st.code(f"https://zafirox-minijuegos.streamlit.app/?ref={usuario}")

# --- SOLICITAR RETIRO ---
elif menu_seleccionado == "💸 Solicitar Retiro":
  st.title("💸 Solicitar Retiro a Cuentas Reales")
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
          f"❌ Saldo insuficiente. El mínimo requerido es de **{minimo_retiro}"
          f" monedas** (Tienes {saldo_disp:.2f})."
      )
    elif not cuenta_destino.strip():
      st.error(f"❌ Por favor ingresa los datos correctos para {metodo_pago}.")
    else:
      nuevo_saldo_post_retiro = saldo_disp - minimo_retiro
      update_saldo(usuario, nuevo_saldo_post_retiro)
      st.success("🎉 ¡Solicitud de retiro enviada con éxito!")
      st.info(
          "Se ha procesado el envío de"
          f" **$ {minimo_retiro * tasa_conversion:.2f} USD** hacia tu cuenta"
          f" de **{metodo_pago}** ({cuenta_destino}). Plazo de 24-48 horas."
      )
      st.rerun()
