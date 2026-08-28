import streamlit as st
import streamlit.components.v1 as components
import time
import datetime
import random

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
    .floating-timer {
        position: fixed;
        top: 60px;
        right: 15px;
        background: rgba(30, 30, 30, 0.9);
        color: #f59e0b;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: bold;
        z-index: 99999;
        border: 1px solid #f59e0b;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DE LA SESIÓN ---
if 'saldo' not in st.session_state:
    st.session_state.saldo = 31.60
if 'tiempo_inicio' not in st.session_state:
    st.session_state.tiempo_inicio = time.time()
if 'mina_pos' not in st.session_state:
    st.session_state.mina_pos = random.randint(1, 5)
if 'tiempo_sesion_video' not in st.session_state:
    st.session_state.tiempo_sesion_video = 300  # 5 minutos de cuenta regresiva para el bono de video

# Calcular el tiempo restante de la sesión de video de forma dinámica
tiempo_transcurrido_total = int(time.time() - st.session_state.tiempo_inicio)
tiempo_restante_video = max(0, st.session_state.tiempo_sesion_video - (tiempo_transcurrido_total % st.session_state.tiempo_sesion_video))
minutos_v = tiempo_restante_video // 60
segundos_v = tiempo_restante_video % 60

# --- WIDGET FLOTANTE DE TEMPORIZADOR REGRESIVO (POR ENCIMA DE TODO) ---
st.markdown(f"""
    <div class="floating-timer">
        ⏳ Bono Video: {minutos_v:02d}:{segundos_v:02d}
    </div>
""", unsafe_allow_html=True)

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
            "Minijuego Bloques (Hard)",
            "Minijuego Snake (Hard)",
            "Caza de Minas (Difícil)",
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

if opcion == "Minijuego Bloques (Hard)":
    st.title("🧩 Minijuego de Bloques (Modo Difícil)")
    st.write("¡Velocidad alta estilo Arcade! Pon a prueba tus reflejos para acumular puntos.")
    
    tetris_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 10px; }
            #game-container { max-width: 320px; margin: auto; background: #1e1e1e; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            button { background: #ef4444; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-top: 10px; width: 100%; font-weight: bold; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <h3>🔥 Arcade Extremo</h3>
            <p>Puntuación: <span id="score">10</span></p>
            <canvas id="canvas" width="200" height="150" style="background:#111; display:block; margin: 0 auto; border-radius: 5px;"></canvas>
            <button onclick="actionBlock()">⚡ Acción / Colocar Pieza</button>
        </div>
        <script>
            let score = 10;
            function actionBlock() {
                if(Math.random() > 0.45) {
                    score += 10;
                } else {
                    score = Math.max(0, score - 8);
                }
                document.getElementById('score').innerText = score;
            }
        </script>
    </body>
    </html>
    """
    components.html(tetris_html, height=350)

elif opcion == "Minijuego Snake (Hard)":
    st.title("🐍 Minijuego Snake (Modo Difícil)")
    st.write("¡La serpiente se mueve a alta velocidad y el margen de error es mínimo!")
    
    snake_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 5px; }
            .controls { display: grid; grid-template-columns: repeat(3, 60px); gap: 6px; justify-content: center; margin-top: 12px; }
            button { background: #ef4444; color: white; border: none; padding: 14px; font-size: 20px; border-radius: 8px; cursor: pointer; font-weight: bold; }
            button:active { background: #dc2626; transform: scale(0.95); }
            .empty { background: transparent; border: none; cursor: default; }
        </style>
    </head>
    <body>
        <div style="max-width: 300px; margin: auto;">
            <p>Puntuación: <span id="snake-score" style="color: #ef4444; font-weight: bold; font-size: 18px;">0</span></p>
            <canvas id="snakeCanvas" width="220" height="220" style="background: #111; border: 2px solid #ef4444; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
            
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
                    ctx.fillStyle = (i === 0) ? "#ef4444" : "#991b1b";
                    ctx.fillRect(snake[i].x, snake[i].y, box, box);
                }

                ctx.fillStyle = "#22c55e";
                ctx.fillRect(food.x, food.y, box, box);

                d = nextD;
                let snakeX = snake[0].x;
                let snakeY = snake[0].y;

                if (d === 'LEFT') snakeX -= box;
                if (d === 'UP') snakeY -= box;
                if (d === 'RIGHT') snakeX += box;
                if (d === 'DOWN') snakeY += box;

                if (snakeX === food.x && snakeY === food.y) {
                    score += 10;
                    document.getElementById("snake-score").innerText = score;
                    food = {x: Math.floor(Math.random() * 21) * box, y: Math.floor(Math.random() * 21) * box};
                } else {
                    snake.pop();
                }

                if (snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height) {
                    snake = [{x: 100, y: 100}];
                    score = 0;
                    document.getElementById("snake-score").innerText = score;
                    d = "RIGHT";
                    nextD = "RIGHT";
                    return;
                }

                snake.unshift({x: snakeX, y: snakeY});
            }

            let game = setInterval(draw, 70); // Alta velocidad
        </script>
    </body>
    </html>
    """
    components.html(snake_html, height=410)

elif opcion == "Caza de Minas (Difícil)":
    st.title("💣 Caza de Minas (Modo Difícil)")
    st.write("Hay 5 casillas con **trampas ocultas**. Si eliges mal, perderás saldo. ¡Alto riesgo, alta recompensa!")
    
    cols = st.columns(5)
    for i in range(1, 6):
        with cols[i-1]:
            if st.button(f"Casilla {i}"):
                if i == st.session_state.mina_pos:
                    st.session_state.saldo = max(0.0, st.session_state.saldo - 2.50)
                    st.error(f"💥 ¡BOOM! La casilla {i} ocultaba una mina. -2.50 💎")
                    st.session_state.mina_pos = random.randint(1, 5)
                    st.rerun()
                else:
                    st.session_state.saldo += 2.00
                    st.success(f"🎉 ¡Zona segura! +2.00 💎")
                    st.session_state.mina_pos = random.randint(1, 5)
                    st.rerun()

elif opcion == "Ruleta de la Suerte":
    st.title("🎡 Ruleta de la Suerte Extrema")
    st.write("Gira la ruleta bajo tu propio riesgo: puedes duplicar tus gemas o perderlas.")
    if st.button("¡Girar con Riesgo!"):
        resultado = random.choice([4.00, -2.00, 8.00, -3.00, 15.00])
        st.session_state.saldo = max(0.0, st.session_state.saldo + resultado)
        if resultado > 0:
            st.success(f"🎉 ¡Ganaste {resultado} 💎!")
        else:
            st.error(f"⚠️ ¡Cayó penalización! Perdiste {abs(resultado)} 💎.")
        st.rerun()

elif opcion == "Caja Misteriosa":
    st.title("📦 Caja Misteriosa de Alto Riesgo")
    st.write("Una caja cerrada que esconde premios jugosos o sorpresas amargas.")
    if st.button("Abrir Caja"):
        premio = random.choice([3.50, -1.50, 6.00])
        st.session_state.saldo = max(0.0, st.session_state.saldo + premio)
        if premio > 0:
            st.success(f"🎁 ¡Descubriste {premio} 💎!")
        else:
            st.error(f"💀 ¡Era una trampa! Perdiste {abs(premio)} 💎.")
        st.rerun()

elif opcion == "Ganar por Tiempo y Anuncios (Monetag)":
    st.title("⏱️ Sesión de Video y Anuncios Monetag")
    st.write("Mantén abierta tu sesión y utiliza tu enlace directo de Monetag para acumular bonos por uso estilo Terybit.")
    
    tiempo_transcurrido = int(time.time() - st.session_state.tiempo_inicio)
    st.info(f"⏳ Llevas **{tiempo_transcurrido} segundos** activos en la plataforma.")
    
    if st.button("Reclamar Bono por Tiempo Activo"):
        st.session_state.saldo += 0.50
        st.success("¡Bono por tiempo reclamado! +0.50 💎")
        
    st.markdown("---")
    st.subheader("📺 Enlace Directo de Monetag")
    st.write("Pega aquí tu enlace directo exacto que te otorga Monetag para que los usuarios abran tu publicidad de forma correcta:")
    
    enlace_monetag = st.text_input("Tu enlace directo de Monetag:", value="https://www.profitablecpmrate.com/tu_codigo_aqui")
    
    st.markdown(f"""
        <div style="text-align: center; margin: 15px 0;">
            <a href="{enlace_monetag}" target="_blank">
                <button style="background-color: #f59e0b; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%;">
                    🚀 Ver Anuncio Monetag (Abrir enlace publicitario)
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Confirmar visualización"):
        st.session_state.saldo += 1.00
        st.success("¡Visualización registrada y acreditada! +1.00 💎")
        st.rerun()

elif opcion == "Invitar Amigos":
    st.title("👥 Invitar Amigos con Recompensa")
    st.write("Comparte tu enlace de referido personalizado. Ganas un bono automático cada vez que un invitado se registra.")
    st.code("https://zafirox.streamlit.app/?ref=Lud337", language="text")
    st.success("Recompensa activa: 5.00 💎 por cada amigo verificado.")

elif opcion == "Ranking Semanal Top 4":
    st.title("🏆 Competencia Semanal de Puntajes")
    st.write("¡Los **4 mejores jugadores** de la semana se llevan premios directos a su cuenta!")
    
    ahora = datetime.datetime.now()
    proximo_domingo = ahora + datetime.timedelta(days=(6 - ahora.weekday()) % 7)
    tiempo_restante = proximo_domingo - ahora
    
    st.warning(f"⏰ **Cierre del ranking en:** {tiempo_restante.days} días y {tiempo_restante.seconds // 3600} horas.")
    
    st.markdown("""
    | Puesto | Usuario | Puntuación | Premio Semanal |
    | :---: | :--- | :---: | :---: |
    | 🥇 **1°** | **Lud337 (Tú)** | 1,650 pts | $50.000 COP |
    | 🥈 **2°** | Carlos_99 | 1,420 pts | $30.000 COP |
    | 🥉 **3°** | SofiGamer | 1,200 pts | $20.000 COP |
    | 🏅 **4°** | AndresX | 990 pts | $10.000 COP |
    """)

elif opcion == "Solicitar Retiro y Conversor":
    st.title("💰 Conversor de Dinero y Retiro Real")
    st.write(f"Tu saldo disponible es de **{st.session_state.saldo:.2f} 💎**.")
    
    tasa_conversion = 4000 
    valor_cop = st.session_state.saldo * tasa_conversion
    
    st.info(f"💱 **Conversor automático:** Tus {st.session_state.saldo:.2f} 💎 equivalen a **${valor_cop:,.0f} COP**.")
    
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
            st.success(f"¡Retiro de ${monto_cop_retiro:,.0f} COP solicitado con éxito por {metodo} ({cuenta_destino})!")
        else:
            st.error("Por favor completa los datos de destino o verifica que tu saldo sea suficiente para este retiro.")
