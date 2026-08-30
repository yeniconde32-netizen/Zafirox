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

# --- OCULTAR MENÚ FLOTANTE Y BOTÓN DE STREAMLIT ---
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
div[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
            "saldo_cop": 0.0,
            "premio_reclamado_semana": False,
            "invitado_por": None,
            "referidos_propios": [],
            "telefono": "",
            "documento": "",
            "titular": "",
            "metodo_favorito": "Nequi (Colombia)"
        },
        "Carlos_99": {
            "password": "456", 
            "saldo": 10.00,
            "saldo_cop": 0.0,
            "premio_reclamado_semana": False,
            "invitado_por": "Lud337",
            "referidos_propios": [],
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

# Inicializar lista de solicitudes de retiro globales si no existe
if 'retiros_globales' not in st.session_state:
    st.session_state.retiros_globales = []

# --- CAPTURAR REFERIDO DE LA URL ---
params = st.query_params
if "ref" in params and st.session_state.usuario_actual is None:
    referidor = params["ref"]
    st.session_state.invitado_por = referidor

# --- PANTALLA DE LOGIN / REGISTRO ---
if st.session_state.usuario_actual is None:
    st.title("💎 Zafiro Vice Club - Acceso")
    st.write("Inicia sesión o regístrate para gestionar tu saldo y retiros con memoria persistente.")
    
    if "invitado_por" in st.session_state:
        st.info(f"🎁 Estás siendo invitado por el usuario: **{st.session_state.invitado_por}** (Recibirás un bono al registrarte).")
    
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
        
        # --- CAJA DE TEXTO PARA CÓDIGO DE REFERIDO MANUAL ---
        ref_por_url = st.session_state.get("invitado_por", "")
        codigo_invitado = st.text_input(
            "Código de Invitado / Patrocinador (Opcional)", 
            value=ref_por_url, 
            key="reg_patrocinador", 
            placeholder="Ej: Lud337"
        )
        
        if st.button("Crear Cuenta", key="btn_register"):
            if user_reg and pass_reg:
                db = st.session_state.usuarios_db
                if user_reg in db:
                    st.error("El usuario ya existe.")
                else:
                    patrocinador = codigo_invitado.strip() if codigo_invitado else None
                    
                    # Validar que el patrocinador exista realmente
                    if patrocinador and patrocinador not in db:
                        st.warning("⚠️ El código de patrocinador ingresado no existe. Se creará la cuenta sin referido.")
                        patrocinador = None

                    # Bono de bienvenida para el nuevo usuario
                    bono_inicial = 0.005 if patrocinador else 0.0
                    
                    db[user_reg] = {
                        "password": pass_reg, 
                        "saldo": bono_inicial, 
                        "saldo_cop": 0.0,
                        "premio_reclamado_semana": False,
                        "invitado_por": patrocinador,
                        "referidos_propios": [],
                        "telefono": "",
                        "documento": "",
                        "titular": "",
                        "metodo_favorito": "Nequi (Colombia)"
                    }
                    
                    # Registrar en la lista del patrocinador y darle su comisión
                    if patrocinador and patrocinador in db:
                        if "referidos_propios" not in db[patrocinador]:
                            db[patrocinador]["referidos_propios"] = []
                        if user_reg not in db[patrocinador]["referidos_propios"]:
                            db[patrocinador]["referidos_propios"].append(user_reg)
                        db[patrocinador]["saldo"] += 0.002 # Comisión inmediata

                    guardar_db(db)
                    st.session_state.usuario_actual = user_reg
                    st.success(f"¡Cuenta creada con éxito! Bienvenido al club, {user_reg}.")
                    st.rerun()
            else:
                st.warning("Completa todos los campos.")
    
    st.stop()

usuario = st.session_state.usuario_actual
st.session_state.usuarios_db = cargar_db()

# Seguridad por si el usuario actual fue borrado
if usuario not in st.session_state.usuarios_db:
    st.session_state.usuario_actual = None
    st.rerun()

datos_usuario = st.session_state.usuarios_db[usuario]
saldo_actual = datos_usuario["saldo"]
saldo_cop_actual = datos_usuario.get("saldo_cop", 0.0)

def actualizar_saldo(cantidad):
    nuevo_saldo = max(0.0, st.session_state.usuarios_db[usuario]["saldo"] + cantidad)
    st.session_state.usuarios_db[usuario]["saldo"] = nuevo_saldo
    guardar_db(st.session_state.usuarios_db)

def actualizar_saldo_cop(cantidad_cop):
    nuevo_saldo_cop = max(0.0, st.session_state.usuarios_db[usuario].get("saldo_cop", 0.0) + cantidad_cop)
    st.session_state.usuarios_db[usuario]["saldo_cop"] = nuevo_saldo_cop
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
    
    lista_opciones = [
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
    
    if usuario == "Lud337":
        lista_opciones.append("👑 Panel de Administración (Pagos & Control)")
    
    opcion = st.selectbox("Selecciona una sección:", lista_opciones)
    
    st.markdown("---")
    st.write("💎 **Tu Saldo Actual:**")
    st.metric(label="Diamantes", value=f"{saldo_actual:.4f} 💎")
    st.metric(label="Pesos Acumulados", value=f"${saldo_cop_actual:,.0f} COP")

    st.markdown("---")
    st.markdown("### Patrocinador")
    st.components.v1.html(banner_anuncio_html, height=120)

# --- CONTENIDO DE SECCIONES ---

if opcion == "📻 Radio Vice City (Emisoras 24/7)":
    st.title("📻 Zafiro Radio - Transmisión en Vivo")
    st.write("Disfruta de las emisoras originales de Vice City (con sus comerciales y estilo clásico) y las estaciones de Zafiro con música variada y aleatoria (electrónica, salsa y pop continuo):")
    
    lista_emisoras = [
        {
            "nombre": "📻 Zafiro Radio (Oficial Vice City - Con Comerciales)", 
            "url": "https://files.catbox.moe/lz5hd3.m4a", 
            "desc": "Emisora oficial con bloques comerciales clásicos de la ciudad.",
            "tipo": "vice_original"
        },
        {
            "nombre": "🎺 Radio Espantoso (Vice City - Salsa & Tropical)", 
            "url": "https://stream.zeno.fm/f3wvbbqmdg8uv", 
            "desc": "Música latina continua, salsa, ritmos tropicales y sabor caribeño de Vice City.",
            "tipo": "vice_original"
        },
        {
            "nombre": "💖 Emotion 98.3 (Vice City - Baladas & Pop Romántico)", 
            "url": "https://stream.zeno.fm/0r0xa792kwzuv", 
            "desc": "Éxitos suaves, pop nostálgico y baladas clásicas continuas de la época.",
            "tipo": "vice_original"
        },
        {
            "nombre": "⚡ Zafiro Trance & Electronic (Música Aleatoria 24/7)", 
            "url": "https://stream.zeno.fm/3g63w7k44cwtv", 
            "desc": "Pistas electrónicas y de baile continuas para acompañar tus ganancias en segundo plano.",
            "tipo": "zafiro_variada"
        },
        {
            "nombre": "🔮 Zafiro Club Beats & Mix Variado", 
            "url": "https://stream.zeno.fm/f3wvbbqmdg8uv", 
            "desc": "Selección aleatoria de éxitos variados, dance y energía para no parar.",
            "tipo": "zafiro_variada"
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
            <h4 style="margin: 0; color: #00d2ff;">{emisora_actual['nombre']}</h4>
            <p style="font-style: italic; margin-top: 5px; font-size: 13px;">{emisora_actual['desc']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.audio(emisora_actual["url"], format="audio/mp3")
    
    st.markdown("---")
    st.markdown("#### 📢 Espacio Publicitario Patrocinado (Apoya los pagos reales):")
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
    st.metric(label="Saldo Disponible en Diamantes", value=f"{saldo_actual:.4f} 💎")
    st.metric(label="Saldo Disponible en Pesos", value=f"${saldo_cop_actual:,.0f} COP")
    
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
    st.markdown("#### Patrocinador:")
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
    st.markdown("#### Patrocinador:")
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
    st.write("Comparte tu enlace de referido único y gana comisiones automáticas de **0.002 💎** por cada amigo registrado:")
    
    link_ref = f"https://zafirox-app.streamlit.app/?ref={usuario}"
    st.code(link_ref)
    st.info("¡Cada amigo que cree su cuenta con este enlace te sumará comisiones y engrosará tu comunidad!")
    
    mis_referidos = datos_usuario.get("referidos_propios", [])
    st.markdown(f"👥 **Tus referidos registrados hasta ahora:** `{len(mis_referidos)}` usuarios")
    if mis_referidos:
        for r in mis_referidos:
            st.write(f"- 👤 `{r}`")

elif opcion == "🏆 Competencia Semanal":
    st.title("🏆 Competencia Semanal de Usuarios")
    st.write("¡Los usuarios con más actividad de domingo a domingo se llevan premios directos en pesos colombianos (COP)! Además de tus ganancias diarias en actividades, puedes reclamar tu premio semanal aquí según tu posición:")
    
    st.markdown(
        """
        - 🥇 **1er Lugar:** $50,000 COP
        - 🥈 **2do Lugar:** $30,000 COP
        - 🥉 **3er Lugar:** $15,000 COP
        - 🏅 **Del 3er lugar hacia abajo (Participantes Activos):** Premios variables de **$1,000 COP**, **$500 COP** o **$100 COP**
        """
    )
    
    st.markdown("---")
    st.subheader("🎯 Reclamar Premio Semanal")
    
    premio_ya_reclamado = datos_usuario.get("premio_reclamado_semana", False)
    
    if premio_ya_reclamado:
        st.info("✅ Ya has reclamado tu recompensa de la competencia semanal en este ciclo. ¡Sigue activo para el siguiente!")
    else:
        puesto_seleccionado = st.selectbox(
            "Selecciona tu posición o categoría en el ranking semanal:",
            [
                "1er Lugar ($50,000 COP)",
                "2do Lugar ($30,000 COP)",
                "3er Lugar ($15,000 COP)",
                "Participante Activo ($1,000 COP)",
                "Participante Activo ($500 COP)",
                "Participante Activo ($100 COP)"
            ],
            key="select_puesto_semanal"
        )
        
        if st.button("🎁 Acreditar Mi Premio Semanal a Pesos", key="btn_reclamar_premio_semanal"):
            if "1er" in puesto_seleccionado:
                premio_monto = 50000.0
            elif "2do" in puesto_seleccionado:
                premio_monto = 30000.0
            elif "3er" in puesto_seleccionado:
                premio_monto = 15000.0
            elif "1,000" in puesto_seleccionado:
                premio_monto = 1000.0
            elif "500" in puesto_seleccionado:
                premio_monto = 500.0
            else:
                premio_monto = 100.0
                
            actualizar_saldo_cop(premio_monto)
            st.session_state.usuarios_db[usuario]["premio_reclamado_semana"] = True
            guardar_db(st.session_state.usuarios_db)
            
            st.success(f"🎉 ¡Felicidades! Se han sumado **${premio_monto:,.0f} COP** a tu saldo en pesos de manera persistente.")
            st.balloons()
            time.sleep(1.5)
            st.rerun()

elif opcion == "💸 Pasarela de Pagos (Nequi, Daviplata, PayPal, Bancos)":
    st.title("💸 Pasarela de Pagos y Retiros Seguros")
    st.write("Solicita el retiro de tus fondos. Las solicitudes pasan por un filtro de seguridad y revisión de administración antes de ser despachadas.")
    
    cop_por_usd = 4000
    total_diamantes_en_cop = saldo_actual * cop_por_usd
    saldo_total_disponible_cop = total_diamantes_en_cop + saldo_cop_actual
    
    st.info(
        f"💵 **Resumen de Fondos Disponibles:**\n\n"
        f"- Diamantes: **{saldo_actual:.4f} 💎** (Equivalente a ~${total_diamantes_en_cop:,.0f} COP)\n"
        f"- Saldo en Pesos (Premios): **${saldo_cop_actual:,.0f} COP**\n"
        f"--------------------------------------------------\n"
        f"- **Saldo Total Global Disponible:** **${saldo_total_disponible_cop:,.0f} COP**"
    )
    
    st.markdown("---")
    st.subheader("🛡️ Formulario de Solicitud de Retiro")
    
    metodos_disponibles = [
        "Nequi (Colombia)", 
        "Daviplata (Colombia)", 
        "PayPal (Dólares / Euros)", 
        "Transferencia Bancaria (Bancolombia / Davivienda / BBVA)", 
        "Convenio EPS / Subsidio de Salud"
    ]
    
    fav_guardado = datos_usuario.get("metodo_favorito", "Nequi (Colombia)")
    idx_fav = metodos_disponibles.index(fav_guardado) if fav_guardado in metodos_disponibles else 0
    
    metodo_pago = st.selectbox("Selecciona el método de destino:", metodos_disponibles, index=idx_fav, key="select_metodopago_completo")
    
    val_tel_guardado = datos_usuario.get("telefono", "")
    val_doc_guardado = datos_usuario.get("documento", "")
    val_titular_guardado = datos_usuario.get("titular", "")
    
    if "Nequi" in metodo_pago or "Daviplata" in metodo_pago:
        num_cuenta = st.text_input("Número de Celular (Cuenta Destino)", value=val_tel_guardado, placeholder="Ej: 3001234567", key="input_celular_wallet")
        titular = st.text_input("Nombre y Apellido del Titular", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_wallet")
        documento = st.text_input("Número de Cédula / Documento de Identidad", value=val_doc_guardado, placeholder="Ej: 1020304050", key="input_doc_wallet")
    elif "PayPal" in metodo_pago:
        num_cuenta = st.text_input("Correo Electrónico Asociado al PayPal", value=val_tel_guardado, placeholder="tucorreo@dominio.com", key="input_paypal_mail")
        titular = st.text_input("Nombre Completo del Titular PayPal", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_paypal")
        documento = st.text_input("País de Residencia", value=val_doc_guardado, placeholder="Ej: Colombia / México", key="input_doc_paypal")
    elif "Transferencia Bancaria" in metodo_pago:
        banco_elegido = st.selectbox("Entidad Bancaria:", ["Bancolombia", "Davivienda", "BBVA Colombia", "Nu Colombia"], key="select_banco")
        num_cuenta = st.text_input("Número de Cuenta", value=val_tel_guardado, placeholder="Ej: 03129847120", key="input_numbanco")
        titular = st.text_input("Titular de la Cuenta", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_banco")
        documento = st.text_input("Cédula del Titular", value=val_doc_guardado, placeholder="Ej: 1020304050", key="input_doc_banco")
    else:
        num_cuenta = st.text_input("Código de Afiliación EPS", value=val_tel_guardado, placeholder="Ej: EPS9988221", key="input_numeps")
        titular = st.text_input("Beneficiario Titular", value=val_titular_guardado, placeholder="Ej: Carlos Andrés Pérez", key="input_titular_eps")
        documento = st.text_input("Cédula de Ciudadanía", value=val_doc_guardado, placeholder="Ej: 1020304050", key="input_doc_eps")
        
    tipo_retiro = st.radio(
        "¿Qué deseas retirar?",
        [
            "Retirar Saldo en Pesos (Premios Semanales)",
            "Retirar Diamantes (Convertidos a COP)",
            "Retirar TODO el saldo combinado (Pesos + Diamantes)"
        ],
        key="radio_tipo_retiro"
    )
    
    if "Pesos" in tipo_retiro and "Combinado" not in tipo_retiro:
        monto_cop_retirar = st.number_input("Monto en Pesos (COP) a retirar", min_value=0.0, max_value=float(saldo_cop_actual), value=float(min(1000.0, saldo_cop_actual)), step=100.0, key="input_monto_cop")
    elif "Diamantes" in tipo_retiro:
        monto_diamantes_retirar = st.number_input("Monto en 💎 a retirar", min_value=0.0, max_value=float(saldo_actual), value=float(min(1.0, saldo_actual)), step=0.1, key="input_monto_diamantes")
    else:
        st.write(f"💼 **Se solicitará el retiro total:** ${saldo_total_disponible_cop:,.0f} COP")
        
    st.markdown("---")
    st.markdown("#### 📢 Interacción Publicitaria Requerida para Procesar Solicitud:")
    st.write("Para evitar spam y financiar la pasarela de pagos, por favor haz clic en el anuncio inferior antes de enviar tu solicitud:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    if st.button("🔒 Enviar Solicitud de Retiro a Administración", key="btn_enviar_solicitud"):
        if saldo_total_disponible_cop <= 0:
            st.error("❌ No tienes fondos disponibles para retirar.")
        elif not num_cuenta or not titular or not documento:
            st.warning("⚠️ Completa todos los campos de datos de destino.")
        else:
            st.session_state.usuarios_db[usuario]["telefono"] = num_cuenta
            st.session_state.usuarios_db[usuario]["documento"] = documento
            st.session_state.usuarios_db[usuario]["titular"] = titular
            st.session_state.usuarios_db[usuario]["metodo_favorito"] = metodo_pago
            
            if "Pesos" in tipo_retiro and "Combinado" not in tipo_retiro:
                monto_final_cop = monto_cop_retirar
                st.session_state.usuarios_db[usuario]["saldo_cop"] -= monto_cop_retirar
                desc_monto = f"${monto_cop_retirar:,.0f} COP"
            elif "Diamantes" in tipo_retiro:
                monto_final_cop = monto_diamantes_retirar * cop_por_usd
                st.session_state.usuarios_db[usuario]["saldo"] -= monto_diamantes_retirar
                desc_monto = f"💎 {monto_diamantes_retirar:.4f} (~${monto_final_cop:,.0f} COP)"
            else:
                monto_final_cop = saldo_total_disponible_cop
                st.session_state.usuarios_db[usuario]["saldo"] = 0.0
                st.session_state.usuarios_db[usuario]["saldo_cop"] = 0.0
                desc_monto = f"TOTAL: ${monto_final_cop:,.0f} COP"
                
            guardar_db(st.session_state.usuarios_db)
            
            solicitud_nueva = {
                "usuario": usuario,
                "metodo": metodo_pago,
                "cuenta": num_cuenta,
                "titular": titular,
                "documento": documento,
                "monto_texto": desc_monto,
                "monto_cop": monto_final_cop,
                "estado": "Pendiente de Aprobación"
            }
            st.session_state.retiros_globales.append(solicitud_nueva)
            
            st.success(
                f"✅ ¡Solicitud enviada con éxito!\n\n"
                f"Tus fondos han sido descontados y puestos en cola de revisión para transferencia por `{metodo_pago}`. "
                f"El administrador validará tu interacción publicitaria y despachará el pago a `{num_cuenta}`."
            )
            st.balloons()

# --- PANEL DE ADMINISTRACIÓN SEGURO CON CONTRASEÑA ---
if usuario == "Lud337" and opcion == "👑 Panel de Administración (Pagos & Control)":
    st.title("👑 Panel de Administración de Zafiro Vice")
    st.write("Zona restringida y blindada para el control financiero de la plataforma.")
    
    if "admin_autorizado" not in st.session_state:
        st.session_state.admin_autorizado = False
        
    if not st.session_state.admin_autorizado:
        st.warning("🔒 Esta sección requiere una Clave de Seguridad de Administrador.")
        clave_admin_ingresada = st.text_input("Introduce la Clave de Admin", type="password", key="input_clave_admin")
        
        if st.button("Desbloquear Panel", key="btn_desbloquear_admin"):
            # Puedes cambiar 'MiClaveSecreta123' por la contraseña que tú prefieras
            if clave_admin_ingresada == "MiClaveSecreta123":
                st.session_state.admin_autorizado = True
                st.success("✅ ¡Acceso concedido al Panel de Administración!")
                st.rerun()
            else:
                st.error("❌ Clave incorrecta. Acceso denegado.")
    else:
        if st.button("🔒 Bloquear Panel de Nuevo", key="btn_bloquear_admin"):
            st.session_state.admin_autorizado = False
            st.rerun()
            
        st.markdown("---")
        st.subheader("📥 Bandeja de Solicitudes de Retiro Pendientes")
        
        if not st.session_state.retiros_globales:
            st.info("No hay solicitudes de retiro pendientes en este momento.")
        else:
            for idx, sol in enumerate(st.session_state.retiros_globales):
                if sol["estado"] == "Pendiente de Aprobación":
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="background: #222530; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #ffcc00;">
                                <p style="margin: 0; font-weight: bold; color: #00d2ff;">Usuario: {sol['usuario']}</p>
                                <p style="margin: 5px 0;"><b>Método:</b> {sol['metodo']} | <b>Cuenta/Celular:</b> {sol['cuenta']}</p>
                                <p style="margin: 5px 0;"><b>Titular:</b> {sol['titular']} (Doc: {sol['documento']})</p>
                                <p style="margin: 5px 0; color: #00ffcc;"><b>Monto a Pagar:</b> {sol['monto_texto']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        col_aprob, col_rech = st.columns(2)
                        with col_aprob:
                            if st.button(f"✅ Aprobar Pago #{idx}", key=f"aprobar_{idx}"):
                                st.session_state.retiros_globales[idx]["estado"] = "Aprobado y Pagado"
                                st.success(f"¡Pago a {sol['usuario']} marcado como PAGADO!")
                                time.sleep(1)
                                st.rerun()
                        with col_rech:
                            if st.button(f"❌ Rechazar y Reintegrar #{idx}", key=f"rechazar_{idx}"):
                                db = cargar_db()
                                if sol['usuario'] in db:
                                    db[sol['usuario']]["saldo_cop"] += sol['monto_cop']
                                    guardar_db(db)
                                st.session_state.retiros_globales[idx]["estado"] = "Rechazado"
                                st.warning(f"Solicitud rechazada y fondos devueltos a {sol['usuario']}.")
                                time.sleep(1)
                                st.rerun()
                                
        st.markdown("---")
        st.subheader("👥 Base de Datos General de Usuarios Registrados")
        db_actual = cargar_db()
        st.write(f"Total de usuarios registrados en la plataforma: **{len(db_actual)}**")
        
        for u_name, u_data in db_actual.items():
            with st.expander(f"👤 {u_name} (Diamantes: {u_data.get('saldo', 0):.4f} | Pesos: ${u_data.get('saldo_cop', 0):,.0f})"):
                st.write(f"- **Patrocinador / Referido por:** {u_data.get('invitado_por', 'Ninguno')}")
                st.write(f"- **Referidos propios:** {len(u_data.get('referidos_propios', []))}")
                st.write(f"- **Método favorito:** {u_data.get('metodo_favorito', 'N/A')}")
                st.write(f"- **Teléfono / Cuenta guardada:** {u_data.get('telefono', 'No registrado')} (Doc: {u_data.get('documento', 'N/A')})")
