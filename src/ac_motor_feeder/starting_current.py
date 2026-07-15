"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
MOTOR STARTING CURRENT

This module calculates the motor starting current
from the accepted motor rated current and the
manufacturer starting-current ratio.

Current supported starting method:

DOL - Direct-On-Line starting

The starting current is calculated as:

    Is = kI * In

where:

    Is - motor starting current, A;
    kI - starting current ratio Is/In;
    In - motor rated nameplate current, A.
"""


# =============================================================================
# STARTING CURRENT ERROR
# =============================================================================

class StartingCurrentError(ValueError):
    """
    Error raised when motor starting current
    cannot be calculated.
    """

    pass


# =============================================================================
# STARTING METHOD DESCRIPTIONS
# =============================================================================

STARTING_METHOD_DESCRIPTIONS = {
    "DOL": "Direct-On-Line starting",
    "STAR_DELTA": "Star-Delta starting",
    "SOFT_START": "Soft starter",
    "VFD": "Variable Frequency Drive",
}


# =============================================================================
# STARTING CURRENT CALCULATION
# =============================================================================

def calculate_starting_current(
    motor,
    design_current,
):
    """
    Calculate motor starting current.

    For DOL starting:

        Is = kI * In

    The manufacturer motor nameplate current is used
    as the rated motor current.

    Parameters
    ----------
    motor : dict
        Validated motor data.

    design_current : dict
        Motor design current calculation result.

    Returns
    -------
    dict
        Motor starting-current calculation results.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(motor, dict):
        raise StartingCurrentError(
            "Motor data must be provided as a dictionary."
        )

    if not isinstance(design_current, dict):
        raise StartingCurrentError(
            "Design current data must be provided as a dictionary."
        )

    required_motor_parameters = (
        "starting_method",
        "starting_current_ratio",
        "starting_time_s",
    )

    for parameter in required_motor_parameters:
        if parameter not in motor:
            raise StartingCurrentError(
                f"Required motor parameter '{parameter}' is missing."
            )

    if "nameplate_current_a" not in design_current:
        raise StartingCurrentError(
            "Nameplate motor current is missing "
            "from design current results."
        )

    # -------------------------------------------------------------------------
    # MOTOR STARTING DATA
    # -------------------------------------------------------------------------

    starting_method = str(
        motor["starting_method"]
    ).strip().upper()

    starting_current_ratio = float(
        motor["starting_current_ratio"]
    )

    starting_time_s = float(
        motor["starting_time_s"]
    )

    rated_current_a = float(
        design_current["nameplate_current_a"]
    )

    # -------------------------------------------------------------------------
    # NUMERICAL DATA CHECK
    # -------------------------------------------------------------------------

    if rated_current_a <= 0:
        raise StartingCurrentError(
            "Motor rated current must be greater than zero."
        )

    if starting_current_ratio <= 0:
        raise StartingCurrentError(
            "Starting current ratio must be greater than zero."
        )

    if starting_time_s <= 0:
        raise StartingCurrentError(
            "Motor starting time must be greater than zero."
        )

    # -------------------------------------------------------------------------
    # STARTING METHOD CHECK
    # -------------------------------------------------------------------------

    if starting_method not in STARTING_METHOD_DESCRIPTIONS:
        raise StartingCurrentError(
            f"Unknown motor starting method '{starting_method}'."
        )

    if starting_method != "DOL":
        raise StartingCurrentError(
            f"Starting method '{starting_method}' is recognized but "
            "is not supported in the current DEE version. "
            "Current supported starting method: DOL."
        )

    # -------------------------------------------------------------------------
    # STARTING CURRENT CALCULATION
    # -------------------------------------------------------------------------

    starting_current_a = (
        starting_current_ratio
        * rated_current_a
    )

    # -------------------------------------------------------------------------
    # STARTING CURRENT PERCENT
    # -------------------------------------------------------------------------

    starting_current_percent = (
        starting_current_a
        / rated_current_a
        * 100.0
    )

    # -------------------------------------------------------------------------
    # STARTING TIME CLASSIFICATION
    #
    # IMPORTANT:
    # This classification is descriptive only.
    # It is NOT used for Schneider Electric equipment selection.
    # Equipment selection will later be performed using official
    # Schneider Electric coordination and product data.
    # -------------------------------------------------------------------------

    if starting_time_s <= 5.0:
        starting_time_class = "SHORT"

    elif starting_time_s <= 10.0:
        starting_time_class = "MEDIUM"

    else:
        starting_time_class = "LONG"

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "starting_method": starting_method,

        "starting_method_description":
            STARTING_METHOD_DESCRIPTIONS[starting_method],

        "rated_current_a": rated_current_a,

        "starting_current_ratio":
            starting_current_ratio,

        "starting_current_a":
            starting_current_a,

        "starting_current_percent":
            starting_current_percent,

        "starting_time_s":
            starting_time_s,

        "starting_time_class":
            starting_time_class,

        "starting_data_source":
            "NAMEPLATE / MANUFACTURER DATA",

        "starting_current_status":
            "CALCULATED",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_motor = {
        "starting_method": "DOL",
        "starting_current_ratio": 7.5,
        "starting_time_s": 3.5,
    }

    test_design_current = {
        "nameplate_current_a": 28.5,
    }

    result = calculate_starting_current(
        motor=test_motor,
        design_current=test_design_current,
    )

    print("=" * 76)
    print("DEE - MOTOR STARTING CURRENT")
    print("=" * 76)

    print()

    print(
        f"Starting method               = "
        f"{result['starting_method']} "
        f"({result['starting_method_description']})"
    )

    print(
        f"Rated motor current In        = "
        f"{result['rated_current_a']:.2f} A "
        f"(motor nameplate full-load current, FLC)"
    )

    print(
        f"Starting current ratio Is/In  = "
        f"{result['starting_current_ratio']:.2f} "
        f"(manufacturer starting-current ratio)"
    )

    print()

    print(
        f"Starting current Is           = "
        f"{result['starting_current_a']:.2f} A "
        f"(calculated motor starting current)"
    )

    print(
        f"Starting current              = "
        f"{result['starting_current_percent']:.0f} % In "
        f"(starting current relative to rated current)"
    )

    print()

    print(
        f"Starting time ts              = "
        f"{result['starting_time_s']:.2f} s "
        f"(motor acceleration time)"
    )

    print(
        f"Starting time class           = "
        f"{result['starting_time_class']} "
        f"(descriptive starting-time classification)"
    )

    print()

    print(
        f"Starting data source          = "
        f"{result['starting_data_source']} "
        f"(starting parameters data source)"
    )

    print(
        f"Starting current status       = "
        f"{result['starting_current_status']} "
        f"(starting-current calculation status)"
    )

    print("=" * 76)