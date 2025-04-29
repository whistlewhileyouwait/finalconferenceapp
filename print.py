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
