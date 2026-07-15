"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
SCHNEIDER ELECTRIC MOTOR CIRCUIT BREAKER SELECTION

This module selects a Schneider Electric motor circuit breaker
for a three-phase AC motor feeder.

Current supported product family:

    TeSys Deca GV2ME

Current selection conditions:

    1. motor rated current must be within
       the thermal adjustment range;

    2. motor circuit breaker rated operational voltage
       must be suitable for the system voltage;

    3. ultimate short-circuit breaking capacity Icu
       must be not lower than the calculated prospective
       three-phase short-circuit current at the installation point;

    4. magnetic trip threshold is checked against
       the calculated motor starting current.

Current starting method:

    DOL - Direct-On-Line starting

Methodological basis:

    Schneider Electric TeSys Deca product data
    and Schneider Electric motor protection methodology.
"""


# =============================================================================
# MOTOR CIRCUIT BREAKER SELECTION ERROR
# =============================================================================

class MotorCircuitBreakerSelectionError(ValueError):
    """
    Error raised when a motor circuit breaker cannot be selected.
    """

    pass


# =============================================================================
# SCHNEIDER ELECTRIC TESYS DECA GV2ME DATA
#
# Current DEE digitized product table.
#
# IMPORTANT:
# This table contains the product parameters required
# by the current DEE selection algorithm.
#
# Additional Schneider Electric product parameters
# and coordination tables will be added separately.
# =============================================================================

SCHNEIDER_GV2ME_DATA = (
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME01",
        "thermal_min_a": 0.10,
        "thermal_max_a": 0.16,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME02",
        "thermal_min_a": 0.16,
        "thermal_max_a": 0.25,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME03",
        "thermal_min_a": 0.25,
        "thermal_max_a": 0.40,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME04",
        "thermal_min_a": 0.40,
        "thermal_max_a": 0.63,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME05",
        "thermal_min_a": 0.63,
        "thermal_max_a": 1.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME06",
        "thermal_min_a": 1.00,
        "thermal_max_a": 1.60,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME07",
        "thermal_min_a": 1.60,
        "thermal_max_a": 2.50,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME08",
        "thermal_min_a": 2.50,
        "thermal_max_a": 4.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME10",
        "thermal_min_a": 4.00,
        "thermal_max_a": 6.30,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME14",
        "thermal_min_a": 6.00,
        "thermal_max_a": 10.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME16",
        "thermal_min_a": 9.00,
        "thermal_max_a": 14.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME20",
        "thermal_min_a": 13.00,
        "thermal_max_a": 18.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 100.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME21",
        "thermal_min_a": 17.00,
        "thermal_max_a": 23.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 50.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME22",
        "thermal_min_a": 20.00,
        "thermal_max_a": 25.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 50.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "reference": "GV2ME32",
        "thermal_min_a": 24.00,
        "thermal_max_a": 32.00,
        "magnetic_trip_multiplier": 13.0,
        "rated_operational_voltage_v": 690.0,
        "icu_400v_ka": 10.0,
    },
)


# =============================================================================
# MOTOR CIRCUIT BREAKER SELECTION
# =============================================================================

def select_motor_circuit_breaker(
    motor,
    design_current,
    starting_current,
    short_circuit,
    installation,
):
    """
    Select Schneider Electric TeSys Deca GV2ME
    motor circuit breaker.

    Parameters
    ----------
    motor : dict
        Validated motor data.

    design_current : dict
        Motor design current results.

    starting_current : dict
        Motor starting-current results.

    short_circuit : dict
        Short-circuit current calculation results.

    installation : dict
        Validated installation data.

    Returns
    -------
    dict
        Selected motor circuit breaker data.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(motor, dict):
        raise MotorCircuitBreakerSelectionError(
            "Motor data must be provided as a dictionary."
        )

    if not isinstance(design_current, dict):
        raise MotorCircuitBreakerSelectionError(
            "Design current data must be provided as a dictionary."
        )

    if not isinstance(starting_current, dict):
        raise MotorCircuitBreakerSelectionError(
            "Starting current data must be provided as a dictionary."
        )

    if not isinstance(short_circuit, dict):
        raise MotorCircuitBreakerSelectionError(
            "Short-circuit data must be provided as a dictionary."
        )

    if not isinstance(installation, dict):
        raise MotorCircuitBreakerSelectionError(
            "Installation data must be provided as a dictionary."
        )

    # -------------------------------------------------------------------------
    # REQUIRED PARAMETERS
    # -------------------------------------------------------------------------

    required_motor_parameters = (
        "rated_power_kw",
    )

    required_design_current_parameters = (
        "design_current_a",
    )

    required_starting_parameters = (
        "starting_method",
        "starting_current_a",
    )

    required_short_circuit_parameters = (
        "feeder_end_short_circuit_current_ka",
    )

    required_installation_parameters = (
        "system_voltage_v",
    )

    for parameter in required_motor_parameters:
        if parameter not in motor:
            raise MotorCircuitBreakerSelectionError(
                f"Required motor parameter '{parameter}' is missing."
            )

    for parameter in required_design_current_parameters:
        if parameter not in design_current:
            raise MotorCircuitBreakerSelectionError(
                f"Required design-current parameter "
                f"'{parameter}' is missing."
            )

    for parameter in required_starting_parameters:
        if parameter not in starting_current:
            raise MotorCircuitBreakerSelectionError(
                f"Required starting-current parameter "
                f"'{parameter}' is missing."
            )

    for parameter in required_short_circuit_parameters:
        if parameter not in short_circuit:
            raise MotorCircuitBreakerSelectionError(
                f"Required short-circuit parameter "
                f"'{parameter}' is missing."
            )

    for parameter in required_installation_parameters:
        if parameter not in installation:
            raise MotorCircuitBreakerSelectionError(
                f"Required installation parameter "
                f"'{parameter}' is missing."
            )

    # -------------------------------------------------------------------------
    # INPUT VALUES
    # -------------------------------------------------------------------------

    motor_rated_power_kw = float(
        motor["rated_power_kw"]
    )

    design_current_a = float(
        design_current["design_current_a"]
    )

    starting_method = str(
        starting_current["starting_method"]
    ).strip().upper()

    starting_current_a = float(
        starting_current["starting_current_a"]
    )

    short_circuit_current_ka = float(
        short_circuit[
            "feeder_end_short_circuit_current_ka"
        ]
    )

    system_voltage_v = float(
        installation["system_voltage_v"]
    )

    # -------------------------------------------------------------------------
    # NUMERICAL CHECK
    # -------------------------------------------------------------------------

    if motor_rated_power_kw <= 0:
        raise MotorCircuitBreakerSelectionError(
            "Motor rated power must be greater than zero."
        )

    if design_current_a <= 0:
        raise MotorCircuitBreakerSelectionError(
            "Motor design current must be greater than zero."
        )

    if starting_current_a <= 0:
        raise MotorCircuitBreakerSelectionError(
            "Motor starting current must be greater than zero."
        )

    if short_circuit_current_ka <= 0:
        raise MotorCircuitBreakerSelectionError(
            "Short-circuit current must be greater than zero."
        )

    if system_voltage_v <= 0:
        raise MotorCircuitBreakerSelectionError(
            "System voltage must be greater than zero."
        )

    if starting_method != "DOL":
        raise MotorCircuitBreakerSelectionError(
            f"Starting method '{starting_method}' is not supported. "
            f"Current supported starting method: DOL."
        )

    # -------------------------------------------------------------------------
    # SEARCH PERMISSIBLE DEVICES
    # -------------------------------------------------------------------------

    permissible_devices = []

    for device in SCHNEIDER_GV2ME_DATA:

        thermal_range_check = (
            device["thermal_min_a"]
            <= design_current_a
            <= device["thermal_max_a"]
        )

        voltage_check = (
            system_voltage_v
            <= device["rated_operational_voltage_v"]
        )

        breaking_capacity_check = (
            device["icu_400v_ka"]
            >= short_circuit_current_ka
        )

        magnetic_trip_current_a = (
            device["magnetic_trip_multiplier"]
            * device["thermal_max_a"]
        )

        starting_current_check = (
            starting_current_a
            < magnetic_trip_current_a
        )

        if (
            thermal_range_check
            and voltage_check
            and breaking_capacity_check
            and starting_current_check
        ):
            permissible_devices.append(
                {
                    **device,

                    "magnetic_trip_current_a":
                        magnetic_trip_current_a,

                    "thermal_range_check":
                        "PERMISSIBLE",

                    "voltage_check":
                        "PERMISSIBLE",

                    "breaking_capacity_check":
                        "PERMISSIBLE",

                    "starting_current_check":
                        "PERMISSIBLE",
                }
            )

    # -------------------------------------------------------------------------
    # DEVICE AVAILABILITY CHECK
    # -------------------------------------------------------------------------

    if not permissible_devices:
        raise MotorCircuitBreakerSelectionError(
            "No permissible Schneider Electric TeSys Deca GV2ME "
            "motor circuit breaker was found for the current "
            "motor feeder data."
        )

    # -------------------------------------------------------------------------
    # DEVICE SELECTION
    #
    # Select the device with the lowest upper thermal setting.
    # -------------------------------------------------------------------------

    selected_device = min(
        permissible_devices,
        key=lambda device: device["thermal_max_a"],
    )

    # -------------------------------------------------------------------------
    # THERMAL SETTING
    # -------------------------------------------------------------------------

    thermal_setting_a = design_current_a

    # -------------------------------------------------------------------------
    # MARGINS
    # -------------------------------------------------------------------------

    breaking_capacity_margin_ka = (
        selected_device["icu_400v_ka"]
        - short_circuit_current_ka
    )

    magnetic_trip_margin_a = (
        selected_device["magnetic_trip_current_a"]
        - starting_current_a
    )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        **selected_device,

        "motor_rated_power_kw":
            motor_rated_power_kw,

        "design_current_a":
            design_current_a,

        "starting_method":
            starting_method,

        "starting_current_a":
            starting_current_a,

        "short_circuit_current_ka":
            short_circuit_current_ka,

        "system_voltage_v":
            system_voltage_v,

        "thermal_setting_a":
            thermal_setting_a,

        "breaking_capacity_margin_ka":
            breaking_capacity_margin_ka,

        "magnetic_trip_margin_a":
            magnetic_trip_margin_a,

        "selection_source":
            "SCHNEIDER ELECTRIC TESYS DECA PRODUCT DATA",

        "selection_status":
            "SELECTED",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_motor = {
        "rated_power_kw": 15.0,
    }

    test_design_current = {
        "design_current_a": 28.5,
    }

    test_starting_current = {
        "starting_method": "DOL",
        "starting_current_a": 213.75,
    }

    test_short_circuit = {
        "feeder_end_short_circuit_current_ka": 1.36,
    }

    test_installation = {
        "system_voltage_v": 400.0,
    }

    result = select_motor_circuit_breaker(
        motor=test_motor,
        design_current=test_design_current,
        starting_current=test_starting_current,
        short_circuit=test_short_circuit,
        installation=test_installation,
    )

    print("=" * 76)
    print("DEE - MOTOR CIRCUIT BREAKER SELECTION")
    print("=" * 76)

    print()

    print(
        f"Manufacturer                  = "
        f"{result['manufacturer']} "
        f"(selected device manufacturer)"
    )

    print(
        f"Product series                = "
        f"{result['series']} "
        f"(motor protection product family)"
    )

    print(
        f"Selected reference            = "
        f"{result['reference']} "
        f"(Schneider Electric product reference)"
    )

    print()

    print(
        f"Motor rated power Pn          = "
        f"{result['motor_rated_power_kw']:.2f} kW "
        f"(motor rated output power)"
    )

    print(
        f"Motor design current IB       = "
        f"{result['design_current_a']:.2f} A "
        f"(accepted motor feeder design current)"
    )

    print()

    print(
        f"Thermal adjustment range      = "
        f"{result['thermal_min_a']:.2f} ... "
        f"{result['thermal_max_a']:.2f} A "
        f"(motor overload protection adjustment range)"
    )

    print(
        f"Accepted thermal setting Ir   = "
        f"{result['thermal_setting_a']:.2f} A "
        f"(thermal protection setting based on motor FLC)"
    )

    print(
        f"Thermal range check           = "
        f"{result['thermal_range_check']} "
        f"(motor current within thermal adjustment range)"
    )

    print()

    print(
        f"System voltage Un             = "
        f"{result['system_voltage_v']:.0f} V "
        f"(motor feeder system voltage)"
    )

    print(
        f"Device rated voltage Ue       = "
        f"{result['rated_operational_voltage_v']:.0f} V "
        f"(motor circuit breaker rated operational voltage)"
    )

    print(
        f"Voltage check                 = "
        f"{result['voltage_check']} "
        f"(device voltage suitability check)"
    )

    print()

    print(
        f"Calculated short-circuit Ik3  = "
        f"{result['short_circuit_current_ka']:.2f} kA "
        f"(prospective fault current at installation point)"
    )

    print(
        f"Breaking capacity Icu         = "
        f"{result['icu_400v_ka']:.2f} kA "
        f"(ultimate breaking capacity at 400 V)"
    )

    print(
        f"Breaking capacity margin      = "
        f"{result['breaking_capacity_margin_ka']:.2f} kA "
        f"(Icu minus calculated short-circuit current)"
    )

    print(
        f"Breaking capacity check       = "
        f"{result['breaking_capacity_check']} "
        f"(Icu not lower than prospective fault current)"
    )

    print()

    print(
        f"Starting method               = "
        f"{result['starting_method']} "
        f"(Direct-On-Line starting)"
    )

    print(
        f"Motor starting current Is     = "
        f"{result['starting_current_a']:.2f} A "
        f"(calculated motor starting current)"
    )

    print(
        f"Magnetic trip threshold       = "
        f"{result['magnetic_trip_current_a']:.2f} A "
        f"(instantaneous magnetic trip threshold)"
    )

    print(
        f"Magnetic trip margin          = "
        f"{result['magnetic_trip_margin_a']:.2f} A "
        f"(magnetic trip threshold minus starting current)"
    )

    print(
        f"Starting current check        = "
        f"{result['starting_current_check']} "
        f"(starting current below magnetic trip threshold)"
    )

    print()

    print(
        f"Selection source              = "
        f"{result['selection_source']} "
        f"(equipment selection data source)"
    )

    print(
        f"Selection status              = "
        f"{result['selection_status']} "
        f"(motor circuit breaker selection status)"
    )

    print("=" * 76)