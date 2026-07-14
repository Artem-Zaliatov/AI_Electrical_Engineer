"""
Digital Electrical Engineer (DEE)

P01 - SHAFT HEIGHT SELECTION

Selection of the standard shaft height h
for an asynchronous motor.

Reference:

    Kopylov
    Figure 9.18

Protection degrees:

    IP44 - Figure 9.18a
    IP23 - Figure 9.18b

INPUT:

    power_kw   - rated output power P2, kW
    poles      - number of poles 2p
    protection - IP44 or IP23

OUTPUT:

    standard shaft height h, mm


IMPORTANT
---------

The tables below are digitized engineering data
obtained from Kopylov Figure 9.18.

The diagram gives recommended shaft-height zones
depending on:

    P2
    2p
    protection degree

The continuous diagram is converted to standard
shaft heights.

For IP23, combinations outside the digitized
Figure 9.18b operating area are not artificially
clamped to h = 160 mm.

Such combinations are reported as unavailable.
"""


# ================================================================
# STANDARD MOTOR POWERS
# ================================================================

STANDARD_POWERS_KW = (
    0.55,
    0.75,
    1.10,
    1.50,
    2.20,
    3.00,
    4.00,
    5.50,
    7.50,
    11.00,
    15.00,
    18.50,
    22.00,
    30.00,
    37.00,
    45.00,
    55.00,
    75.00,
    90.00,
    110.00,
    132.00,
    160.00,
    200.00,
    250.00,
    315.00,
)


# ================================================================
# SUPPORTED NUMBERS OF POLES
# ================================================================

SUPPORTED_POLES = (
    2,
    4,
    6,
    8,
)


# ================================================================
# IP44
#
# KOPYLOV FIGURE 9.18a
#
# Existing digitized data retained.
# ================================================================

IP44_SHAFT_HEIGHT_DATA = {

    2: {
        0.55: 63,
        0.75: 71,
        1.10: 71,
        1.50: 80,
        2.20: 80,
        3.00: 90,
        4.00: 100,
        5.50: 100,
        7.50: 112,
        11.00: 132,
        15.00: 160,
        18.50: 160,
        22.00: 180,
        30.00: 180,
        37.00: 200,
        45.00: 200,
        55.00: 225,
        75.00: 250,
        90.00: 250,
        110.00: 280,
        132.00: 280,
        160.00: 315,
        200.00: 315,
        250.00: 355,
        315.00: 355,
    },

    4: {
        0.55: 71,
        0.75: 71,
        1.10: 80,
        1.50: 80,
        2.20: 90,
        3.00: 100,
        4.00: 100,
        5.50: 112,
        7.50: 132,
        11.00: 132,
        15.00: 160,
        18.50: 160,
        22.00: 180,
        30.00: 180,
        37.00: 200,
        45.00: 200,
        55.00: 225,
        75.00: 250,
        90.00: 250,
        110.00: 280,
        132.00: 280,
        160.00: 315,
        200.00: 315,
        250.00: 355,
        315.00: 355,
    },

    6: {
        0.55: 71,
        0.75: 80,
        1.10: 80,
        1.50: 90,
        2.20: 100,
        3.00: 112,
        4.00: 112,
        5.50: 132,
        7.50: 132,
        11.00: 160,
        15.00: 160,
        18.50: 180,
        22.00: 200,
        30.00: 200,
        37.00: 225,
        45.00: 250,
        55.00: 250,
        75.00: 280,
        90.00: 280,
        110.00: 315,
        132.00: 315,
        160.00: 355,
        200.00: 355,
        250.00: 355,
        315.00: None,
    },

    8: {
        0.55: 80,
        0.75: 90,
        1.10: 90,
        1.50: 100,
        2.20: 112,
        3.00: 112,
        4.00: 132,
        5.50: 132,
        7.50: 160,
        11.00: 160,
        15.00: 180,
        18.50: 200,
        22.00: 200,
        30.00: 225,
        37.00: 250,
        45.00: 250,
        55.00: 280,
        75.00: 280,
        90.00: 315,
        110.00: 315,
        132.00: 355,
        160.00: 355,
        200.00: 355,
        250.00: None,
        315.00: None,
    },
}


# ================================================================
# IP23
#
# KOPYLOV FIGURE 9.18b
#
# RE-DIGITIZED DATA
#
# The previous IP23 table was rejected because low-power
# combinations were artificially clamped to h = 160 mm and
# medium-power shaft heights were overestimated.
#
# The new data follow the position of the corresponding
# 2p zones in Figure 9.18b.
#
# None:
#
#     combination is outside the accepted digitized area
#     of Figure 9.18b.
# ================================================================

IP23_SHAFT_HEIGHT_DATA = {

    # ------------------------------------------------------------
    # 2p = 2
    # ------------------------------------------------------------

    2: {
        0.55: None,
        0.75: None,
        1.10: None,
        1.50: None,
        2.20: None,
        3.00: None,
        4.00: None,
        5.50: None,
        7.50: None,
        11.00: None,

        15.00: 160,
        18.50: 160,
        22.00: 180,
        30.00: 180,
        37.00: 200,
        45.00: 200,
        55.00: 225,
        75.00: 250,
        90.00: 250,
        110.00: 280,
        132.00: 280,
        160.00: 315,
        200.00: 315,
        250.00: 355,
        315.00: 355,
    },


    # ------------------------------------------------------------
    # 2p = 4
    # ------------------------------------------------------------

    4: {
        0.55: None,
        0.75: None,
        1.10: None,
        1.50: None,
        2.20: None,
        3.00: None,
        4.00: None,
        5.50: None,

        7.50: 160,
        11.00: 160,
        15.00: 180,
        18.50: 180,
        22.00: 200,
        30.00: 200,
        37.00: 225,
        45.00: 225,
        55.00: 250,
        75.00: 250,
        90.00: 280,
        110.00: 280,
        132.00: 315,
        160.00: 315,
        200.00: 355,
        250.00: 355,
        315.00: 355,
    },


    # ------------------------------------------------------------
    # 2p = 6
    # ------------------------------------------------------------

    6: {
        0.55: None,
        0.75: None,
        1.10: None,
        1.50: None,
        2.20: None,
        3.00: None,
        4.00: None,

        5.50: 160,
        7.50: 160,
        11.00: 180,
        15.00: 180,
        18.50: 200,
        22.00: 200,
        30.00: 225,

        # Control point:
        # P2 = 37 kW, 2p = 6
        # Figure 9.18b -> h approximately 220...230 mm
        # Standard shaft height -> 225 mm
        37.00: 225,

        45.00: 225,
        55.00: 250,
        75.00: 250,
        90.00: 280,
        110.00: 280,
        132.00: 315,
        160.00: 315,
        200.00: 355,
        250.00: 355,
        315.00: None,
    },


    # ------------------------------------------------------------
    # 2p = 8
    # ------------------------------------------------------------

    8: {
        0.55: None,
        0.75: None,
        1.10: None,
        1.50: None,
        2.20: None,
        3.00: None,

        4.00: 160,
        5.50: 160,
        7.50: 180,
        11.00: 180,
        15.00: 200,
        18.50: 200,
        22.00: 225,
        30.00: 225,
        37.00: 250,
        45.00: 250,
        55.00: 280,
        75.00: 280,
        90.00: 315,
        110.00: 315,
        132.00: 355,
        160.00: 355,
        200.00: 355,
        250.00: None,
        315.00: None,
    },
}


# ================================================================
# DATA COLLECTION
# ================================================================

SHAFT_HEIGHT_DATA = {
    "IP44": IP44_SHAFT_HEIGHT_DATA,
    "IP23": IP23_SHAFT_HEIGHT_DATA,
}


# ================================================================
# NORMALIZE PROTECTION DEGREE
# ================================================================

def normalize_protection(protection):
    """
    Normalize protection degree.

    Examples:

        ip44
        IP44
        Ip44

    ->

        IP44
    """

    protection = str(
        protection
    ).strip().upper()

    if protection not in SHAFT_HEIGHT_DATA:

        raise ValueError(
            "Unsupported protection degree: "
            f"{protection}. "
            "Supported values: IP44, IP23."
        )

    return protection


# ================================================================
# NORMALIZE NUMBER OF POLES
# ================================================================

def normalize_poles(poles):
    """
    Validate number of poles 2p.
    """

    try:

        poles = int(
            poles
        )

    except (
        TypeError,
        ValueError,
    ) as error:

        raise ValueError(
            "Number of poles 2p must be an integer."
        ) from error

    if poles not in SUPPORTED_POLES:

        raise ValueError(
            "Unsupported number of poles 2p: "
            f"{poles}. "
            "Supported values: 2, 4, 6, 8."
        )

    return poles


# ================================================================
# NORMALIZE POWER
# ================================================================

def normalize_power(power_kw):
    """
    Convert input power to float.
    """

    try:

        power_kw = float(
            power_kw
        )

    except (
        TypeError,
        ValueError,
    ) as error:

        raise ValueError(
            "Rated output power P2 must be numeric."
        ) from error

    if power_kw <= 0:

        raise ValueError(
            "Rated output power P2 must be greater than zero."
        )

    return power_kw


# ================================================================
# FIND STANDARD POWER
# ================================================================

def find_standard_power(
    power_kw,
    tolerance=1e-9,
):
    """
    Find an exact standard power value.

    The current DEE Section 1 calculation uses
    the standard motor power series.
    """

    for standard_power in STANDARD_POWERS_KW:

        if abs(
            power_kw
            - standard_power
        ) <= tolerance:

            return standard_power

    raise ValueError(
        f"P2 = {power_kw:g} kW is not included in the "
        "digitized standard power series for Figure 9.18. "
        "Use one of the standard P2 values defined in "
        "STANDARD_POWERS_KW."
    )


# ================================================================
# SELECT SHAFT HEIGHT
# ================================================================

def select_shaft_height(
    power_kw,
    poles,
    protection,
):
    """
    Select standard shaft height h.

    Parameters
    ----------
    power_kw : float
        Rated output power P2, kW.

    poles : int
        Number of poles 2p.

    protection : str
        IP44 or IP23.

    Returns
    -------
    int
        Standard shaft height h, mm.
    """

    power_kw = normalize_power(
        power_kw
    )

    poles = normalize_poles(
        poles
    )

    protection = normalize_protection(
        protection
    )

    standard_power = find_standard_power(
        power_kw
    )

    protection_data = SHAFT_HEIGHT_DATA[
        protection
    ]

    pole_data = protection_data[
        poles
    ]

    shaft_height = pole_data[
        standard_power
    ]


    # ============================================================
    # OUTSIDE DIGITIZED DIAGRAM AREA
    # ============================================================

    if shaft_height is None:

        figure = (
            "Figure 9.18a"
            if protection == "IP44"
            else "Figure 9.18b"
        )

        raise ValueError(
            f"P2 = {standard_power:.2f} kW, "
            f"2p = {poles}, "
            f"{protection}: "
            f"combination is outside the accepted "
            f"digitized area of Kopylov {figure}. "
            f"Shaft height h cannot be selected "
            f"reliably from the current digitized data."
        )


    # ============================================================
    # RESULT
    # ============================================================

    return shaft_height


# ================================================================
# PRINT DATA TABLE
# ================================================================

def print_shaft_height_table(
    protection,
):
    """
    Print shaft-height selection table.
    """

    protection = normalize_protection(
        protection
    )

    data = SHAFT_HEIGHT_DATA[
        protection
    ]

    figure = (
        "9.18a"
        if protection == "IP44"
        else "9.18b"
    )

    print()
    print("=" * 82)

    print(
        "DEE - SHAFT HEIGHT SELECTION"
    )

    print(
        f"KOPYLOV FIGURE {figure}"
    )

    print(
        f"PROTECTION DEGREE: {protection}"
    )

    print("=" * 82)

    print(
        f"{'P2, kW':>10} | "
        f"{'2p=2':>12} | "
        f"{'2p=4':>12} | "
        f"{'2p=6':>12} | "
        f"{'2p=8':>12}"
    )

    print("-" * 82)

    for power_kw in STANDARD_POWERS_KW:

        row = [
            f"{power_kw:10.2f}"
        ]

        for poles in SUPPORTED_POLES:

            shaft_height = data[
                poles
            ][
                power_kw
            ]

            if shaft_height is None:

                value = "N/A"

            else:

                value = (
                    f"{shaft_height} mm"
                )

            row.append(
                f"{value:>12}"
            )

        print(
            " | ".join(
                row
            )
        )

    print("=" * 82)


# ================================================================
# MODULE TEST
# ================================================================

if __name__ == "__main__":

    print()
    print("=" * 82)
    print("DEE - SHAFT HEIGHT SELECTION TEST")
    print("=" * 82)


    # ============================================================
    # IP44 TABLE
    # ============================================================

    print_shaft_height_table(
        protection="IP44"
    )


    # ============================================================
    # IP23 TABLE
    # ============================================================

    print_shaft_height_table(
        protection="IP23"
    )


    # ============================================================
    # CONTROL TEST
    #
    # This is intentionally retained as an engineering
    # regression check.
    # ============================================================

    print()
    print("=" * 82)
    print("CONTROL TEST")
    print("=" * 82)

    control_cases = (

        (
            15.0,
            4,
            "IP44",
        ),

        (
            55.0,
            8,
            "IP44",
        ),

        (
            37.0,
            6,
            "IP23",
        ),

        (
            55.0,
            6,
            "IP23",
        ),
    )

    for (
        power_kw,
        poles,
        protection,
    ) in control_cases:

        try:

            shaft_height = select_shaft_height(
                power_kw=power_kw,
                poles=poles,
                protection=protection,
            )

            print(
                f"P2 = {power_kw:7.2f} kW | "
                f"2p = {poles:2d} | "
                f"{protection:4s} | "
                f"h = {shaft_height:3d} mm"
            )

        except ValueError as error:

            print(
                f"P2 = {power_kw:7.2f} kW | "
                f"2p = {poles:2d} | "
                f"{protection:4s} | "
                f"ERROR: {error}"
            )

    print("=" * 82)