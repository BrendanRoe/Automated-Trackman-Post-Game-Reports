import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

PITCH_COLORS = {
    "Fastball": "#D62728",    # Red
    "Sinker": "#F28E2B",      # Orange
    "Cutter": "#7A3EB1",      # Purple
    "Slider": "#F2C300",      # Yellow
    "Curveball": "#2F70B7",    # Blue
    "ChangeUp": "#2CA25F",     # Green
    "Splitter": "#006400",     # Dark Green
    "Sweeper": "#8B4513",      # Brown
}

# --------------------------------------------------
# PITCH MOVEMENT CHART
# --------------------------------------------------

def create_pitch_movement_chart(
    pitcher_data,
    output_path,
    pitcher_name
):
    """
    Create a sample-report-style pitch movement chart.
    """

    # --------------------------------------------------
    # PITCH TYPE COLORS
    # --------------------------------------------------

    pitch_colors = PITCH_COLORS

    # --------------------------------------------------
    # CREATE FIGURE
    # --------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(5.5, 6.0)
    )

    # --------------------------------------------------
    # PLOT EACH PITCH TYPE
    # --------------------------------------------------

    pitch_types = (
        pitcher_data["TaggedPitchType"]
        .dropna()
        .unique()
    )

    for pitch_type in pitch_types:

        pitch_data = pitcher_data[
            pitcher_data["TaggedPitchType"] == pitch_type
        ].copy()

        color = pitch_colors.get(
            pitch_type,
            "#555555"
        )

        # ----------------------------------------------
        # INDIVIDUAL PITCHES
        # ----------------------------------------------

        ax.scatter(
            pitch_data["HorzBreak"],
            pitch_data["InducedVertBreak"],
            s=45,
            color=color,
            alpha=0.65,
            edgecolor="white",
            linewidth=0.5,
            label=pitch_type
        )

        # ----------------------------------------------
        # PITCH-TYPE AVERAGE
        # ----------------------------------------------

        avg_hb = pitch_data["HorzBreak"].mean()
        avg_ivb = pitch_data["InducedVertBreak"].mean()

        ax.scatter(
            avg_hb,
            avg_ivb,
            s=350,
            color=color,
            edgecolor="white",
            linewidth=1.5,
            zorder=5
        )

    # --------------------------------------------------
    # ZERO LINES
    # --------------------------------------------------

    ax.axhline(
        0,
        color="#777777",
        linewidth=0.8,
        zorder=1
    )

    ax.axvline(
        0,
        color="#777777",
        linewidth=0.8,
        zorder=1
    )

    # --------------------------------------------------
    # GRID
    # --------------------------------------------------

    ax.grid(
        True,
        linestyle="-",
        linewidth=0.5,
        alpha=0.25
    )

    ax.set_axisbelow(True)

    # --------------------------------------------------
    # AXIS LABELS
    # --------------------------------------------------

    ax.set_xlabel(
        "Horizontal Break (in)",
        fontsize=9
    )

    ax.set_ylabel(
        "Induced Vertical Break (in)",
        fontsize=9
    )

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    ax.set_title(
        "PITCH MOVEMENT",
        fontsize=12,
        fontweight="bold",
        pad=12
    )

    # --------------------------------------------------
    # LEGEND
    # --------------------------------------------------

    handles, labels = ax.get_legend_handles_labels()

    if handles:

        ax.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=4,
            frameon=False,
            fontsize=8,
            handletextpad=0.4,
            columnspacing=1.0
        )

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=250,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()

def create_pitch_location_chart(
    pitcher_data,
    output_path,
    pitcher_name
):
    """
    Create a sample-report-style pitch location chart.
    """

    # --------------------------------------------------
    # PITCH TYPE COLORS
    # --------------------------------------------------

    pitch_colors = PITCH_COLORS

    # --------------------------------------------------
    # CREATE FIGURE
    # --------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(5.5, 6.0)
    )

    # --------------------------------------------------
    # PITCH TYPES
    # --------------------------------------------------

    pitch_types = (
        pitcher_data["TaggedPitchType"]
        .dropna()
        .unique()
    )

    # --------------------------------------------------
    # PITCH CALLS
    # --------------------------------------------------

    strike_calls = {
        "StrikeCalled",
        "StrikeSwinging",
        "FoulBallNotFieldable",
        "InPlay",
    }

    # --------------------------------------------------
    # PLOT EACH PITCH TYPE
    # --------------------------------------------------

    for pitch_type in pitch_types:

        pitch_data = pitcher_data[
            pitcher_data["TaggedPitchType"] == pitch_type
        ].copy()

        color = pitch_colors.get(
            pitch_type,
            "#555555"
        )

        # ----------------------------------------------
        # FILLED PITCHES
        # ----------------------------------------------

        filled = pitch_data[
            pitch_data["PitchCall"].isin(
                strike_calls
            )
        ]

        if not filled.empty:

            ax.scatter(
                filled["PlateLocSide"],
                filled["PlateLocHeight"],
                s=55,
                color=color,
                edgecolor=color,
                alpha=0.9,
                linewidth=0.8,
                label=pitch_type
            )

        # ----------------------------------------------
        # OPEN PITCHES
        # ----------------------------------------------

        open_pitches = pitch_data[
            ~pitch_data["PitchCall"].isin(
                strike_calls
            )
        ]

        if not open_pitches.empty:

            ax.scatter(
                open_pitches["PlateLocSide"],
                open_pitches["PlateLocHeight"],
                s=55,
                facecolors="white",
                edgecolors=color,
                linewidth=1.8,
                alpha=1.0
            )

    # --------------------------------------------------
    # STRIKE ZONE
    # --------------------------------------------------

    strike_zone_x = [
        -0.83,
        0.83,
        0.83,
        -0.83,
        -0.83
    ]

    strike_zone_y = [
        1.50,
        1.50,
        3.50,
        3.50,
        1.50
    ]

    ax.plot(
        strike_zone_x,
        strike_zone_y,
        color="black",
        linewidth=1.8,
        zorder=3
    )

    # --------------------------------------------------
    # STRIKE ZONE INTERNAL LINES
    # --------------------------------------------------

    ax.plot(
        [-0.83, 0.83],
        [2.50, 2.50],
        color="#777777",
        linewidth=0.8,
        zorder=2
    )

    ax.plot(
        [0, 0],
        [1.50, 3.50],
        color="#777777",
        linewidth=0.8,
        zorder=2
    )

    # --------------------------------------------------
    # BUFFER ZONE
    # ONE BALL WIDTH OUTSIDE THE STRIKE ZONE
    # --------------------------------------------------

    buffer_x = [
        -1.66,
        1.66,
        1.66,
        -1.66,
        -1.66
    ]

    buffer_y = [
        0.50,
        0.50,
        4.50,
        4.50,
        0.50
    ]

    ax.plot(
        buffer_x,
        buffer_y,
        color="#777777",
        linewidth=1.0,
        linestyle="--",
        zorder=1
    )

    # --------------------------------------------------
    # HOME PLATE
    # --------------------------------------------------

    plate = Polygon(
        [
            (-0.55, -0.10),
            (0.55, -0.10),
            (0.55, -0.02),
            (0.00, -0.12),
            (-0.55, -0.02)
        ],
        closed=True,
        facecolor="white",
        edgecolor="#777777",
        linewidth=0.8
    )

    ax.add_patch(plate)

    # --------------------------------------------------
    # AXIS LIMITS
    # --------------------------------------------------

    ax.set_xlim(
        -2.5,
        2.5
    )

    ax.set_ylim(
        -0.45,
        5.0
    )

    # --------------------------------------------------
    # REMOVE DEFAULT GRID
    # --------------------------------------------------

    ax.grid(
        False
    )

    # --------------------------------------------------
    # AXIS LABELS
    # --------------------------------------------------

    ax.set_xlabel(
        "Catcher's view · feet",
        fontsize=8,
        labelpad=8
    )

    ax.set_ylabel(
        "",
        fontsize=8
    )

    # --------------------------------------------------
    # TICK LABELS
    # --------------------------------------------------

    ax.tick_params(
        labelsize=8
    )

    # --------------------------------------------------
    # CLEAN UP Y AXIS
    # --------------------------------------------------

    ax.set_yticks(
        [0, 1, 2, 3, 4, 5]
    )

    # --------------------------------------------------
    # LEGEND
    # --------------------------------------------------

    handles, labels = ax.get_legend_handles_labels()

    if handles:

        ax.legend(
            handles,
            labels,
            loc="upper center",
            bbox_to_anchor=(0.5, -0.12),
            ncol=4,
            frameon=False,
            fontsize=8,
            handletextpad=0.4,
            columnspacing=1.0
        )

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    ax.set_title(
        "PITCH LOCATION",
        fontsize=12,
        fontweight="bold",
        pad=12
    )

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=250,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()



# --------------------------------------------------
# PITCH USAGE CHART
# --------------------------------------------------

def create_pitch_usage_chart(
    pitch_metrics,
    output_path,
):
    import matplotlib.pyplot as plt

    pitches = []
    usage = []

    for pitch_type, metrics in pitch_metrics.items():
        pitches.append(pitch_type)
        usage.append(metrics["usage_pct"])

    # Reverse so the largest pitch appears at the top.
    pitches = pitches[::-1]
    usage = usage[::-1]

    fig, ax = plt.subplots(figsize=(7.0, 2.8))

    pitch_colors = PITCH_COLORS

    colors = [
        pitch_colors.get(pitch, "#777777")
        for pitch in pitches
    ]

    bars = ax.barh(
        pitches,
        usage,
        color=colors,
        height=0.55,
    )

    ax.set_xlim(0, 100)
    ax.set_xlabel("Usage %")
    ax.set_title(
        "PITCH USAGE",
        fontsize=12,
        fontweight="bold",
        loc="left",
    )

    ax.grid(
        axis="x",
        linestyle="--",
        linewidth=0.6,
        alpha=0.35,
    )

    ax.set_axisbelow(True)

    for bar, value in zip(bars, usage):
        ax.text(
            value + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tight_layout()

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(fig)


# --------------------------------------------------
# TEST PITCH USAGE CHART
# --------------------------------------------------

if __name__ == "__main__":
    test_pitch_metrics = {
        "Fastball": {"usage_pct": 80.4},
        "ChangeUp": {"usage_pct": 9.8},
        "Slider": {"usage_pct": 7.8},
        "Curveball": {"usage_pct": 2.0},
    }

    create_pitch_usage_chart(
        test_pitch_metrics,
        "pitch_usage_test.png",
    )

    print("Pitch usage chart created.")