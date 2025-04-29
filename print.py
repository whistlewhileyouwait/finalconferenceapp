import streamlit as st
import qrcode
from io import BytesIO
import base64
from database import get_all_attendees

st.set_page_config(layout="wide")
st.title("🪪 Printable Conference Badges")

BADGES_PER_ROW = 3

def generate_qr_code_base64(data):
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

attendees = get_all_attendees()
cols = st.columns(BADGES_PER_ROW)

for idx, attendee in enumerate(attendees):
    col = cols[idx % BADGES_PER_ROW]
    with col:
        qr_data = str(attendee["badge_id"])  # Make sure badge_id exists in your table
        qr_img_src = generate_qr_code_base64(qr_data)

        badge_html = f"""
        <div style="
            width: 2.3in;
            height
