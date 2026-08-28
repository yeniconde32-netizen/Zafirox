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

# --- ESTILOS CSS ---
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
            "Minijuego Snake (Funcional)",
            "Caza de Minas",
            "Ruleta de la Suerte",
            "Caja Misteriosa",
            "Ganar por Tiempo y Anuncios (Monetag)",
            "Invitar Amigos",
            "Ranking Semanal Top 4",
            "Solicitar Retiro y Conversor"
        ]
    )
    
    st.markdown("---")
    st.write("💎 **Tu Saldo Actual:**")
    st.metric(label="", value=f"{st.session_state.saldo:.2f} 💎")

# --- CONTENIDO DE LAS SECCIONES ---

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
            button { background: #7c3aed; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-top: 10px; width: 100%; }
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

elif opcion == "Minijuego Snake (Funcional)":
    st.title("🐍 Minijuego Snake Real")
    st.write("¡La serpiente gira correctamente con los controles en pantalla!")
    
    snake_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 5px; }
            .controls { display: grid; grid-template-columns: repeat(3, 60px); gap: 6px; justify-content: center; margin-top: 12px; }
            button { background: #22c55e; color: white; border: none; padding: 14px; font-size: 20px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            button:active { background: #16a34a; transform: scale(0.95); }
            .empty { background: transparent; border: none; cursor: default; box-shadow: none; }
        </style>
    </head>
    <body>
        <div style="max-width: 300px; margin: auto;">
            <p>Puntuación: <span id="snake-score" style="color: #22c55e; font-weight: bold; font-size: 18px;">0</span></p>
            <canvas id="snakeCanvas" width="220" height="220" style="background: #111; border: 2px solid #22c55e; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            
            <div class="controls">
                <button class="empty"></button>
                <button onclick="changeDir('UP')">⬆️</button>
                <button class="empty"></button>
                <button onclick="changeDir('LEFT')">⬅️</button>
                <button onclick="changeDir('DOWN')">⬇️</button>
                <button onclick="changeDir('RIGHT')">➡️</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById("snakeCanvas");
            const ctx = canvas.getContext("2d");
            
            let score = 0;
            let box = 10;
            let snake = [{x: 100, y: 100}];
            let food = {x: Math.floor(Math.random() * 20) * box, y: Math.floor(Math.random() * 20) * box};
            let d = "RIGHT";
            let nextD = "RIGHT";

            function changeDir(direction) {
                if (direction === 'UP' && d !== 'DOWN') nextD = 'UP';
                if (direction === 'DOWN' && d !== 'UP') nextD = 'DOWN';
                if (direction === 'LEFT' && d !== 'RIGHT') nextD = 'LEFT';
                if (direction === 'RIGHT' && d !== 'LEFT') nextD = 'RIGHT';
            }

            function draw() {
                ctx.fillStyle = "#111";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                for (let i = 0; i < snake.length; i++) {
                    ctx.fillStyle = (i === 0) ? "#22c55e" : "#15803d";
                    ctx.fillRect(snake[i].x, snake[i].y, box, box);
                }

                ctx.fillStyle = "#ef4444";
                ctx.fillRect(food.x, food.y, box, box);

                d = nextD;
                let snakeX = snake[0].x;
                let snakeY = snake[0].y;

                if (d === 'LEFT') snakeX -= box;
                if (d === 'UP') snakeY -= box;
                if (d === 'RIGHT') snakeX += box;
                if (d === 'DOWN') snakeY += box;

                if (snakeX === food.x && snakeY === food.y) {
                    score += 5;
                    document.getElementById("snake-score").innerText = score;
                    food = {x: Math.floor(Math.random() * 21) * box, y: Math.floor(Math.random() * 21) * box};
                } else {
                    snake.pop();
                }

                let newHead = {x: snakeX, y: snakeY};
                
                // Atravesar paredes o reiniciar si choca
                if (snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height) {
                    snake = [{x: 100, y: 100}];
                    score = 0;
                    document.getElementById("snake-score").innerText = score;
                    d = "RIGHT";
                    nextD = "RIGHT";
                    return;
                }

                snake.unshift(newHead);
            }

            let game = setInterval(draw, 120);
        </script>
    </body>
    </html>
    """
    components.html(snake_html, height=410)

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

elif opcion == "Ganar por Tiempo y Anuncios (Monetag)":
    st.title("⏱️ Tiempo y Anuncios Monetag")
    st.write("Monitorea tu tiempo activo y visualiza anuncios de Monetag integrados para monetizar la app.")
    
    tiempo_transcurrido = int(time.time() - st.session_state.tiempo_inicio)
    st.info(f"⏳ Llevas **{tiempo_transcurrido} segundos** activos en la aplicación.")
    
    if st.button("Reclamar Bono por Tiempo Activo"):
        st.session_state.saldo += 0.50
        st.success("¡Bono por tiempo reclamado! +0.50 💎")
        
    st.markdown("---")
    st.subheader("📺 Anuncio Monetag (Directo)")
    st.write("Haz clic en el botón de abajo para activar el enlace/anuncio de Monetag y registrar tu visualización:")
    
    # Integración real del enlace de anuncio o script de Monetag
    monetag_url = "https://your_monetag_ad_link_here.com" # Reemplaza con tu enlace directo de Monetag
    st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="{monetag_url}" target="_blank">
                <button style="background-color: #f59e0b; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%;">
                    🚀 Ver Anuncio Patrocinado (Monetag)
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Ya vi el anuncio, acreditar recompensa"):
        st.session_state.saldo += 1.00
        st.success("¡Recompensa de anuncio acreditada con éxito! +1.00 💎")
        st.rerun()

elif opcion == "Invitar Amigos":
    st.title("👥 Invitar Amigos con Recompensa")
    st.write("Comparte tu enlace de registro. Ganas bonos automáticos cuando tus amigos se registran y quedan fijos.")
    st.code("https://zafirox.streamlit.app/?ref=Lud337", language="text")
    st.success("Recompensa activa: 5.00 💎 por cada amigo registrado.")

elif opcion == "Ranking Semanal Top 4":
    st.title("🏆 Competencia Semanal")
    st.write("¡Los **4 primeros puestos** por actividades y misiones se llevan premios en dinero real cada semana!")
    
    ahora = datetime.datetime.now()
    proximo_domingo = ahora + datetime.timedelta(days=(6 - ahora.weekday()) % 7)
    tiempo_restante = proximo_domingo - ahora
    
    st.warning(f"⏰ **Cierre del ranking en:** {tiempo_restante.days} días y {tiempo_restante.seconds // 3600} horas.")
    
    st.markdown("""
    | Puesto | Usuario | Puntuación | Premio Semanal |
    | :---: | :--- | :---: | :---: |
    | 🥇 **1°** | **Lud337 (Tú)** | 1,450 pts | $50.000 COP / USDT |
    | 🥈 **2°** | Carlos_99 | 1,320 pts | $30.000 COP / USDT |
    | 🥉 **3°** | SofiGamer | 1,100 pts | $20.000 COP / USDT |
    | 🏅 **4°** | AndresX | 950 pts | $10.000 COP / USDT |
    """)

elif opcion == "Solicitar Retiro y Conversor":
    st.title("💰 Conversor de Dinero y Retiro Real")
    st.write(f"Tu saldo actual es de **{st.session_state.saldo:.2f} 💎**.")
    
    # --- CONVERSOR DE DINERO ---
    # Tasa de conversión: 1 Diamante = $4,000 COP (o el valor que prefieras configurar)
    tasa_conversion = 4000 
    valor_cop = st.session_state.saldo * tasa_conversion
    
    st.info(f"💱 **Conversor automático:** Tus {st.session_state.saldo:.2f} 💎 equivalen a **${valor_cop:,.0f} COP** (Aprox. ${st.session_state.saldo * 1.0:.2f} USD).")
    
    st.markdown("---")
    st.subheader("Métodos de Retiro Disponibles")
    
    metodo = st.selectbox(
        "Selecciona tu método de pago:",
        ["Nequi", "DaviPlata", "PayPal", "PSE"]
    )
    
    cuenta_destino = st.text_input(f"Número de celular / Cuenta o Correo para {metodo}")
    monto_retiro = st.number_input("Monto en 💎 a retirar", min_value=5.0, max_value=float(max(5.0, st.session_state.saldo)), value=5.0)
    
    monto_cop_retiro = monto_retiro * tasa_conversion
    st.write(f"Monto a recibir: **${monto_cop_retiro:,.0f} COP**")
    
    if st.button("📤 Enviar Solicitud de Retiro"):
        if cuenta_destino and st.session_state.saldo >= monto_retiro:
            st.session_state.saldo -= monto_retiro
            st.success(f"¡Retiro de ${monto_cop_retiro:,.0f} COP procesado con éxito a través de {metodo} ({cuenta_destino})!")
        else:
            st.error("Por favor completa los datos de destino o verifica que tu saldo sea suficiente.")
