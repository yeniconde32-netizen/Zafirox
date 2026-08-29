import streamlit as st
import datetime
import random
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="ZafiroX - Minijuegos y Recompensas",
    page_icon="💎",
    layout="centered"
)

# --- VERIFICACIÓN DE MONETAG ---
st.markdown("""
    <head>
        <meta name="monetag" content="6ba08c123fda0819816831b7ff2a2480">
    </head>
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
<div style="text-align: center; margin: 15px 0; background: #1a1c23; padding: 10px; border-radius: 8px;">
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
        "Lud337": {"password": "123", "saldo": 31.60},
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

# Sincronizamos usuario activo y base de datos
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
            "Minijuego Bloques (Hard)",
            "Minijuego Snake (Hard)",
            "Caza de Minas (Casino)",
            "Cofres Misteriosos de Tensión",
            "Caja Misteriosa",
            "Sesión de Videos y Monetag",
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

if opcion == "Minijuego Bloques (Hard)":
    st.title("🧩 Minijuego de Bloques (Modo Difícil)")
    st.write("¡Velocidad alta estilo Arcade para poner a prueba tus reflejos!")
    if st.button("Jugar y Superar Nivel (+0.25 💎)"):
        actualizar_saldo(0.25)
        st.success("¡Nivel superado con éxito! Ganaste 💎 0.25")

elif opcion == "Minijuego Snake (Hard)":
    st.title("🐍 Minijuego Snake (Modo Difícil)")
    st.write("¡Come la mayor cantidad de manzanas sin chocar con los bordes!")
    if st.button("Completar Partida Snake (+0.25 💎)"):
        actualizar_saldo(0.25)
        st.success("¡Excelente partida de Snake! Ganaste 💎 0.25")

elif opcion == "Caza de Minas (Casino)":
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

elif opcion == "Sesión de Videos y Monetag":
    st.title("📺 Sesión de Videos y Monetag")
    st.write("Mira los anuncios patrocinados abajo para reclamar tus recompensas diarias:")
    st.components.v1.html(banner_anuncio_html, height=120)
    if st.button("Reclamar Bonus por Ver Anuncio (+0.20 💎)"):
        actualizar_saldo(0.20)
        st.success("¡Recompensa acreditada con éxito!")

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
    <div style="text-align: center; font-size: 16px; font-weight: bold; background: #222; padding: 10px; border-radius: 8px; color: white;">
        ⏱️ Cierre del ranking: <span id="live-clock"></span>
    </div>
    <script>
        let countDownDate = new Date().getTime() + (2 * 24 * 60 * 60 * 1000);
        let x = setInterval(function() {
            let now = new Date().getTime();
            let distance = countDownDate - now;
            let days = Math.floor(distance / (1000 * 60 * 60 * 24));
            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);
            let el = document.getElementById("live-clock");
            if(el) { el.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s "; }
            if (distance < 0) {
                clearInterval(x);
                if(el) { el.innerHTML = "¡COMPETENCIA FINALIZADA!"; }
            }
        }, 1000);
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
