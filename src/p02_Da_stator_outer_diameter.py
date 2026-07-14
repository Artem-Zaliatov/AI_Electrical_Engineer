"""
Selection of stator outer diameter Da.

DEE engineering dataset.

Source:
Kopylov, asynchronous motor design method.

Selection principle:

    shaft height h -> recommended outer stator diameter Da

DEE selection rule:

    Da = lower value of the recommended range

Units:

    h  - mm
    Da - m
"""


# ================================================================
# OUTER STATOR DIAMETER DATA
# ================================================================

DA_DATA = {
    56: (0.080, 0.096),
    63: (0.100, 0.108),
    71: (0.116, 0.122),
    80: (0.131, 0.139),
    90: (0.149, 0.157),

    100: (0.168, 0.175),
    112: (0.191, 0.197),
    132: (0.225, 0.233),
    160: (0.272, 0.285),
    180: (0.313, 0.322),

    200: (0.349, 0.359),
    225: (0.392, 0.406),
    250: (0.437, 0.452),
    280: (0.520, 0.530),
    315: (0.590, 0.590),
    355: (0.660, 0.660),
}


# ================================================================
# SELECTION FUNCTION
# ================================================================

def select_outer_stator_diameter(shaft_height_mm):
    """
    Select outer stator diameter Da.

    Parameters
    ----------
    shaft_height_mm : int
        Standard shaft height h, mm.

    Returns
    -------
    tuple
        Da_selected, Da_min, Da_max

    All diameter values are returned in metres.
    """

    if shaft_height_mm not in DA_DATA:
        raise ValueError(
            f"No outer stator diameter data for "
            f"h = {shaft_height_mm} mm."
        )

    Da_min, Da_max = DA_DATA[shaft_height_mm]

    # DEE selection rule:
    # select lower value of recommended range

    Da_selected = Da_min

    return Da_selected, Da_min, Da_max


# ================================================================
# TEST / DATA OUTPUT
# ================================================================

if __name__ == "__main__":

    print("=" * 72)
    print("DEE - OUTER STATOR DIAMETER DATA")
    print("KOPYLOV REFERENCE TABLE")
    print("SELECTION RULE: LOWER LIMIT OF Da RANGE")
    print("=" * 72)

    print(
        f"{'h, mm':>10} | "
        f"{'Da range, m':>22} | "
        f"{'Selected Da, m':>18}"
    )

    print("-" * 72)

    for h in sorted(DA_DATA):

        Da, Da_min, Da_max = (
            select_outer_stator_diameter(h)
        )

        if Da_min == Da_max:
            da_range = f"{Da_min:.3f}"
        else:
            da_range = (
                f"{Da_min:.3f} ... {Da_max:.3f}"
            )

        print(
            f"{h:10d} | "
            f"{da_range:>22} | "
            f"{Da:18.3f}"
        )

    print("=" * 72)

    print()
    print("SELECTION PRINCIPLE:")
    print("h -> Da range -> lower Da value")