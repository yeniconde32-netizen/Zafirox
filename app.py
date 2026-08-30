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
    st.write("Disfruta de las emisoras originales de Vice City (con sus locuciones y anuncios) y las emisoras de Zafiro con **música alegre, variada y continua en segundo plano** (compatibles con streaming directo):")
    
    # Lista actualizada con enlaces robustos de streaming continuo para segundo plano y emisoras originales
    lista_emisoras = [
        {
            "nombre": "📻 Zafiro Radio (Oficial Vice City - Con Comerciales)", 
            "url": "https://files.catbox.moe/lz5hd3.m4a", 
            "desc": "Grabación personalizada con bloques comerciales clásicos de Vice City.",
            "tipo": "vice_original"
        },
        {
            "nombre": "🎺 Radio Espantoso (Vice City - Salsa & Tropical)", 
            "url": "https://stream.zeno.fm/f3wvbbqmdg8uv", 
            "desc": "Salsa clásica, ritmos latinos y sabor tropical continuo de Vice City.",
            "tipo": "vice_original"
        },
        {
            "nombre": "💖 Emotion 98.3 (Vice City - Baladas & Pop Romántico)", 
            "url": "https://stream.zeno.fm/0r0xa792kwzuv", 
            "desc": "Éxitos suaves, pop nostálgico y baladas románticas continuas.",
            "tipo": "vice_original"
        },
        {
            "nombre": "🎉 Zafiro Fiesta & Latin Mix (Música Alegre 24/7)", 
            "url": "https://stream.zeno.fm/3g63w7k44cwtv", 
            "desc": "Música alegre, variada y bailable en alta definición para segundo plano.",
            "tipo": "zafiro_variada"
        },
        {
            "nombre": "⚡ Zafiro Club Electronic & Dance Mix", 
            "url": "https://stream.zeno.fm/f3wvbbqmdg8uv", 
            "desc": "Pistas electrónicas dinámicas y continuas para acompañar tus ganancias.",
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
    
    # Reproductor HTML5 optimizado con atributos de reproducción continua y streaming nativo
    reproductor_html = f"""
    <div style="text-align: center; background: #111318; padding: 15px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #333;">
        <audio controls autoplay preload="auto" style="width: 100%; max-width: 400px;">
            <source src="{emisora_actual["url"]}" type="audio/mpeg">
            <source src="{emisora_actual["url"]}" type="audio/mp4">
            Tu navegador no soporta el reproductor de audio en directo.
        </audio>
        <p style="color: #aaa; font-size: 11px; margin-top: 8px;">💡 <em>Consejo móvil:</em> Puedes minimizar o cambiar de sección en la app y el audio continuará reproduciéndose en segundo plano.</p>
    </div>
    """
    st.components.v1.html(reproductor_html, height=110)
    
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 10px;">
            <a href="{emisora_actual["url"]}" download="Zafiro_Stream_Audio" target="_blank" style="display: inline-block; background: #00b0ff; color: white; text-decoration: none; padding: 10px 22px; border-radius: 6px; font-weight: bold; font-size: 14px; box-shadow: 0 3px 10px rgba(0,0,176,0.3);">
                📥 Descargar / Abrir Archivo de Audio
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Mostrar comerciales solo si es la emisora oficial de Zafiro Vice
    if emisora_actual["tipo"] == "vice_original":
        with st.expander("📢 Comerciales Falsos y Locución Original de Vice City"):
            st.write(
                "**[SFX: Estática de radio clásica y sonido de gaviotas]**\n\n"
                "*Locutor:* ¿Cansado de que el banco te ponga peros para tus retiros? En **Banco de Vice City**, tu dinero está seguro... o al menos hasta que el director tome un vuelo privado a las Bahamas. ¡Invierte hoy!\n\n"
                "**[SFX: Sonido de motores V8 acelerando en Ocean Drive]**\n"
                "*Locutor:* ¿Buscas velocidad y discreción? Ven a **Prendas y Rines 'El Chino'** en Ocean Beach. Cambiamos tu reloj de oro por fichas reales al instante. ¡Sin preguntas, sin testigos!"
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
            <p style="margin:
