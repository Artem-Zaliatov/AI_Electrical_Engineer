"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
MOTOR DESIGN CURRENT

This module performs:

1. Control calculation of the motor rated current.
2. Comparison with the manufacturer nameplate current.
3. Acceptance of the motor circuit design current IB.

For an existing motor, the manufacturer full-load current (FLC)
is accepted as the motor circuit design current.
"""


# =============================================================================
# IMPORTS
# =============================================================================

from math import sqrt


# =============================================================================
# DESIGN CURRENT ERROR
# =============================================================================

class DesignCurrentError(ValueError):
    """
    Error raised when the motor design current cannot be calculated.
    """

    pass


# =============================================================================
# DESIGN CURRENT CALCULATION
# =============================================================================

def calculate_design_current(motor):
    """
    Calculate and accept the motor circuit design current.

    The calculated motor current is determined from:

        Icalc = Pn / (sqrt(3) * Un * eta * cos(phi))

    where:

        Pn       - motor rated output power, W;
        Un       - motor rated line voltage, V;
        eta      - motor rated efficiency;
        cos(phi) - motor rated power factor.

    For an existing motor, the manufacturer nameplate current
    is accepted as the motor circuit design current:

        IB = In

    Parameters
    ----------
    motor : dict
        Validated motor data.

    Returns
    -------
    dict
        Motor current calculation results.
    """

    if not isinstance(motor, dict):
        raise DesignCurrentError(
            "Motor data must be provided as a dictionary."
        )

    # -------------------------------------------------------------------------
    # REQUIRED MOTOR PARAMETERS
    # -------------------------------------------------------------------------

    required_parameters = (
        "rated_power_kw",
        "rated_voltage_v",
        "rated_current_a",
        "efficiency",
        "power_factor",
    )

    for parameter in required_parameters:
        if parameter not in motor:
            raise DesignCurrentError(
                f"Required motor parameter '{parameter}' is missing."
            )

    # -------------------------------------------------------------------------
    # MOTOR DATA
    # -------------------------------------------------------------------------

    rated_power_kw = float(
        motor["rated_power_kw"]
    )

    rated_voltage_v = float(
        motor["rated_voltage_v"]
    )

    nameplate_current_a = float(
        motor["rated_current_a"]
    )

    efficiency = float(
        motor["efficiency"]
    )

    power_factor = float(
        motor["power_factor"]
    )

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if rated_power_kw <= 0:
        raise DesignCurrentError(
            "Motor rated power must be greater than zero."
        )

    if rated_voltage_v <= 0:
        raise DesignCurrentError(
            "Motor rated voltage must be greater than zero."
        )

    if nameplate_current_a <= 0:
        raise DesignCurrentError(
            "Motor nameplate current must be greater than zero."
        )

    if not 0 < efficiency <= 1:
        raise DesignCurrentError(
            "Motor efficiency must be greater than zero and not exceed 1."
        )

    if not 0 < power_factor <= 1:
        raise DesignCurrentError(
            "Motor power factor must be greater than zero and not exceed 1."
        )

    # -------------------------------------------------------------------------
    # CONTROL CALCULATION OF MOTOR CURRENT
    # -------------------------------------------------------------------------

    rated_power_w = (
        rated_power_kw
        * 1000.0
    )

    calculated_current_a = (
        rated_power_w
        / (
            sqrt(3.0)
            * rated_voltage_v
            * efficiency
            * power_factor
        )
    )

    # -------------------------------------------------------------------------
    # CURRENT DEVIATION
    # -------------------------------------------------------------------------

    current_deviation_a = (
        nameplate_current_a
        - calculated_current_a
    )

    current_deviation_percent = (
        abs(current_deviation_a)
        / nameplate_current_a
        * 100.0
    )

    # -------------------------------------------------------------------------
    # ACCEPT MOTOR CIRCUIT DESIGN CURRENT
    # -------------------------------------------------------------------------

    design_current_a = (
        nameplate_current_a
    )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "calculated_current_a": calculated_current_a,
        "nameplate_current_a": nameplate_current_a,

        "current_deviation_a": current_deviation_a,
        "current_deviation_percent": current_deviation_percent,

        "design_current_a": design_current_a,

        "current_source": "NAMEPLATE FLC",
        "design_current_status": "ACCEPTED",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_motor = {
        "rated_power_kw": 15.0,
        "rated_voltage_v": 400.0,
        "rated_current_a": 28.5,
        "efficiency": 0.921,
        "power_factor": 0.86,
    }

    result = calculate_design_current(
        test_motor,
    )

    print("=" * 76)
    print("DEE - MOTOR DESIGN CURRENT")
    print("=" * 76)

    print()
    print(
        f"Calculated motor current Icalc = "
        f"{result['calculated_current_a']:.2f} A "
        f"(control calculation from Pn, Un, eta and cos(phi))"
    )

    print(
        f"Nameplate motor current In     = "
        f"{result['nameplate_current_a']:.2f} A "
        f"(manufacturer motor full-load current, FLC)"
    )

    print()
    print(
        f"Current deviation              = "
        f"{result['current_deviation_a']:+.2f} A "
        f"(nameplate current minus calculated current)"
    )

    print(
        f"Current deviation              = "
        f"{result['current_deviation_percent']:.2f} % "
        f"(absolute current deviation relative to nameplate FLC)"
    )

    print()
    print(
        f"Accepted design current IB     = "
        f"{result['design_current_a']:.2f} A "
        f"(motor circuit design current based on nameplate FLC)"
    )

    print(
        f"Current source                 = "
        f"{result['current_source']} "
        f"(accepted current data source)"
    )

    print(
        f"Design current status          = "
        f"{result['design_current_status']} "
        f"(design current acceptance status)"
    )

    print("=" * 76)