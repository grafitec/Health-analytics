import pandas as pd


def process_data(df):
    """Clean and prepare raw Google Sheets data."""

    df = df.copy()

    # Remove accidental whitespace from column names
    df.columns = df.columns.str.strip()

    # Rename columns to short, readable names
    column_mapping = {
        "Tidstämpel": "timestamp",
        "Datum": "date",
        "Har jag tagit vitamintabletter idag?": "vitamin",
        "Har jag druckit tillräckligt mycket vatten idag?  En frisk vuxen person behöver dricka ungefär 1,5 till 2 liter vatten per dag": "water",
        "Har jag styrketränat idag? Svara i timmar": "workout_hr",
        "Jag har spelat paddel, hur länge körde jag? Svara i timmar": "paddel_hr",
        "Har jag promenerat något idag? Svara i antal km": "walk_km ",
        "Har jag promenerat något idag? Svara i antal timmar": "walk_hr ",
        "Har pokemon varit delaktigt i någon form under aktiviteten": "pokemon",
        "Om jag tänker efter och svarar ärligt, har jag ätit bra idag?": "food",
        "Hur mycket har jag sovit, ange i timmar. Den rekommenderade sömnmängden för 60-åringar är 7 till 9 timmar per natt": "sleep_hr",
        "Har jag sovit dag eller natt": "sleep_day_night",
        "Idag har jag jobbat natt": "worked_night",
        "Idag är en återhämtningsdag": "recoveryday",
        "Lägsta puls under dagen": "lowest_pulse",
        "Högsta puls under dagen": "highest_pulse",
        "Genomsnittlig puls under dagen": "average_day_pulse",
        "Genomsnittlig puls under aktivitet": "average_activity_pulse",
        "Annan aktivitet att skriva ner": "other_activity",
        "Antal steg per dag. Rekommenderat är 10k per dag": "steps",
    }

    df = df.rename(columns=column_mapping)

    # Convert dates; invalid values become missing
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert timestamp if present
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            format="%Y-%m-%d %H.%M.%S",
            errors="coerce",
        )

    # Convert numeric measurements
    numeric_columns = [
        "workout_hr",
        "steps",
        "paddel_hr",
        "walk_km",
        "walk_hr",
        "sleep_hr",
        "lowest_pulse",
        "highest_pulse",
        "average_day_pulse",
        "average_activity_pulse",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # True/false
    df["recoveryday"] = df["recoveryday"].map({"Yes": True, "No": False,})
    df["worked_night"] = df["worked_night"].map({"Yes": True, "No": False,})
    df["sleep_day_night"] = df["sleep_day_night"].map({"Yes": True, "No": False,})
    df["vitamin"] = df["vitamin"].map({"Yes": True, "No": False,})
    df["pokemon"] = df["pokemon"].map({"Yes": True, "No": False,})

    return df