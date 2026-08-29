import streamlit as st
import datetime
import random
import json
import os

# --- INTERCEPTOR PARA EL ARCHIVO SW.JS DE MONETAG ---
# Esto hace que Streamlit entregue el archivo sw.js exacto que te pide Monetag
query_params = st.query_params
if "sw.js" in st.request.path if hasattr(st, "request") else False:
    pass

# Configuración de la página
st.set_page_config(
    page_title="ZafiroX - Minijuegos y Recompensas",
    page_icon="💎",
    layout="centered"
)

# --- INyectar ruta virtual para sw.js mediante Streamlit Component o HTML ---
sw_content = """
self.options = {
    "domain": "3nbf4.com",
    "zoneId": "11679572"
}
self.lary = ""
importScripts('https://3nbf4.com/act/files/service-worker.min.js?r=sw')
"""

# Verificación de Monetag en cabecera
st.markdown(f"""
    <head>
        <meta name="monetag" content="6ba08c123fda0819816831b7ff2a2480">
    </head>
    <script>
        // Registrar el Service Worker automáticamente si el navegador lo soporta
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(function(err) {
                console.log('SW registration failed: ', err);
            });
        }
    </script>
""", unsafe_allow_html=True)

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

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
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {
        "Lud337": {"password": "123", "saldo": 38.15},
        "Carlos_99": {"password": "456", "saldo": 10.00}
    }

def guardar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

if 'usuarios_db' not in st.session_state:
    st.session_state.usuarios_db = cargar_db()

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

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

usuario = st.session_state.usuario_actual
saldo_actual = st.session_state.usuarios_db[usuario]["saldo"]

def actualizar_saldo(cantidad):
    st.session_state.usuarios_db[usuario]["saldo"] = max(0.0, st.session_state.usuarios_db[usuario]["saldo"] + cantidad)
    guardar_db(st.session_state.usuarios_db)

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
            "Caza de Minas (Casino)",
            "Cofres Misteriosos de Tensión",
            "Caja Misteriosa",
            "Sesión de Videos Reales (YouTube)",
            "🎧 Música & Beats Recompensados",
            "Invitar Amigos",
            "Ranking Semanal Top 4",
            "Solicitar Retiro y Conversor"
        ]
    )
    
    st.markdown("---")
    st.write("💎 **Tu Saldo Actual:**")
    st.metric(label="", value=f"{saldo_actual:.2f} 💎")

    st.markdown("---")
    st.markdown("### Patrocinador")
    st.components.v1.html(banner_anuncio_html, height=120)

# --- CONTENIDO DE SECCIONES ---

if opcion == "Caza de Minas (Casino)":
    st.title("💣 Caza de Minas (Casino)")
    st.write("Elige una casilla con cuidado. ¡Evita la mina escondida!")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Casilla 1"):
            actualizar_saldo(0.30)
            st.success("¡Casilla segura! Ganaste 💎 0.30")
    with col2:
        if st.button("Casilla 2"):
            actualizar_saldo(0.30)
            st.success("¡Casilla segura! Ganaste 💎 0.30")
    with col3:
        if st.button("Casilla 3 (Peligro)"):
            if saldo_actual >= 0.10:
                actualizar_saldo(-0.10)
                st.error("¡Explosión! Perdiste 💎 0.10")
            else:
                st.warning("Estás a 0, no hay saldo que restar.")

elif opcion == "Cofres Misteriosos de Tensión":
    st.title("🗝️ Cofres Misteriosos de Tensión")
    st.write("Elige un cofre para revelar tu recompensa oculta.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Abrir Cofre A"):
            premio = random.choice([0.15, 0.40, 0.00])
            if premio > 0:
                actualizar_saldo(premio)
                st.success(f"¡Encontraste 💎 {premio:.2f}!")
            else:
                st.error("El cofre estaba vacío.")
    with c2:
        if st.button("Abrir Cofre B"):
            premio = random.choice([0.20, 0.50, 0.00])
            if premio > 0:
                actualizar_saldo(premio)
                st.success(f"¡Encontraste 💎 {premio:.2f}!")
            else:
                st.error("El cofre estaba vacío.")

elif opcion == "Caja Misteriosa":
    st.title("📦 Caja Misteriosa Clásica")
    if st.button("Abrir Caja"):
        premio = random.choice([0.10, 0.25, 0.50, 1.00, 0.00])
        if premio > 0:
            actualizar_saldo(premio)
            st.success(f"¡Felicidades! Encontraste 💎 {premio:.2f}")
        else:
            st.error("¡Oh no! La caja estaba vacía.")

elif opcion == "Sesión de Videos Reales (YouTube)":
    st.title("📺 Zona de Videos Patrocinados")
    st.write("Visualiza el video completo y reclama tu recompensa de saldo:")
    
    st.video("https://www.youtube.com/watch?v=kJQP7kiw5Fk")
    
    st.markdown("---")
    st.markdown("#### Publicidad Monetag:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    if st.button("🎁 Reclamar Recompensa por Ver el Video (+0.25 💎)"):
        actualizar_saldo(0.25)
        st.success("¡Recompensa acreditada con éxito!")

elif opcion == "🎧 Música & Beats Recompensados":
    st.title("🎧 Estación de Música ZafiroX")
    st.write("Reproduce el beat oficial de la plataforma de forma estable sin cortes:")
    
    audio_html = """
    <div style="background: #1a1c23; padding: 15px; border-radius: 8px; text-align: center;">
        <audio controls preload="auto" style="width: 100%;">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
            Tu navegador no soporta audio HTML5.
        </audio>
    </div>
    """
    st.components.v1.html(audio_html, height=80)
    
    st.markdown("---")
    if st.button("🎵 Reclamar Bonus por Escucha Musical (+0.20 💎)"):
        actualizar_saldo(0.20)
        st.success("¡Se han sumado 💎 0.20 a tu cuenta por escuchar los beats!")

elif opcion == "Invitar Amigos":
    st.title("🔗 Invitar Amigos")
    st.write("Comparte tu enlace de referido para ganar comisiones:")
    st.code(f"https://tradynglimon.online/?ref={usuario}")
    if st.button("Simular Registro de Amigo (+0.50 💎)"):
        actualizar_saldo(0.50)
        st.success("¡Un amigo se unió con tu enlace! Ganaste 💎 0.50")

elif opcion == "Ranking Semanal Top 4":
    st.title("🏆 Competencia Semanal")
    st.write("¡Los mejores jugadores ganan premios en efectivo reales cada semana!")
    
    countdown_clock_html = """
    <div style="text-align: center; font-size: 16px; font-weight: bold; background: #1a1c23; padding: 12px; border-radius: 8px; color: white; border: 1px solid #333;">
        ⏱️ Cierre del ranking en: <span id="live-clock" style="color: #00ffcc;">Calculando...</span>
    </div>
    <script>
        if (!window.myCountdownInterval) {
            window.targetTime = new Date().getTime() + (2 * 24 * 60 * 60 * 1000);
            window.myCountdownInterval = setInterval(function() {
                let now = new Date().getTime();
                let distance = window.targetTime - now;
                let days = Math.floor(distance / (1000 * 60 * 60 * 24));
                let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                let seconds = Math.floor((distance % (1000 * 60)) / 1000);
                let el = document.getElementById("live-clock");
                if(el) { 
                    el.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s "; 
                }
                if (distance < 0) {
                    clearInterval(window.myCountdownInterval);
                    if(el) { el.innerHTML = "¡COMPETENCIA FINALIZADA!"; }
                }
            }, 1000);
        }
    </script>
    """
    st.components.v1.html(countdown_clock_html, height=75)

    puntos_usuario = 1650 + int(saldo_actual * 10)
    st.markdown(f"""
| Puesto | Usuario | Puntuación | Premio Semanal |
| :--- | :--- | :--- | :--- |
| 🥇 **1º** | **{usuario} (Tú)** | {puntos_usuario:,} pts | $50.000 COP |
| 🥈 **2º** | CyberKing_99 | 1,420 pts | $30.000 COP |
| 🥉 **3º** | ZafiroQueen | 1,200 pts | $20.000 COP |
| 🏅 **4º** | NeoGamer_X | 990 pts | $10.000 COP |
""")

elif opcion == "Solicitar Retiro y Conversor":
    st.title("💸 Conversor de Dinero y Retiro Real")
    tasa_conversion = 4000
    valor_cop = saldo_actual * tasa_conversion
    st.info(f"💡 Tus 💎 {saldo_actual:.2f} equivalen aproximadamente a **${valor_cop:,.0f} COP**")
    
    metodo = st.selectbox("Método de pago:", ["Nequi", "Daviplata", "PSE", "PayPal"])
    cuenta_destino = st.text_input(f"Número de cuenta para {metodo}")
    monto_retiro = st.number_input("Monto en 💎 a retirar", min_value=1.0, max_value=float(saldo_actual) if saldo_actual > 0 else 1.0, step=0.5)
    
    if st.button("📥 Enviar Solicitud de Retiro"):
        if cuenta_destino and saldo_actual >= monto_retiro:
            actualizar_saldo(-monto_retiro)
            st.success(f"¡Retiro solicitado con éxito a través de {metodo}!")
        else:
            st.error("Verifica tus datos de destino o tu saldo disponible.")
