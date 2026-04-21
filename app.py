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
    <meta charset="UTF-8">
    <style>
    body {{
        margin: 0;
        background: white;
        font-family: Arial;
    }}

    .wrap {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    .wheel-area {{
        position: relative;
        width: 520px;
        height: 520px;
    }}

    /* ✅ FIX KIM */
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
        border-radius: 50%;
    }}

    .center-btn {{
        position: absolute;
        width: 100px;
        height: 100px;
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
    }}
    </style>
    </head>
    <body>

    <div class="wrap">
        <div class="wheel-area">
            <div class="pointer"></div>
            <canvas id="wheel" width="500" height="500"></canvas>
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
    const spinBtn = document.getElementById("spinBtn");
    const overlay = document.getElementById("overlay");
    const winnerText = document.getElementById("winnerText");

    const size = canvas.width;
    const center = size / 2;
    const radius = center - 10;
    const arc = (Math.PI * 2) / names.length;

    const colors = ["#ff4d6d","#3a86ff","#8338ec","#ffbe0b","#2ec4b6","#8ac926"];

    let rotation = 0;
    let spinning = false;

    function draw() {{
        ctx.clearRect(0,0,size,size);

        for(let i=0;i<names.length;i++) {{
            const angle = rotation + i*arc - Math.PI/2;

            ctx.beginPath();
            ctx.moveTo(center,center);
            ctx.arc(center,center,radius,angle,angle+arc);
            ctx.fillStyle = colors[i%colors.length];
            ctx.fill();

            ctx.save();
            ctx.translate(center,center);
            ctx.rotate(angle+arc/2);
            ctx.fillStyle="white";
            ctx.font="bold 20px Arial";
            ctx.textAlign="right";
            ctx.fillText(names[i], radius-20,0);
            ctx.restore();
        }}
    }}

    function easeOut(t) {{
        return 1 - Math.pow(1-t,3);
    }}

    function getWinner() {{
        const deg = (2*Math.PI - rotation%(2*Math.PI));
        return Math.floor(deg/arc)%names.length;
    }}

    function spin() {{
        if(spinning) return;
        spinning = true;

        const extraSpins = 5 + Math.random() * 5;
        const randomOffset = Math.random() * Math.PI * 2;

        const startRotation = rotation;
        const finalRotation = rotation + extraSpins * Math.PI * 2 + randomOffset;

        const duration = 4000;
        let start = null;

        function anim(t) {{
            if(!start) start = t;
            let progress = (t - start) / duration;
            if(progress > 1) progress = 1;

            let eased = easeOut(progress);

            rotation = startRotation + (finalRotation - startRotation) * eased;

            draw();

            if(progress < 1) {{
                requestAnimationFrame(anim);
            }} else {{
                spinning = false;

                let winner = names[getWinner()];

                // 🎆 pháo hoa
                for(let i=0;i<5;i++) {{
                    confetti({{
                        particleCount: 100,
                        spread: 70,
                        origin: {{y:0.6}}
                    }});
                }}

                winnerText.innerHTML = "🎉 " + winner;
                overlay.style.display = "flex";
            }}
        }}

        requestAnimationFrame(anim);
    }}

    spinBtn.onclick = spin;

    overlay.onclick = () => overlay.style.display="none";

    draw();
    </script>

    </body>
    </html>
    """

    components.html(html_code, height=700, scrolling=False)
