import streamlit as st
import datetime
import random
import json
import os
import time

# Configuración de la página
st.set_page_config(
    page_title="ZafiroX - Economía Real",
    page_icon="💎",
    layout="centered"
)

# --- CÓDIGO HTML PARA EL DISPLAY AD ---
banner_anuncio_html = """
<div style="text-align: center; margin: 10px 0; background: #1a1c23; padding: 12px; border-radius: 8px; min-height: 90px;">
    <p style="color: #888; font-size: 11px; margin-bottom: 5px;">Publicidad Patrocinada</p>
    <script async src="https://alwingulla.com/act/files/tag.min.js" data-zone="11679572" data-sdk="show_12345"></script>
</div>
"""

# --- ARCHIVO DE PERSISTENCIA ---
DB_FILE = "usuarios_db.json"

def cargar_db():
    """Carga la base de datos de usuarios desde el archivo JSON."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {
        "Lud337": {"password": "123", "saldo": 38.15},
        "Carlos_99": {"password": "456", "saldo": 10.00}
    }

def guardar_db(db):
    """Guarda la base de datos de usuarios en el archivo JSON de forma segura."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=4)
    except IOError:
        st.error("Error crítico: No se pudo guardar la base de datos. Los cambios podrían perderse.")

# Inicialización de session_state
if 'usuarios_db' not in st.session_state:
    st.session_state.usuarios_db = cargar_db()

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

if 'videos_vistos' not in st.session_state:
    st.session_state.videos_vistos = {}

if 'musica_escuchada' not in st.session_state:
    st.session_state.musica_escuchada = {}

# --- PANTALLA DE LOGIN / REGISTRO ---
if st.session_state.usuario_actual is None:
    st.title("💎 ZafiroX - Acceso de Usuarios")
    st.write("Inicia sesión o regístrate para gestionar tu saldo y retiros.")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        user_login = st.text_input("Usuario", key="login_user", placeholder="Tu nombre de usuario")
        pass_login = st.text_input("Contraseña", type="password", key="login_pass", placeholder="Tu contraseña")
        
        if st.button("Entrar a ZafiroX"):
            db = st.session_state.usuarios_db
            if user_login in db and db[user_login]["password"] == pass_login:
                st.session_state.usuario_actual = user_login
                st.success(f"¡Bienvenido de nuevo, {user_login}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
                
    with tab2:
        user_reg = st.text_input("Nuevo Usuario", key="reg_user", placeholder="Elige un usuario")
        pass_reg = st.text_input("Nueva Contraseña", type="password", key="reg_pass", placeholder="Elige una contraseña")
        if st.button("Crear Cuenta"):
            if user_reg and pass_reg:
                db = st.session_state.usuarios_db
                if user_reg in db:
                    st.error("El usuario ya existe.")
                else:
                    db[user_reg] = {"password": pass_reg, "saldo": 0.00}
                    guardar_db(db)
                    st.session_state.usuario_actual = user_reg
                    st.success(f"¡Cuenta creada con éxito! Bienvenido, {user_reg}.")
                    st.rerun()
            else:
                st.warning("Completa todos los campos.")
    
    st.stop()

# --- LOGICA DE SESIÓN ---
usuario = st.session_state.usuario_actual
st.session_state.usuarios_db = cargar_db()
saldo_actual = st.session_state.usuarios_db[usuario]["saldo"]

def actualizar_saldo(cantidad):
    """Actualiza el saldo del usuario actual y guarda en la DB."""
    nuevo_saldo = max(0.0, st.session_state.usuarios_db[usuario]["saldo"] + cantidad)
    st.session_state.usuarios_db[usuario]["saldo"] = nuevo_saldo
    guardar_db(st.session_state.usuarios_db)
    st.rerun()

# --- MENÚ LATERAL ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/controller.png", width=60)
    st.title("ZafiroX")
    st.write(f"Hola, **{usuario}** 👋")
    
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_actual = None
        st.rerun()
        
    st.markdown("---")
    st.subheader("Menú Principal")
    
    opcion = st.selectbox(
        "Selecciona una sección:",
        [
            "💎 Resumen de Saldo",
            "💣 Caza de Minas (Casino)",
            "🗝️ Cofres Misteriosos",
            "📦 Caja Misteriosa Clásica",
            "🎡 Ruleta de la Fortuna",
            "📺 Zona de Tráilers (Anime Clásico & Cómics)",
            "🎧 Estación de Música",
            "🔗 Invitar Amigos",
            "🏆 Competencia Semanal",
            "💸 Conversor y Retiros (Nequi / PayPal)"
        ]
    )
    
    st.markdown("---")
    st.write("💎 **Tu Saldo Actual:**")
    st.metric(label="", value=f"{saldo_actual:.4f} 💎")

    st.markdown("---")
    st.markdown("### Patrocinador")
    st.components.v1.html(banner_anuncio_html, height=120)

# --- CONTENIDO DE SECCIONES ---

if opcion == "💎 Resumen de Saldo":
    st.title("💎 Resumen de Saldo y Actividad")
    st.metric(label="Saldo Disponible", value=f"{saldo_actual:.4f} 💎")
    
    st.markdown("---")
    st.subheader("⏳ Tiempo Restante para Premios Semanales (Domingo a Domingo)")
    
    # Cálculo real del tiempo restante hasta el próximo domingo a la medianoche
    ahora = datetime.datetime.now()
    dias_para_domingo = (6 - ahora.weekday()) % 7
    if dias_para_domingo == 0 and (ahora.hour > 0 or ahora.minute > 0 or ahora.second > 0):
        dias_para_domingo = 7
    
    proximo_domingo = (ahora + datetime.timedelta(days=dias_para_domingo)).replace(hour=0, minute=0, second=0, microsecond=0)
    diferencia = proximo_domingo - ahora
    
    dias = diferencia.days
    horas = diferencia.seconds // 3600
    minutos = (diferencia.seconds % 3600) // 60
    
    # Contador regresivo grande en la pantalla principal
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #651fff, #3d5afe); padding: 20px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <h2 style="margin: 0; font-size: 24px; text-transform: uppercase; letter-spacing: 2px;">⏰ Cierre de Premios en:</h2>
            <p style="font-size: 38px; font-weight: bold; margin: 10px 0;">{dias} Días : {horas} Horas : {minutos} Min</p>
            <p style="margin: 0; font-size: 14px; opacity: 0.9;">¡Mantén tu lugar en el ranking de domingo a domingo para llevarte el gran premio!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.info(f"Bienvenido de nuevo, {usuario}. Utiliza el menú lateral para navegar por las secciones y generar recompensas.")

elif opcion == "💣 Caza de Minas (Casino)":
    st.title("💣 Caza de Minas (Casino)")
    st.write("Elige una casilla con cuidado. ¡Evita la mina escondida!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Casilla 1", key="mina_1"):
            premio = 0.002
            actualizar_saldo(premio)
            st.success(f"✅ ¡Casilla segura! Ganaste 💎 {premio:.4f}")
    with col2:
        if st.button("Casilla 2", key="mina_2"):
            premio = 0.002
            actualizar_saldo(premio)
            st.success(f"✅ ¡Casilla segura! Ganaste 💎 {premio:.4f}")
    with col3:
        if st.button("Casilla 3 (Peligro)", key="mina_3"):
            castigo = 0.003
            if saldo_actual >= castigo:
                actualizar_saldo(-castigo)
                st.error(f"💥 ¡Explosión! Perdiste 💎 {castigo:.4f}")
            else:
                st.warning("⚠️ Estás a 0, no hay saldo que restar.")

elif opcion == "🗝️ Cofres Misteriosos":
    st.title("🗝️ Cofres Misteriosos de Tensión")
    st.write("Elige un cofre para revelar tu recompensa oculta.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Abrir Cofre A", key="cofre_a"):
            premio = random.choice([0.001, 0.0005, 0.0000])
            if premio > 0:
                actualizar_saldo(premio)
                st.success(f"🎉 ¡Encontraste 💎 {premio:.4f}!")
            else:
                st.error("🚫 El cofre estaba vacío.")
    with c2:
        if st.button("Abrir Cofre B", key="cofre_b"):
            premio = random.choice([0.001, 0.0005, 0.0000])
            if premio > 0:
                actualizar_saldo(premio)
                st.success(f"🎉 ¡Encontraste 💎 {premio:.4f}!")
            else:
                st.error("🚫 El cofre estaba vacío.")

elif opcion == "📦 Caja Misteriosa Clásica":
    st.title("📦 Caja Misteriosa Clásica")
    if st.button("Abrir Caja", key="caja_clasica"):
        premio = random.choice([0.005, 0.001, 0.0005, 0.0000, 0.0000])
        if premio > 0:
            actualizar_saldo(premio)
            st.success(f"💎 ¡Felicidades! Encontraste 💎 {premio:.4f}")
        else:
            st.error("🪹 ¡Oh no! La caja estaba vacía.")

elif opcion == "🎡 Ruleta de la Fortuna":
    st.title("🎡 Ruleta de la Fortuna ZafiroX")
    st.write("¡Gira la ruleta mágica y prueba tu suerte para ganar premios instantáneos!")
    
    if st.button("🎲 ¡Girar Ruleta Ahora!", key="girar_ruleta"):
        premio_ruleta = random.choice([0.0005, 0.0010, 0.0020, 0.0050, 0.0100, 0.0000])
        if premio_ruleta > 0:
            actualizar_saldo(premio_ruleta)
            st.success(f"🎰 ¡La ruleta se detuvo y ganaste 💎 {premio_ruleta:.4f}!")
        else:
            st.warning("🔄 ¡Casi cae! Esta vez fue un giro nulo, ¡vuelve a intentar!")

elif opcion == "📺 Zona de Tráilers (Anime Clásico & Cómics)":
    st.title("📺 Zona de Tráilers y Resúmenes (Anime Clásico & Cómics)")
    st.write("Disfruta de los resúmenes y tráilers retro de anime clásico y cómics, y reclama tu recompensa:")
    
    # Enlaces de video estables y funcionales optimizados para reproductores web
    videos_retro = {
        "Resumen Retro: Anime Clásico 90s (Openings & Promos)": "https://www.w3schools.com/html/mov_bbb.mp4",
        "Tráiler Corto: Leyendas del Manga y Cómics": "https://www.w3schools.com/html/movie.mp4",
        "Especial Anime Antiguo: Joyas Ocultas": "https://www.w3schools.com/html/mov_bbb.mp4"
    }
    
    video_nombre = st.selectbox("Elige un contenido para ver:", list(videos_retro.keys()))
    url_video = videos_retro[video_nombre]
    
    st.video(url_video)
    
    st.markdown("---")
    st.markdown("#### Publicidad Monetag:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_video_clave = f"{usuario}_visto_{url_video}"
    
    if estado_video_clave in st.session_state.videos_vistos:
        st.button("🎁 Recompensa ya reclamada", disabled=True, key="btn_video_disabled")
    else:
        if st.button(f"🎁 Reclamar Recompensa (+0.005 💎)", key="btn_video_claim"):
            actualizar_saldo(0.005)
            st.session_state.videos_vistos[estado_video_clave] = True
            st.success("✅ ¡Recompensa acreditada con éxito!")
            st.rerun()

elif opcion == "🎧 Estación de Música":
    st.title("🎧 Estación de Música ZafiroX")
    st.write("Disfruta de la selección musical (estilo acústico/pop alegre como Jason Mraz y Bruno Mars) y reclama tu bonus:")
    
    pistas = {
        "Acústico Inspirador (Estilo Jason Mraz)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "Pop Alegre y Ritmo (Estilo Bruno Mars)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "Electro Dance (Energía)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "Melodía Suave de Guitarra": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"
    }
    
    pista_nombre = st.selectbox("Elige una pista de audio:", list(pistas.keys()))
    url_audio = pistas[pista_nombre]
    
    st.audio(url_audio)
    
    st.markdown("---")
    st.markdown("#### Publicidad Patrocinada:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_musica_clave = f"{usuario}_musica_{url_audio}"
    
    if estado_musica_clave in st.session_state.musica_escuchada:
        st.button("🎵 Bonus ya reclamado hoy", disabled=True, key="btn_musica_disabled")
    else:
        if st.button("🎵 Reclamar Bonus Musical (+0.003 💎)", key="btn_musica_claim"):
            actualizar_saldo(0.003)
            st.session_state.musica_escuchada[estado_musica_clave] = True
            st.success("✅ ¡Bonus musical acreditado!")
            st.rerun()

elif opcion == "🔗 Invitar Amigos":
    st.title("🔗 Invitar Amigos")
    st.write("Comparte tu enlace de referido único y gana un porcentaje de comisión sostenible:")
    link_ref = f"https://zafirox-app.streamlit.app/?ref={usuario}"
    st.code(link_ref)
    st.info("¡Cada amigo activo te otorga un bono directo en tu saldo!")

elif opcion == "🏆 Competencia Semanal":
    st.title("🏆 Competencia Semanal de Usuarios")
    st.write("¡Los usuarios con más actividad de domingo a domingo se llevan los premios acumulados altos!")
    
    st.markdown(
        """
        - 🥇 **1er Lugar:** $50.00 USD en Premios
        - 🥈 **2do Lugar:** $30.00 USD en Premios
        - 🥉 **3er Lugar:** $15.00 USD en Premios
        """
    )
    st.success("¡Sigue participando en las minas, ruleta, música y viendo los contenidos para escalar posiciones!")

elif opcion == "💸 Conversor y Retiros (Nequi / PayPal)":
    st.title("💸 Conversor de Divisas y Retiros")
    st.write("Convierte tus diamantes a moneda local o divisa internacional y solicita tu pago.")
    
    st.metric(label="Saldo Disponible en Diamantes", value=f"{saldo_actual:.4f} 💎")
    
    cop_por_usd = 4000
    eur_por_usd = 0.92
    
    total_cop = saldo_actual * cop_por_usd
    total_eur = saldo_actual * eur_por_usd
    
    st.info(f"💵 **Equivalencias aproximadas:**\n\n- En Pesos Colombianos (COP): **${total_cop:,.2f} COP**\n- En Euros (EUR): **€{total_eur:.2f} EUR**\n- En Dólares (USD): **${saldo_actual:.2f} USD**")
    
    st.markdown("---")
    st.subheader("Solicitar Retiro")
    
    metodo_pago = st.selectbox("Selecciona tu Método de Pago:", ["Nequi (Colombia)", "PayPal (Dólares USD)", "PayPal (Euros EUR)"])
    
    if "Nequi" in metodo_pago:
        num_cuenta = st.text_input("Número de cuenta para Nequi", placeholder="Ej: 3001234567")
    else:
        num_cuenta = st.text_input("Correo electrónico de tu cuenta PayPal", placeholder="tucorreo@dominio.com")
        
    monto_retirar = st.number_input("Monto en 💎 a retirar", min_value=0.0, max_value=float(saldo_actual), value=float(min(1.0, saldo_actual)), step=0.1)
    
    if st.button("📥 Enviar Solicitud de Retiro", key="btn_retirar"):
        if saldo_actual <= 0:
            st.error("❌ No tienes saldo disponible para retirar.")
        elif not num_cuenta:
            st.warning("⚠️ Por favor ingresa los datos de tu cuenta destino.")
        elif monto_retirar <= 0:
            st.warning("⚠️ El monto a retirar debe ser mayor a 0.")
        elif monto_retirar > saldo_actual:
            st.error("❌ No puedes retirar más de tu saldo actual.")
        else:
            st.session_state.usuarios_db[usuario]["saldo"] -= monto_retirar
            guardar_db(st.session_state.usuarios_db)
            st.success(f"🎉 ¡Solicitud de retiro por 💎 {monto_retirar:.4f} enviada con éxito a {metodo_pago}!")
            st.balloons()
            time.sleep(2)
            st.rerun()
