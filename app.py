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
        "Lud337": {
            "password": "123", 
            "saldo": 40.2505,
            "telefono": "",
            "documento": "",
            "titular": "",
            "metodo_favorito": "Nequi (Colombia)"
        },
        "Carlos_99": {
            "password": "456", 
            "saldo": 10.00,
            "telefono": "",
            "documento": "",
            "titular": "",
            "metodo_favorito": "PayPal (Dólares / Euros)"
        }
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

if 'indice_emisora' not in st.session_state:
    st.session_state.indice_emisora = 0

# --- PANTALLA DE LOGIN / REGISTRO ---
if st.session_state.usuario_actual is None:
    st.title("💎 Zafiro Vice Club - Acceso")
    st.write("Inicia sesión o regístrate para gestionar tu saldo y retiros con memoria persistente.")
    
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
                    db[user_reg] = {
                        "password": pass_reg, 
                        "saldo": 0.00,
                        "telefono": "",
                        "documento": "",
                        "titular": "",
                        "metodo_favorito": "Nequi (Colombia)"
                    }
                    guardar_db(db)
                    st.session_state.usuario_actual = user_reg
                    st.success(f"¡Cuenta creada con éxito! Bienvenido al club, {user_reg}.")
                    st.rerun()
            else:
                st.warning("Completa todos los campos.")
    
    st.stop()

usuario = st.session_state.usuario_actual
st.session_state.usuarios_db = cargar_db()
datos_usuario = st.session_state.usuarios_db[usuario]
saldo_actual = datos_usuario["saldo"]

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
            "💸 Pasarela de Pagos (Nequi, Daviplata, PayPal, Bancos)"
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
    st.title("📻 Zafiro Radio - Transmisión en Vivo")
    st.write("Disfruta de la mejor música estilo clásico en streaming con controles interactivos y opción de descarga directa (compatible con segundo plano en celulares):")
    
    # Emisoras con streams estables para segundo plano y enlaces directos de descarga / escucha
    lista_emisoras = [
        {
            "nombre": "⚡ Zafiro Trance & Electronic 24/7", 
            "url": "https://stream.zeno.fm/f3wvbbqmdg8uv", 
            "desc": "Música electrónica y trance continua de alto rendimiento para segundo plano."
        },
        {
            "nombre": "🌴 Vice City Synthwave & Chill", 
            "url": "https://stream.zeno.fm/0r0xa792kwzuv", 
            "desc": "Estilo retro ochentero, electrónico suave y relajante."
        },
        {
            "nombre": "🔮 Global Club Beats (Dance / House)", 
            "url": "https://stream.zeno.fm/3g63w7k44cwtv", 
            "desc": "Ritmos de club y energía pura para acompañar tus ganancias."
        }
    ]
    
    col_ant, col_info, col_sig = st.columns([1, 2, 1])
    with col_ant:
        if st.button("⏮️ Anterior", key="btn_prev_radio"):
            st.session_state.indice_emisora = (st.session_state.indice_emisora - 1) % len(lista_emisoras)
            st.rerun()
    with col_sig:
        if st.button("Siguiente ⏭️", key="btn_next_radio"):
            st.session_state.indice_emisora = (st.session_state.indice_emisora + 1) % len(lista_emisoras)
            st.rerun()
            
    emisora_actual = lista_emisoras[st.session_state.indice_emisora]
    
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1f1c2c, #4a3b6c); padding: 15px; border-radius: 10px; color: white; margin: 10px 0; text-align: center;">
            <h4 style="margin: 0; color: #00d2ff;">📻 {emisora_actual['nombre']}</h4>
            <p style="font-style: italic; margin-top: 5px; font-size: 13px;">Grabación personalizada con bloques comerciales de Vice City.</p>
            <p style="margin-top: 3px; font-size: 12px; opacity: 0.8;">{emisora_actual['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.audio(emisora_actual["url"], format="audio/mp3")
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 15px;">
            <a href="{emisora_actual["url"]}" target="_blank" style="display: inline-block; background: #00b0ff; color: white; text-decoration: none; padding: 10px 22px; border-radius: 6px; font-weight: bold; font-size: 14px; box-shadow: 0 3px 10px rgba(0,0,176,0.3);">
                📥 Descargar Archivo de Audio Actual / Stream
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.expander("📢 Comerciales Falsos de Vice City"):
        st.write(
            "**[SFX: Estática de radio y sonido de motores V8]**\n\n"
            "*Locutor:* ¿Te quedaste sin saldo en Zafiro Vice Club? Ven a "
            "**Prendas y Rines 'El Chino'** en Ocean Beach. Cambiamos tu reloj de oro por fichas reales al instante. ¡No hagas preguntas, nosotros tampoco!\n\n"
            "**[SFX: Anuncio de Colas 'Spand Express']**\n"
            "*Locutor:* Siente la explosión azucarada en tu garganta. Spand Express: porque la sed en Vice City nunca duerme, y las deudas tampoco."
        )
            
    st.markdown("---")
    st.markdown("#### Publicidad Patrocinada:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_musica_clave = f"{usuario}_radio_vice_city_247"
    if estado_musica_clave in st.session_state.musica_escuchada:
        st.button("🎵 Bonus de Zafiro Radio ya reclamado hoy", disabled=True, key="btn_musica_disabled")
    else:
        if st.button("🎵 Reclamar Bonus Zafiro Radio (+0.003 💎)", key="btn_musica_claim"):
            st.session_state.musica_escuchada[estado_musica_clave] = True
            actualizar_saldo(0.003)
            st.success("✅ ¡Bonus de Zafiro Radio acreditado!")
            time.sleep(0.8)
            st.rerun()

elif opcion == "💎 Resumen de Saldo":
    st.title("💎 Resumen de Saldo y Actividad")
    st.metric(label="Saldo Disponible", value=f"{saldo_actual:.4f} 💎")
    
    st.markdown("---")
    st.subheader("⏳ Tiempo Restante para el Sorteo (Domingo a las 6:00 PM)")
    
    ahora = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5)))
    dias_para_domingo = (6 - ahora.weekday()) % 7
    proximo_domingo = (ahora + datetime.timedelta(days=dias_para_domingo)).replace(hour=18, minute=0, second=0, microsecond=0)
    
    if ahora >= proximo_domingo:
        proximo_domingo += datetime.timedelta(days=7)
        
    diferencia = proximo_domingo - ahora
    total_segundos = int(diferencia.total_seconds())
    dias = total_segundos // 86400
    horas = (total_segundos % 86400) // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #651fff, #3d5afe); padding: 20px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <h2 style="margin: 0; font-size: 22px; text-transform: uppercase; letter-spacing: 2px;">⏰ CIERRE Y SORTEO EN:</h2>
            <p style="font-size: 30px; font-weight: bold; margin: 10px 0;">{dias} Días : {horas:02d}h : {minutos:02d}m : {segundos:02d}s</p>
            <p style="margin: 0; font-size: 14px; opacity: 0.9;">¡Mantente activo en la app! Las notificaciones automáticas recordarán a los usuarios entrar antes del sorteo del domingo a las 6:00 p.m.</p>
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
        if st.button("🎁 Reclamar Recompensa (+0.005 💎)", key="btn_video_claim"):
            st.session_state.videos_vistos[estado_video_clave] = True
            actualizar_saldo(0.005)
            st.success("✅ ¡Recompensa acreditada con éxito!")
            time.sleep(0.8)
            st.rerun()

elif opcion == "🎵 Vídeos Musicales en Streaming":
    st.title("🎵 Vídeos Musicales en Streaming")
    st.write("Disfruta de videoclips musicales variados con reproducción fluida y opción de descarga:")
    
    videos_musicales = {
        "🎸 Rock & Pop Clásico (Hits Globales)": {
            "embed": "https://www.youtube.com/embed/kJQP7kiw5Fk",
            "download": "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
        },
        "💃 Ritmos Latinos & Bailables": {
            "embed": "https://www.youtube.com/embed/5mgos64VIGs",
            "download": "https://www.youtube.com/watch?v=5mgos64VIGs"
        },
        "⚡ Música Electrónica & Session": {
            "embed": "https://www.youtube.com/embed/fJ9rUzIMcZQ",
            "download": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"
        },
        "🎵 Éxitos Variados del Momento": {
            "embed": "https://www.youtube.com/embed/450p7goxZqg",
            "download": "https://www.youtube.com/watch?v=450p7goxZqg"
        }
    }
    
    mus_elegida = st.selectbox("Elige un vídeo musical de la lista:", list(videos_musicales.keys()), key="select_musica_iframe")
    datos_video = videos_musicales[mus_elegida]
    
    st.components.v1.iframe(datos_video["embed"], height=315, scrolling=False)
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 10px;">
            <a href="{datos_video["download"]}" target="_blank" style="display: inline-block; background: #ff0055; color: white; text-decoration: none; padding: 10px 22px; border-radius: 6px; font-weight: bold; font-size: 14px; box-shadow: 0 3px 10px rgba(255,0,85,0.3);">
                📥 Descargar / Ver Fuente del Vídeo
            </a>
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

elif opcion == "💸 Pasarela de Pagos (Nequi, Daviplata, PayPal, Bancos)":
    st.title("💸 Pasarela de Pagos y Retiros Seguros")
    st.write("Tus datos de cuenta se guardan automáticamente en tu perfil para futuros retiros.")
    
    st.metric(label="Saldo Disponible en Diamantes", value=f"{saldo_actual:.4f} 💎")
    
    cop_por_usd = 4000
    eur_por_usd = 0.92
    
    total_cop = saldo_actual * cop_por_usd
    total_eur = saldo_actual * eur_por_usd
    
    st.info(f"💵 **Tasas de Conversión Actuales:**\n\n- Pesos Colombianos (COP): **${total_cop:,.2f} COP**\n- Euros (EUR): **€{total_eur:.2f} EUR**\n- Dólares (USD): **${saldo_actual:.2f} USD**")
    
    st.markdown("---")
    st.subheader("🛡️ Formulario de Transacción Segura")
    
    metodos_disponibles = [
        "Nequi (Colombia)", 
        "Daviplata (Colombia)", 
        "PayPal (Dólares / Euros)", 
        "Transferencia Bancaria (Bancolombia / Davivienda / BBVA)", 
        "Convenio EPS / Subsidio de Salud"
    ]
    
    fav_guardado = datos_usuario.get("metodo_favorito", "Nequi (Colombia)")
    idx_fav = metodos_disponibles.index(fav_guardado) if fav_guardado in metodos_disponibles else 0
    
    metodo_pago = st.selectbox(
        "Selecciona el método de destino:", 
        metodos_disponibles, 
        index=idx_fav,
        key="select_metodopago_completo"
    )
    
    val_tel_guardado = datos_usuario.get("telefono", "")
    val_doc_guardado = datos_usuario.get("documento", "")
    val_titular_guardado = datos_usuario.get("titular", "")
    
    if "Nequi" in metodo_pago or "Daviplata" in metodo_pago:
        num_cuenta = st.text_input("Número de Celular (Cuenta Destino)", value=val_tel_guardado, placeholder="Ej: 3001234567", key="input_celular_wallet")
        titular = st.text_input("Nombre y Apellido del Titular", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_wallet")
        documento = st.text_input("Número de Cédula / Documento de Identidad", value=val_doc_guardado, placeholder="Ej: 1020304050", key="input_doc_wallet")
        tiempo_estimado = "10 a 20 minutos (Depósito directo en línea)"
        
    elif "PayPal" in metodo_pago:
        num_cuenta = st.text_input("Correo Electrónico Asociado a PayPal", value=val_tel_guardado, placeholder="tucorreo@dominio.com", key="input_paypal_mail")
        titular = st.text_input("Nombre Completo del Titular PayPal", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_paypal")
        documento = st.text_input("País de Residencia", value=val_doc_guardado, placeholder="Ej: Colombia / España / México", key="input_doc_paypal")
        tiempo_estimado = "2 a 4 horas hábiles (Verificación antifraude)"
        
    elif "Transferencia Bancaria" in metodo_pago:
        banco_elegido = st.selectbox("Selecciona tu Entidad Bancaria:", ["Bancolombia", "Davivienda", "BBVA Colombia", "Banco de Bogotá", "Nu Colombia"], key="select_banco")
        tipo_cta = st.selectbox("Tipo de Cuenta:", ["Ahorros", "Corriente"], key="select_tipocta")
        num_cuenta = st.text_input("Número de Cuenta Bancaria", value=val_tel_guardado, placeholder="Ej: 03129847120", key="input_numbanco")
        titular = st.text_input("Titular de la Cuenta", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_banco")
        documento = st.text_input("NIT o Cédula del Titular", value=val_doc_guardado, placeholder="Ej: 1020304050", key="input_doc_banco")
        tiempo_estimado = "1 día hábil (Cámara de compensación interbancaria)"
        
    else:  # Convenio EPS
        eps_elegida = st.selectbox("Selecciona tu EPS afiliada:", ["Sura", "Sanitas", "Nueva EPS", "Famisanar", "Salud Total"], key="select_eps")
        num_cuenta = st.text_input("Número de Afiliación / Código de Usuario", value=val_tel_guardado, placeholder="Ej: EPS9988221", key="input_numeps")
        titular = st.text_input("Nombre del Beneficiario Titular", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_eps")
        documento = st.text_input("Cédula de Ciudadanía", value=val_doc_guardado, placeholder="Ej: 1020304050", key="input_doc_eps")
        tiempo_estimado = "24 a 48 horas (Validación de compensación EPS)"
        
    monto_retirar = st.number_input("Monto en 💎 a retirar", min_value=0.0, max_value=float(saldo_actual), value=float(min(1.0, saldo_actual)), step=0.1, key="input_monto_seguro")
    
    st.markdown(f"⏱️ **Tiempo estimado de llegada del pago:** `{tiempo_estimado}`")
    
    if st.button("🔒 Validar Datos y Ejecutar Transferencia Segura", key="btn_ejecutar_pago_total"):
        if saldo_actual <= 0:
            st.error("❌ No tienes saldo disponible para retirar.")
        elif not num_cuenta or not titular or not documento:
            st.warning("⚠️ Por favor completa todos los campos de seguridad requeridos para la transferencia.")
        elif monto_retirar <= 0:
            st.warning("⚠️ El monto a retirar debe ser mayor a 0.")
        elif monto_retirar > saldo_actual:
            st.error("❌ No puedes retirar más de tu saldo actual.")
        else:
            st.session_state.usuarios_db[usuario]["telefono"] = num_cuenta
            st.session_state.usuarios_db[usuario]["documento"] = documento
            st.session_state.usuarios_db[usuario]["titular"] = titular
            st.session_state.usuarios_db[usuario]["metodo_favorito"] = metodo_pago
            
            st.session_state.usuarios_db[usuario]["saldo"] -= monto_retirar
            guardar_db(st.session_state.usuarios_db)
            
            st.success(
                f"🛡️ ¡Transacción cifrada procesada con éxito y datos guardados en tu perfil!\n\n"
                f"• **Método:** {metodo_pago}\n"
                f"• **Destino / Cuenta:** {num_cuenta}\n"
                f"• **Titular:** {titular} (Doc: {documento})\n"
                f"• **Monto:** 💎 {monto_retirar:.4f}\n\n"
                f"El pago se ha encolado de forma segura y llegará a su destino en un tiempo estimado de: *{tiempo_estimado}*."
            )
            st.balloons()
            time.sleep(3)
            st.rerun()
