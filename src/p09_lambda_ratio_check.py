"""
Check of the ratio lambda = l_delta / tau.

DEE engineering dataset.

Source:
Kopylov, asynchronous motor design method.
Figure 9.25.

Figure 9.25:
    a - IP44
    b - IP23

The module does NOT select lambda.

The actual lambda value is calculated from previously
obtained motor dimensions:

    lambda = l_delta / tau

The calculated value is checked against the permissible
range from Kopylov Figure 9.25.

Units:

    h       - mm
    l_delta - m
    tau     - m
"""


# ================================================================
# DIGITIZED DATA
# KOPYLOV FIGURE 9.25
# ================================================================


# ================================================================
# IP44
# FIGURE 9.25 a
#
# Two diagram areas:
#
#     h <= 250 mm
#     h >= 280 mm
#
# Data format:
#
#     poles: (
#         lambda_min,
#         lambda_max,
#     )
# ================================================================

LAMBDA_DATA_IP44_SMALL = {

    2: (0.35, 0.80),
    4: (0.55, 1.05),
    6: (0.80, 1.35),
    8: (1.00, 1.65),
    10: (1.30, 1.95),
    12: (1.55, 2.25),
}


LAMBDA_DATA_IP44_LARGE = {

    2: (0.30, 0.65),
    4: (0.50, 0.90),
    6: (0.75, 1.20),
    8: (1.05, 1.50),
    10: (1.40, 1.90),
    12: (1.75, 2.25),
}


# ================================================================
# IP23
# FIGURE 9.25 b
# ================================================================

LAMBDA_DATA_IP23 = {

    2: (0.25, 0.85),
    4: (0.40, 1.20),
    6: (0.70, 1.65),
    8: (1.05, 2.10),
    10: (1.55, 2.65),
    12: (2.00, 3.00),
}


# ================================================================
# AUXILIARY FUNCTIONS
# ================================================================

def linear_interpolate(
    x,
    x1,
    y1,
    x2,
    y2,
):

    return y1 + (
        (y2 - y1)
        * (x - x1)
        / (x2 - x1)
    )


def interpolate_lambda_range(
    poles,
    data,
):

    available_poles = sorted(data.keys())

    if poles < available_poles[0]:
        raise ValueError(
            f"2p = {poles} is below Figure 9.25 range."
        )

    if poles > available_poles[-1]:
        raise ValueError(
            f"2p = {poles} is above Figure 9.25 range."
        )

    if poles in data:

        return data[poles]

    for index in range(
        len(available_poles) - 1
    ):

        poles1 = available_poles[index]
        poles2 = available_poles[index + 1]

        if poles1 <= poles <= poles2:

            lambda_min1, lambda_max1 = (
                data[poles1]
            )

            lambda_min2, lambda_max2 = (
                data[poles2]
            )

            lambda_min = linear_interpolate(
                poles,
                poles1,
                lambda_min1,
                poles2,
                lambda_min2,
            )

            lambda_max = linear_interpolate(
                poles,
                poles1,
                lambda_max1,
                poles2,
                lambda_max2,
            )

            return (
                lambda_min,
                lambda_max,
            )

    raise ValueError(
        "Unable to determine lambda range."
    )


# ================================================================
# DATA SELECTION
# ================================================================

def select_lambda_data(
    h,
    protection,
):

    protection = protection.upper()

    if protection == "IP44":

        if h <= 250:

            return (
                LAMBDA_DATA_IP44_SMALL,
                "Figure 9.25a, h <= 250 mm",
            )

        if h >= 280:

            return (
                LAMBDA_DATA_IP44_LARGE,
                "Figure 9.25a, h >= 280 mm",
            )

        raise ValueError(
            "Figure 9.25a does not explicitly define "
            "the range 250 < h < 280 mm."
        )

    if protection == "IP23":

        return (
            LAMBDA_DATA_IP23,
            "Figure 9.25b",
        )

    raise ValueError(
        f"Unsupported protection degree: {protection}"
    )


# ================================================================
# LAMBDA CALCULATION
# ================================================================

def calculate_lambda(
    l_delta,
    tau,
):

    if tau <= 0:

        raise ValueError(
            "Pole pitch tau must be greater than zero."
        )

    if l_delta <= 0:

        raise ValueError(
            "Calculated length l_delta must be greater than zero."
        )

    lambda_value = l_delta / tau

    return round(
        lambda_value,
        3,
    )


# ================================================================
# LAMBDA CHECK
# ================================================================

def check_lambda_ratio(
    h,
    l_delta,
    tau,
    poles,
    protection,
):

    lambda_value = calculate_lambda(
        l_delta=l_delta,
        tau=tau,
    )

    data, figure = select_lambda_data(
        h=h,
        protection=protection,
    )

    lambda_min, lambda_max = (
        interpolate_lambda_range(
            poles=poles,
            data=data,
        )
    )

    lambda_min = round(
        lambda_min,
        3,
    )

    lambda_max = round(
        lambda_max,
        3,
    )

    is_permissible = (
        lambda_min
        <= lambda_value
        <= lambda_max
    )

    if is_permissible:

        status = "PERMISSIBLE"

    else:

        status = "NOT PERMISSIBLE"

    return {
        "lambda": lambda_value,
        "lambda_min": lambda_min,
        "lambda_max": lambda_max,
        "is_permissible": is_permissible,
        "status": status,
        "figure": figure,
    }


# ================================================================
# TEST / RESULT OUTPUT
# ================================================================

if __name__ == "__main__":

    print("=" * 100)

    print(
        "DEE - LAMBDA RATIO CHECK"
    )

    print(
        "KOPYLOV FIGURE 9.25"
    )

    print("=" * 100)

    tests = (

        # Kopylov reference case
        (
            160,
            0.140,
            0.145,
            4,
            "IP44",
        ),

        # IP44 tests
        (
            180,
            0.180,
            0.160,
            4,
            "IP44",
        ),

        (
            225,
            0.250,
            0.180,
            6,
            "IP44",
        ),

        (
            280,
            0.300,
            0.200,
            8,
            "IP44",
        ),

        (
            315,
            0.400,
            0.220,
            10,
            "IP44",
        ),

        # IP23 tests
        (
            160,
            0.180,
            0.160,
            4,
            "IP23",
        ),

        (
            225,
            0.280,
            0.180,
            6,
            "IP23",
        ),

        (
            280,
            0.400,
            0.200,
            8,
            "IP23",
        ),

        (
            315,
            0.550,
            0.220,
            10,
            "IP23",
        ),
    )

    print()

    print(
        f"{'IP':>6} | "
        f"{'h, mm':>8} | "
        f"{'2p':>4} | "
        f"{'l_delta, m':>11} | "
        f"{'tau, m':>8} | "
        f"{'lambda':>8} | "
        f"{'lambda min':>10} | "
        f"{'lambda max':>10} | "
        f"{'STATUS':>16}"
    )

    print("-" * 100)

    for (
        h,
        l_delta,
        tau,
        poles,
        protection,
    ) in tests:

        result = check_lambda_ratio(
            h=h,
            l_delta=l_delta,
            tau=tau,
            poles=poles,
            protection=protection,
        )

        print(
            f"{protection:>6} | "
            f"{h:8d} | "
            f"{poles:4d} | "
            f"{l_delta:11.3f} | "
            f"{tau:8.3f} | "
            f"{result['lambda']:8.3f} | "
            f"{result['lambda_min']:10.3f} | "
            f"{result['lambda_max']:10.3f} | "
            f"{result['status']:>16}"
        )

    print("=" * 100)

    print()

    print(
        "KOPYLOV REFERENCE TEST"
    )

    result = check_lambda_ratio(
        h=160,
        l_delta=0.140,
        tau=0.145,
        poles=4,
        protection="IP44",
    )

    print(
        f"lambda = {result['lambda']}"
    )

    print(
        f"permissible range = "
        f"{result['lambda_min']} ... "
        f"{result['lambda_max']}"
    )

    print(
        f"status = {result['status']}"
    )

    print(
        f"source = {result['figure']}"
    )

    print("=" * 100)