import streamlit as st

# Barra lateral con perfil y menú desplegable
with st.sidebar:
    st.markdown("### Hola, Lud337 👋")
    st.markdown("Tu Saldo (Monedas)")
    st.markdown("## **27.40 💎**")
    st.markdown("---")
    st.markdown("### Menú")
    
    menu_opcion = st.selectbox(
        "Selecciona una sección",
        [
            "🎁 Caja Misteriosa",
            "💎 Caza de Gemas (Nuevo)",
            "🎡 Ruleta de la Suerte",
            "📺 Ver Videos Premiados",
            "👥 Invitar Amigos",
            "💵 Solicitar Retiro",
            "🚪 Cerrar Sesión"
        ],
        label_visibility="collapsed"
    )

monetag_url = "https://omg10.com/4/11676106"

# Lógica detallada para cada opción del menú
if "Caza de Gemas" in menu_opcion:
    st.title("💎 Caza de Gemas")
    st.write("¡Encuentra la gema oculta y gana monedas extra!")
    if st.button("Buscar Gema"):
        st.success("¡Encontraste 5.00 💎!")

elif "Ruleta de la Suerte" in menu_opcion:
    st.title("🎡 Ruleta de la Suerte")
    st.write("¡Gira la ruleta para duplicar tus recompensas!")
    if st.button("Girar Ruleta"):
        st.info("¡Ganaste 2.00 💎!")

elif "Caja Misteriosa" in menu_opcion:
    st.title("🎁 Caja Misteriosa")
    st.write("Abre la caja para descubrir tu premio sorpresa.")
    if st.button("Abrir Caja"):
        st.warning("¡Premio de 10.00 💎 desbloqueado!")

elif "Ver Videos Premiados" in menu_opcion:
    st.title("📺 Ver Videos Premiados")
    st.write("Apóyanos haciendo clic en el botón para ver el contenido patrocinado:")
    st.markdown(
        f"""
        <a href="{monetag_url}" target="_blank" style="
            display: inline-block;
            padding: 0.6em 1.2em;
            color: white;
            background-color: #6C63FF;
            text-align: center;
            text-decoration: none;
            font-weight: bold;
            border-radius: 8px;
            margin: 10px 0;
        ">🎁 Reclamar bonificación / Ver anuncio</a>
        """,
        unsafe_allow_html=True
    )

elif "Invitar Amigos" in menu_opcion:
    st.title("👥 Invitar Amigos")
    st.write("Comparte tu enlace de referencia con tus amigos:")
    st.code("https://zafirox-minijuegos.streamlit.app/?ref=Lud337")

elif "Solicitar Retiro" in menu_opcion:
    st.title("💵 Solicitar Retiro")
    st.write("Métodos disponibles: PayPal, Nequi, Daviplata, PSE.")
    st.info("Tu saldo actual es de 27.40 💎. Acumula el mínimo para retirar.")

else:
    st.title("🚪 Cerrar Sesión")
    st.write("Has cerrado sesión correctamente.")
