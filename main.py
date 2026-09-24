import pandas as pd
from pathlib import Path
from datetime import datetime

# --------------------------------------------------
# LOAD TRACKMAN DATA
# --------------------------------------------------

data_folder = Path("data")

csv_files = sorted(data_folder.glob("*.csv"))

print("TRACKMAN POST-GAME ANALYZER")
print("===========================")
print()

print("Available TrackMan files:")
print()

for i, file in enumerate(csv_files, start=1):
    print(f"{i}. {file.name}")

print()
print("N. Analyze newest game")
print("Q. Quit")
print()

choice = input("Select a game or option: ").strip()

if choice.upper() == "Q":
    print("Exiting program.")
    exit()

elif choice.upper() == "N":
    csv_file = csv_files[-1]

else:
    choice = int(choice)
    csv_file = csv_files[choice - 1]

print()
print(f"Loading: {csv_file.name}")
print()

data = pd.read_csv(csv_file)

pitcher_team = data["PitcherTeam"].iloc[0]
home_team = data["HomeTeam"].iloc[0]
away_team = data["AwayTeam"].iloc[0]

if pitcher_team == home_team:
    opponent = away_team
else:
    opponent = home_team

game_date_obj = datetime.strptime(
    str(data["Date"].iloc[0]),
    "%Y-%m-%d"
)

game_date = (
    f"{game_date_obj.strftime('%B')} "
    f"{game_date_obj.day}, "
    f"{game_date_obj.year}"
)

# ----------------------
# TEAM NAME DICTIONARY
# ----------------------

team_names = {

    # ------------------------------
    # ACC
    # ------------------------------

    "NOR_WOL": "NC State",
    "DUK_BLU": "Duke",

    # ------------------------------
    # North Carolina D1
    # ------------------------------
    "APP_MOU": "App State",



    # ------------------------------
    # Additional opponents
    # ------------------------------
    "LIB_FLA": "Liberty",




}

# Convert TrackMan team codes to display names
opponent = team_names.get(opponent, opponent)

print("TRACKMAN POST-GAME ANALYZER")
print("===========================")
print()

print(f"Total pitches: {len(data)}")
print()


# --------------------------------------------------
# PITCHER SUMMARY
# --------------------------------------------------

pitchers = data["Pitcher"].value_counts()

print("PITCHERS")
print("--------")

for pitcher, pitch_count in pitchers.items():
    print(f"{pitcher}: {pitch_count} pitches")

print()


# --------------------------------------------------
# PITCH METRICS BY PITCH TYPE
# --------------------------------------------------

print("PITCH EFFECTIVENESS")
print("-------------------")

for pitcher in pitchers.index:

    pitcher_data = data[data["Pitcher"] == pitcher]

    print()
    print("=" * 75)
    print(pitcher)
    print("=" * 75)

    pitch_types = pitcher_data["TaggedPitchType"].value_counts()

    for pitch_type, count in pitch_types.items():

        pitch_data = pitcher_data[
            pitcher_data["TaggedPitchType"] == pitch_type
        ]

        # ------------------------------
        # Usage
        # ------------------------------

        usage = (count / len(pitcher_data)) * 100

        # ------------------------------
        # Pitch outcome categories
        # ------------------------------

        called_strikes = pitch_data["PitchCall"].eq("StrikeCalled")
        swinging_strikes = pitch_data["PitchCall"].eq("StrikeSwinging")
        fouls = pitch_data["PitchCall"].eq("FoulBallNotFieldable")
        in_play = pitch_data["PitchCall"].eq("InPlay")

        # ------------------------------
        # Strike %
        # ------------------------------

        strikes = (
            called_strikes
            | swinging_strikes
            | fouls
            | in_play
        ).sum()

        strike_pct = strikes / count * 100

        # ------------------------------
        # Swings
        # ------------------------------

        swings = (
            swinging_strikes
            | fouls
            | in_play
        ).sum()

        # ------------------------------
        # Whiff %
        # ------------------------------

        whiffs = swinging_strikes.sum()

        if swings > 0:
            whiff_pct = whiffs / swings * 100
        else:
            whiff_pct = 0

        # ------------------------------
        # CSW %
        # ------------------------------

        csw = (
            called_strikes
            | swinging_strikes
        ).sum()

        csw_pct = csw / count * 100

        # ------------------------------
        # Print results
        # ------------------------------

        print()
        print(f"{pitch_type}")
        print(f"  Usage:      {usage:.1f}%")
        print(f"  Strike %:   {strike_pct:.1f}%")
        print(f"  Whiff %:    {whiff_pct:.1f}%")
        print(f"  CSW %:      {csw_pct:.1f}%")

print()
print("LOCATION COLUMNS")
print("----------------")

for column in data.columns:
    if any(word in column.lower() for word in [
        "plate",
        "px",
        "pz",
        "zone"
    ]):
        print(column)

print()
print("PLATE LOCATION SAMPLE")
print("---------------------")

print(
    data[
        ["Pitcher", "TaggedPitchType", "PitchCall",
         "PlateLocSide", "PlateLocHeight"]
    ].head(20).to_string(index=False)
)

# --------------------------------------------------
# CHASE RATE
# --------------------------------------------------

print()
print("CHASE RATE")
print("----------")

# Provisional strike zone
zone_left = -0.83
zone_right = 0.83
zone_bottom = 1.5
zone_top = 3.5

# Determine whether each pitch is inside the zone
data["InZone"] = (
    data["PlateLocSide"].between(zone_left, zone_right)
    & data["PlateLocHeight"].between(zone_bottom, zone_top)
)

# Determine whether each pitch was a swing
swing_calls = [
    "StrikeSwinging",
    "FoulBallNotFieldable",
    "InPlay"
]

data["Swing"] = data["PitchCall"].isin(swing_calls)

# Outside-zone pitches
data["OutsideZone"] = ~data["InZone"]

for pitcher in data["Pitcher"].dropna().unique():

    pitcher_data = data[
        data["Pitcher"] == pitcher
    ]

    outside_zone = pitcher_data[
        pitcher_data["OutsideZone"]
    ]

    chase_swings = outside_zone[
        outside_zone["Swing"]
    ]

    outside_count = len(outside_zone)
    chase_count = len(chase_swings)

    if outside_count > 0:
        chase_pct = chase_count / outside_count * 100
    else:
        chase_pct = 0

    print()
    print(pitcher)
    print(f"  Outside-zone pitches: {outside_count}")
    print(f"  Swings outside zone:  {chase_count}")
    print(f"  Chase %:              {chase_pct:.1f}%")

# --------------------------------------------------
# CHASE RATE BY PITCH TYPE
# --------------------------------------------------

print()
print("CHASE RATE BY PITCH TYPE")
print("------------------------")

for pitcher in data["Pitcher"].dropna().unique():

    pitcher_data = data[
        data["Pitcher"] == pitcher
    ]

    print()
    print("=" * 60)
    print(pitcher)
    print("=" * 60)

    pitch_types = pitcher_data["TaggedPitchType"].value_counts()

    for pitch_type, pitch_count in pitch_types.items():

        pitch_data = pitcher_data[
            pitcher_data["TaggedPitchType"] == pitch_type
        ]

        # Pitches outside the strike zone
        outside_zone = pitch_data[
            pitch_data["OutsideZone"]
        ]

        # Swings at pitches outside the zone
        chase_swings = outside_zone[
            outside_zone["Swing"]
        ]

        outside_count = len(outside_zone)
        chase_count = len(chase_swings)

        # Calculate chase rate
        if outside_count > 0:
            chase_pct = (
                chase_count / outside_count
            ) * 100
        else:
            chase_pct = 0

        print()
        print(pitch_type)
        print(f"  Outside-zone pitches: {outside_count}")
        print(f"  Chase swings:         {chase_count}")
        print(f"  Chase %:              {chase_pct:.1f}%")





from analyzer import analyze_pitcher
from reports import generate_report
from pdf_report import create_pitcher_pdf
from charts import (
    create_pitch_location_chart,
    create_pitch_usage_chart,
    create_pitch_movement_chart
)

# --------------------------------------------------
# GENERATE REPORT FOR EVERY PITCHER
# --------------------------------------------------

pitchers = (
    data["Pitcher"]
    .dropna()
    .unique()
)

print()
print("=" * 70)
print("TRACKMAN POST-GAME REPORT GENERATOR")
print("=" * 70)

print()
print(f"Pitchers found: {len(pitchers)}")

for pitcher in pitchers:

    # Get this pitcher's data
    pitcher_data = data[data["Pitcher"] == pitcher].copy()

    # Determine this pitcher's team
    pitcher_team = pitcher_data["PitcherTeam"].iloc[0]

    # Get the home and away teams
    home_team = pitcher_data["HomeTeam"].iloc[0]
    away_team = pitcher_data["AwayTeam"].iloc[0]

    # The opponent is the team that is not the pitcher's team
    if pitcher_team == home_team:
        opponent = away_team
    else:
        opponent = home_team

    # Convert TrackMan team codes to display names
    opponent = team_names.get(opponent, opponent)

    print()
    print("=" * 70)
    print(f"GENERATING REPORT: {pitcher}")
    print("=" * 70)

    # Analyze pitcher
    report = analyze_pitcher(
        data,
        pitcher
    )

    # Generate formatted report
    formatted_report = generate_report(
        report
    )

    # Display report
    print()
    print(formatted_report)

    # --------------------------------------------------
    # SAVE REPORT TO FILE
    # --------------------------------------------------

    game_name = csv_file.stem

    reports_folder = Path("reports") / game_name
    reports_folder.mkdir(parents=True, exist_ok=True)

    # Create a safe filename
    safe_name = (
        pitcher
        .replace(",", "")
        .replace(" ", "_")
    )

    
    # --------------------------------------------------
    # CREATE PITCH LOCATION CHART
    # --------------------------------------------------

    pitcher_data = data[
        data["Pitcher"] == pitcher
    ].copy()

    chart_file = (
        reports_folder
        / f"{safe_name}_pitch_location.png"
    )

    create_pitch_location_chart(
        pitcher_data,
        str(chart_file),
        pitcher
    )

    # --------------------------------------------------
    # CREATE PITCH MOVEMENT CHART
    # --------------------------------------------------

    movement_chart_file = (
        reports_folder
        / f"{safe_name}_pitch_movement.png"
    )

    create_pitch_movement_chart(
        pitcher_data,
        str(movement_chart_file),
        pitcher
    )

    # --------------------------------------------------
    # CREATE PITCH USAGE CHART
    # --------------------------------------------------

    pitch_counts = (
        pitcher_data["TaggedPitchType"]
        .value_counts()
    )

    pitch_metrics = {}

    for pitch_type, count in pitch_counts.items():

        usage_pct = (
            count / len(pitcher_data)
        ) * 100

        pitch_metrics[pitch_type] = {
            "usage_pct": usage_pct
        }
        pitch_usage_file = (
        reports_folder
        / f"{safe_name}_pitch_usage.png"
    )

    create_pitch_usage_chart(
        pitch_metrics,
        str(pitch_usage_file)
    )
    report_file = (
        reports_folder
        / f"{safe_name}.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(formatted_report)

    print()
    print(
        f"Report saved to: {report_file}"
    )
    # --------------------------------------------------
    # CREATE PDF REPORT
    # --------------------------------------------------

    pdf_file = (
        reports_folder
        / f"{safe_name}.pdf"
    )

    create_pitcher_pdf(
    report,
    str(pdf_file),
    str(chart_file),
    str(pitch_usage_file),
    str(movement_chart_file),
    opponent,
    game_date
)

    print()
    print(
        f"PDF created: {pdf_file}"
    )
# --------------------------------------------------
