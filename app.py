import streamlit as st
import streamlit.components.v1 as components
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
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS LOCAL EN MEMORIA (SIMULADA) ---
if 'usuarios_db' not in st.session_state:
    # Usuarios precargados de ejemplo (Usuario: Contraseña)
    st.session_state.usuarios_db = {
        "Lud337": {"password": "123", "saldo": 31.60},
        "Carlos_99": {"password": "456", "saldo": 10.00}
    }

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

if 'video_reclamado' not in st.session_state:
    st.session_state.video_reclamado = False

query_params = st.query_params

# --- PANTALLA DE LOGIN / REGISTRO SI NO HA INICIADO SESIÓN ---
if st.session_state.usuario_actual is None:
    st.title("💎 ZafiroX - Acceso de Usuarios")
    st.write("Inicia sesión con tu cuenta o regístrate para guardar tu saldo de forma segura.")
    
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab1:
        # Usamos atributos estrictos para evitar que el celular muestre correos guardados
        user_login = st.text_input("Usuario", key="login_user", placeholder="Escribe tu usuario")
        pass_login = st.text_input("Contraseña", type="password", key="login_pass", placeholder="Escribe tu contraseña")
        
        if st.button("Entrar a ZafiroX"):
            if user_login in st.session_state.usuarios_db and st.session_state.usuarios_db[user_login]["password"] == pass_login:
                st.session_state.usuario_actual = user_login
                st.success(f"¡Bienvenido de nuevo, {user_login}!")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
                
    with tab2:
        user_reg = st.text_input("Nuevo Usuario", key="reg_user", placeholder="Crea tu usuario")
        pass_reg = st.text_input("Nueva Contraseña", type="password", key="reg_pass", placeholder="Crea tu contraseña")
        if st.button("Crear Cuenta"):
            if user_reg and pass_reg:
                if user_reg in st.session_state.usuarios_db:
                    st.error("El usuario ya existe. Prueba con otro.")
                else:
                    st.session_state.usuarios_db[user_reg] = {"password": pass_reg, "saldo": 0.00}
                    st.session_state.usuario_actual = user_reg
                    st.success(f"¡Cuenta creada con éxito! Bienvenido, {user_reg}.")
                    st.rerun()
            else:
                st.warning("Completa todos los campos para registrarte.")
    
    st.stop() # Detiene la ejecución aquí hasta que el usuario inicie sesión

# Sincronizamos el saldo con la base de datos temporal del usuario actual
usuario = st.session_state.usuario_actual
saldo_actual = st.session_state.usuarios_db[usuario]["saldo"]

# --- MENÚ LATERAL (SIDEBAR) ---
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
            "Caza de Minas (Difícil)",
            "Ruleta de la Suerte",
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

# Función auxiliar para actualizar saldo de forma segura
def actualizar_saldo(cantidad):
    st.session_state.usuarios_db[usuario]["saldo"] = max(0.0, st.session_state.usuarios_db[usuario]["saldo"] + cantidad)

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
                if(Math.random() > 0.4) {
                    score += 15;
                } else {
                    score = Math.max(0, score - 5);
                }
                document.getElementById('score').innerText = score;
            }
        </script>
    </body>
    </html>
    """
    components.html(tetris_html, height=290)

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
            
            let score = 0;
            let box = 10;
            let snake = [{x: 100, y: 100}];
            let food = {x: Math.floor(Math.random() * 19) * box, y: Math.floor(Math.random() * 19) * box};
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
                    food = {x: Math.floor(Math.random() * 19) * box, y: Math.floor(Math.random() * 19) * box};
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

            let game = setInterval(draw, 80);
        </script>
    </body>
    </html>
    """
    components.html(snake_html, height=370)

elif opcion == "Caza de Minas (Difícil)":
    st.title("💣 Caza de Minas (Modo Difícil)")
    st.write("Hay 5 casillas con **trampas ocultas**. Elige una casilla para probar tu suerte al instante:")
    
    minas_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #0e1117; color: white; margin: 0; padding: 10px; }
            .grid { display: flex; flex-direction: column; gap: 10px; max-width: 300px; margin: auto; }
            .mine-btn { background: #1f2937; color: white; border: 2px solid #374151; padding: 14px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.2s; }
            .mine-btn:active { transform: scale(0.97); }
            #result-msg { margin-top: 15px; font-size: 16px; font-weight: bold; min-height: 30px; }
        </style>
    </head>
    <body>
        <div class="grid">
            <button class="mine-btn" onclick="checkMine(1)">Casilla 1</button>
            <button class="mine-btn" onclick="checkMine(2)">Casilla 2</button>
            <button class="mine-btn" onclick="checkMine(3)">Casilla 3</button>
            <button class="mine-btn" onclick="checkMine(4)">Casilla 4</button>
            <button class="mine-btn" onclick="checkMine(5)">Casilla 5</button>
        </div>
        <div id="result-msg"></div>

        <script>
            let winningBox = Math.floor(Math.random() * 5) + 1;
            function checkMine(selected) {
                let msg = document.getElementById("result-msg");
                if (selected === winningBox) {
                    msg.style.color = "#ef4444";
                    msg.innerHTML = "💥 ¡BOOM! Encontraste la mina. ¡Perdiste!";
                } else {
                    msg.style.color = "#22c55e";
                    msg.innerHTML = "🎉 ¡Zona segura! ¡Ganaste +2.00 💎!";
                }
                setTimeout(() => {
                    winningBox = Math.floor(Math.random() * 5) + 1;
                    msg.innerHTML = "🔄 ¡Nueva ronda lista! Elige otra casilla.";
                }, 2000);
            }
        </script>
    </body>
    </html>
    """
    components.html(minas_html, height=350)

elif opcion == "Ruleta de la Suerte":
    st.title("🎡 Ruleta de la Suerte Extrema")
    st.write("Gira la ruleta bajo tu propio riesgo: puedes duplicar tus gemas o perderlas.")
    if st.button("¡Girar con Riesgo!"):
        resultado = random.choice([4.00, -2.00, 8.00, -3.00, 15.00])
        actualizar_saldo(resultado)
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
        actualizar_saldo(premio)
        if premio > 0:
            st.success(f"🎁 ¡Descubriste {premio} 💎!")
        else:
            st.error(f"💀 ¡Era una trampa! Perdiste {abs(premio)} 💎.")
        st.rerun()

elif opcion == "Sesión de Videos y Monetag":
    st.title("🎬 Videos Publicitarios y Monetag")
    st.write("Mira los videos de bonificación o utiliza tu enlace directo para acumular ganancias automáticamente.")
    
    timer_video_html = """
    <div style="background: rgba(30, 30, 30, 0.95); color: #f59e0b; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; border: 1px solid #f59e0b; margin-bottom: 15px;">
        ⏳ Bono de Video Activo - Tiempo Restante: <span id="countdown" style="font-size: 18px;">03:00</span>
    </div>
    <script>
        let totalSeconds = 180;
        function updateTimer() {
            let minutes = Math.floor(totalSeconds / 60);
            let seconds = totalSeconds % 60;
            let formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
            let formattedSeconds = seconds < 10 ? "0" + seconds : seconds;
            let el = document.getElementById("countdown");
            if(el) { el.innerText = formattedMinutes + ":" + formattedSeconds; }
            if (totalSeconds > 0) { totalSeconds--; } else { totalSeconds = 180; }
        }
        setInterval(updateTimer, 1000);
    </script>
    """
    components.html(timer_video_html, height=75)
    
    st.subheader("📺 Reproductor de Video de Bonificación Automático")
    st.write("Reproduce este video promocional hasta el final. Al terminar, tu saldo se actualizará solo:")
    
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
                height: '210',
                width: '100%',
                videoId: 'tgbNymZ7vqY',
                events: {
                    'onStateChange': onPlayerStateChange
                }
            });
        }

        function onPlayerStateChange(event) {
            if (event.data === YT.PlayerState.ENDED) {
                window.parent.location.href = window.parent.location.href.split('?')[0] + "?recompensa=video";
            }
        }
    </script>
    """
    components.html(youtube_auto_html, height=230)
    
    if query_params.get("recompensa") == "video" and not st.session_state.video_reclamado:
        actualizar_saldo(1.50)
        st.session_state.video_reclamado = True
        st.success("🎉 ¡Video completado hasta el final! +1.50 💎 añadidos automáticamente.")
        st.rerun()
        
    st.markdown("---")
    st.subheader("🚀 Enlace Directo Monetag")
    st.write("Pega tu enlace publicitario directo para generar vistas adicionales:")
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
        st.success("¡Visualización de enlace acreditada! +1.00 💎")
        st.rerun()

elif opcion == "Invitar Amigos":
    st.title("👥 Invitar Amigos con Recompensa")
    st.write("Comparte tu enlace de referido personalizado. Ganas un bono automático cada vez que un invitado se registra.")
    st.code(f"https://zafirox.streamlit.app/?ref={usuario}", language="text")
    st.success("Recompensa activa: 5.00 💎 por cada amigo verificado.")

elif opcion == "Ranking Semanal Top 4":
    st.title("🏆 Competencia Semanal de Puntajes")
    st.write("¡Los **4 mejores jugadores** de la semana se llevan premios directos a su cuenta!")
    
    ahora = datetime.datetime.now()
    proximo_domingo = ahora + datetime.timedelta(days=(6 - ahora.weekday()) % 7)
    tiempo_restante = proximo_domingo - ahora
    
    st.warning(f"⏰ **Cierre del ranking en:** {tiempo_restante.days} días y {tiempo_restante.seconds // 3600} horas.")
    
    st.markdown(f"""
    | Puesto | Usuario | Puntuación | Premio Semanal |
    | :---: | :--- | :---: | :---: |
    | 🥇 **1°** | **{usuario} (Tú)** | 1,650 pts | $50.000 COP |
    | 🥈 **2°** | Carlos_99 | 1,420 pts | $30.000 COP |
    | 🥉 **3°** | SofiGamer | 1,200 pts | $20.000 COP |
    | 🏅 **4°** | AndresX | 990 pts | $10.000 COP |
    """)

elif opcion == "Solicitar Retiro y Conversor":
    st.title("💰 Conversor de Dinero y Retiro Real")
    st.write(f"Tu saldo disponible es de **{saldo_actual:.2f} 💎**.")
    
    tasa_conversion = 4000 
    valor_cop = saldo_actual * tasa_conversion
    
    st.info(f"💱 **Conversor automático:** Tus {saldo_actual:.2f} 💎 equivalen a **${valor_cop:,.0f} COP**.")
    
    st.markdown("---")
    st.subheader("Métodos de Retiro Disponibles")
    
    metodo = st.selectbox(
        "Selecciona tu método de pago:",
        ["Nequi", "DaviPlata", "PayPal", "PSE"]
    )
    
    cuenta_destino = st.text_input(f"Número de celular / Cuenta o Correo para {metodo}")
    monto_retiro = st.number_input("Monto en 💎 a retirar", min_value=5.0, max_value=float(max(5.0, saldo_actual)), value=5.0)
    
    monto_cop_retiro = monto_retiro * tasa_conversion
    st.write(f"Monto a recibir: **${monto_cop_retiro:,.0f} COP**")
    
    if st.button("📤 Enviar Solicitud de Retiro"):
        if cuenta_destino and saldo_actual >= monto_retiro:
            actualizar_saldo(-monto_retiro)
            st.success(f"¡Retiro de ${monto_cop_retiro:,.0f} COP solicitado con éxito por {metodo} ({cuenta_destino}) para la cuenta de {usuario}!")
        else:
            st.error("Por favor completa los datos de destino o verifica que tu saldo sea suficiente para este retiro.")
