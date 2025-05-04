def generate_ce_report():
    # 1) Load your data
    attendees = get_all_attendees()   # list of dicts { "badge_id", "name", "email", … }
    raw_logs  = get_scan_log()        # list of dicts { "badge_id", "name", "email", "timestamp" (datetime) }

    # 2) Group all scan timestamps by badge_id
    scans_by = {}
    for entry in raw_logs:
        bid = entry["badge_id"]
        scans_by.setdefault(bid, []).append(entry["timestamp"])

    # 3) Pre‑parse your session start/end into datetimes
    parsed_sessions = []
    for s in conference_sessions:
        start = datetime.datetime.strptime(s["start"], "%Y-%m-%d %H:%M")
        end   = datetime.datetime.strptime(s["end"],   "%Y-%m-%d %H:%M")
        parsed_sessions.append((s["title"], start, end))

    # 4) Build one row per attendee
    rows = []
    for a in attendees:
        bid  = int(a["badge_id"])
        row  = {
            "Badge ID": bid,
            "Name":      a["name"],
            "Email":     a["email"]
        }
        times = scans_by.get(bid, [])
        # for each session, put a ✅ if any scan falls inside its window
        for title, start, end in parsed_sessions:
            row[title] = "✅" if any(start <= ts <= end for ts in times) else ""
        rows.append(row)

    # 5) Return as a DataFrame (sorted by badge)
    df = pd.DataFrame(rows)
    return df.sort_values("Badge ID").reset_index(drop=True)
