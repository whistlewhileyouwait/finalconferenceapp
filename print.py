import streamlit as st
import qrcode
from io import BytesIO
from database import get_all_attendees
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

st.set_page_config(layout="wide")
st.title("🪪 Printable Conference Badges (Multi-page PDF)")

BADGES_PER_ROW = 3
BADGE_WIDTH_INCH = 2.3
BADGE_HEIGHT_INCH = 3.4
PAGE_WIDTH, PAGE_HEIGHT = letter

def generate_qr_code_img(data):
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def create_badge_pdf(attendees):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    x_margin = 0.5 * inch
    y_margin = 0.5 * inch
    x_spacing = (PAGE_WIDTH - 2 * x_margin - BADGES_PER_ROW * BADGE_WIDTH_INCH * inch) / (BADGES_PER_ROW - 1)
    y_spacing = 0.3 * inch

    # Precompute column positions
    x_positions = [x_margin + i * (BADGE_WIDTH_INCH * inch + x_spacing) for i in range(BADGES_PER_ROW)]

    # Start layout
    row_height = BADGE_HEIGHT_INCH * inch + y_spacing
    rows_per_page = int((PAGE_HEIGHT - 2 * y_margin + y_spacing) // row_height)
    badges_per_page = BADGES_PER_ROW * rows_per_page

    for idx, attendee in enumerate(attendees):
        badge_idx_on_page = idx % badges_per_page
        col = badge_idx_on_page % BADGES_PER_ROW
        row = badge_idx_on_page // BADGES_PER_ROW

        # If first badge on a new page
        if badge_idx_on_page == 0 and idx != 0:
            c.showPage()

        x = x_positions[col]
        y = PAGE_HEIGHT - y_margin - (row + 1) * row_height + y_spacing

        # Draw badge border
        c.rect(x, y, BADGE_WIDTH_INCH * inch, BADGE_HEIGHT_INCH * inch)

        # Text
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 0.1 * inch, y + BADGE_HEIGHT_INCH * inch - 0.4 * inch, attendee['name'])

        c.setFont("Helvetica", 10)
        c.drawString(x + 0.1 * inch, y + BADGE_HEIGHT_INCH * inch - 0.7 * inch, attendee['email'])
        c.drawString(x + 0.1 * inch, y + BADGE_HEIGHT_INCH * inch - 0.9 * inch, f"Badge #: {attendee['badge_id']}")

        # QR code
        qr_img = generate_qr_code_img(str(attendee['badge_id']))
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        img = Image.open(qr_buffer)

        qr_x = x + BADGE_WIDTH_INCH * inch / 2 - 0.4 * inch
        qr_y = y + 0.2 * inch
        c.drawInlineImage(img, qr_x, qr_y, width=0.8 * inch, height=0.8 * inch)

    c.save()
    buffer.seek(0)
    return buffer

# Fetch attendees
attendees = get_all_attendees()

if st.button("Generate PDF of Badges"):
    pdf_buffer = create_badge_pdf(attendees)
    st.download_button(
        label="📄 Download Conference Badges PDF",
        data=pdf_buffer,
        file_name="conference_badges.pdf",
        mime="application/pdf"
    )

