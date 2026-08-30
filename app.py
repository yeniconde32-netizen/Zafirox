import streamlit as st
import datetime
import random
import json
import os
import time

# Configuración de la página
st.set_page_config(
    page_title="Zafiro Vice Club - Economía Real",
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
    st.title("💎 Zafiro Vice Club - Acceso")
    st.write("Inicia sesión o regístrate para gestionar tu saldo y retiros en Vice City.")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        user_login = st.text_input("Usuario", key="login_user", placeholder="Tu nombre de usuario")
        pass_login = st.text_input("Contraseña", type="password", key="login_pass", placeholder="Tu contraseña")
        
        if st.button("Entrar a Zafiro Vice", key="btn_login"):
            db = st.session_state.usuarios_db
            if user_login in db and db[user_login]["password"] == pass_login:
                st.session_state.usuario_actual = user_login
                st.success(f"¡Bienvenido de nuevo a Vice City, {user_login}!")
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
                    st.success(f"¡Cuenta creada con éxito! Bienvenido al club, {user_reg}.")
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
    st.title("Zafiro Vice Club")
    st.write(f"Hola, **{usuario}** 👋")
    
    if st.button("🚪 Cerrar Sesión", key="btn_logout"):
        st.session_state.usuario_actual = None
        st.rerun()
        
    st.markdown("---")
    st.subheader("Menú Principal")
    
    opcion = st.selectbox(
        "Selecciona una sección:",
        [
            "📻 Radio Vice City (Emisoras 24/7)",
            "💎 Resumen de Saldo",
            "💣 Caza de Minas (Casino)",
            "🗝️ Cofres Misteriosos",
            "📦 Caja Misteriosa Clásica",
            "🎡 Ruleta de la Fortuna",
            "📺 Zona Multimedia & Educativa",
            "🎵 Vídeos Musicales en Streaming",
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

if opcion == "📻 Radio Vice City (Emisoras 24/7)":
    st.title("📻 Radio Vice City - Zafiro Vice Club")
    st.write("Sintoniza las emisoras oficiales con locutores inspirados en Vice City (**Emotion 98.3** y **Radio Espantoso**), comerciales falsos y música en vivo:")
    
    # Selector de emisora estilo Vice City
    estacion_emisora = st.selectbox(
        "Elige tu estación:",
        [
            "Emotion 98.3 (Baladas & Ochenteras)",
            "Radio Espantoso (Latin Groove & Salsa)"
        ]
    )
    
    if "Emotion 98.3" in estacion_emisora:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #2b1055, #7597de); padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
                <h4 style="margin: 0; color: #ff007f;">📻 Emotion 98.3 FM</h4>
                <p style="font-style: italic; margin-top: 8px; font-size: 14px;">
                "Siente el dolor, siente el amor... aquí en Emotion con Fernando Martínez. Para todos los apostadores de <strong>Zafiro Vice Club</strong> que perdieron la cabeza (y el saldo) en las tragamonedas, pero que siguen bailando bajo la lluvia de neón."
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #1b4332, #40916c); padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
                <h4 style="margin: 0; color: #ffb703;">📻 Radio Espantoso AM</h4>
                <p style="font-style: italic; margin-top: 8px; font-size: 14px;">
                "¡Ay, mamacita! ¡Sube el volumen de tu bólido en Vice City y muévete con Ramón Daboia! Si vas a retirar tus ganancias de <strong>Zafiro Vice Club</strong> por Nequi o PayPal, hazlo con sabor tropical, ¡qué caramba!"
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # HTML Interactivo con playlist y reproductor seguro anti-bloqueos (Tu enlace oficial de primero)
    mini_emisora_html = """
    <div style="background: #1e1e2f; padding: 20px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
        <h3 style="margin-top: 0; color: #00d2ff;">🎧 Transmisión en Vivo - Vice Waves</h3>
        <p id="nowPlaying" style="margin-top: 5px; font-size: 15px; color: #4cd137; font-weight: bold;">Selecciona una pista o dale Play</p>
        
        <audio id="zafiroRadio" controls style="width: 100%; border-radius: 8px; margin-top: 10px;"></audio>
        
        <div style="margin-top: 15px; display: flex; justify-content: center; gap: 15px;">
            <button onclick="prevTrack()" style="background: #651fff; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;">⏮️ Anterior</button>
            <button onclick="nextTrack()" style="background: #651fff; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px;">Siguiente ⏭️</button>
        </div>
    </div>

    <script>
        const playlist = [
            { name: "📻 Grabación Oficial Personalizada (Zafiro Vice)", url: "https://files.catbox.moe/lz5hd3.m4a" },
            { name: "📻 Emotion 98.3: Balada Ochentera & Neón", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" },
            { name: "🎺 Radio Espantoso: Ritmo Tropical & Salsa", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" },
            { name: "🎷 Emotion 98.3: Sintes Románticos de Medianoche", url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3" }
        ];

        let currentTrack = 0;
        const audioPlayer = document.getElementById('zafiroRadio');
        const nowPlayingText = document.getElementById('nowPlaying');

        function loadTrack(index) {
            if (index >= playlist.length) currentTrack = 0;
            if (index < 0) currentTrack = playlist.length - 1;
            else currentTrack = index;

            audioPlayer.src = playlist[currentTrack].url;
            nowPlayingText.innerText = "Reproduciendo: " + playlist[currentTrack].name;
        }

        function nextTrack() {
            loadTrack(currentTrack + 1);
            audioPlayer.play();
        }

        function prevTrack() {
            loadTrack(currentTrack - 1);
            audioPlayer.play();
        }

        audioPlayer.addEventListener('ended', function() {
            currentTrack = (currentTrack + 1) % playlist.length;
            loadTrack(currentTrack);
            audioPlayer.play();
        });

        loadTrack(currentTrack);
    </script>
    """
    
    st.components.v1.html(mini_emisora_html, height=240)
    
    with st.expander("📢 Comerciales Falsos de Vice City (Bloque Comercial)"):
        if "Emotion" in estacion_emisora:
            st.write(
                "**[SFX: Estática de radio y sonido de gaviotas de fondo]**\n\n"
                "*Locutor serio:* ¿Cansado de que el banco te ponga peros para tus retiros? "
                "En **Banco de Vice City**, tu dinero está seguro... o al menos hasta que el director tome un vuelo privado a las Bahamas. "
                "¡Invierta hoy, sufra mañana!"
            )
        else:
            st.write(
                "**[SFX: Sonido de bocina de camión y bongos tropicales]**\n\n"
                "*Locutor alegre:* ¡Amigo contrabandista y fan de las cajitas sorpresa! ¿Tu bólido quedó hecho un colador? "
                "Ven a **Chota-Repuestos**. Enderezamos chasis a punta de martillo y cinta de aislar. "
                "¡Pregunta por la garantía de una cuadra!"
            )
            
    st.markdown("---")
    st.markdown("#### Publicidad Patrocinada:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_musica_clave = f"{usuario}_radio_vice_city_247"
    
    if estado_musica_clave in st.session_state.musica_escuchada:
        st.button("🎵 Bonus de Emisora ya reclamado hoy", disabled=True, key="btn_musica_disabled")
    else:
        if st.button("🎵 Reclamar Bonus Radio Vice City (+0.003 💎)", key="btn_musica_claim"):
            st.session_state.musica_escuchada[estado_musica_clave] = True
            actualizar_saldo(0.003)
            st.success("✅ ¡Bonus de Radio Vice City acreditado!")
            time.sleep(0.8)
            st.rerun()

elif opcion == "💎 Resumen de Saldo":
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
            <p style="margin: 0; font-size: 14px; opacity: 0.9;">¡Domingo a las 6:00 p.m. se definen los ganadores semanales en Zafiro Vice Club!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    time.sleep(1)
    st.rerun()

elif opcion == "💣 Caza de Minas (Casino)":
    st.title("💣 Caza de Minas (Casino Vice)")
    st.write("Elige una casilla con cuidado. ¡Evita la mina escondida en Ocean Beach!")
    
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
    st.title("🎡 Ruleta de la Fortuna Zafiro Vice")
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

elif opcion == "📺 Zona Multimedia & Educativa":
    st.title("📺 Zona Multimedia & Educación")
    st.write("Disfruta de contenido clásico y cursos educativos con reproducción integrada:")
    
    multimedia_videos = {
        "⚔️ Anime Clásico - Tráiler / Recuerdo": "https://www.youtube.com/embed/9bZkp7q19f0",
        "🐉 Animación & Openings Legendarios": "https://www.youtube.com/embed/LXb3EKWsInQ",
        "📊 Curso Básico de Trading & Finanzas": "https://www.youtube.com/embed/tgbNymZ7vqY",
        "💡 Aprende Marketing Digital desde Cero": "https://www.youtube.com/embed/3JZ_D3ELwOQ"
    }
    
    item_seleccionado = st.selectbox("Selecciona tu contenido favorito:", list(multimedia_videos.keys()), key="select_multimedia")
    url_embed = multimedia_videos[item_seleccionado]
    
    st.info(f"👉 Reproduciendo: **{item_seleccionado}**")
    st.components.v1.iframe(url_embed, height=315, scrolling=False)
    
    st.markdown("---")
    st.markdown("#### Publicidad Patrocinada:")
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
    st.write("Disfruta de videoclips musicales variados con reproducción fluida:")
    
    videos_musicales = {
        "🎸 Rock & Pop Clásico (Hits Globales)": "https://www.youtube.com/embed/kJQP7kiw5Fk",
        "💃 Ritmos Latinos & Bailables": "https://www.youtube.com/embed/5mgos64VIGs",
        "⚡ Música Electrónica & Session": "https://www.youtube.com/embed/fJ9rUzIMcZQ",
        "🎵 Éxitos Variados del Momento": "https://www.youtube.com/embed/450p7goxZqg"
    }
    
    mus_elegida = st.selectbox("Elige un vídeo musical de la lista:", list(videos_musicales.keys()), key="select_musica_iframe")
    embed_mus_url = videos_musicales[mus_elegida]
    
    st.components.v1.iframe(embed_mus_url, height=315, scrolling=False)
    
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

elif opcion == "🔗 Invitar Amigos":
    st.title("🔗 Invitar Amigos a Zafiro Vice Club")
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
    st.success("¡Sigue participando para escalar posiciones en el ranking de Vice City!")

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
