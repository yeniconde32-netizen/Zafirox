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
    st.subheader("¡Juega, acumula y gana!")
    
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
    st.sidebar.metric(label="Tu Saldo (Monedas)", value=f"{user_data['balance']:.2f}")
    
    menu = st.sidebar.selectbox("Menú", ["Minijuego (Caja Misteriosa)", "Invitar Amigos", "Solicitar Retiro", "Cerrar Sesión"])
    
    if menu == "Minijuego (Caja Misteriosa)":
        st.title("🎁 Abre Cajas y Gana")
        st.write("Haz clic en el botón para abrir una caja misteriosa. Cada apertura te da monedas de forma aleatoria.")
        
        st.info("💡 *Tip:* Aquí podrás integrar en el futuro tus anuncios de video premiados.")
        
        if st.button("Abrir Caja Misteriosa 🚀", use_container_width=True):
            premio = round(random.uniform(1.0, 15.0), 2)
            user_data["balance"] += premio
            st.success(f"¡Felicidades! Encontraste **{premio} monedas** en la caja.")
            st.rerun()

    elif menu == "Invitar Amigos":
        st.title("👥 Programa de Referidos")
        st.write("Comparte tu enlace o código único con tus amigos. Ganas un porcentaje de lo que ellos generen.")
        
        codigo_referido = f"https://zafirox.streamlit.app/?ref={st.session_state.username}"
        st.text_input("Tu enlace de invitación:", value=codigo_referido)
        st.metric("Amigos invitados", user_data["referrals"])

    elif menu == "Solicitar Retiro":
        st.title("💸 Retirar Fondos")
        st.write("Transfiere tus monedas a tu cuenta de pago cuando alcances el mínimo (Mínimo: 500 monedas).")
        
        metodo = st.selectbox("Método de Pago", ["PayPal", "Nequi", "Daviplata"])
        cuenta_destino = st.text_input(f"Correo o Número de cuenta ({metodo})")
        
        if st.button("Solicitar Retiro"):
            if user_data["balance"] >= 500:
                if cuenta_destino:
                    st.success(f"¡Solicitud de retiro enviada con éxito a {cuenta_destino}! Procesaremos tu pago en 24-48 horas.")
                    user_data["balance"] -= 500
                else:
                    st.warning("Por favor ingresa los datos de tu cuenta.")
            else:
                st.error("No tienes el saldo suficiente para retirar. ¡Sigue jugando!")

    elif menu == "Cerrar Sesión":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
