import streamlit as st

monetag_url = "https://omg10.com/4/11676106"

st.title("¡Bienvenido a ZafiroX!")
st.write("Apóyanos haciendo clic en el siguiente botón:")

# Botón estilizado como enlace que abre en una pestaña nueva de forma segura
st.markdown(
    f"""
    <a href="{monetag_url}" target="_blank" style="
        display: inline-block;
        padding: 0.5em 1em;
        color: white;
        background-color: #6C63FF;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        border-radius: 5px;
        margin: 10px 0;
    ">🎁 Reclamar bonificación / Ver anuncio</a>
    """,
    unsafe_allow_html=True
)
