import streamlit as st
import random
import time

st.title("🎡 Vòng quay chọn người thắng")

# Nhập danh sách
names_input = st.text_area(
    "Nhập danh sách (mỗi người 1 dòng)",
    "An\nBình\nChi\nDũng\nHà\nLan"
)

names = [n.strip() for n in names_input.split("\n") if n.strip()]

if len(names) == 0:
    st.warning("Vui lòng nhập danh sách!")
else:
    if st.button("🎯 Quay!"):
        placeholder = st.empty()

        # hiệu ứng quay
        for i in range(20):
            temp = random.choice(names)
            placeholder.markdown(f"## 🔄 {temp}")
            time.sleep(0.1)

        winner = random.choice(names)
        placeholder.markdown(f"## 🎉 Người thắng: **{winner}**")

        st.balloons()
