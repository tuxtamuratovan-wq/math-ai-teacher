import streamlit as st
from openai import OpenAI
import base64

st.set_page_config(
    page_title="Math AI Teacher",
    page_icon="📐",
    layout="centered"
)

st.title("📐 Math AI Teacher")
st.write("Algebra va geometriya misolingizni rasmga olib yuklang.")

# API key
api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="API kalitingizni shu yerga kiriting."
)

if not api_key:
    st.info("Avval OpenAI API kalitingizni kiriting.")
    st.stop()

client = OpenAI(api_key=api_key)

# Rasm yuklash
uploaded_file = st.file_uploader(
    "📷 Misol rasmini yuklang",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Siz yuborgan misol",
        use_container_width=True
    )

    level = st.selectbox(
        "Tushuntirish darajasi:",
        [
            "Juda sodda",
            "Oddiy",
            "Imtihon darajasida",
            "Batafsil"
        ]
    )

    if st.button("🧠 Misolni tushuntir", type="primary"):

        with st.spinner("Misolni tahlil qilyapman..."):

            image_bytes = uploaded_file.read()

            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            mime_type = uploaded_file.type

            prompt = f"""
Sen professional matematika o'qituvchisisan.

Rasmda algebra yoki geometriya masalasi bor.

O'quvchiga masalani O'ZBEK TILIDA tushuntir.

Tushuntirish darajasi: {level}

Qoidalar:

1. Avval masalada nima berilganini ayt.
2. Nimani topish kerakligini ayt.
3. Kerakli formula yoki teoremani tushuntir.
4. Masalani bosqichma-bosqich yech.
5. Har bir qadam NIMA UCHUN bajarilganini tushuntir.
6. Yakuniy javobni alohida ko'rsat.
7. Agar geometriya bo'lsa, chizmaga qarab
   nuqtalar, burchaklar va tomonlarni aniq ajrat.
8. Agar rasm noaniq bo'lsa, taxmin qilma.
   Qaysi qism noaniq ekanini ayt.
9. Faqat javobni berib qo'yma — o'rgat.

Oxirida:
"💡 Eslab qol:" degan bo'lim yaratib,
shu turdagi masalani yechishning asosiy usulini
qisqa qilib yoz.
"""

            response = client.responses.create(
                model="gpt-5.6-luna",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": prompt
                            },
                            {
                                "type": "input_image",
                                "image_url": (
                                    f"data:{mime_type};base64,"
                                    f"{image_base64}"
                                )
                            }
                        ]
                    }
                ]
            )

            answer = response.output_text

        st.divider()
        st.subheader("👩‍🏫 Tushuntirish")
        st.markdown(answer)

        st.success("✅ Misol tushuntirildi!")
