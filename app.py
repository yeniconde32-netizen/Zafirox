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
    try:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=4)
    except IOError:
        st.error("Error crítico: No se pudo guardar la base de datos.")

if 'usuarios_db' not in st.session_state:
    st.session_state.usuarios_db = cargar_db()

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

if 'videos_vistos' not in st.session_state:
    st.session_state.videos_vistos = {}

if 'musica_escuchada' not in st.session_state:
    st.session_state.musica_escuchada = {}

if 'videomusica_vista' not in st.session_state:
    st.session_state.videomusica_vista = {}

# --- PANTALLA DE LOGIN / REGISTRO ---
if st.session_state.usuario_actual is None:
    st.title("💎 ZafiroX - Acceso de Usuarios")
    st.write("Inicia sesión o regístrate para gestionar tu saldo y retiros.")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        user_login = st.text_input("Usuario", key="login_user", placeholder="Tu nombre de usuario")
        pass_login = st.text_input("Contraseña", type="password", key="login_pass", placeholder="Tu contraseña")
        
        if st.button("Entrar a ZafiroX", key="btn_login"):
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
        if st.button("Crear Cuenta", key="btn_register"):
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

usuario = st.session_state.usuario_actual
st.session_state.usuarios_db = cargar_db()
saldo_actual = st.session_state.usuarios_db[usuario]["saldo"]

def actualizar_saldo(cantidad):
    nuevo_saldo = max(0.0, st.session_state.usuarios_db[usuario]["saldo"] + cantidad)
    st.session_state.usuarios_db[usuario]["saldo"] = nuevo_saldo
    guardar_db(st.session_state.usuarios_db)

# --- MENÚ LATERAL ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/controller.png", width=60)
    st.title("ZafiroX")
    st.write(f"Hola, **{usuario}** 👋")
    
    if st.button("🚪 Cerrar Sesión", key="btn_logout"):
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
            "📺 Zona Multimedia (Anime, Carranga, Trading & Cine)",
            "🎵 Vídeos Musicales en Streaming",
            "🎧 Emisora ZafiroX (Pop, Rock & Hits en Vivo)",
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
    st.subheader("⏳ Tiempo Restante para el Sorteo (Domingo a las 6:00 PM)")
    
    ahora = datetime.datetime.now()
    dias_para_domingo = (6 - ahora.weekday()) % 7
    proximo_domingo = (ahora + datetime.timedelta(days=dias_para_domingo)).replace(hour=18, minute=0, second=0, microsecond=0)
    
    if ahora >= proximo_domingo:
        proximo_domingo += datetime.timedelta(days=7)
        
    diferencia = proximo_domingo - ahora
    dias = diferencia.days
    horas = diferencia.seconds // 3600
    minutos = (diferencia.seconds % 3600) // 60
    segundos = diferencia.seconds % 60
    
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #651fff, #3d5afe); padding: 20px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <h2 style="margin: 0; font-size: 22px; text-transform: uppercase; letter-spacing: 2px;">⏰ Cierre y Sorteo en:</h2>
            <p style="font-size: 34px; font-weight: bold; margin: 10px 0;">{dias} Días : {horas:02d}h : {minutos:02d}m : {segundos:02d}s</p>
            <p style="margin: 0; font-size: 14px; opacity: 0.9;">¡Domingo a las 6:00 p.m. se definen los ganadores semanales!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    time.sleep(1)
    st.rerun()

elif opcion == "💣 Caza de Minas (Casino)":
    st.title("💣 Caza de Minas (Casino)")
    st.write("Elige una casilla con cuidado. ¡Evita la mina escondida!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Casilla 1", key="mina_1"):
            actualizar_saldo(0.002)
            st.success("✅ ¡Casilla segura! Ganaste 💎 0.0020")
            time.sleep(0.8)
            st.rerun()
    with col2:
        if st.button("Casilla 2", key="mina_2"):
            actualizar_saldo(0.002)
            st.success("✅ ¡Casilla segura! Ganaste 💎 0.0020")
            time.sleep(0.8)
            st.rerun()
    with col3:
        if st.button("Casilla 3 (Peligro)", key="mina_3"):
            castigo = 0.003
            if saldo_actual >= castigo:
                actualizar_saldo(-castigo)
                st.error(f"💥 ¡Explosión! Perdiste 💎 {castigo:.4f}")
            else:
                st.warning("⚠️ Estás a 0, no hay saldo que restar.")
            time.sleep(0.8)
            st.rerun()

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
            time.sleep(0.8)
            st.rerun()
    with c2:
        if st.button("Abrir Cofre B", key="cofre_b"):
            premio = random.choice([0.001, 0.0005, 0.0000])
            if premio > 0:
                actualizar_saldo(premio)
                st.success(f"🎉 ¡Encontraste 💎 {premio:.4f}!")
            else:
                st.error("🚫 El cofre estaba vacío.")
            time.sleep(0.8)
            st.rerun()

elif opcion == "📦 Caja Misteriosa Clásica":
    st.title("📦 Caja Misteriosa Clásica")
    if st.button("Abrir Caja", key="caja_clasica"):
        premio = random.choice([0.005, 0.001, 0.0005, 0.0000, 0.0000])
        if premio > 0:
            actualizar_saldo(premio)
            st.success(f"💎 ¡Felicidades! Encontraste 💎 {premio:.4f}")
        else:
            st.error("🪹 ¡Oh no! La caja estaba vacía.")
        time.sleep(0.8)
        st.rerun()

elif opcion == "🎡 Ruleta de la Fortuna":
    st.title("🎡 Ruleta de la Fortuna ZafiroX")
    st.write("¡Gira la ruleta mágica y prueba tu suerte para ganar premios instantáneos!")
    
    if st.button("🎲 ¡Girar Ruleta Ahora!", key="girar_ruleta"):
        premio_ruleta = random.choice([0.0005, 0.0010, 0.0020, 0.0050, 0.0100, 0.0000])
        if premio_ruleta > 0:
            actualizar_saldo(premio_ruleta)
            st.success(f"🎰 ¡La ruleta giró y ganaste 💎 {premio_ruleta:.4f}!")
        else:
            st.warning("🔄 ¡Casi cae! Esta vez fue un giro nulo, ¡vuelve a intentar!")
        time.sleep(1)
        st.rerun()

elif opcion == "📺 Zona Multimedia (Anime, Carranga, Trading & Cine)":
    st.title("📺 Zona Multimedia Variada y Educativa")
    st.write("Disfruta de más de 10 opciones de contenido seleccionado: anime, música de Boyacá, finanzas, trading y estrenos de cine:")
    
    multimedia_videos = {
        "📊 Curso Básico de Trading & Finanzas Personales": "https://www.youtube.com/watch?v=1O_Cw_Ghjk0",
        "💡 Aprende a Monetizar y Hacer Marketing Digital": "https://www.youtube.com/watch?v=2v81g0IFO78",
        "🎻 Jorge Velosa y los Carrangueros de Ráquira (Carranga Boyacense)": "https://www.youtube.com/watch?v=3g56h8qL1Xo",
        "🎸 My Chemical Romance - Welcome to the Black Parade (Rock Hit)": "https://www.youtube.com/watch?v=kDWgsQhbaqU",
        "🎬 Tráiler Estreno Cine / Películas Nuevas": "https://www.youtube.com/watch?v=8Qn_spdM5Zg",
        "⛩️ Anime Opening Legendario (Colección Especial)": "https://www.youtube.com/watch?v=xMhNN7IwE60",
        "📈 Finanzas Exitosas y Estrategias de Dinero": "https://www.youtube.com/watch?v=6p_VFkk_Bl4",
        "🎵 Música Carranga Tradicional de Boyacá (Clásico)": "https://www.youtube.com/watch?v=5qap5aO4i9A",
        "🎸 Rock Alternativo Sesión Especial (Hits)": "https://www.youtube.com/watch?v=hTWKbfoikeg",
        "🚀 Tutorial Avanzado de Emprendimiento & Negocios": "https://www.youtube.com/watch?v=jfKfPfyJRdk"
    }
    
    item_seleccionado = st.selectbox("Selecciona tu contenido favorito:", list(multimedia_videos.keys()), key="select_multimedia")
    url_seleccionada = multimedia_videos[item_seleccionado]
    
    st.info(f"👉 Has seleccionado: **{item_seleccionado}**\n\nHaz clic en el siguiente botón para abrir y reproducir el contenido al instante sin bloqueos:")
    st.markdown(f'<a href="{url_seleccionada}" target="_blank"><button style="background-color:#651fff; color:white; padding:12px 20px; border:none; border-radius:8px; font-weight:bold; cursor:pointer; width:100%;">▶️ Reproducir Contenido en Pantalla Completa / YouTube</button></a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Publicidad Monetag:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_video_clave = f"{usuario}_multimedia_{item_seleccionado}"
    
    if estado_video_clave in st.session_state.videos_vistos:
        st.button("🎁 Recompensa ya reclamada", disabled=True, key="btn_video_disabled")
    else:
        if st.button(f"🎁 Reclamar Recompensa (+0.005 💎)", key="btn_video_claim"):
            st.session_state.videos_vistos[estado_video_clave] = True
            actualizar_saldo(0.005)
            st.success("✅ ¡Recompensa acreditada con éxito!")
            time.sleep(0.8)
            st.rerun()

elif opcion == "🎵 Vídeos Musicales en Streaming":
    st.title("🎵 Vídeos Musicales en Streaming")
    st.write("Disfruta de tus videoclips musicales favoritos y una selección ampliada con más éxitos:")
    
    videos_musicales = {
        "Videoclip Pop & Hits Globales": "https://www.youtube.com/embed/9bZkp7q19f0",
        "Videoclip Dance & Party Electrónica": "https://www.youtube.com/embed/kJQP7kiw5Fk",
        "Videoclip Rock & Alternative Vibes": "https://www.youtube.com/embed/hTWKbfoikeg",
        "Videoclip Synthwave & Retro Beats": "https://www.youtube.com/embed/4xDzrJKXOOY",
        "Videoclip Rock Clásico Internacional (Hits Adicionales)": "https://www.youtube.com/embed/kDWgsQhbaqU",
        "Videoclip Pop Latino & Urbano (Variedad)": "https://www.youtube.com/embed/kJQP7kiw5Fk"
    }
    
    mus_elegida = st.selectbox("Elige un vídeo musical de la lista:", list(videos_musicales.keys()), key="select_musica_iframe")
    embed_mus_url = videos_musicales[mus_elegida]
    
    st.markdown(
        f"""
        <div style="position: relative; width: 100%; height: 315px; margin-bottom: 15px;">
            <iframe src="{embed_mus_url}?enablejsapi=1&autoplay=0&rel=0" title="Reproductor ZafiroX" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width: 100%; height: 100%; border-radius: 10px;"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("#### Publicidad Patrocinada:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_vidmus_clave = f"{usuario}_vidmus_{mus_elegida}"
    
    if estado_vidmus_clave in st.session_state.videomusica_vista:
        st.button("🎥 Vídeo musical ya reclamado", disabled=True, key="btn_vidmus_disabled")
    else:
        if st.button("🎥 Reclamar Bonus de Vídeo Musical (+0.004 💎)", key="btn_vidmus_claim"):
            st.session_state.videomusica_vista[estado_vidmus_clave] = True
            actualizar_saldo(0.004)
            st.success("✅ ¡Bonus de vídeo musical acreditado!")
            time.sleep(0.8)
            st.rerun()

elif opcion == "🎧 Emisora ZafiroX (Pop, Rock & Hits en Vivo)":
    st.title("🎧 Emisora ZafiroX - Estación de Radio Oficial")
    st.write("Conéctate a la emisora oficial de la app. Disfruta de la mejor selección musical continua con artistas de pop, rock, My Chemical Romance y éxitos variados:")
    
    pistas = {
        "📻 01. Emisora ZafiroX Pop & Hits Globales (En Vivo)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🎸 02. Rock Alternativo & Energía Estilo My Chemical Romance": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "🎤 03. Pop Comercial & Ritmo Suave Internacional": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "⚡ 04. Rock & Roll Session (Estilo Radio FM)": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "🎹 05. Balada Pop & Melodías Acústicas": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
        "🎧 06. Electronic & Pop Mix Especial": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
        "🔥 07. Rock Classics & Power Chords": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
        "🌟 08. Top Hits Modern Pop Session": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3"
    }
    
    pista_nombre = st.selectbox("Selecciona una pista de la emisora:", list(pistas.keys()), key="select_pista")
    url_audio = pistas[pista_nombre]
    
    st.audio(url_audio)
    
    st.markdown("---")
    st.markdown("#### Publicidad Patrocinada:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_musica_clave = f"{usuario}_musica_{pista_nombre}"
    
    if estado_musica_clave in st.session_state.musica_escuchada:
        st.button("🎵 Bonus musical ya reclamado hoy", disabled=True, key="btn_musica_disabled")
    else:
        if st.button("🎵 Reclamar Bonus Musical (+0.003 💎)", key="btn_musica_claim"):
            st.session_state.musica_escuchada[estado_musica_clave] = True
            actualizar_saldo(0.003)
            st.success("✅ ¡Bonus musical acreditado!")
            time.sleep(0.8)
            st.rerun()

elif opcion == "🔗 Invitar Amigos":
    st.title("🔗 Invitar Amigos")
    st.write("Comparte tu enlace de referido único y gana comisiones:")
    link_ref = f"https://zafirox-app.streamlit.app/?ref={usuario}"
    st.code(link_ref)
    st.info("¡Cada amigo activo te otorga un bono directo en tu saldo!")

elif opcion == "🏆 Competencia Semanal":
    st.title("🏆 Competencia Semanal de Usuarios")
    st.write("¡Los usuarios con más actividad de domingo a domingo se llevan premios altos!")
    
    st.markdown(
        """
        - 🥇 **1er Lugar:** $50.00 USD en Premios
        - 🥈 **2do Lugar:** $30.00 USD en Premios
        - 🥉 **3er Lugar:** $15.00 USD en Premios
        """
    )
    st.success("¡Sigue participando para escalar posiciones!")

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
    
    metodo_pago = st.selectbox("Selecciona tu Método de Pago:", ["Nequi (Colombia)", "PayPal (Dólares USD)", "PayPal (Euros EUR)"], key="select_metodopago")
    
    if "Nequi" in metodo_pago:
        num_cuenta = st.text_input("Número de cuenta para Nequi", placeholder="Ej: 3001234567", key="input_nequi")
    else:
        num_cuenta = st.text_input("Correo electrónico de tu cuenta PayPal", placeholder="tucorreo@dominio.com", key="input_paypal")
        
    monto_retirar = st.number_input("Monto en 💎 a retirar", min_value=0.0, max_value=float(saldo_actual), value=float(min(1.0, saldo_actual)), step=0.1, key="input_monto")
    
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
