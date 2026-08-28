import streamlit as st
import random # Necesario para la ruleta

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

# --- Lógica del Juego: Caza de Gemas (Encuentra la Gema) ---
if "Caza de Gemas" in menu_opcion:
    st.markdown("# 💎 Caza de Gemas")
    st.markdown("### ¡Encuentra la gema oculta y gana 5.00 💎!")
    st.info("Selecciona una de las 4 rocas para buscar.")

    # Definimos los emojis de las rocas y el premio
    rocabotones = ['🪨', '🪨', '🪨', '💎'] # Una gema, tres rocas
    random.shuffle(rocabotones) # Mezclamos las posiciones

    # Creamos 4 columnas para organizar los botones
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(rocabotones[0], key="gema1"):
            if rocabotones[0] == '💎':
                st.balloons() # ¡Efecto de celebración!
                st.success("¡Encontraste la Gema! +5.00 💎")
            else:
                st.error("¡Es solo una roca! Intenta de nuevo.")
    
    with col2:
        if st.button(rocabotones[1], key="gema2"):
            if rocabotones[1] == '💎':
                st.balloons()
                st.success("¡Encontraste la Gema! +5.00 💎")
            else:
                st.error("¡Es solo una roca! Intenta de nuevo.")

    with col3:
        if st.button(rocabotones[2], key="gema3"):
            if rocabotones[2] == '💎':
                st.balloons()
                st.success("¡Encontraste la Gema! +5.00 💎")
            else:
                st.error("¡Es solo una roca! Intenta de nuevo.")

    with col4:
        if st.button(rocabotones[3], key="gema4"):
            if rocabotones[3] == '💎':
                st.balloons()
                st.success("¡Encontraste la Gema! +5.00 💎")
            else:
                st.error("¡Es solo una roca! Intenta de nuevo.")

# --- Lógica del Juego: Ruleta de la Suerte ---
elif "Ruleta de la Suerte" in menu_opcion:
    st.markdown("# 🎡 Ruleta de la Suerte")
    st.markdown("### ¡Gira la ruleta para duplicar tus recompensas! (Max. 10.00 💎)")
    st.warning("Gira todos los días para multiplicar tus ganancias.")

    # Definimos los premios posibles
    premios_ruleta = [
        ("2.00 💎", 2.00),
        ("0.50 💎", 0.50),
        ("10.00 💎", 10.00),
        ("1.00 💎", 1.00),
        ("¡Mala suerte! 0 💎", 0.00),
        ("5.00 💎", 5.00),
        ("3.00 💎", 3.00)
    ]
    
    # Usamos iconos grandes para simular la ruleta visualmente
    st.markdown("---")
    col_r1, col_r2, col_r3 = st.columns([1,2,1])
    with col_r2:
        st.image("https://i.ibb.co/2M0gQ6z/ruleta-icono.png", width=250) # Imagen de ruleta de ejemplo
        
        if st.button("🎲 ¡GIRAR RULETA AHORA!", key="girar_ruleta"):
            resultado_texto, resultado_valor = random.choice(premios_ruleta)
            st.success(f"¡La ruleta se detuvo en: {resultado_texto}!")
            # Aquí deberías sumar el resultado_valor al saldo del usuario.

# --- Resto de secciones (sin cambios) ---
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
