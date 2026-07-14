"""
Selection of voltage coefficient kE.

DEE engineering dataset.

Source:
Kopylov, asynchronous motor design method.

Digitization of the diagram:

    kE = f(Da, 2p)

Selection principle:

    outer stator diameter Da
    +
    number of poles 2p
    ->
    voltage coefficient kE

Linear interpolation is used between digitized
reference points.

Units:

    Da - m
    2p - number of poles
    kE - dimensionless
"""


# ================================================================
# DIGITIZED kE DATA
# ================================================================

KE_DATA = {

    # 2 poles

    2: (
        (0.08, 0.970),
        (0.10, 0.972),
        (0.15, 0.976),
        (0.20, 0.980),
        (0.30, 0.984),
        (0.40, 0.987),
        (0.50, 0.989),
        (0.60, 0.991),
        (0.70, 0.993),
        (0.80, 0.995),
    ),

    # 4 poles

    4: (
        (0.08, 0.945),
        (0.10, 0.950),
        (0.15, 0.960),
        (0.20, 0.968),
        (0.30, 0.976),
        (0.40, 0.981),
        (0.50, 0.985),
        (0.60, 0.988),
        (0.70, 0.991),
        (0.80, 0.993),
    ),

    # 6 poles

    6: (
        (0.08, 0.910),
        (0.10, 0.920),
        (0.15, 0.940),
        (0.20, 0.953),
        (0.30, 0.967),
        (0.40, 0.975),
        (0.50, 0.981),
        (0.60, 0.985),
        (0.70, 0.989),
        (0.80, 0.992),
    ),

    # 8 poles

    8: (
        (0.08, 0.880),
        (0.10, 0.890),
        (0.15, 0.912),
        (0.20, 0.930),
        (0.30, 0.951),
        (0.40, 0.964),
        (0.50, 0.973),
        (0.60, 0.980),
        (0.70, 0.985),
        (0.80, 0.989),
    ),

    # 10 poles

    10: (
        (0.08, 0.850),
        (0.10, 0.862),
        (0.15, 0.885),
        (0.20, 0.905),
        (0.30, 0.930),
        (0.40, 0.948),
        (0.50, 0.960),
        (0.60, 0.970),
        (0.70, 0.978),
        (0.80, 0.984),
    ),

    # 12 poles

    12: (
        (0.08, 0.820),
        (0.10, 0.833),
        (0.15, 0.860),
        (0.20, 0.882),
        (0.30, 0.912),
        (0.40, 0.932),
        (0.50, 0.947),
        (0.60, 0.959),
        (0.70, 0.969),
        (0.80, 0.977),
    ),
}


# ================================================================
# LINEAR INTERPOLATION
# ================================================================

def linear_interpolate(x, x1, y1, x2, y2):
    """
    Linear interpolation between two reference points.
    """

    return y1 + (
        (y2 - y1)
        * (x - x1)
        / (x2 - x1)
    )


# ================================================================
# SELECTION FUNCTION
# ================================================================

def select_voltage_coefficient(Da, poles):
    """
    Select voltage coefficient kE.

    Parameters
    ----------
    Da : float
        Outer stator diameter, m.

    poles : int
        Number of poles 2p.

    Returns
    -------
    float
        Voltage coefficient kE.
    """

    if poles not in KE_DATA:
        raise ValueError(
            f"No kE data for 2p = {poles}. "
            "Supported values: 2, 4, 6, 8, 10, 12."
        )

    points = KE_DATA[poles]

    Da_min = points[0][0]
    Da_max = points[-1][0]

    if Da < Da_min or Da > Da_max:
        raise ValueError(
            f"Da = {Da:.3f} m is outside the digitized "
            f"kE diagram range "
            f"{Da_min:.2f} ... {Da_max:.2f} m."
        )

    # Exact reference point

    for Da_point, kE_point in points:

        if abs(Da - Da_point) < 1e-9:

            return round(
                kE_point,
                3,
            )

    # Linear interpolation

    for index in range(len(points) - 1):

        Da1, kE1 = points[index]
        Da2, kE2 = points[index + 1]

        if Da1 <= Da <= Da2:

            kE = linear_interpolate(
                Da,
                Da1,
                kE1,
                Da2,
                kE2,
            )

            return round(
                kE,
                3,
            )

    raise ValueError(
        "Unable to determine kE."
    )


# ================================================================
# TEST / RESULT OUTPUT
# ================================================================

if __name__ == "__main__":

    print("=" * 82)
    print("DEE - VOLTAGE COEFFICIENT kE")
    print("KOPYLOV DIGITIZED DIAGRAM")
    print("=" * 82)

    print()

    print(
        f"{'Da, m':>10} | "
        f"{'2p=2':>9} | "
        f"{'2p=4':>9} | "
        f"{'2p=6':>9} | "
        f"{'2p=8':>9} | "
        f"{'2p=10':>9} | "
        f"{'2p=12':>9}"
    )

    print("-" * 82)

    test_diameters = (
        0.080,
        0.100,
        0.116,
        0.131,
        0.149,
        0.168,
        0.191,
        0.225,
        0.272,
        0.313,
        0.349,
        0.392,
        0.437,
        0.520,
        0.590,
        0.660,
    )

    for Da in test_diameters:

        values = []

        for poles in (
            2,
            4,
            6,
            8,
            10,
            12,
        ):

            kE = select_voltage_coefficient(
                Da=Da,
                poles=poles,
            )

            values.append(kE)

        print(
            f"{Da:10.3f} | "
            f"{values[0]:9.3f} | "
            f"{values[1]:9.3f} | "
            f"{values[2]:9.3f} | "
            f"{values[3]:9.3f} | "
            f"{values[4]:9.3f} | "
            f"{values[5]:9.3f}"
        )

    # ============================================================
    # KOPYLOV REFERENCE RESULT
    # ============================================================

    print()
    print("=" * 82)
    print("KOPYLOV REFERENCE RESULT")
    print("=" * 82)

    Da_test = 0.272
    poles_test = 4

    kE_test = select_voltage_coefficient(
        Da=Da_test,
        poles=poles_test,
    )

    print()
    print(f"Outer stator diameter:       Da = {Da_test:.3f} m")
    print(f"Number of poles:             2p = {poles_test}")

    print(
        "Selection method:            "
        "Kopylov digitized diagram"
    )

    print(
        "Interpolation method:        "
        "linear interpolation"
    )

    print()

    print(
        f"RESULT:                      "
        f"kE = {kE_test:.3f}"
    )

    print()
    print("=" * 82)