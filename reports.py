def generate_report(report):
    """
    Turn analyzed pitcher data into a readable
    post-game report.
    """

    pitcher = report["pitcher"]
    total_pitches = report["total_pitches"]

    overall = report["overall"]
    pitch_metrics = report["pitch_metrics"]

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    lines = []

    lines.append("=" * 70)
    lines.append(
        f"{pitcher.upper()} - POST-GAME PITCHING REPORT"
    )
    lines.append("=" * 70)

    lines.append("")

    # --------------------------------------------------
    # OVERALL METRICS
    # --------------------------------------------------

    lines.append("OVERALL METRICS")
    lines.append("-" * 70)

    lines.append(
        f"Total Pitches: {total_pitches}"
    )

    lines.append(
        f"Strike %:      {overall['strike_pct']:.1f}%"
    )

    lines.append(
        f"Whiff %:       {overall['whiff_pct']:.1f}%"
    )

    lines.append(
        f"CSW %:         {overall['csw_pct']:.1f}%"
    )

    lines.append(
        f"Chase %:       {overall['chase_pct']:.1f}%"
    )

    lines.append("")

    # --------------------------------------------------
    # PITCH ARSENAL
    # --------------------------------------------------

    lines.append("PITCH ARSENAL")
    lines.append("-" * 70)

    lines.append(
        f"{'Pitch':<15}"
        f"{'Usage':>10}"
        f"{'Velo':>10}"
        f"{'Spin':>10}"
        f"{'IVB':>10}"
        f"{'HB':>10}"
    )

    lines.append("-" * 70)

    for pitch_type, metrics in pitch_metrics.items():

        lines.append(
            f"{pitch_type:<15}"
            f"{metrics['usage_pct']:>9.1f}%"
            f"{metrics['avg_velocity']:>10.1f}"
            f"{metrics['avg_spin']:>10.0f}"
            f"{metrics['avg_ivb']:>10.1f}"
            f"{metrics['avg_hb']:>10.1f}"
        )

    lines.append("")

    # --------------------------------------------------
    # PITCH EFFECTIVENESS
    # --------------------------------------------------

    lines.append("PITCH EFFECTIVENESS")
    lines.append("-" * 70)

    lines.append(
        f"{'Pitch':<15}"
        f"{'Strike':>10}"
        f"{'Whiff':>10}"
        f"{'CSW':>10}"
        f"{'Chase':>10}"
    )

    lines.append("-" * 70)

    for pitch_type, metrics in pitch_metrics.items():

        lines.append(
            f"{pitch_type:<15}"
            f"{metrics['strike_pct']:>9.1f}%"
            f"{metrics['whiff_pct']:>9.1f}%"
            f"{metrics['csw_pct']:>9.1f}%"
            f"{metrics['chase_pct']:>9.1f}%"
        )

    lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)