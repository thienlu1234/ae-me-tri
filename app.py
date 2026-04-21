import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Vòng quay chọn người thắng", page_icon="🍻", layout="wide")

st.title("🍻🍻🍻 Vòng quay của anh em Mễ Trì")

default_names = "An\nBình\nChi\nDũng\nHà\nLan\nNhung"
names_input = st.text_area(
    "Nhập danh sách (mỗi người 1 dòng)",
    value=default_names,
    height=180
)

names = [n.strip() for n in names_input.split("\n") if n.strip()]

if "Nhung" not in names:
    st.error("❌ Không có Nhung nên không chơi")
elif len(names) < 2:
    st.warning("Hãy nhập ít nhất 2 người để quay.")
else:
    names_js = str(names)

    html_code = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
    <meta charset="UTF-8">
    <style>
    body {{
        margin: 0;
        background: white;
        font-family: Arial, sans-serif;
    }}

    .wrap {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    /* 🔥 FIX MOBILE */
    .wheel-area {{
        position: relative;
        width: 90vw;        /* co theo màn hình */
        max-width: 520px;   /* giữ đẹp trên desktop */
        aspect-ratio: 1/1;  /* luôn là hình tròn */
    }}

    .pointer {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 0;
        border-left: 20px solid transparent;
        border-right: 20px solid transparent;
        border-top: 40px solid red;
        z-index: 10;
    }}

    canvas {{
        width: 100%;   /* 🔥 responsive */
        height: 100%;
        border-radius: 50%;
    }}

    .center-btn {{
        position: absolute;
        width: 20%;   /* 🔥 tự co theo màn hình */
        height: 20%;
        background: radial-gradient(circle, #ffd95a, #f4b400);
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        cursor: pointer;
        z-index: 20;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }}

    .center-btn:active {{
        transform: translate(-50%, -50%) scale(0.95);
    }}

    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.6);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 100;
    }}

    .winner-box {{
        background: white;
        padding: 40px;
        border-radius: 20px;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }}
    </style>
    </head>
    <body>

    <div class="wrap">
        <div class="wheel-area">
            <div class="pointer"></div>
            <canvas id="wheel"></canvas>  <!-- 🔥 bỏ width/height -->
            <div class="center-btn" id="spinBtn"></div>
        </div>
    </div>

    <div class="overlay" id="overlay">
        <div class="winner-box" id="winnerText"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

    <script>
    const names = {names_js};
    const canvas = document.getElementById("wheel");
    const ctx = canvas.getContext("2d");

    /* 🔥 FIX RESIZE */
    function resizeCanvas() {{
        const size = canvas.parentElement.clientWidth;
        canvas.width = size;
        canvas.height = size;
    }}

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    const spinBtn = document.getElementById("spinBtn");
    const overlay = document.getElementById("overlay");
    const winnerText = document.getElementById("winnerText");

    let size = canvas.width;
    let center = size / 2;
    let radius = center - 10;
    let arc = (Math.PI * 2) / names.length;
    const twoPi = Math.PI * 2;

    const colors = [
        "#ff4d6d", "#3a86ff", "#8338ec", "#ffbe0b",
        "#2ec4b6", "#8ac926", "#f72585", "#4cc9f0",
        "#7209b7", "#f77f00", "#4361ee", "#43aa8b"
    ];

    let rotation = 0;
    let spinning = false;

    function draw() {{
        size = canvas.width;
        center = size / 2;
        radius = center - 10;
        arc = (Math.PI * 2) / names.length;

        ctx.clearRect(0, 0, size, size);

        for (let i = 0; i < names.length; i++) {{
            const startAngle = rotation + i * arc - Math.PI / 2;
            const endAngle = startAngle + arc;

            ctx.beginPath();
            ctx.moveTo(center, center);
            ctx.arc(center, center, radius, startAngle, endAngle);
            ctx.closePath();
            ctx.fillStyle = colors[i % colors.length];
            ctx.fill();

            ctx.save();
            ctx.translate(center, center);
            ctx.rotate(startAngle + arc / 2);
            ctx.fillStyle = "white";
            ctx.font = Math.max(14, size / 25) + "px Arial";  /* 🔥 chữ auto */
            ctx.textAlign = "right";
            ctx.textBaseline = "middle";
            ctx.fillText(names[i], radius - 20, 0);
            ctx.restore();
        }}
    }}

    function easeOutCubic(t) {{
        return 1 - Math.pow(1 - t, 3);
    }}

    function spin() {{
        if (spinning) return;
        spinning = true;

        const targetIndex = names.indexOf("Nhung");

        const targetRotationBase = -(targetIndex * arc + arc / 2);

        const extraSpins = 5 + Math.random() * 5;
        const minRotation = rotation + extraSpins * twoPi;

        let finalRotation = targetRotationBase;
        while (finalRotation < minRotation) {{
            finalRotation += twoPi;
        }}

        const startRotation = rotation;
        const duration = 4000;
        let startTime = null;

        function anim(timestamp) {{
            if (!startTime) startTime = timestamp;

            let progress = (timestamp - startTime) / duration;
            if (progress > 1) progress = 1;

            const eased = easeOutCubic(progress);
            rotation = startRotation + (finalRotation - startRotation) * eased;

            draw();

            if (progress < 1) {{
                requestAnimationFrame(anim);
            }} else {{
                rotation = finalRotation;
                draw();
                spinning = false;

                for (let i = 0; i < 5; i++) {{
                    confetti({{
                        particleCount: 100,
                        spread: 70,
                        origin: {{ y: 0.6 }}
                    }});
                }}

                winnerText.innerHTML = "🎉 Nhung";
                overlay.style.display = "flex";
            }}
        }}

        requestAnimationFrame(anim);
    }}

    spinBtn.onclick = spin;
    overlay.onclick = () => overlay.style.display = "none";

    draw();
    </script>

    </body>
    </html>
    """

    components.html(html_code, height=700, scrolling=False)
