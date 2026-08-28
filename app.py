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
            "🎬 Sesión de Video (Nuevo)",
            "👥 Invitar Amigos",
            "💵 Solicitar Retiro",
            "🚪 Cerrar Sesión"
        ],
        label_visibility="collapsed"
    )

monetag_url = "https://omg10.com/4/11676106"

# Secciones con diseño visual enriquecido
if "Caza de Gemas" in menu_opcion:
    st.markdown("# 💎 Caza de Gemas")
    st.markdown("### ¡Encuentra la gema oculta y gana monedas extra!")
    st.info("Selecciona una roca para descubrir qué hay debajo.")
    if st.button("🔍 Buscar Gema"):
        st.success("¡Felicidades! Encontraste 5.00 💎")

elif "Ruleta de la Suerte" in menu_opcion:
    st.markdown("# 🎡 Ruleta de la Suerte")
    st.markdown("### ¡Gira la ruleta para duplicar tus recompensas!")
    st.warning("Gira todos los días para multiplicar tus ganancias.")
    if st.button("🎲 Girar Ruleta"):
        st.success("¡Increíble! Ganaste 2.00 💎")

elif "Caja Misteriosa" in menu_opcion:
    st.markdown("# 🎁 Caja Misteriosa")
    st.markdown("### Abre la caja para descubrir tu premio sorpresa.")
    if st.button("📦 Abrir Caja"):
        st.success("¡Premio de 10.00 💎 desbloqueado con éxito!")

elif "Ver Videos Premiados" in menu_opcion:
    st.markdown("# 📺 Ver Videos Premiados")
    st.markdown("### Apóyanos haciendo clic en el botón para ver el contenido patrocinado:")
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="{monetag_url}" target="_blank" style="
                display: inline-block;
                padding: 0.8em 1.5em;
                color: white;
                background-color: #6C63FF;
                text-align: center;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1em;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">🎁 Reclamar bonificación / Ver anuncio</a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif "Sesión de Video" in menu_opcion:
    st.markdown("# 🎬 Sesión de Video")
    st.markdown("### Disfruta de la transmisión y contenido exclusivo en video:")
    
    # Puedes incrustar un video de ejemplo de YouTube o un reproductor multimedia
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    st.markdown("---")
    st.info("💡 **Consejo:** Mira el video completo para desbloquear tu bonificación diaria.")
    if st.button("🎁 Reclamar Bono por Video"):
        st.success("¡Has sumado 3.00 💎 por ver la sesión de video!")

elif "Invitar Amigos" in menu_opcion:
    st.markdown("# 👥 Invitar Amigos")
    st.markdown("### Comparte tu enlace de referencia con tus amigos:")
    st.code("https://zafirox-minijuegos.streamlit.app/?ref=Lud337")

elif "Solicitar Retiro" in menu_opcion:
    st.markdown("# 💵 Solicitar Retiro")
    st.markdown("### Métodos de pago disponibles:")
    st.markdown("- 🅿️ PayPal\n- 💛 Nequi\n- 💚 Daviplata\n- 💙 PSE")
    st.info("Tu saldo actual es de 27.40 💎. ¡Sigue sumando para retirar!")

else:
    st.markdown("# 🚪 Cerrar Sesión")
    st.markdown("Has cerrado sesión correctamente.")
