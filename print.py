import streamlit as st
import qrcode
from io import BytesIO
import base64
from database import get_all_attendees  # Make sure this exists and is working

# Streamlit page setup
st.set_page_config(layout="wide")
st.title("🪪 Printable Conference Badges")

# Layout setting
BADGES_PER_ROW = 3

# Function to generate QR code and return as base64 string
def generate_qr_code_base64(data):
    qr = qrcode.QRCode(box_size=2, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Fetch attendee data
attendees = get_all_attendees()

# Create columns for badge layout
cols = st.columns(BADGES_PER_ROW)

for idx, attendee in enumerate(attendees):
    col = cols[idx % BADGES_PER_ROW]
    with col:
        qr_data = str(attendee["badge_id"])  # Or whatever unique value you want encoded
        qr_img_src = generate_qr_code_base64(qr_data)

        badge_html = f"""
        <div style="
            width: 2.3in;
            height: 3.4in;
            border: 1px solid black;
            padding: 10px;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 10px;
        ">
            <div>
                <h2 style='margin: 0; font-size: 20px'>{attendee['name']}</h2>
                <p style='margin: 4px 0; font-size: 12px'>{attendee['email']}</p>
                <p style='margin: 4px 0; font-size: 12px'>Badge #: {attendee['badge_id']}</p>
            </div>
            <div style="text-align: center;">
                <img src="{qr_img_src}" width="80" height="80" />
            </div>
        </div>
        """

        st.markdown(badge_html, unsafe_allow_html=True)

# Print instructions
st.markdown("⬇️ **Copy and paste into Word/Docs to print.** Each badge is sized 2.3×3.4 inches for vertical holders.")
