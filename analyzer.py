import pandas as pd


def analyze_pitcher(data, pitcher_name):
    """
    Analyze one pitcher from a TrackMan dataset.

    Returns a dictionary containing:
    - Overall pitcher metrics
    - Pitch-by-pitch-type metrics
    - Pitch location information
    """

    # --------------------------------------------------
    # GET PITCHER DATA
    # --------------------------------------------------

    pitcher_data = data[
        data["Pitcher"] == pitcher_name
    ].copy()

    total_pitches = len(pitcher_data)

    # --------------------------------------------------
    # PITCH OUTCOME DEFINITIONS
    # --------------------------------------------------

    called_strikes = pitcher_data["PitchCall"].eq(
        "StrikeCalled"
    )

    swinging_strikes = pitcher_data["PitchCall"].eq(
        "StrikeSwinging"
    )

    fouls = pitcher_data["PitchCall"].eq(
        "FoulBallNotFieldable"
    )

    in_play = pitcher_data["PitchCall"].eq(
        "InPlay"
    )

    # A swing occurs when the hitter:
    # - Swings and misses
    # - Fouls the ball
    # - Puts the ball in play

    swings = (
        swinging_strikes
        | fouls
        | in_play
    )

    whiffs = swinging_strikes

    # --------------------------------------------------
    # STRIKE %
    # --------------------------------------------------

    strikes = (
        called_strikes
        | swinging_strikes
        | fouls
        | in_play
    ).sum()

    if total_pitches > 0:
        strike_pct = (
            strikes / total_pitches
        ) * 100
    else:
        strike_pct = 0

    # --------------------------------------------------
    # WHIFF %
    # --------------------------------------------------

    total_swings = swings.sum()
    total_whiffs = whiffs.sum()

    if total_swings > 0:
        whiff_pct = (
            total_whiffs / total_swings
        ) * 100
    else:
        whiff_pct = 0

    # --------------------------------------------------
    # CSW %
    # --------------------------------------------------

    csw = (
        called_strikes
        | swinging_strikes
    ).sum()

    if total_pitches > 0:
        csw_pct = (
            csw / total_pitches
        ) * 100
    else:
        csw_pct = 0

    # --------------------------------------------------
    # STRIKE ZONE
    # --------------------------------------------------

    zone_left = -0.83
    zone_right = 0.83
    zone_bottom = 1.5
    zone_top = 3.5

    pitcher_data["InZone"] = (
        pitcher_data["PlateLocSide"].between(
            zone_left,
            zone_right
        )
        &
        pitcher_data["PlateLocHeight"].between(
            zone_bottom,
            zone_top
        )
    )

    # --------------------------------------------------
    # CHASE %
    # --------------------------------------------------

    pitcher_data["Swing"] = swings

    pitcher_data["OutsideZone"] = (
        ~pitcher_data["InZone"]
    )

    outside_zone = pitcher_data[
        pitcher_data["OutsideZone"]
    ]

    chase_swings = outside_zone[
        outside_zone["Swing"]
    ]

    outside_zone_count = len(outside_zone)
    chase_count = len(chase_swings)

    if outside_zone_count > 0:
        chase_pct = (
            chase_count / outside_zone_count
        ) * 100
    else:
        chase_pct = 0

    # --------------------------------------------------
    # PITCH TYPE METRICS
    # --------------------------------------------------

    pitch_metrics = {}

    pitch_types = (
        pitcher_data["TaggedPitchType"]
        .dropna()
        .unique()
    )

    for pitch_type in pitch_types:

        pitch_data = pitcher_data[
            pitcher_data["TaggedPitchType"]
            == pitch_type
        ]

        pitch_count = len(pitch_data)

        # ------------------------------
        # Usage
        # ------------------------------

        usage = (
            pitch_count / total_pitches
        ) * 100

        # ------------------------------
        # Pitch outcomes
        # ------------------------------

        pitch_called_strikes = (
            pitch_data["PitchCall"]
            .eq("StrikeCalled")
        )

        pitch_swinging_strikes = (
            pitch_data["PitchCall"]
            .eq("StrikeSwinging")
        )

        pitch_fouls = (
            pitch_data["PitchCall"]
            .eq("FoulBallNotFieldable")
        )

        pitch_in_play = (
            pitch_data["PitchCall"]
            .eq("InPlay")
        )

        # ------------------------------
        # Strike %
        # ------------------------------

        pitch_strikes = (
            pitch_called_strikes
            | pitch_swinging_strikes
            | pitch_fouls
            | pitch_in_play
        ).sum()

        if pitch_count > 0:
            pitch_strike_pct = (
                pitch_strikes / pitch_count
            ) * 100
        else:
            pitch_strike_pct = 0

        # ------------------------------
        # Whiff %
        # ------------------------------

        pitch_swings = (
            pitch_swinging_strikes
            | pitch_fouls
            | pitch_in_play
        ).sum()

        pitch_whiffs = (
            pitch_swinging_strikes
        ).sum()

        if pitch_swings > 0:
            pitch_whiff_pct = (
                pitch_whiffs / pitch_swings
            ) * 100
        else:
            pitch_whiff_pct = 0

        # ------------------------------
        # CSW %
        # ------------------------------

        pitch_csw = (
            pitch_called_strikes
            | pitch_swinging_strikes
        ).sum()

        if pitch_count > 0:
            pitch_csw_pct = (
                pitch_csw / pitch_count
            ) * 100
        else:
            pitch_csw_pct = 0

        # ------------------------------
        # Chase %
        # ------------------------------

        pitch_outside_zone = pitch_data[
            pitch_data["OutsideZone"]
        ]

        pitch_chase_swings = pitch_outside_zone[
            pitch_outside_zone["Swing"]
        ]

        outside_count = len(
            pitch_outside_zone
        )

        chase_count = len(
            pitch_chase_swings
        )

        if outside_count > 0:
            pitch_chase_pct = (
                chase_count / outside_count
            ) * 100
        else:
            pitch_chase_pct = 0

        # ------------------------------
        # Physical pitch metrics
        # ------------------------------

        avg_velocity = (
            pitch_data["RelSpeed"].mean()
        )

        max_velocity = (
            pitch_data["RelSpeed"].max()
        )

        avg_spin = (
            pitch_data["SpinRate"].mean()
        )

        avg_ivb = (
            pitch_data["InducedVertBreak"].mean()
        )

        avg_hb = (
            pitch_data["HorzBreak"].mean()
        )

        avg_extension = (
            pitch_data["Extension"].mean()
        )

        avg_release_height = (
            pitch_data["RelHeight"].mean()
        )

        avg_vaa = (
            pitch_data["VertApprAngle"].mean()
        )

        # ------------------------------
        # Store pitch information
        # ------------------------------

        pitch_metrics[pitch_type] = {

            "count": pitch_count,

            "usage_pct": usage,

            "strike_pct": pitch_strike_pct,

            "whiff_pct": pitch_whiff_pct,

            "csw_pct": pitch_csw_pct,

            "chase_pct": pitch_chase_pct,

            "avg_velocity": avg_velocity,

            "max_velocity": max_velocity,

            "avg_spin": avg_spin,

            "avg_ivb": avg_ivb,

            "avg_hb": avg_hb,

            "avg_extension": avg_extension,

            "avg_release_height": avg_release_height,

            "avg_vaa": avg_vaa
        }

    # --------------------------------------------------
    # FINAL REPORT DATA
    # --------------------------------------------------

    report = {

        "pitcher": pitcher_name,

        "total_pitches": total_pitches,

        "overall": {

            "strike_pct": strike_pct,

            "whiff_pct": whiff_pct,

            "csw_pct": csw_pct,

            "chase_pct": chase_pct
        },

        "pitch_metrics": pitch_metrics,

        "location_data": pitcher_data
    }

    return report