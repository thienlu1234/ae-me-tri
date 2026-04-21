function spin() {{
    if (spinning) return;
    spinning = true;

    const targetIndex = names.indexOf("Nhung");

    const extraSpins = 5 + Math.random() * 5;
    const sliceAngle = (2 * Math.PI) / names.length;

    // 🔥 Công thức chuẩn 100% (không lệch)
    const finalRotation =
        extraSpins * Math.PI * 2 +
        (Math.PI / 2) - (targetIndex * sliceAngle + sliceAngle / 2);

    const startRotation = rotation;
    const duration = 4000;
    let start = null;

    function anim(t) {{
        if (!start) start = t;
        let progress = (t - start) / duration;
        if (progress > 1) progress = 1;

        const eased = easeOut(progress);

        rotation = startRotation + (finalRotation - startRotation) * eased;

        draw();

        if (progress < 1) {{
            requestAnimationFrame(anim);
        }} else {{
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
