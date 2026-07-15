"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
STEADY-STATE VOLTAGE DROP

This module calculates the voltage drop in a balanced
three-phase motor feeder under steady-state operating conditions.

Methodological basis:
- Schneider Electric Electrical Installation Guide;
- IEC 60364 conductor sizing methodology.

For a balanced three-phase circuit:

    delta_U = sqrt(3) * IB * (R*cos(phi) + X*sin(phi)) * L

where:

    delta_U  - line-to-line voltage drop, V;
    IB       - motor feeder design current, A;
    R        - conductor resistance, ohm/km;
    X        - conductor reactance, ohm/km;
    cos(phi) - motor power factor;
    sin(phi) - sine of the motor phase angle;
    L        - one-way cable length, km.

Current supported configuration:
- copper conductor;
- PVC insulated cable;
- balanced three-phase motor feeder.
"""


# =============================================================================
# IMPORTS
# =============================================================================

from math import sqrt


# =============================================================================
# VOLTAGE DROP ERROR
# =============================================================================

class VoltageDropError(ValueError):
    """
    Error raised when voltage drop cannot be calculated.
    """

    pass


# =============================================================================
# CABLE ELECTRICAL DATA
#
# Copper conductor resistance values:
# approximate conductor resistance at 70 deg C.
#
# Reactance:
# 0.08 ohm/km is used for the current supported
# low-voltage three-phase cable configuration.
#
# IMPORTANT:
# The cable electrical data block will later be expanded
# for specific cable construction and manufacturer data.
# =============================================================================

CU_PVC_CABLE_ELECTRICAL_DATA = {
    1.5: {
        "resistance_ohm_km": 14.48,
        "reactance_ohm_km": 0.08,
    },
    2.5: {
        "resistance_ohm_km": 8.87,
        "reactance_ohm_km": 0.08,
    },
    4.0: {
        "resistance_ohm_km": 5.52,
        "reactance_ohm_km": 0.08,
    },
    6.0: {
        "resistance_ohm_km": 3.69,
        "reactance_ohm_km": 0.08,
    },
    10.0: {
        "resistance_ohm_km": 2.19,
        "reactance_ohm_km": 0.08,
    },
    16.0: {
        "resistance_ohm_km": 1.38,
        "reactance_ohm_km": 0.08,
    },
    25.0: {
        "resistance_ohm_km": 0.875,
        "reactance_ohm_km": 0.08,
    },
    35.0: {
        "resistance_ohm_km": 0.627,
        "reactance_ohm_km": 0.08,
    },
    50.0: {
        "resistance_ohm_km": 0.464,
        "reactance_ohm_km": 0.08,
    },
    70.0: {
        "resistance_ohm_km": 0.322,
        "reactance_ohm_km": 0.08,
    },
    95.0: {
        "resistance_ohm_km": 0.244,
        "reactance_ohm_km": 0.08,
    },
    120.0: {
        "resistance_ohm_km": 0.195,
        "reactance_ohm_km": 0.08,
    },
    150.0: {
        "resistance_ohm_km": 0.157,
        "reactance_ohm_km": 0.08,
    },
    185.0: {
        "resistance_ohm_km": 0.126,
        "reactance_ohm_km": 0.08,
    },
    240.0: {
        "resistance_ohm_km": 0.098,
        "reactance_ohm_km": 0.08,
    },
    300.0: {
        "resistance_ohm_km": 0.078,
        "reactance_ohm_km": 0.08,
    },
}


# =============================================================================
# VOLTAGE DROP CALCULATION
# =============================================================================

def calculate_voltage_drop(
    motor,
    design_current,
    cable,
    installation,
):
    """
    Calculate steady-state voltage drop in the motor feeder.

    Parameters
    ----------
    motor : dict
        Validated motor data.

    design_current : dict
        Motor design current calculation results.

    cable : dict
        Selected cable current-carrying capacity results.

    installation : dict
        Validated installation data.

    Returns
    -------
    dict
        Steady-state voltage-drop calculation results.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(motor, dict):
        raise VoltageDropError(
            "Motor data must be provided as a dictionary."
        )

    if not isinstance(design_current, dict):
        raise VoltageDropError(
            "Design current data must be provided as a dictionary."
        )

    if not isinstance(cable, dict):
        raise VoltageDropError(
            "Cable data must be provided as a dictionary."
        )

    if not isinstance(installation, dict):
        raise VoltageDropError(
            "Installation data must be provided as a dictionary."
        )

    required_motor_parameters = (
        "power_factor",
    )

    required_design_current_parameters = (
        "design_current_a",
    )

    required_cable_parameters = (
        "selected_cross_section_mm2",
    )

    required_installation_parameters = (
        "system_voltage_v",
        "cable_length_m",
    )

    for parameter in required_motor_parameters:
        if parameter not in motor:
            raise VoltageDropError(
                f"Required motor parameter '{parameter}' is missing."
            )

    for parameter in required_design_current_parameters:
        if parameter not in design_current:
            raise VoltageDropError(
                f"Required design current parameter "
                f"'{parameter}' is missing."
            )

    for parameter in required_cable_parameters:
        if parameter not in cable:
            raise VoltageDropError(
                f"Required cable parameter '{parameter}' is missing."
            )

    for parameter in required_installation_parameters:
        if parameter not in installation:
            raise VoltageDropError(
                f"Required installation parameter "
                f"'{parameter}' is missing."
            )

    # -------------------------------------------------------------------------
    # INPUT VALUES
    # -------------------------------------------------------------------------

    design_current_a = float(
        design_current["design_current_a"]
    )

    system_voltage_v = float(
        installation["system_voltage_v"]
    )

    cable_length_m = float(
        installation["cable_length_m"]
    )

    cross_section_mm2 = float(
        cable["selected_cross_section_mm2"]
    )

    power_factor = float(
        motor["power_factor"]
    )

    # -------------------------------------------------------------------------
    # NUMERICAL DATA CHECK
    # -------------------------------------------------------------------------

    if design_current_a <= 0:
        raise VoltageDropError(
            "Motor design current must be greater than zero."
        )

    if system_voltage_v <= 0:
        raise VoltageDropError(
            "System voltage must be greater than zero."
        )

    if cable_length_m <= 0:
        raise VoltageDropError(
            "Cable length must be greater than zero."
        )

    if not 0 < power_factor <= 1:
        raise VoltageDropError(
            "Motor power factor must be greater than zero "
            "and not exceed 1."
        )

    if cross_section_mm2 not in CU_PVC_CABLE_ELECTRICAL_DATA:
        raise VoltageDropError(
            f"Cable cross-section {cross_section_mm2:.1f} mm2 "
            f"is not available in the cable electrical data table."
        )

    # -------------------------------------------------------------------------
    # CABLE ELECTRICAL DATA
    # -------------------------------------------------------------------------

    cable_data = CU_PVC_CABLE_ELECTRICAL_DATA[
        cross_section_mm2
    ]

    resistance_ohm_km = float(
        cable_data["resistance_ohm_km"]
    )

    reactance_ohm_km = float(
        cable_data["reactance_ohm_km"]
    )

    # -------------------------------------------------------------------------
    # POWER FACTOR COMPONENTS
    # -------------------------------------------------------------------------

    sin_phi = sqrt(
        1.0
        - power_factor ** 2
    )

    # -------------------------------------------------------------------------
    # CABLE LENGTH
    # -------------------------------------------------------------------------

    cable_length_km = (
        cable_length_m
        / 1000.0
    )

    # -------------------------------------------------------------------------
    # ACTIVE AND REACTIVE VOLTAGE-DROP COMPONENTS
    # -------------------------------------------------------------------------

    active_component_ohm_km = (
        resistance_ohm_km
        * power_factor
    )

    reactive_component_ohm_km = (
        reactance_ohm_km
        * sin_phi
    )

    equivalent_component_ohm_km = (
        active_component_ohm_km
        + reactive_component_ohm_km
    )

    # -------------------------------------------------------------------------
    # VOLTAGE DROP
    # -------------------------------------------------------------------------

    voltage_drop_v = (
        sqrt(3.0)
        * design_current_a
        * equivalent_component_ohm_km
        * cable_length_km
    )

    voltage_drop_percent = (
        voltage_drop_v
        / system_voltage_v
        * 100.0
    )

    motor_terminal_voltage_v = (
        system_voltage_v
        - voltage_drop_v
    )

    # -------------------------------------------------------------------------
    # DEE STEADY-STATE CHECK
    #
    # 5 percent is used as the motor terminal-voltage assessment limit
    # for the current module.
    # -------------------------------------------------------------------------

    maximum_voltage_drop_percent = 5.0

    if voltage_drop_percent <= maximum_voltage_drop_percent:
        voltage_drop_check = "PERMISSIBLE"
    else:
        voltage_drop_check = "NOT PERMISSIBLE"

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "design_current_a":
            design_current_a,

        "system_voltage_v":
            system_voltage_v,

        "cable_length_m":
            cable_length_m,

        "cable_length_km":
            cable_length_km,

        "cross_section_mm2":
            cross_section_mm2,

        "power_factor":
            power_factor,

        "sin_phi":
            sin_phi,

        "resistance_ohm_km":
            resistance_ohm_km,

        "reactance_ohm_km":
            reactance_ohm_km,

        "active_component_ohm_km":
            active_component_ohm_km,

        "reactive_component_ohm_km":
            reactive_component_ohm_km,

        "equivalent_component_ohm_km":
            equivalent_component_ohm_km,

        "voltage_drop_v":
            voltage_drop_v,

        "voltage_drop_percent":
            voltage_drop_percent,

        "motor_terminal_voltage_v":
            motor_terminal_voltage_v,

        "maximum_voltage_drop_percent":
            maximum_voltage_drop_percent,

        "voltage_drop_check":
            voltage_drop_check,

        "voltage_drop_source":
            "SCHNEIDER ELECTRIC EIG / IEC METHODOLOGY",

        "voltage_drop_status":
            "CALCULATED",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_motor = {
        "power_factor": 0.86,
    }

    test_design_current = {
        "design_current_a": 28.5,
    }

    test_cable = {
        "selected_cross_section_mm2": 6.0,
    }

    test_installation = {
        "system_voltage_v": 400.0,
        "cable_length_m": 45.0,
    }

    result = calculate_voltage_drop(
        motor=test_motor,
        design_current=test_design_current,
        cable=test_cable,
        installation=test_installation,
    )

    print("=" * 76)
    print("DEE - STEADY-STATE VOLTAGE DROP")
    print("=" * 76)

    print()

    print(
        f"Motor design current IB       = "
        f"{result['design_current_a']:.2f} A "
        f"(motor feeder design current)"
    )

    print(
        f"System voltage Un             = "
        f"{result['system_voltage_v']:.0f} V "
        f"(three-phase line voltage)"
    )

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
        f"Cable resistance R            = "
        f"{result['resistance_ohm_km']:.3f} ohm/km "
        f"(conductor resistance)"
    )

    print(
        f"Cable reactance X             = "
        f"{result['reactance_ohm_km']:.3f} ohm/km "
        f"(cable inductive reactance)"
    )

    print()

    print(
        f"Power factor cos(phi)         = "
        f"{result['power_factor']:.3f} "
        f"(motor rated power factor)"
    )

    print(
        f"sin(phi)                      = "
        f"{result['sin_phi']:.3f} "
        f"(sine of motor phase angle)"
    )

    print()

    print(
        f"Voltage drop delta_U          = "
        f"{result['voltage_drop_v']:.2f} V "
        f"(steady-state line voltage drop)"
    )

    print(
        f"Voltage drop delta_U          = "
        f"{result['voltage_drop_percent']:.2f} % "
        f"(steady-state voltage drop)"
    )

    print(
        f"Motor terminal voltage        = "
        f"{result['motor_terminal_voltage_v']:.2f} V "
        f"(estimated motor terminal voltage)"
    )

    print()

    print(
        f"Maximum voltage drop          = "
        f"{result['maximum_voltage_drop_percent']:.2f} % "
        f"(current motor voltage-drop assessment limit)"
    )

    print(
        f"Voltage drop check            = "
        f"{result['voltage_drop_check']} "
        f"(steady-state voltage-drop check)"
    )

    print(
        f"Voltage drop source           = "
        f"{result['voltage_drop_source']} "
        f"(calculation methodology source)"
    )

    print(
        f"Voltage drop status           = "
        f"{result['voltage_drop_status']} "
        f"(voltage-drop calculation status)"
    )

    print("=" * 76)