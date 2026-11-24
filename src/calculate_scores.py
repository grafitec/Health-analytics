import pandas as pd

def steps(df, points_data, period_start, period_end, today=None):
    # Hämta aktivitetens inställningar
    steps_row = points_data[points_data["activity"] == "steps"]

    steps_goal = steps_row["goal"].iloc[0]
    step_points = steps_row["point_at_100"].iloc[0]

    # Dagens datum
    if today is None:
        today = pd.Timestamp.today().normalize()
    else:
        today = pd.Timestamp(today).normalize()

    # Datum för perioden
    start = pd.Timestamp(period_start).normalize()
    end = pd.Timestamp(period_end).normalize()

    # Räkna endast dagar som har passerat
    end = min(end, today - pd.Timedelta(days=1))

    if end < start:
        return 0, 0, []

    # Skapa en lista med alla dagar i perioden
    expected_dates = pd.date_range(start, end, freq="D")

    # Förbered data
    data = pd.DataFrame({
        "date": pd.to_datetime(df["date"], errors="coerce").dt.normalize(),
        "steps": pd.to_numeric(df["steps"], errors="coerce")
    })

    data = data.dropna(subset=["date", "steps"])

    # Samla steg per dag
    daily_steps = data.groupby("date")["steps"].max()

    # Hitta dagar som saknar rapportering
    missing_dates = expected_dates.difference(daily_steps.index)

    # Dagar utan rapportering räknas som 0 steg
    daily_steps = daily_steps.reindex(expected_dates, fill_value=0)

    # Beräkna resultat
    step_total = daily_steps.sum()
    step_goal_total = len(expected_dates) * steps_goal

    step_procent = round((step_total / step_goal_total) * 100, 1)

    step_total_points = round((step_points * step_procent) / 100, 1)

    # Gör datumen lite snyggare
    missing_dates = [
        date.strftime("%Y-%m-%d")
        for date in missing_dates
    ]

    print(missing_dates)

    return step_total_points, step_procent, missing_dates