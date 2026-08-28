import streamlit as st
import streamlit.components.v1 as components
import time
import datetime

# Configuración de la página
st.set_page_config(
    page_title="ZafiroX - Minijuegos y Recompensas",
    page_icon="💎",
    layout="centered"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DE LA SESIÓN ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 31.60
if 'tiempo_inicio' not in st.session_state:
    st.session_state.tiempo_inicio = time.time()

# --- MENÚ LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/controller.png", width=60)
    st.title("ZafiroX")
    st.write("Hola, **Lud337** 👋")
    
    st.markdown("---")
    st.subheader("Menú Principal")
    
    opcion = st.selectbox(
        "Selecciona una sección:",
        [
            "Minijuego Bloques",
            "Minijuego Snake",
            "Caza de Minas",
            "Ruleta de la Suerte",
            "Caja Misteriosa",
            "Ganar por Tiempo y Anuncios",
            "Invitar Amigos",
            "Ranking Semanal Top 4",
            "Solicitar Retiro"
        ]
    )
    
    st.markdown("---")
    st.write("💎 **Tu Saldo Actual:**")
    st.metric(label="", value=f"{st.session_state.saldo:.2f} 💎")

# --- CONTENIDO DE LAS SECCIONES ---

if opcion == "Minijuego Bloques":
    st.title("🧩 Minijuego de Bloques")
    st.write("¡Rompe líneas y acumula puntos de bonificación en tiempo real!")
    
    tetris_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 10px; }
            #game-container { max-width: 320px; margin: auto; background: #1e1e1e; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            button { background: #7c3aed; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-top: 10px; width: 100%; }
            button:hover { background: #6d28d9; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <h3>🕹️ Área de Juego Arcade</h3>
            <p>Puntuación: <span id="score">15</span></p>
            <canvas id="canvas" width="200" height="150" style="background:#111; display:block; margin: 0 auto; border-radius: 5px;"></canvas>
            <button onclick="addPoint()">🎮 Jugar / Sumar Puntos</button>
        </div>
        <script>
            let score = 15;
            function addPoint() {
                score += 5;
                document.getElementById('score').innerText = score;
            }
        </script>
    </body>
    </html>
    """
    components.html(tetris_html, height=350)

elif opcion == "Minijuego Snake":
    st.title("🐍 Minijuego Snake")
    st.write("¡Controla a la culebra con los 4 botones direccionales independientes!")
    
    snake_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 5px; }
            .controls { display: grid; grid-template-columns: repeat(3, 55px); gap: 5px; justify-content: center; margin-top: 10px; }
            button { background: #22c55e; color: white; border: none; padding: 12px; font-size: 18px; border-radius: 6px; cursor: pointer; }
            button:hover { background: #16a34a; }
            .empty { background: transparent; border: none; cursor: default; }
        </style>
    </head>
    <body>
        <div style="max-width: 300px; margin: auto;">
            <p>Puntuación: <span id="snake-score">0</span></p>
            <canvas id="snakeCanvas" width="200" height="200" style="background: #111; border: 2px solid #22c55e; border-radius: 5px;"></canvas>
            
            <div class="controls">
                <button class="empty"></button>
                <button onclick="dir('UP')">⬆️</button>
                <button class="empty"></button>
                <button onclick="dir('LEFT')">⬅️</button>
                <button onclick="dir('DOWN')">⬇️</button>
                <button onclick="dir('RIGHT')">➡️</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById("snakeCanvas");
            const ctx = canvas.getContext("2d");
            let score = 0;
            let snake = [{x: 100, y: 100}];
            let dx = 10, dy = 0;

            function dir(direction) {
                if (direction === 'UP' && dy === 0) { dx = 0; dy = -10; score += 2; }
                if (direction === 'DOWN' && dy === 0) { dx = 0; dy = 10; score += 2; }
                if (direction === 'LEFT' && dx === 0) { dx = -10; dy = 0; score += 2; }
                if (direction === 'RIGHT' && dx === 0) { dx = 10; dy = 0; score += 2; }
                document.getElementById("snake-score").innerText = score;
            }

            function main() {
                setTimeout(() => {
                    ctx.fillStyle = "#111";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = "#22c55e";
                    snake.forEach(part => { ctx.fillRect(part.x, part.y, 10, 10); });
                    let head = {x: (snake[0].x + dx + canvas.width) % canvas.width, y: (snake[0].y + dy + canvas.height) % canvas.height};
                    snake.unshift(head);
                    snake.pop();
                    main();
                }, 150);
            }
            main();
        </script>
    </body>
    </html>
    """
    components.html(snake_html, height=380)

elif opcion == "Caza de Minas":
    st.title("💣 Caza de Minas")
    st.write("¡Evita las minas ocultas y multiplica tus ganancias!")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Casilla 1 🎁"):
            st.session_state.saldo += 1.50
            st.success("¡Casilla segura! +1.50 💎")
            st.rerun()
    with col2:
        if st.button("Casilla 2 💣"):
            st.session_state.saldo -= 0.50
            st.error("¡Boom! Tocaste una mina. -0.50 💎")
            st.rerun()
    with col3:
        if st.button("Casilla 3 🎁"):
            st.session_state.saldo += 2.00
            st.success("¡Gran botín! +2.00 💎")
            st.rerun()

elif opcion == "Ruleta de la Suerte":
    st.title("🎡 Ruleta de la Suerte")
    st.write("¡Gira la ruleta y prueba tu suerte para ganar premios diarios!")
    if st.button("¡Girar Ruleta Ahora!"):
        st.session_state.saldo += 3.00
        st.success("¡Felicidades! Ganaste 3.00 💎")
        st.rerun()

elif opcion == "Caja Misteriosa":
    st.title("📦 Caja Misteriosa")
    st.write("Abre la caja secreta para revelar tu recompensa sorpresa.")
    if st.button("Abrir Caja Misteriosa"):
        st.session_state.saldo += 1.25
        st.success("¡Encontraste una recompensa oculta de 1.25 💎!")
        st.rerun()

elif opcion == "Ganar por Tiempo y Anuncios":
    st.title("⏱️ Ganancia por Tiempo y Anuncios")
    st.write("Monitorea tu tiempo en la línea y mira anuncios cortos para sumar saldo extra.")
    
    tiempo_transcurrido = int(time.time() - st.session_state.tiempo_inicio)
    st.info(f"⏳ Llevas **{tiempo_transcurrido} segundos** activos en la aplicación.")
    
    if st.button("Reclamar Bono por Tiempo (Cada 60s)"):
        if tiempo_transcurrido >= 10: # Ajustable para prueba rápida
            st.session_state.saldo += 0.50
            st.success("¡Bono por tiempo reclamado con éxito! +0.50 💎")
        else:
            st.warning("Aún no ha pasado el tiempo suficiente para este bono.")
            
    st.markdown("---")
    st.subheader("📺 Anuncios Cortos (Monetización Dueño)")
    st.write("Mira este espacio publicitario corto para apoyar la app y recibir recompensas inmediatas:")
    if st.button("Ver Anuncio Corto Patrocinado"):
        st.session_state.saldo += 0.80
        st.success("¡Anuncio completado! +0.80 💎 sumados a tu cuenta.")
        st.rerun()

elif opcion == "Invitar Amigos":
    st.title("👥 Invitar Amigos con Recompensa")
    st.write("Comparte tu enlace de registro. Ganas bonos automáticos cuando tus amigos se registran y quedan fijos en la plataforma.")
    st.code("https://zafirox.streamlit.app/?ref=Lud337", language="text")
    st.success("Recompensa activa: 5.00 💎 por cada amigo registrado y activo.")

elif opcion == "Ranking Semanal Top 4":
    st.title("🏆 Competencia Semanal")
    st.write("¡Los **4 primeros puestos** por actividades, misiones y tiempo en la app se llevan premios en dinero real cada semana!")
    
    # Temporizador regresivo semanal simulado
    ahora = datetime.datetime.now()
    proximo_domingo = ahora + datetime.timedelta(days=(6 - ahora.weekday()) % 7)
    tiempo_restante = proximo_domingo - ahora
    
    st.warning(f"⏰ **Tiempo restante para el cierre del ranking:** {tiempo_restante.days} días y {tiempo_restante.seconds // 3600} horas.")
    
    st.markdown("""
    | Puesto | Usuario | Puntuación | Premio Semanal |
    | :---: | :--- | :---: | :---: |
    | 🥇 **1°** | **Lud337 (Tú)** | 1,450 pts | $50.000 COP / USDT |
    | 🥈 **2°** | Carlos_99 | 1,320 pts | $30.000 COP / USDT |
    | 🥉 **3°** | SofiGamer | 1,100 pts | $20.000 COP / USDT |
    | 🏅 **4°** | AndresX | 950 pts | $10.000 COP / USDT |
    """)

elif opcion == "Solicitar Retiro":
    st.title("💰 Solicitar Retiro de Dinero Real")
    st.write(f"Tu saldo actual disponible es de **{st.session_state.saldo:.2f} 💎**.")
    
    metodo = st.selectbox(
        "Selecciona tu método de pago preferido:",
        ["Nequi", "DaviPlata", "PayPal", "PSE"]
    )
    
    cuenta_destino = st.text_input(f"Número de cuenta / Celular o Correo para {metodo}")
    monto_retiro = st.number_input("Monto en 💎 a retirar", min_value=5.0, max_value=float(max(5.0, st.session_state.saldo)), value=5.0)
    
    if st.button("📤 Enviar Solicitud de Retiro"):
        if cuenta_destino and st.session_state.saldo >= monto_retiro:
            st.session_state.saldo -= monto_retiro
            st.success(f"¡Retiro de {monto_retiro:.2f} 💎 procesado con éxito a través de {metodo} ({cuenta_destino})!")
        else:
            st.error("Por favor completa los datos de destino o verifica que tengas saldo suficiente.")
