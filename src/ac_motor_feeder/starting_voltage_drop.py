"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
MOTOR STARTING VOLTAGE DROP

This module estimates the motor feeder cable voltage drop
during Direct-On-Line motor starting.

Current supported starting method:

    DOL - Direct-On-Line starting

The same balanced three-phase cable voltage-drop relationship
is applied using the motor starting current.

The starting power factor is a separate input parameter because
the rated motor power factor must not be automatically used
for the starting condition.
"""


# =============================================================================
# IMPORTS
# =============================================================================

from math import sqrt


# =============================================================================
# STARTING VOLTAGE DROP ERROR
# =============================================================================

class StartingVoltageDropError(ValueError):
    """
    Error raised when starting voltage drop cannot be calculated.
    """

    pass


# =============================================================================
# STARTING VOLTAGE DROP CALCULATION
# =============================================================================

def calculate_starting_voltage_drop(
    starting_current,
    voltage_drop,
    starting_power_factor,
):
    """
    Calculate motor feeder voltage drop during DOL starting.

    Parameters
    ----------
    starting_current : dict
        Motor starting-current calculation results.

    voltage_drop : dict
        Steady-state voltage-drop calculation results.
        Cable R and X data are reused.

    starting_power_factor : float
        Motor starting power factor.

    Returns
    -------
    dict
        Starting voltage-drop calculation results.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(starting_current, dict):
        raise StartingVoltageDropError(
            "Starting current data must be provided as a dictionary."
        )

    if not isinstance(voltage_drop, dict):
        raise StartingVoltageDropError(
            "Voltage drop data must be provided as a dictionary."
        )

    required_starting_parameters = (
        "starting_method",
        "starting_current_a",
        "starting_time_s",
    )

    required_voltage_drop_parameters = (
        "system_voltage_v",
        "cable_length_m",
        "cable_length_km",
        "cross_section_mm2",
        "resistance_ohm_km",
        "reactance_ohm_km",
    )

    for parameter in required_starting_parameters:
        if parameter not in starting_current:
            raise StartingVoltageDropError(
                f"Required starting-current parameter "
                f"'{parameter}' is missing."
            )

    for parameter in required_voltage_drop_parameters:
        if parameter not in voltage_drop:
            raise StartingVoltageDropError(
                f"Required voltage-drop parameter "
                f"'{parameter}' is missing."
            )

    # -------------------------------------------------------------------------
    # INPUT VALUES
    # -------------------------------------------------------------------------

    starting_method = str(
        starting_current["starting_method"]
    ).strip().upper()

    starting_current_a = float(
        starting_current["starting_current_a"]
    )

    starting_time_s = float(
        starting_current["starting_time_s"]
    )

    system_voltage_v = float(
        voltage_drop["system_voltage_v"]
    )

    cable_length_m = float(
        voltage_drop["cable_length_m"]
    )

    cable_length_km = float(
        voltage_drop["cable_length_km"]
    )

    cross_section_mm2 = float(
        voltage_drop["cross_section_mm2"]
    )

    resistance_ohm_km = float(
        voltage_drop["resistance_ohm_km"]
    )

    reactance_ohm_km = float(
        voltage_drop["reactance_ohm_km"]
    )

    starting_power_factor = float(
        starting_power_factor
    )

    # -------------------------------------------------------------------------
    # DATA CHECK
    # -------------------------------------------------------------------------

    if starting_method != "DOL":
        raise StartingVoltageDropError(
            f"Starting method '{starting_method}' is not supported. "
            f"Current supported starting method: DOL."
        )

    if starting_current_a <= 0:
        raise StartingVoltageDropError(
            "Starting current must be greater than zero."
        )

    if starting_time_s <= 0:
        raise StartingVoltageDropError(
            "Starting time must be greater than zero."
        )

    if system_voltage_v <= 0:
        raise StartingVoltageDropError(
            "System voltage must be greater than zero."
        )

    if cable_length_km <= 0:
        raise StartingVoltageDropError(
            "Cable length must be greater than zero."
        )

    if not 0 < starting_power_factor <= 1:
        raise StartingVoltageDropError(
            "Starting power factor must be greater than zero "
            "and not exceed 1."
        )

    # -------------------------------------------------------------------------
    # STARTING POWER FACTOR COMPONENTS
    # -------------------------------------------------------------------------

    starting_sin_phi = sqrt(
        1.0
        - starting_power_factor ** 2
    )

    # -------------------------------------------------------------------------
    # ACTIVE AND REACTIVE COMPONENTS
    # -------------------------------------------------------------------------

    active_component_ohm_km = (
        resistance_ohm_km
        * starting_power_factor
    )

    reactive_component_ohm_km = (
        reactance_ohm_km
        * starting_sin_phi
    )

    equivalent_component_ohm_km = (
        active_component_ohm_km
        + reactive_component_ohm_km
    )

    # -------------------------------------------------------------------------
    # STARTING VOLTAGE DROP
    # -------------------------------------------------------------------------

    starting_voltage_drop_v = (
        sqrt(3.0)
        * starting_current_a
        * equivalent_component_ohm_km
        * cable_length_km
    )

    starting_voltage_drop_percent = (
        starting_voltage_drop_v
        / system_voltage_v
        * 100.0
    )

    starting_terminal_voltage_v = (
        system_voltage_v
        - starting_voltage_drop_v
    )

    starting_terminal_voltage_percent = (
        starting_terminal_voltage_v
        / system_voltage_v
        * 100.0
    )

    # -------------------------------------------------------------------------
    # CURRENT DEE STARTING VOLTAGE-DROP ASSESSMENT
    #
    # 15 percent is used as the current project assessment limit.
    #
    # This is an engineering project criterion in the current module.
    # It must not be presented as a universal Schneider product limit.
    # -------------------------------------------------------------------------

    maximum_starting_voltage_drop_percent = 15.0

    if (
        starting_voltage_drop_percent
        <= maximum_starting_voltage_drop_percent
    ):
        starting_voltage_drop_check = "PERMISSIBLE"
    else:
        starting_voltage_drop_check = "NOT PERMISSIBLE"

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "starting_method":
            starting_method,

        "starting_current_a":
            starting_current_a,

        "starting_time_s":
            starting_time_s,

        "system_voltage_v":
            system_voltage_v,

        "cable_length_m":
            cable_length_m,

        "cross_section_mm2":
            cross_section_mm2,

        "resistance_ohm_km":
            resistance_ohm_km,

        "reactance_ohm_km":
            reactance_ohm_km,

        "starting_power_factor":
            starting_power_factor,

        "starting_sin_phi":
            starting_sin_phi,

        "active_component_ohm_km":
            active_component_ohm_km,

        "reactive_component_ohm_km":
            reactive_component_ohm_km,

        "equivalent_component_ohm_km":
            equivalent_component_ohm_km,

        "starting_voltage_drop_v":
            starting_voltage_drop_v,

        "starting_voltage_drop_percent":
            starting_voltage_drop_percent,

        "starting_terminal_voltage_v":
            starting_terminal_voltage_v,

        "starting_terminal_voltage_percent":
            starting_terminal_voltage_percent,

        "maximum_starting_voltage_drop_percent":
            maximum_starting_voltage_drop_percent,

        "starting_voltage_drop_check":
            starting_voltage_drop_check,

        "starting_voltage_drop_source":
            "SCHNEIDER ELECTRIC EIG / PROJECT ASSESSMENT",

        "starting_voltage_drop_status":
            "CALCULATED",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_starting_current = {
        "starting_method": "DOL",
        "starting_current_a": 213.75,
        "starting_time_s": 3.5,
    }

    test_voltage_drop = {
        "system_voltage_v": 400.0,
        "cable_length_m": 45.0,
        "cable_length_km": 0.045,
        "cross_section_mm2": 6.0,
        "resistance_ohm_km": 3.69,
        "reactance_ohm_km": 0.08,
    }

    result = calculate_starting_voltage_drop(
        starting_current=test_starting_current,
        voltage_drop=test_voltage_drop,
        starting_power_factor=0.35,
    )

    print("=" * 76)
    print("DEE - MOTOR STARTING VOLTAGE DROP")
    print("=" * 76)

    print()

    print(
        f"Starting method               = "
        f"{result['starting_method']} "
        f"(Direct-On-Line starting)"
    )

    print(
        f"Starting current Is           = "
        f"{result['starting_current_a']:.2f} A "
        f"(motor starting current)"
    )

    print(
        f"Starting time ts              = "
        f"{result['starting_time_s']:.2f} s "
        f"(motor acceleration time)"
    )

    print()

    print(
        f"Starting power factor         = "
        f"{result['starting_power_factor']:.3f} "
        f"(motor power factor during starting)"
    )

    print(
        f"Starting sin(phi)             = "
        f"{result['starting_sin_phi']:.3f} "
        f"(sine of starting phase angle)"
    )

    print()

    print(
        f"Cable length L                = "
        f"{result['cable_length_m']:.1f} m "
        f"(one-way cable length)"
    )

    print(
        f"Conductor section S           = "
        f"{result['cross_section_mm2']:.1f} mm2 "
        f"(selected phase conductor cross-section)"
    )

    print()

    print(
        f"Starting voltage drop         = "
        f"{result['starting_voltage_drop_v']:.2f} V "
        f"(motor feeder voltage drop during starting)"
    )

    print(
        f"Starting voltage drop         = "
        f"{result['starting_voltage_drop_percent']:.2f} % "
        f"(starting voltage drop)"
    )

    print(
        f"Starting terminal voltage     = "
        f"{result['starting_terminal_voltage_v']:.2f} V "
        f"(estimated motor terminal voltage during starting)"
    )

    print(
        f"Starting terminal voltage     = "
        f"{result['starting_terminal_voltage_percent']:.2f} % Un "
        f"(motor starting terminal voltage)"
    )

    print()

    print(
        f"Maximum starting voltage drop = "
        f"{result['maximum_starting_voltage_drop_percent']:.2f} % "
        f"(current project assessment limit)"
    )

    print(
        f"Starting voltage-drop check   = "
        f"{result['starting_voltage_drop_check']} "
        f"(starting voltage-drop assessment)"
    )

    print(
        f"Starting voltage-drop source  = "
        f"{result['starting_voltage_drop_source']} "
        f"(calculation and assessment source)"
    )

    print(
        f"Starting voltage-drop status  = "
        f"{result['starting_voltage_drop_status']} "
        f"(starting voltage-drop calculation status)"
    )

    print("=" * 76)