def create_badge_pdf(attendees):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    x_margin = 0.5 * inch
    y_margin = 0.5 * inch
    x_spacing = (width - 2 * x_margin - BADGES_PER_ROW * BADGE_WIDTH_INCH * inch) / (BADGES_PER_ROW - 1)
    y_spacing = 0.3 * inch

    x_positions = [x_margin + i * (BADGE_WIDTH_INCH * inch + x_spacing) for i in range(BADGES_PER_ROW)]
    y_position = height - y_margin - BADGE_HEIGHT_INCH * inch

    badge_idx = 0

    for attendee in attendees:
        col = badge_idx % BADGES_PER_ROW
        if badge_idx > 0 and col == 0:
            y_position -= BADGE_HEIGHT_INCH * inch + y_spacing
            if y_position < 0:
                c.showPage()
                y_position = height - y_margin - BADGE_HEIGHT_INCH * inch

        # FRONT SIDE
        # Draw border
        c.rect(x_positions[col], y_position, BADGE_WIDTH_INCH * inch, BADGE_HEIGHT_INCH * inch)

        # Draw text
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_positions[col] + 0.1*inch, y_position + BADGE_HEIGHT_INCH*inch - 0.4*inch, attendee['name'])

        c.setFont("Helvetica", 9)
        c.drawString(x_positions[col] + 0.1*inch, y_position + BADGE_HEIGHT_INCH*inch - 0.7*inch, attendee['email'])
        c.drawString(x_positions[col] + 0.1*inch, y_position + BADGE_HEIGHT_INCH*inch - 0.9*inch, f"{attendee['badge_id']}")

        # Generate and draw QR code
        qr_img = generate_qr_code_img(str(attendee["badge_id"]))
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        qr_reader = Image.open(qr_buffer)

        qr_x = x_positions[col] + BADGE_WIDTH_INCH*inch/2 - 0.4*inch
        qr_y = y_position + 0.2*inch
        c.drawInlineImage(qr_reader, qr_x, qr_y, width=0.8*inch, height=0.8*inch)

        c.showPage()  # ⚡ NEW: After each front, force a new page for the back!

        # BACK SIDE
        # Create the back side of the badge
        c.rect(x_margin, height - y_margin - BADGE_HEIGHT_INCH * inch, BADGE_WIDTH_INCH * inch, BADGE_HEIGHT_INCH * inch)

        c.setFont("Helvetica", 10)
        notes = [
            "FOR CE CREDITS:",
            "Scan in when you arrive each day",
            "Scan out when you leave for the day",
            "Make sure all info on badge is correct",
        ]
        text_y = height - y_margin - 0.7 * inch
        for line in notes:
            c.drawString(x_margin + 0.2*inch, text_y, line)
            text_y -= 0.3*inch

        c.showPage()  # ⚡ NEW: After each back, move to the next front

        badge_idx += 1

    c.save()
    buffer.seek(0)
    return buffer
