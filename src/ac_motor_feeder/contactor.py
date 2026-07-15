"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
SCHNEIDER ELECTRIC CONTACTOR SELECTION

This module selects a Schneider Electric TeSys Deca contactor
for a three-phase asynchronous motor.

Current supported product family:

    TeSys Deca LC1D

Current motor utilisation category:

    AC-3 / AC-3e

Selection conditions:

    1. contactor AC-3 operational current Ie
       must be not lower than the motor design current IB;

    2. motor rated power at 400 V must be not lower
       than the motor rated output power;

    3. contactor rated operational voltage must be suitable
       for the motor feeder system voltage;

    4. contactor coil voltage and current type must correspond
       to the control circuit supply.

Methodological basis:

    Schneider Electric TeSys Deca product data.
"""


# =============================================================================
# CONTACTOR SELECTION ERROR
# =============================================================================

class ContactorSelectionError(ValueError):
    """
    Error raised when a contactor cannot be selected.
    """

    pass


# =============================================================================
# SCHNEIDER ELECTRIC TESYS DECA LC1D DATA
#
# Digitized DEE selection table.
#
# The base contactor reference is stored separately from the coil suffix.
# Final product reference:
#
#     base reference + coil suffix
#
# Example:
#
#     LC1D32 + M7 = LC1D32M7
# =============================================================================

SCHNEIDER_LC1D_DATA = (
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D09",
        "ie_ac3_a": 9.0,
        "motor_power_400v_kw": 4.0,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D12",
        "ie_ac3_a": 12.0,
        "motor_power_400v_kw": 5.5,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D18",
        "ie_ac3_a": 18.0,
        "motor_power_400v_kw": 7.5,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D25",
        "ie_ac3_a": 25.0,
        "motor_power_400v_kw": 11.0,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D32",
        "ie_ac3_a": 32.0,
        "motor_power_400v_kw": 15.0,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D38",
        "ie_ac3_a": 38.0,
        "motor_power_400v_kw": 18.5,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D40A",
        "ie_ac3_a": 40.0,
        "motor_power_400v_kw": 18.5,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D50A",
        "ie_ac3_a": 50.0,
        "motor_power_400v_kw": 22.0,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D65A",
        "ie_ac3_a": 65.0,
        "motor_power_400v_kw": 30.0,
        "rated_operational_voltage_v": 690.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D80",
        "ie_ac3_a": 80.0,
        "motor_power_400v_kw": 37.0,
        "rated_operational_voltage_v": 1000.0,
    },
    {
        "manufacturer": "SCHNEIDER ELECTRIC",
        "series": "TESYS DECA",
        "base_reference": "LC1D95",
        "ie_ac3_a": 95.0,
        "motor_power_400v_kw": 45.0,
        "rated_operational_voltage_v": 1000.0,
    },
)


# =============================================================================
# SCHNEIDER ELECTRIC COIL DATA
# =============================================================================

SCHNEIDER_LC1D_COIL_DATA = (
    {
        "control_voltage_v": 24.0,
        "control_current_type": "AC",
        "coil_suffix": "B7",
        "coil_description": "24 V AC 50/60 Hz",
    },
    {
        "control_voltage_v": 48.0,
        "control_current_type": "AC",
        "coil_suffix": "E7",
        "coil_description": "48 V AC 50/60 Hz",
    },
    {
        "control_voltage_v": 110.0,
        "control_current_type": "AC",
        "coil_suffix": "F7",
        "coil_description": "110 V AC 50/60 Hz",
    },
    {
        "control_voltage_v": 220.0,
        "control_current_type": "AC",
        "coil_suffix": "M7",
        "coil_description": "220 V AC 50/60 Hz",
    },
    {
        "control_voltage_v": 230.0,
        "control_current_type": "AC",
        "coil_suffix": "P7",
        "coil_description": "230 V AC 50/60 Hz",
    },
    {
        "control_voltage_v": 24.0,
        "control_current_type": "DC",
        "coil_suffix": "BD",
        "coil_description": "24 V DC",
    },
    {
        "control_voltage_v": 48.0,
        "control_current_type": "DC",
        "coil_suffix": "ED",
        "coil_description": "48 V DC",
    },
)


# =============================================================================
# CONTACTOR SELECTION
# =============================================================================

def select_contactor(
    motor,
    design_current,
    installation,
):
    """
    Select Schneider Electric TeSys Deca LC1D contactor.

    Parameters
    ----------
    motor : dict
        Validated motor data.

    design_current : dict
        Motor design-current calculation results.

    installation : dict
        Validated installation data.

    Returns
    -------
    dict
        Selected Schneider Electric contactor data.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(motor, dict):
        raise ContactorSelectionError(
            "Motor data must be provided as a dictionary."
        )

    if not isinstance(design_current, dict):
        raise ContactorSelectionError(
            "Design current data must be provided as a dictionary."
        )

    if not isinstance(installation, dict):
        raise ContactorSelectionError(
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

    required_installation_parameters = (
        "system_voltage_v",
        "control_voltage_v",
        "control_current_type",
    )

    for parameter in required_motor_parameters:
        if parameter not in motor:
            raise ContactorSelectionError(
                f"Required motor parameter '{parameter}' is missing."
            )

    for parameter in required_design_current_parameters:
        if parameter not in design_current:
            raise ContactorSelectionError(
                f"Required design-current parameter "
                f"'{parameter}' is missing."
            )

    for parameter in required_installation_parameters:
        if parameter not in installation:
            raise ContactorSelectionError(
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

    system_voltage_v = float(
        installation["system_voltage_v"]
    )

    control_voltage_v = float(
        installation["control_voltage_v"]
    )

    control_current_type = str(
        installation["control_current_type"]
    ).strip().upper()

    # -------------------------------------------------------------------------
    # NUMERICAL CHECK
    # -------------------------------------------------------------------------

    if motor_rated_power_kw <= 0:
        raise ContactorSelectionError(
            "Motor rated power must be greater than zero."
        )

    if design_current_a <= 0:
        raise ContactorSelectionError(
            "Motor design current must be greater than zero."
        )

    if system_voltage_v <= 0:
        raise ContactorSelectionError(
            "System voltage must be greater than zero."
        )

    if control_voltage_v <= 0:
        raise ContactorSelectionError(
            "Control voltage must be greater than zero."
        )

    if control_current_type not in (
        "AC",
        "DC",
    ):
        raise ContactorSelectionError(
            "Control current type must be AC or DC."
        )

    # -------------------------------------------------------------------------
    # SELECT CONTACTOR BASE
    # -------------------------------------------------------------------------

    permissible_contactors = []

    for contactor in SCHNEIDER_LC1D_DATA:

        current_check = (
            contactor["ie_ac3_a"]
            >= design_current_a
        )

        power_check = (
            contactor["motor_power_400v_kw"]
            >= motor_rated_power_kw
        )

        voltage_check = (
            contactor["rated_operational_voltage_v"]
            >= system_voltage_v
        )

        if (
            current_check
            and power_check
            and voltage_check
        ):
            permissible_contactors.append(
                {
                    **contactor,

                    "current_check":
                        "PERMISSIBLE",

                    "power_check":
                        "PERMISSIBLE",

                    "voltage_check":
                        "PERMISSIBLE",
                }
            )

    if not permissible_contactors:
        raise ContactorSelectionError(
            "No permissible Schneider Electric TeSys Deca "
            "LC1D contactor was found for the current motor data."
        )

    selected_contactor = min(
        permissible_contactors,
        key=lambda contactor: (
            contactor["ie_ac3_a"],
            contactor["motor_power_400v_kw"],
        ),
    )

    # -------------------------------------------------------------------------
    # SELECT COIL
    # -------------------------------------------------------------------------

    selected_coil = None

    for coil in SCHNEIDER_LC1D_COIL_DATA:

        voltage_match = (
            coil["control_voltage_v"]
            == control_voltage_v
        )

        current_type_match = (
            coil["control_current_type"]
            == control_current_type
        )

        if (
            voltage_match
            and current_type_match
        ):
            selected_coil = coil
            break

    if selected_coil is None:
        raise ContactorSelectionError(
            f"No supported TeSys Deca LC1D coil was found for "
            f"{control_voltage_v:.0f} V "
            f"{control_current_type} control supply."
        )

    # -------------------------------------------------------------------------
    # FINAL PRODUCT REFERENCE
    # -------------------------------------------------------------------------

    final_reference = (
        selected_contactor["base_reference"]
        + selected_coil["coil_suffix"]
    )

    # -------------------------------------------------------------------------
    # SELECTION MARGINS
    # -------------------------------------------------------------------------

    current_margin_a = (
        selected_contactor["ie_ac3_a"]
        - design_current_a
    )

    power_margin_kw = (
        selected_contactor["motor_power_400v_kw"]
        - motor_rated_power_kw
    )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        **selected_contactor,
        **selected_coil,

        "reference":
            final_reference,

        "motor_rated_power_kw":
            motor_rated_power_kw,

        "design_current_a":
            design_current_a,

        "system_voltage_v":
            system_voltage_v,

        "current_margin_a":
            current_margin_a,

        "power_margin_kw":
            power_margin_kw,

        "utilisation_category":
            "AC-3 / AC-3e",

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

    test_installation = {
        "system_voltage_v": 400.0,
        "control_voltage_v": 220.0,
        "control_current_type": "AC",
    }

    result = select_contactor(
        motor=test_motor,
        design_current=test_design_current,
        installation=test_installation,
    )

    print("=" * 76)
    print("DEE - CONTACTOR SELECTION")
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
        f"(contactor product family)"
    )

    print(
        f"Selected reference            = "
        f"{result['reference']} "
        f"(Schneider Electric product reference)"
    )

    print()

    print(
        f"Utilisation category          = "
        f"{result['utilisation_category']} "
        f"(squirrel-cage motor starting and stopping duty)"
    )

    print()

    print(
        f"Motor rated power Pn          = "
        f"{result['motor_rated_power_kw']:.2f} kW "
        f"(motor rated output power)"
    )

    print(
        f"Contactor motor power         = "
        f"{result['motor_power_400v_kw']:.2f} kW "
        f"(permissible motor power at 400 V)"
    )

    print(
        f"Motor power margin            = "
        f"{result['power_margin_kw']:.2f} kW "
        f"(contactor motor power minus motor rated power)"
    )

    print(
        f"Motor power check             = "
        f"{result['power_check']} "
        f"(contactor motor power suitability check)"
    )

    print()

    print(
        f"Motor design current IB       = "
        f"{result['design_current_a']:.2f} A "
        f"(accepted motor feeder design current)"
    )

    print(
        f"Contactor operational Ie      = "
        f"{result['ie_ac3_a']:.2f} A "
        f"(rated operational current in AC-3)"
    )

    print(
        f"Current margin                = "
        f"{result['current_margin_a']:.2f} A "
        f"(contactor operational current minus motor design current)"
    )

    print(
        f"Current check                 = "
        f"{result['current_check']} "
        f"(AC-3 operational current suitability check)"
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
        f"(contactor rated operational voltage)"
    )

    print(
        f"Voltage check                 = "
        f"{result['voltage_check']} "
        f"(contactor voltage suitability check)"
    )

    print()

    print(
        f"Control circuit voltage Uc    = "
        f"{result['control_voltage_v']:.0f} V "
        f"{result['control_current_type']} "
        f"(control circuit supply)"
    )

    print(
        f"Selected coil                 = "
        f"{result['coil_suffix']} "
        f"({result['coil_description']})"
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
        f"(contactor selection status)"
    )

    print("=" * 76)