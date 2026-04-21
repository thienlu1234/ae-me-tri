import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Vòng quay chọn người thắng", page_icon="🎡", layout="wide")

st.title("🎡 Vòng quay chọn người thắng")

default_names = "An\nBình\nChi\nDũng\nHà\nLan"
names_input = st.text_area(
    "Nhập danh sách (mỗi người 1 dòng)",
    value=default_names,
    height=180
)

names = [n.strip() for n in names_input.split("\n") if n.strip()]

if len(names) < 2:
    st.warning("Hãy nhập ít nhất 2 người để quay.")
else:
    names_js = str(names)

    html_code = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8" />
        <style>
            * {{
                box-sizing: border-box;
                font-family: Arial, sans-serif;
            }}

            body {{
                margin: 0;
                padding: 0;
                background: white;
            }}

            .wrap {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 10px 0 30px;
            }}

            .wheel-area {{
                position: relative;
                width: 520px;
                height: 520px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .pointer {{
                position: absolute;
                top: 8px;
                left: 50%;
                transform: translateX(-50%);
                width: 0;
                height: 0;
                border-left: 22px solid transparent;
                border-right: 22px solid transparent;
                border-top: 0;
                border-bottom: 42px solid #e53935;
                z-index: 20;
                filter: drop-shadow(0 2px 2px rgba(0,0,0,0.25));
            }}

            canvas {{
                border-radius: 50%;
                background: #fff;
                box-shadow:
                    0 0 0 10px #d4a017,
                    0 0 0 18px #f7d774,
                    0 10px 25px rgba(0,0,0,0.2);
            }}

            .center-circle {{
                position: absolute;
                width: 90px;
                height: 90px;
                border-radius: 50%;
                background: radial-gradient(circle, #ffd95a 0%, #f4b400 60%, #c88700 100%);
                border: 6px solid #fff3c4;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                z-index: 15;
            }}

            .spin-btn {{
                margin-top: 28px;
                padding: 14px 34px;
                border: none;
                border-radius: 14px;
                background: linear-gradient(180deg, #ff6aa2 0%, #ff3d7f 100%);
                color: white;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 6px 16px rgba(255, 61, 127, 0.35);
                transition: transform 0.15s ease;
            }}

            .spin-btn:hover {{
                transform: translateY(-1px);
            }}

            .spin-btn:disabled {{
                opacity: 0.6;
                cursor: not-allowed;
            }}

            .result {{
                margin-top: 24px;
                font-size: 30px;
                font-weight: bold;
                color: #1f2a44;
                text-align: center;
                min-height: 40px;
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="wheel-area">
                <div class="pointer"></div>
                <canvas id="wheel" width="460" height="460"></canvas>
                <div class="center-circle"></div>
            </div>

            <button class="spin-btn" id="spinBtn">🎯 Quay!</button>
            <div class="result" id="result">🎉 Người thắng: ?</div>
        </div>

        <script>
            const names = {names_js};
            const canvas = document.getElementById("wheel");
            const ctx = canvas.getContext("2d");
            const resultEl = document.getElementById("result");
            const spinBtn = document.getElementById("spinBtn");

            const size = canvas.width;
            const center = size / 2;
            const radius = center - 10;
            const sliceAngle = (Math.PI * 2) / names.length;

            const colors = [
                "#ff4d6d", "#3a86ff", "#8338ec", "#ffbe0b",
                "#2ec4b6", "#8ac926", "#ff924c", "#9d4edd",
                "#00b4d8", "#f15bb5", "#43aa8b", "#f3722c"
            ];

            let currentRotation = 0;
            let isSpinning = false;

            function drawWheel(rotation = 0) {{
                ctx.clearRect(0, 0, size, size);

                for (let i = 0; i < names.length; i++) {{
                    const startAngle = rotation + i * sliceAngle - Math.PI / 2;
                    const endAngle = startAngle + sliceAngle;

                    ctx.beginPath();
                    ctx.moveTo(center, center);
                    ctx.arc(center, center, radius, startAngle, endAngle);
                    ctx.closePath();
                    ctx.fillStyle = colors[i % colors.length];
                    ctx.fill();

                    ctx.save();
                    ctx.translate(center, center);
                    ctx.rotate(startAngle + sliceAngle / 2);

                    ctx.fillStyle = "#ffffff";
                    ctx.font = "bold 28px Arial";
                    ctx.textAlign = "right";
                    ctx.textBaseline = "middle";

                    let text = names[i];
                    const maxWidth = radius * 0.62;
                    while (ctx.measureText(text).width > maxWidth && text.length > 8) {{
                        text = text.slice(0, -1);
                    }}

                    ctx.fillText(text, radius - 25, 0);
                    ctx.restore();
                }}

                // viền ngoài
                ctx.beginPath();
                ctx.arc(center, center, radius, 0, Math.PI * 2);
                ctx.lineWidth = 8;
                ctx.strokeStyle = "#d4a017";
                ctx.stroke();
            }}

            function easeOutCubic(t) {{
                return 1 - Math.pow(1 - t, 3);
            }}

            function getWinnerIndex(finalRotation) {{
                const normalized = (Math.PI * 2 - (finalRotation % (Math.PI * 2))) % (Math.PI * 2);
                return Math.floor(normalized / sliceAngle) % names.length;
            }}

            function spin() {{
                if (isSpinning) return;

                isSpinning = true;
                spinBtn.disabled = true;
                resultEl.innerHTML = "🎡 Đang quay...";

                const extraSpins = 5 + Math.random() * 4;
                const randomOffset = Math.random() * Math.PI * 2;
                const startRotation = currentRotation;
                const finalRotation = currentRotation + extraSpins * Math.PI * 2 + randomOffset;

                const duration = 5000;
                const startTime = performance.now();

                function animate(now) {{
                    const elapsed = now - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = easeOutCubic(progress);

                    currentRotation = startRotation + (finalRotation - startRotation) * eased;
                    drawWheel(currentRotation);

                    if (progress < 1) {{
                        requestAnimationFrame(animate);
                    }} else {{
                        const winnerIndex = getWinnerIndex(currentRotation);
                        const winner = names[winnerIndex];
                        resultEl.innerHTML = "🎉 Người thắng: " + winner;
                        isSpinning = false;
                        spinBtn.disabled = false;
                    }}
                }}

                requestAnimationFrame(animate);
            }}

            spinBtn.addEventListener("click", spin);

            drawWheel(currentRotation);
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=700, scrolling=False)
