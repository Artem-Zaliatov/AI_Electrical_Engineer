"""
Selection of inner stator diameter coefficient KD.

DEE engineering dataset.

Source:
Kopylov, asynchronous motor design method.

Selection principle:

    number of poles 2p -> recommended KD range

DEE selection rule:

    KD = midpoint of the recommended range

The selected value is rounded to two decimal places.
"""


# ================================================================
# INNER DIAMETER COEFFICIENT DATA
# ================================================================

KD_DATA = {
    2: (0.52, 0.60),
    4: (0.62, 0.68),
    6: (0.70, 0.72),
    8: (0.72, 0.75),
    10: (0.75, 0.77),
    12: (0.75, 0.77),
}


# ================================================================
# SELECTION FUNCTION
# ================================================================

def select_inner_diameter_coefficient(poles):
    """
    Select inner stator diameter coefficient KD.

    Parameters
    ----------
    poles : int
        Number of poles 2p.

    Returns
    -------
    tuple
        KD_selected, KD_min, KD_max
    """

    if poles not in KD_DATA:
        raise ValueError(
            f"No KD data for 2p = {poles}. "
            "Supported values: 2, 4, 6, 8, 10, 12."
        )

    KD_min, KD_max = KD_DATA[poles]

    # DEE selection rule:
    # midpoint of recommended range,
    # rounded to two decimal places

    KD_selected = round(
        (KD_min + KD_max) / 2,
        2,
    )

    return KD_selected, KD_min, KD_max


# ================================================================
# TEST / DATA OUTPUT
# ================================================================

if __name__ == "__main__":

    print("=" * 66)
    print("DEE - INNER DIAMETER COEFFICIENT DATA")
    print("KOPYLOV REFERENCE TABLE")
    print("SELECTION RULE: MIDPOINT OF KD RANGE")
    print("=" * 66)

    print(
        f"{'2p':>8} | "
        f"{'KD range':>20} | "
        f"{'Selected KD':>16}"
    )

    print("-" * 66)

    for poles in sorted(KD_DATA):

        KD, KD_min, KD_max = (
            select_inner_diameter_coefficient(poles)
        )

        KD_range = (
            f"{KD_min:.2f} ... {KD_max:.2f}"
        )

        print(
            f"{poles:8d} | "
            f"{KD_range:>20} | "
            f"{KD:16.2f}"
        )

    print("=" * 66)

    print()
    print("SELECTION PRINCIPLE:")
    print("2p -> KD range -> midpoint -> round to 2 decimals")