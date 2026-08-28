import streamlit as st
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="ZafiroX - Minijuegos y Recompensas", layout="centered")

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
            "💎 Caza de Gemas",
            "🎡 Ruleta de la Suerte",
            "🧩 Minijuego Retro",
            "🐍 Minijuego Snake",
            "📺 Ver Videos Premiados",
            "🎬 Sesión de Video con Reto",
            "👥 Invitar Amigos",
            "💵 Solicitar Retiro",
            "🚪 Cerrar Sesión"
        ],
        label_visibility="collapsed"
    )

monetag_url = "https://omg10.com/4/11676106"

if menu_opcion == "💎 Caza de Gemas":
    st.markdown("# 💎 Caza de Gemas (Nivel Difícil)")
    st.markdown("### ¡Encuentra la única gema entre 9 opciones y gana 15.00 💎!")
    st.warning("⚠️ ¡Cuidado con las trampas de rocas vacías!")

    if "gema_secreta" not in st.session_state:
        st.session_state.gema_secreta = random.randint(0, 8)

    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if st.button(f"🪨 Roca {i+1}", key=f"roca_{i}"):
                if i == st.session_state.gema_secreta:
                    st.balloons()
                    st.success("¡Increíble! ¡Encontraste la Gema oculta! +15.00 💎")
                    st.session_state.gema_secreta = random.randint(0, 8)
                else:
                    st.error("❌ ¡Era solo una roca vacía! Perdiste este turno.")

    if st.button("🔄 Reiniciar Tablero"):
        st.session_state.gema_secreta = random.randint(0, 8)
        st.rerun()

elif menu_opcion == "🎡 Ruleta de la Suerte":
    st.markdown("# 🎡 Ruleta de la Suerte")
    st.markdown("### ¡Gira la ruleta gigante para multiplicar tus recompensas!")
    
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.ibb.co/2M0gQ6z/ruleta-icono.png" width="320" style="border-radius: 50%; box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin: 15px 0;">
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🎲 ¡GIRAR LA RULETA AHORA!", use_container_width=True):
        premios = [2.00, 5.00, 10.00, 0.00, 20.00, 1.00]
        premio = random.choice(premios)
        if premio > 0:
            st.success(f"🎉 ¡Felicidades! La ruleta se detuvo en {premio} 💎")
        else:
            st.error("😢 ¡Mala suerte! Cayó en cero.")

elif menu_opcion == "🧩 Minijuego Retro":
    st.markdown("# 🧩 Minijuego de Bloques")
    st.markdown("### ¡Rompe líneas y acumula puntos de bonificación!")
    
    components.html(
        """
        <div style="text-align:center; background:#111; padding:20px; border-radius:12px; color:white; font-family:sans-serif;">
            <h3>🕹️ Área de Juego Arcade</h3>
            <p>Haz clic para acelerar y sumar puntos.</p>
            <div id="score" style="font-size:24px; color:#00ffcc; margin:15px 0;">Puntuación: 0</div>
            <button onclick="addScore()" style="padding:12px 24px; background:#6C63FF; color:white; border:none; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer;">🎮 Jugar / Sumar Puntos</button>
        </div>
        <script>
            let s = 0;
            function addScore() {
                s += Math.floor(Math.random() * 50) + 10;
                document.getElementById('score').innerText = 'Puntuación: ' + s;
            }
        </script>
        """,
        height=260
    )

elif menu_opcion == "🐍 Minijuego Snake":
    st.markdown("# 🐍 Minijuego Snake Retro")
    st.markdown("### ¡Controla la serpiente, come gemas y acumula puntos!")
    
    components.html(
        """
        <div style="text-align:center; background:#18181b; padding:15px; border-radius:12px; color:white; font-family:sans-serif; max-width:320px; margin:auto;">
            <h3>🐍 Culebrita ZafiroX</h3>
            <canvas id="snakeCanvas" width="280" height="280" style="background:#000; border-radius:8px; border:2px solid #6C63FF;"></canvas>
            <div id="snakeScore" style="font-size:18px; color:#00ffcc; margin:10px 0;">Puntuación: 0</div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:5px; max-width:180px; margin:0 auto;">
                <div></div>
                <button onclick="changeDir('UP')" style="padding:10px; background:#6C63FF; color:white; border:none; border-radius:5px; font-weight:bold;">⬆️</button>
                <div></div>
                <button onclick="changeDir('LEFT')" style="padding:10px; background:#6C63FF; color:white; border:none; border-radius:5px; font-weight:bold;">⬅️</button>
                <button onclick="changeDir('DOWN')" style="padding:10px; background:#6C63FF; color:white; border:none; border-radius:5px; font-weight:bold;">⬇️</button>
                <button onclick="changeDir('RIGHT')" style="padding:10px; background:#6C63FF; color:white; border:none; border-radius:5px; font-weight:bold;">➡️</button>
            </div>
        </div>
        <script>
            const canvas = document.getElementById("snakeCanvas");
            const ctx = canvas.getContext("2d");
            let box = 20;
            let snake = [
                {x: 6 * box, y: 6 * box},
                {x: 5 * box, y: 6 * box},
                {x: 4 * box, y: 6 * box}
            ];
            let food = {
                x: Math.floor(Math.random() * 12 + 1) * box,
                y: Math.floor(Math.random() * 12 + 1) * box
            };
            let score = 0;
            let d = "RIGHT";

            function changeDir(dir) {
                if(dir == "LEFT" && d != "RIGHT") d = "LEFT";
                else if(dir == "UP" && d != "DOWN") d = "UP";
                else if(dir == "RIGHT" && d != "LEFT") d = "RIGHT";
                else if(dir == "DOWN" && d != "UP") d = "DOWN";
            }

            function draw() {
                ctx.fillStyle = "#000";
                ctx.fillRect(0, 0, 280, 280);

                for(let i = 0; i < snake.length; i++) {
                    ctx.fillStyle = i == 0 ? "#00ffcc" : "#6C63FF";
                    ctx.fillRect(snake[i].x, snake[i].y, box, box);
                }

                ctx.fillStyle = "#ff416c";
                ctx.fillRect(food.x, food.y, box, box);

                let snakeX = snake[0].x;
                let snakeY = snake[0].y;

                if(d == "LEFT") snakeX -= box;
                if(d == "UP") snakeY -= box;
                if(d == "RIGHT") snakeX += box;
                if(d == "DOWN") snakeY += box;

                if(snakeX == food.x && snakeY == food.y) {
                    score += 5;
                    document.getElementById("snakeScore").innerText = "Puntuación: " + score;
                    food = {
                        x: Math.floor(Math.random() * 12 + 1) * box,
                        y: Math.floor(Math.random() * 12 + 1) * box
                    };
                } else {
                    snake.pop();
                }

                let newHead = {x: snakeX, y: snakeY};

                if(snakeX < 0 || snakeX >= 280 || snakeY < 0 || snakeY >= 280 || collision(newHead, snake)) {
                    clearInterval(game);
                    alert("¡Juego terminado! Puntuación final: " + score);
                    return;
                }

                snake.unshift(newHead);
            }

            function collision(head, array) {
                for(let i = 0; i < array.length; i++) {
                    if(head.x == array[i].x && head.y == array[i].y) return true;
                }
                return false;
            }

            let game = setInterval(draw, 220);
        </script>
        """,
        height=450
    )

elif menu_opcion == "📺 Ver Videos Premiados":
    st.markdown("# 📺 Ver Videos y Anuncios Patrocinados")
    st.markdown("### Haz clic en el botón para ver el anuncio publicitario y registrar tu actividad:")
    
    st.markdown(
        f"""
        <div style="text-align: center; margin: 30px 0;">
            <a href="{monetag_url}" target="_blank" style="
                display: block;
                padding: 1.2em;
                color: white;
                background: linear-gradient(135deg, #FF416C, #FF4B2B);
                text-align: center;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.2em;
                border-radius: 12px;
                box-shadow: 0 6px 12px rgba(255,65,108,0.3);
            ">🎬 VER ANUNCIO PUBLICITARIO (Reclamar 5.00 💎)</a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif menu_opcion == "🎬 Sesión de Video con Reto":
    st.markdown("# 🎬 Sesión de Video Interactiva")
    st.markdown("### Demuestra que viste el contenido respondiendo el reto:")
    
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    st.markdown("---")
    respuesta = st.radio("¿De qué color era el objeto principal al minuto 1:00?", ["Rojo", "Azul", "Verde", "No lo vi"])
    
    if st.button("Validar y Reclamar Bono"):
        if respuesta == "Azul":
            st.success("✅ ¡Respuesta correcta! +5.00 💎 sumados a tu cuenta.")
        else:
            st.error("❌ Respuesta incorrecta o no has visto el video completo. ¡Inténtalo de nuevo!")

elif menu_opcion == "🎁 Caja Misteriosa":
    st.markdown("# 🎁 Caja Misteriosa")
    st.markdown("### Abre la caja para descubrir tu premio sorpresa.")
    if st.button("📦 Abrir Caja"):
        st.success("¡Premio de 10.00 💎 desbloqueado con éxito!")

elif menu_opcion == "👥 Invitar Amigos":
    st.markdown("# 👥 Invitar Amigos")
    st.markdown("### Comparte tu enlace de referencia:")
    st.code("https://zafirox-minijuegos.streamlit.app/?ref=Lud337")

elif menu_opcion == "💵 Solicitar Retiro":
    st.markdown("# 💵 Solicitar Retiro")
    st.markdown("### Métodos disponibles: PayPal, Nequi, Daviplata, PSE")
    st.info("Tu saldo actual es de 27.40 💎. ¡Sigue completando retos para alcanzar el mínimo!")

else:
    st.markdown("# 🚪 Cerrar Sesión")
    st.markdown("Has cerrado sesión correctamente.")
