elif "🐍 Minijuego Snake (Nuevo)" in menu_opcion:
    st.markdown("# 🐍 Minijuego Snake Retro")
    st.markdown("### ¡Controla la serpiente, come gemas y acumula puntos para tu balance!")
    
    # Incrustamos un juego clásico de Snake en HTML5/JS adaptado para móviles
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
            let snake = [{x: 9 * box, y: 10 * box}];
            let food = {
                x: Math.floor(Math.random() * 14) * box,
                y: Math.floor(Math.random() * 14) * box
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
                        x: Math.floor(Math.random() * 14) * box,
                        y: Math.floor(Math.random() * 14) * box
                    };
                } else {
                    snake.pop();
                }

                let newHead = {x: snakeX, y: snakeY};

                if(snakeX < 0 || snakeX >= 280 || snakeY < 0 || snakeY >= 280 || collision(newHead, snake)) {
                    clearInterval(game);
                    alert("¡Juego terminado! Puntuación final: " + score);
                }

                snake.unshift(newHead);
            }

            function collision(head, array) {
                for(let i = 0; i < array.length; i++) {
                    if(head.x == array[i].x && head.y == array[i].y) return true;
                }
                return false;
            }

            let game = setInterval(draw, 180);
        </script>
        """,
        height=450
    )
