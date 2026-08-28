import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="ZafiroX - Minijuegos y Recompensas",
    page_icon="💎",
    layout="centered"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .saldo-box {
        background-color: #1a1c23;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DE LA SESIÓN (SALDO) ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 27.40

# --- MENÚ LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/controller.png", width=60)
    st.title("ZafiroX")
    st.write("Hola, **Lud337** 👋")
    
    st.markdown("---")
    st.subheader("Menú")
    
    opcion = st.selectbox(
        "Selecciona una sección:",
        [
            "Minijuego Bloques",
            "Minijuego Snake",
            "Caza de Gemas",
            "Ruleta de la Suerte",
            "Ver Videos Premiados",
            "Sesión de Video con Reto",
            "Invitar Amigos",
            "Solicitar Retiro"
        ]
    )
    
    st.markdown("---")
    st.write("💎 **Tu Saldo (Monedas):**")
    st.metric(label="", value=f"{st.session_state.saldo:.2f} 💎")

# --- CONTENIDO PRINCIPAL SEGÚN EL MENÚ ---

if opcion == "Minijuego Bloques":
    st.title("🧩 Minijuego de Bloques")
    st.write("¡Rompe líneas y acumula puntos de bonificación!")
    
    tetris_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 10px; }
            #game-container { max-width: 320px; margin: auto; background: #1e1e1e; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            button { background: #7c3aed; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-top: 10px; }
            button:hover { background: #6d28d9; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <h3>🕹️ Área de Juego Arcade</h3>
            <p>Haz clic para acelerar y sumar puntos.</p>
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
    components.html(tetris_html, height=360)

elif opcion == "Minijuego Snake":
    st.title("🐍 Minijuego Snake")
    st.write("¡Controla a la culebra y evita chocar!")
    
    snake_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 10px; }
            .controls { display: grid; grid-template-columns: repeat(3, 50px); gap: 5px; justify-content: center; margin-top: 10px; }
            button { background: #22c55e; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 5px; cursor: pointer; }
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
                if (direction === 'UP' && dy === 0) { dx = 0; dy = -10; score += 1; }
                if (direction === 'DOWN' && dy === 0) { dx = 0; dy = 10; score += 1; }
                if (direction === 'LEFT' && dx === 0) { dx = -10; dy = 0; score += 1; }
                if (direction === 'RIGHT' && dx === 0) { dx = 10; dy = 0; score += 1; }
                document.getElementById("snake-score").innerText = score;
            }

            function main() {
                setTimeout(() => {
                    ctx.fillStyle = "#111";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    ctx.fillStyle = "#22c55e";
                    snake.forEach(part => {
                        ctx.fillRect(part.x, part.y, 10, 10);
                    });
                    
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

elif opcion == "Caza de Gemas":
    st.title("💎 Caza de Gemas")
    st.write("¡Haz clic en las gemas que aparecen para ganar recompensas!")
    if st.button("Buscar Gema Misteriosa"):
        st.session_state.saldo += 0.50
        st.success("¡Encontraste una gema! +0.50 💎")
        st.rerun()

elif opcion == "Ruleta de la Suerte":
    st.title("🎡 Ruleta de la Suerte")
    st.write("¡Gira la ruleta una vez al día para ganar premios aleatorios!")
    if st.button("Girar Ruleta"):
        st.session_state.saldo += 1.00
        st.success("¡Ganaste 1.00 💎 en la ruleta!")
        st.rerun()

elif opcion == "Ver Videos Premiados":
    st.title("📺 Ver Videos Premiados")
    st.write("Mira los videos disponibles para sumar puntos a tu saldo.")
    if st.button("Simular Visualización de Video"):
        st.session_state.saldo += 0.20
        st.success("¡Video visto con éxito! +0.20 💎")
        st.rerun()

elif opcion == "Sesión de Video con Reto":
    st.title("🎬 Sesión de Video con Reto")
    st.write("Completa el reto del video para desbloquear bonificaciones especiales.")
    if st.button("Completar Reto"):
        st.session_state.saldo += 2.00
        st.success("¡Reto completado! +2.00 💎")
        st.rerun()

elif opcion == "Invitar Amigos":
    st.title("👥 Invitar Amigos")
    st.write("Comparte tu enlace de invitación para ganar un porcentaje de las ganancias de tus amigos.")
    st.code("https://zafirox.streamlit.app/?ref=Lud337", language="text")

elif opcion == "Solicitar Retiro":
    st.title("💰 Solicitar Retiro")
    st.write(f"Tu saldo actual disponible es de **{st.session_state.saldo:.2f} 💎**.")
    metodo = st.selectbox("Método de retiro", ["PayPal", "Binance (USDT)", "Transferencia Bancaria"])
    monto = st.number_input("Monto a retirar", min_value=5.0, max_value=float(st.session_state.saldo), value=5.0)
    
    if st.button("Procesar Retiro"):
        if st.session_state.saldo >= monto:
            st.session_state.saldo -= monto
            st.success(f"¡Solicitud de retiro de {monto:.2f} 💎 enviada con éxito mediante {metodo}!")
            st.rerun()
        else:
            st.error("No tienes suficiente saldo.")
