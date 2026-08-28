import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="ZafiroX - Minijuegos y Recompensas", page_icon="💎", layout="centered")

# Inicializar base de datos simulada en memoria
if "users" not in st.session_state:
    st.session_state.users = {
        "demo": {"password": "123", "balance": 150.0, "referrals": 0}
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- PANTALLA DE AUTENTICACIÓN ---
if not st.session_state.logged_in:
    st.title("💎 ZafiroX App")
    st.subheader("¡Juega, acumula gemas y gana dinero real!")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        login_user = st.text_input("Usuario", key="login_u")
        login_pass = st.text_input("Contraseña", type="password", key="login_p")
        if st.button("Entrar"):
            if login_user in st.session_state.users and st.session_state.users[login_user]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
                
    with tab2:
        reg_user = st.text_input("Elige un Usuario", key="reg_u")
        reg_pass = st.text_input("Elige una Contraseña", type="password", key="reg_p")
        if st.button("Crear Cuenta"):
            if reg_user in st.session_state.users:
                st.warning("El usuario ya existe.")
            elif reg_user == "":
                st.warning("Escribe un nombre válido.")
            else:
                st.session_state.users[reg_user] = {"password": reg_pass, "balance": 10.0, "referrals": 0}
                st.success("¡Cuenta creada con éxito! Ya puedes iniciar sesión.")

# --- APLICACIÓN PRINCIPAL ---
else:
    user_data = st.session_state.users[st.session_state.username]
    
    # Barra lateral de navegación
    st.sidebar.title(f"Hola, {st.session_state.username} 👋")
    st.sidebar.metric(label="Tu Saldo (Monedas)", value=f"{user_data['balance']:.2f} 💎")
    
    menu = st.sidebar.selectbox("Menú", [
        "🎁 Caja Misteriosa", 
        "💎 Caza de Gemas (Nuevo)", 
        "🎡 Ruleta de la Suerte", 
        "📺 Ver Videos Premiados", 
        "👥 Invitar Amigos", 
        "💸 Solicitar Retiro", 
        "🚪 Cerrar Sesión"
    ])
    
    if menu == "🎁 Caja Misteriosa":
        st.title("🎁 Abre Cajas y Gana")
        st.write("Haz clic en el botón para abrir una caja misteriosa y descubrir monedas al instante.")
        
        if st.button("Abrir Caja Misteriosa 🚀", use_container_width=True):
            premio = round(random.uniform(1.0, 10.0), 2)
            user_data["balance"] += premio
            st.success(f"¡Felicidades! Encontraste **{premio} monedas**.")
            st.rerun()

    elif menu == "💎 Caza de Gemas (Nuevo)":
        st.title("💎 Caza de Gemas Exclusiva")
        st.write("Elige uno de los 3 cofres ocultos. ¡Uno de ellos esconde una gema de alto valor!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Cofre A 📦", use_container_width=True):
                premio = random.choice([0.5, 5.0, 15.0])
                user_data["balance"] += premio
                st.success(f"¡Cofre A abierto! Ganaste **{premio} monedas**.")
                st.rerun()
        with col2:
            if st.button("Cofre B 📦", use_container_width=True):
                premio = random.choice([1.0, 8.0, 20.0])
                user_data["balance"] += premio
                st.success(f"¡Cofre B abierto! Ganaste **{premio} monedas**.")
                st.rerun()
        with col3:
            if st.button("Cofre C 📦", use_container_width=True):
                premio = random.choice([2.0, 10.0, 25.0])
                user_data["balance"] += premio
                st.success(f"¡Cofre C abierto! Ganaste **{premio} monedas**.")
                st.rerun()

    elif menu == "🎡 Ruleta de la Suerte":
        st.title("🎡 Ruleta ZafiroX")
        st.write("¡Gira la ruleta y prueba tu suerte para acumular más saldo al instante!")
        
        if st.button("Girar Ruleta 🎯", use_container_width=True):
            premio = random.choice([2.0, 5.0, 10.0, 50.0])
            user_data["balance"] += premio
            if premio >= 50.0:
                st.balloons()
                st.success(f"🎉 ¡WOOW! ¡Premio gordo de **{premio} monedas**!")
            else:
                st.success(f"¡Has ganado **{premio} monedas**!")
            st.rerun()

    elif menu == "📺 Ver Videos Premiados":
        st.title("📺 Zona de Anuncios y Videos")
        st.write("Haz clic para simular la visualización de un video publicitario y reclamar tu recompensa directa.")
        
        if st.button("▶️ Reclamar Video Premiado", use_container_width=True):
            premio_video = 5.0
            user_data["balance"] += premio_video
            st.success(f"¡Video completado! Has ganado **{premio_video} monedas**.")
            st.rerun()

    elif menu == "👥 Invitar Amigos":
        st.title("👥 Programa de Referidos")
        st.write("Comparte tu enlace único. Ganas comisiones automáticas por cada amigo que se registre.")
        
        codigo_referido = f"https://zafirox.streamlit.app/?ref={st.session_state.username}"
        st.text_input("Tu enlace de invitación:", value=codigo_referido)
        st.metric("Amigos invitados", user_data["referrals"])

    elif menu == "💸 Solicitar Retiro":
        st.title("💸 Retirar Fondos")
        st.write("Transfiere tus monedas a tu cuenta cuando alcances el mínimo de retiro (Mínimo: 500 monedas).")
        
        metodo = st.selectbox("Método de Pago", ["Nequi", "Daviplata", "PayPal"])
        cuenta_destino = st.text_input(f"Número de celular o correo ({metodo})")
        
        if st.button("Solicitar Retiro"):
            if user_data["balance"] >= 500:
                if cuenta_destino:
                    user_data["balance"] -= 500
                    st.success(f"¡Solicitud enviada a {cuenta_destino}! Procesaremos tu pago en 24-48 horas.")
                else:
                    st.warning("Por favor ingresa los datos de tu cuenta de destino.")
            else:
                st.error("No tienes el saldo suficiente para retirar. ¡Sigue jugando!")

    elif menu == "🚪 Cerrar Sesión":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
