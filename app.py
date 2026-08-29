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

# --- CÓDIGO HTML PARA EL DISPLAY AD (BANNER DE MONETAG) ---
# Reemplaza el script de abajo con el código real que te dé Monetag al crear tu zona Display Ads
banner_anuncio_html = """
<div style="text-align: center; margin: 15px 0; background: #1a1c23; padding: 10px; border-radius: 8px;">
    <p style="color: #888; font-size: 11px; margin-bottom: 5px;">Publicidad Patrocinada</p>
    <!-- PEGA TU SCRIPT DE MONETAG DISPLAY ADS AQUÍ -->
    <script async src="https://alwingulla.com/act/files/tag.min.js" data-zone="TU_ZONA_AQUI" data-sdk="show_12345"></script>
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
        json.dump(db, f)

db_usuarios = cargar_db()

# --- ESTADO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# --- SISTEMA DE LOGIN / REGISTRO ---
if not st.session_state.logged_in:
    st.title("💎 ZafiroX - Iniciar Sesión")
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        user_input = st.text_input("Usuario", key="login_user")
        pass_input = st.text_input("Contraseña", type="password", key="login_pass")
        if st.button("Entrar"):
            if user_input in db_usuarios and db_usuarios[user_input]["password"] == pass_input:
                st.session_state.logged_in = True
                st.session_state.user = user_input
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
                
    with tab2:
        new_user = st.text_input("Nuevo Usuario", key="reg_user")
        new_pass = st.text_input("Nueva Contraseña", type="password", key="reg_pass")
        if st.button("Crear Cuenta"):
            if new_user in db_usuarios:
                st.warning("El usuario ya existe.")
            elif new_user.strip() == "":
                st.error("El usuario no puede estar vacío.")
            else:
                db_usuarios[new_user] = {"password": new_pass, "saldo": 0.0}
                guardar_db(db_usuarios)
                st.success("¡Cuenta creada con éxito! Ve a la pestaña de Iniciar Sesión.")
else:
    # --- APLICACIÓN PRINCIPAL ---
    usuario_actual = st.session_state.user
    saldo_actual = db_usuarios[usuario_actual]["saldo"]

    def actualizar_saldo(cantidad):
        db_usuarios[usuario_actual]["saldo"] += cantidad
        guardar_db(db_usuarios)

    st.sidebar.title(f"Bienvenido, {usuario_actual}")
    st.sidebar.metric("Saldo Disponible", f"💎 {saldo_actual:.2f}")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()

    opcion = st.sidebar.radio("Menú Principal", ["Minijuegos", "Ranking Semanal", "Solicitar Retiro y Conversor"])

    # Mostrar Banner de Anuncios en la barra lateral o principal
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Patrocinador")
    st.sidebar.components.v1.html(banner_anuncio_html, height=120)

    if opcion == "Minijuegos":
        st.title("🎮 Zona de Minijuegos")
        st.write("¡Juega y gana recompensas para tu saldo!")

        juego = st.selectbox("Elige un minijuego:", ["Caja Misteriosa", "Tragamonedas Zafiro", "Memoria Rápida"])

        if juego == "Caja Misteriosa":
            st.subheader("📦 Abre una Caja Misteriosa")
            if st.button("Abrir Caja"):
                premio = random.choice([0.10, 0.25, 0.50, 1.00, 0.00])
                if premio > 0:
                    actualizar_saldo(premio)
                    st.success(f"¡Felicidades! Encontraste 💎 {premio:.2f} en la caja.")
                else:
                    st.error("¡Oh no! La caja estaba vacía.")

        elif juego == "Tragamonedas Zafiro":
            st.subheader("🎰 Gira los Rodillos")
            if st.button("Girar Ruleta"):
                simbolos = ["💎", "🍋", "⭐", "7️⃣", "🍒"]
                res = [random.choice(simbolos) for _ in range(3)]
                st.write(f"### {res[0]} | {res[1]} | {res[2]}")
                if res[0] == res[1] == res[2]:
                    actualizar_saldo(2.00)
                    st.success("¡JACKPOT! Ganaste 💎 2.00")
                elif res[0] == res[1] or res[1] == res[2]:
                    actualizar_saldo(0.50)
                    st.success("¡Buena combinación! Ganaste 💎 0.50")
                else:
                    st.error("Sigue intentando.")

        elif juego == "Memoria Rápida":
            st.subheader("🧠 Acierta el Número Secreto")
            num_secreto = random.randint(1, 5)
            intento = st.number_input("Adivina un número del 1 al 5:", min_value=1, max_value=5, step=1)
            if st.button("Probar Suerte"):
                if intento == num_secreto:
                    actualizar_saldo(1.00)
                    st.success(f"¡Adivinaste! El número era {num_secreto}. Ganaste 💎 1.00")
                else:
                    st.error(f"Fallaste. El número correcto era {num_secreto}.")

    elif opcion == "Ranking Semanal":
        st.title("🏆 Competencia Semanal")
        st.write("¡Los mejores jugadores ganan premios en efectivo reales cada semana!")
        
        # Reloj cuenta regresiva dinámico
        countdown_clock_html = """
        <div style="text-align: center; font-size: 20px; font-weight: bold; background: #222; padding: 10px; border-radius: 8px;">
            ⏱️ Cierre del ranking en tiempo real: <span id="live-clock"></span>
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
| 🥇 **1º** | **{usuario_actual} (Tú)** | {puntos_usuario:,} pts | $50.000 COP |
| 🥈 **2º** | CyberKing_99 | 1,420 pts | $30.000 COP |
| 🥉 **3º** | ZafiroQueen | 1,200 pts | $20.000 COP |
| 🏅 **4º** | NeoGamer_X | 990 pts | $10.000 COP |
""")

    elif opcion == "Solicitar Retiro y Conversor":
        st.title("💸 Conversor de Dinero y Retiro Real")
        st.write(f"Tu saldo disponible es de **💎 {saldo_actual:.2f}**")

        tasa_conversion = 4000
        valor_cop = saldo_actual * tasa_conversion
        st.info(f"💡 **Conversor automático:** Tus 💎 {saldo_actual:.2f} equivalen aproximadamente a **${valor_cop:,.0f} COP**")

        st.markdown("---")
        metodo = st.selectbox("Selecciona tu método de pago:", ["Nequi", "Daviplata", "PSE", "PayPal"])
        cuenta_destino = st.text_input(f"Número de celular / Cuenta para {metodo}")
        monto_retiro = st.number_input("Monto en 💎 a retirar", min_value=1.0, max_value=float(saldo_actual) if saldo_actual > 0 else 1.0, step=0.5)

        monto_cop_retiro = monto_retiro * tasa_conversion
        st.write(f"Monto a recibir: **${monto_cop_retiro:,.0f} COP**")

        if st.button("📥 Enviar Solicitud de Retiro"):
            if cuenta_destino and saldo_actual >= monto_retiro:
                actualizar_saldo(-monto_retiro)
                st.success(f"¡Retiro de ${monto_cop_retiro:,.0f} COP solicitado con éxito a través de {metodo}! Procesando...")
            else:
                st.error("Completa los datos de destino o verifica que tengas suficiente saldo.")
