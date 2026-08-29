import streamlit as st
import datetime
import random
import json
import os

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

# --- ARCHIVO DE PERSISTENCIA PARA QUE NO SE PIERDAN LAS CUENTAS ---
DB_FILE = "usuarios_db.json"

def cargar_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {
        "Lud337": {"password": "123", "saldo": 31.60},
        "Carlos_99": {"password": "456", "saldo": 10.00}
    }

def guardar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

if 'usuarios_db' not in st.session_state:
    st.session_state.usuarios_db = cargar_db()

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

if 'video_reclamado' not in st.session_state:
    st.session_state.video_reclamado = False

query_params = st.query_params

# --- PANTALLA DE LOGIN / REGISTRO ---
if st.session_state.usuario_actual is None:
    st.title("💎 ZafiroX - Acceso de Usuarios")
    st.write("Inicia sesión o regístrate. Tus datos ahora se guardan de forma permanente.")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        user_login = st.text_input("Usuario", key="login_user", placeholder="Tu nombre de usuario")
        pass_login = st.text_input("Contraseña", type="password", key="login_pass", placeholder="Tu contraseña")
        
        if st.button("Entrar a ZafiroX"):
            db = st.session_state.usuarios_db
            if user_login in db and db[user_login]["password"] == pass_login:
                st.session_state.usuario_actual = user_login
                st.success(f"¡Bienvenido de nuevo, {user_login}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
                
    with tab2:
        user_reg = st.text_input("Nuevo Usuario", key="reg_user", placeholder="Elige un usuario")
        pass_reg = st.text_input("Nueva Contraseña", type="password", key="reg_pass", placeholder="Elige una contraseña")
        if st.button("Crear Cuenta"):
            if user_reg and pass_reg:
                db = st.session_state.usuarios_db
                if user_reg in db:
                    st.error("El usuario ya existe.")
                else:
                    db[user_reg] = {"password": pass_reg, "saldo": 0.00}
                    guardar_db(db)
                    st.session_state.usuario_actual = user_reg
                    st.success(f"¡Cuenta creada con éxito! Bienvenido, {user_reg}.")
                    st.rerun()
            else:
                st.warning("Completa todos los campos.")
    
    st.stop()

# Sincronizamos usuario activo y base de datos
usuario = st.session_state.usuario_actual
saldo_actual = st.session_state.usuarios_db[usuario]["saldo"]

def actualizar_saldo(cantidad):
    st.session_state.usuarios_db[usuario]["saldo"] = max(0.0, st.session_state.usuarios_db[usuario]["saldo"] + cantidad)
    guardar_db(st.session_state.usuarios_db)

# --- MENÚ LATERAL ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/controller.png", width=60)
    st.title("ZafiroX")
    st.write(f"Hola, **{usuario}** 👋")
    
    if st.button("🚪 Cerrar Sesión"):
        st.session_state.usuario_actual = None
        st.rerun()
        
    st.markdown("---")
    st.subheader("Menú Principal")
    
    opcion = st.selectbox(
        "Selecciona una sección:",
        [
            "Minijuego Bloques (Hard)",
            "Minijuego Snake (Hard)",
            "Caza de Minas (Casino)",
            "Cofres Misteriosos de Tensión",
            "Caja Misteriosa",
            "Sesión de Videos y Monetag",
            "Invitar Amigos",
            "Ranking Semanal Top 4",
            "Solicitar Retiro y Conversor"
        ]
    )
    
    st.markdown("---")
    st.write("💎 **Tu Saldo Actual:**")
    st.metric(label="", value=f"{saldo_actual:.2f} 💎")

# --- CONTENIDO DE SECCIONES ---

if opcion == "Minijuego Bloques (Hard)":
    st.title("🧩 Minijuego de Bloques (Modo Difícil)")
    st.write("¡Velocidad alta estilo Arcade para poner a prueba tus reflejos!")
    
    tetris_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 10px; }
            #game-container { max-width: 320px; margin: auto; background: #1e1e1e; padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            button { background: #ef4444; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; margin-top: 10px; width: 100%; font-weight: bold; }
            button:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div id="game-container">
            <h3>🔥 Arcade Extremo</h3>
            <p>Puntuación: <span id="score" style="color: #22c55e; font-size: 20px; font-weight: bold;">10</span></p>
            <canvas id="canvas" width="200" height="120" style="background:#111; display:block; margin: 0 auto; border-radius: 5px; border: 1px solid #444;"></canvas>
            <button onclick="actionBlock()">⚡ Acción / Colocar Pieza</button>
        </div>
        <script>
            let score = 10;
            function actionBlock() {
                if(Math.random() > 0.4) { score += 15; } else { score = Math.max(0, score - 5); }
                document.getElementById('score').innerText = score;
            }
        </script>
    </body>
    </html>
    """
    st.components.v1.html(tetris_html, height=290)

elif opcion == "Minijuego Snake (Hard)":
    st.title("🐍 Minijuego Snake (Modo Difícil)")
    st.write("¡Controla la serpiente a alta velocidad y evita chocar!")
    
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
            <canvas id="snakeCanvas" width="200" height="200" style="background: #111; border: 2px solid #ef4444; border-radius: 8px; display: block; margin: 0 auto;"></canvas>
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
            let score = 0, box = 10;
            let snake = [{x: 100, y: 100}];
            let food = {x: Math.floor(Math.random() * 19) * box, y: Math.floor(Math.random() * 19) * box};
            let d = "RIGHT", nextD = "RIGHT";

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
                let snakeX = snake[0].x, snakeY = snake[0].y;
                if (d === 'LEFT') snakeX -= box;
                if (d === 'UP') snakeY -= box;
                if (d === 'RIGHT') snakeX += box;
                if (d === 'DOWN') snakeY += box;
                if (snakeX === food.x && snakeY === food.y) {
                    score += 10;
                    document.getElementById("snake-score").innerText = score;
                    food = {x: Math.floor(Math.random() * 19) * box, y: Math.floor(Math.random() * 19) * box};
                } else { snake.pop(); }
                if (snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height) {
                    snake = [{x: 100, y: 100}]; score = 0;
                    document.getElementById("snake-score").innerText = score;
                    d = "RIGHT"; nextD = "RIGHT";
                    return;
                }
                snake.unshift({x: snakeX, y: snakeY});
            }
            setInterval(draw, 80);
        </script>
    </body>
    </html>
    """
    st.components.v1.html(snake_html, height=370)

elif opcion == "Caza de Minas (Casino)":
    st.title("💣 Caza de Minas (Estilo Casino)")
    st.write("¡Apuesta con inteligencia! Elige una casilla: 4 están a salvo con multiplicadores y 1 oculta la trampa.")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("Casilla 1"):
            res = random.choice([2.0, -1.0])
            actualizar_saldo(res)
            if res > 0: st.success("¡Salvado! +2.0 💎")
            else: st.error("¡Boom! -1.0 💎")
            st.rerun()
    with col2:
        if st.button("Casilla 2"):
            res = random.choice([3.0, -1.5])
            actualizar_saldo(res)
            if res > 0: st.success("¡Salvado! +3.0 💎")
            else: st.error("¡Boom! -1.5 💎")
            st.rerun()
    with col3:
        if st.button("Casilla 3"):
            res = random.choice([1.5, -2.0])
            actualizar_saldo(res)
            if res > 0: st.success("¡Salvado! +1.5 💎")
            else: st.error("¡Boom! -2.0 💎")
            st.rerun()
    with col4:
        if st.button("Casilla 4"):
            res = random.choice([4.0, -2.5])
            actualizar_saldo(res)
            if res > 0: st.success("¡Premio! +4.0 💎")
            else: st.error("¡Boom! -2.5 💎")
            st.rerun()
    with col5:
        if st.button("Casilla 5"):
            res = random.choice([5.0, -3.0])
            actualizar_saldo(res)
            if res > 0: st.success("¡Jackpot! +5.0 💎")
            else: st.error("¡Boom! -3.0 💎")
            st.rerun()

elif opcion == "Cofres Misteriosos de Tensión":
    st.title("🗝️ Cofres de Tensión ZafiroX")
    st.write("Selecciona uno de los 3 cofres ocultos para reclamar tu botín.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎁 Cofre 1"):
            premio = random.choice([5.00, 2.00, -1.00])
            actualizar_saldo(premio)
            if premio > 0: st.success(f"¡Increíble! +{premio} 💎")
            else: st.error("¡Cofre vacío! -1.00 💎")
            st.rerun()
    with col2:
        if st.button("🎁 Cofre 2"):
            premio = random.choice([10.00, 1.00, -2.00])
            actualizar_saldo(premio)
            if premio > 0: st.success(f"¡Premio gordo! +{premio} 💎")
            else: st.error("¡Trampa en el cofre! -2.00 💎")
            st.rerun()
    with col3:
        if st.button("🎁 Cofre 3"):
            premio = random.choice([4.00, 3.00, -1.50])
            actualizar_saldo(premio)
            if premio > 0: st.success(f"¡Buen botín! +{premio} 💎")
            else: st.error("¡Mala suerte! -1.50 💎")
            st.rerun()

elif opcion == "Caja Misteriosa":
    st.title("📦 Caja Misteriosa de Alto Riesgo")
    st.write("Abre la caja para descubrir tu premio o sorpresa.")
    if st.button("Abrir Caja"):
        premio = random.choice([3.50, -1.50, 6.00])
        actualizar_saldo(premio)
        if premio > 0:
            st.success(f"🎁 ¡Descubriste {premio} 💎!")
        else:
            st.error(f"💀 ¡Era una trampa! Perdiste {abs(premio)} 💎.")
        st.rerun()

elif opcion == "Sesión de Videos y Monetag":
    st.title("🎬 Videos Publicitarios y Monetag")
    st.write("Mira los videos de bonificación o utiliza tu enlace directo.")
    
    timer_video_html = """
    <div style="background: rgba(30, 30, 30, 0.95); color: #f59e0b; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; border: 1px solid #f59e0b; margin-bottom: 15px;">
        ⏳ Bono de Video Activo - Tiempo Restante: <span id="countdown" style="font-size: 18px;">03:00</span>
    </div>
    <script>
        let totalSeconds = 180;
        function updateTimer() {
            let minutes = Math.floor(totalSeconds / 60);
            let seconds = totalSeconds % 60;
            let el = document.getElementById("countdown");
            if(el) { el.innerText = (minutes < 10 ? "0" + minutes : minutes) + ":" + (seconds < 10 ? "0" + seconds : seconds); }
            if (totalSeconds > 0) { totalSeconds--; } else { totalSeconds = 180; }
        }
        setInterval(updateTimer, 1000);
    </script>
    """
    st.components.v1.html(timer_video_html, height=75)
    
    youtube_auto_html = """
    <div style="text-align: center;">
        <div id="player" style="border-radius: 8px; overflow: hidden; display:inline-block;"></div>
    </div>
    <script>
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        var player;
        function onYouTubeIframeAPIReady() {
            player = new YT.Player('player', {
                height: '210', width: '100%', videoId: 'tgbNymZ7vqY',
                events: { 'onStateChange': onPlayerStateChange }
            });
        }
        function onPlayerStateChange(event) {
            if (event.data === YT.PlayerState.ENDED) {
                window.parent.location.href = window.parent.location.href.split('?')[0] + "?recompensa=video";
            }
        }
    </script>
    """
    st.components.v1.html(youtube_auto_html, height=230)
    
    if query_params.get("recompensa") == "video" and not st.session_state.video_reclamado:
        actualizar_saldo(1.50)
        st.session_state.video_reclamado = True
        st.success("🎉 ¡Video completado! +1.50 💎 añadidos.")
        st.rerun()
        
    st.markdown("---")
    st.subheader("🚀 Enlace Directo Monetag")
    enlace_monetag = st.text_input("Tu enlace directo de Monetag:", value="https://www.profitablecpmrate.com/tu_codigo_aqui")
    
    st.markdown(f"""
        <div style="text-align: center; margin: 15px 0;">
            <a href="{enlace_monetag}" target="_blank">
                <button style="background-color: #f59e0b; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%;">
                    ⚡ Abrir Enlace Publicitario Monetag
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Confirmar visualización de enlace"):
        actualizar_saldo(1.00)
        st.success("¡Visualización acreditada! +1.00 💎")
        st.rerun()

elif opcion == "Invitar Amigos":
    st.title("👥 Invitar Amigos con Recompensa")
    st.code(f"https://zafirox.streamlit.app/?ref={usuario}", language="text")
    st.success("Recompensa activa: 5.00 💎 por cada amigo invitado.")

elif opcion == "Ranking Semanal Top 4":
    st.title("🏆 Competencia Semanal de Puntajes")
    
    countdown_clock_html = """
    <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #ef4444; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 15px;">
        ⏰ Cierre del ranking en tiempo real: <span id="live-clock" style="font-size: 18px; color: #fff;">Calculando...</span>
    </div>
    <script>
        let countDownDate = new Date().getTime() + (2 * 24 * 60 * 60 * 1000);
        let x = setInterval(function() {
            let now = new Date().getTime();
            let distance = countDownDate - now;
            let days = Math.floor(distance / (1000 * 60 * 60 * 24));
            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);
            document.getElementById("live-clock").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("live-clock").innerHTML = "¡COMPETENCIA FINALIZADA!";
            }
        }, 1000);
    </script>
    """
    st.components.v1.html(countdown_clock_html, height=75)
    
    puntos_usuario = 1650 + int(saldo_actual * 10)
    
    st.markdown(f"""
    | Puesto | Usuario | Puntuación | Premio Semanal |
    | :---: | :--- | :---: | :---: |
    | 🥇 **1°** | **{usuario} (Tú)** | {puntos_usuario:,} pts | $50.000 COP |
    | 🥈 **2°** | CyberKing_99 | 1,420 pts | $30.000 COP |
    | 🥉 **3°** | ZafiroQueen | 1,200 pts | $20.000 COP |
    | 🏅 **4°** | NeoGamer_X | 990 pts | $10.000 COP |
    """)

elif opcion == "Solicitar Retiro y Conversor":
    st.title("💰 Conversor de Dinero y Retiro Real")
    st.write(f"Tu saldo disponible es de **{saldo_actual:.2f} 💎**.")
    
    tasa_conversion = 4000 
    valor_cop = saldo_actual * tasa_conversion
    st.info(f"💱 **Conversor automático:** Tus {saldo_actual:.2f} 💎 equivalen a **${valor_cop:,.0f} COP**.")
    
    st.markdown("---")
    metodo = st.selectbox("Selecciona tu método de pago:", ["Nequi", "DaviPlata", "PayPal", "PSE"])
    cuenta_destino = st.text_input(f"Número de celular / Cuenta o Correo para {metodo}")
    monto_retiro = st.number_input("Monto en 💎 a retirar", min_value=5.0, max_value=float(max(5.0, saldo_actual)), value=5.0)
    
    monto_cop_retiro = monto_retiro * tasa_conversion
    st.write(f"Monto a recibir: **${monto_cop_retiro:,.0f} COP**")
    
    if st.button("📤 Enviar Solicitud de Retiro"):
        if cuenta_destino and saldo_actual >= monto_retiro:
            actualizar_saldo(-monto_retiro)
            st.success(f"¡Retiro de ${monto_cop_retiro:,.0f} COP solicitado con éxito por {metodo} ({cuenta_destino})!")
        else:
            st.error("Completa los datos de destino o verifica que tu saldo sea suficiente.")
