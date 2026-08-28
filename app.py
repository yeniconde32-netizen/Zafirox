import streamlit as st

# Barra lateral con el perfil y menú desplegable
with st.sidebar:
    st.markdown("### Hola, Lud337 👋")
    st.markdown("Tu Saldo (Monedas)")
    st.markdown("## **27.40 💎**")
    st.markdown("---")
    st.markdown("### Menú")
    
    # Selector de opciones del menú (selectbox)
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

# Lógica principal según la opción elegida en el menú
if "Ruleta de la Suerte" in menu_opcion:
    st.title("🎡 Ruleta de la Suerte")
    st.write("¡Gira la ruleta y gana más monedas!")

elif "Ver Videos Premiados" in menu_opcion:
    st.title("📺 Ver Videos Premiados")
    st.write("Apóyanos haciendo clic en el siguiente botón:")
    
    monetag_url = "https://omg10.com/4/11676106"
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

elif "Solicitar Retiro" in menu_opcion:
    st.title("💵 Solicitar Retiro")
    st.write("Tus métodos de retiro disponibles (PayPal, Nequi, Daviplata, PSE).")

elif "Invitar Amigos" in menu_opcion:
    st.title("👥 Invitar Amigos")
    st.write("Tu enlace de referencia:")
    st.code("https://zafirox-minijuegos.streamlit.app/?ref=Lud337")

else:
    st.title(menu_opcion)
    st.write("Sección cargada correctamente.")
