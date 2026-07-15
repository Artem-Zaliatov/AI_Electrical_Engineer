"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
INSTALLATION DATA

This module stores and validates the electrical installation
and motor feeder cable installation conditions.

Methodological basis:
- Schneider Electric Electrical Installation Guide;
- IEC 60364 cable sizing methodology.

Current supported cable configuration:
- copper conductor;
- PVC insulation, 70 deg C;
- three loaded conductors;
- installation method C;
- cable installed in air.
"""


# =============================================================================
# INSTALLATION DATA ERROR
# =============================================================================

class InstallationDataError(ValueError):
    """
    Error raised when installation input data are invalid.
    """

    pass


# =============================================================================
# PARAMETER DESCRIPTIONS
# =============================================================================

CONDUCTOR_MATERIAL_DESCRIPTIONS = {
    "CU": "Copper conductor",
    "AL": "Aluminium conductor",
}


INSULATION_DESCRIPTIONS = {
    "PVC": "PVC insulation, 70 deg C",
    "XLPE": "XLPE insulation, 90 deg C",
}


INSTALLATION_METHOD_DESCRIPTIONS = {
    "C": "Clipped direct / cable fixed on a surface",
}


INSTALLATION_ENVIRONMENT_DESCRIPTIONS = {
    "AIR": "Cable installed in air",
}


# =============================================================================
# AUXILIARY FUNCTIONS
# =============================================================================

def _require_value(data, key):
    """
    Check that a required parameter exists and is not None.
    """

    if key not in data:
        raise InstallationDataError(
            f"Required installation parameter '{key}' is missing."
        )

    if data[key] is None:
        raise InstallationDataError(
            f"Required installation parameter '{key}' is None."
        )

    return data[key]


def _require_positive(data, key):
    """
    Check that a numerical parameter is greater than zero.
    """

    value = _require_value(
        data,
        key,
    )

    if not isinstance(value, (int, float)):
        raise InstallationDataError(
            f"Installation parameter '{key}' must be numerical."
        )

    if value <= 0:
        raise InstallationDataError(
            f"Installation parameter '{key}' must be greater than zero."
        )

    return float(value)


def _require_integer_positive(data, key):
    """
    Check that a parameter is a positive integer.
    """

    value = _require_value(
        data,
        key,
    )

    if not isinstance(value, int):
        raise InstallationDataError(
            f"Installation parameter '{key}' must be an integer."
        )

    if value <= 0:
        raise InstallationDataError(
            f"Installation parameter '{key}' must be greater than zero."
        )

    return value


def _require_choice(data, key, choices):
    """
    Check that a text parameter belongs to permissible choices.
    """

    value = _require_value(
        data,
        key,
    )

    if not isinstance(value, str):
        raise InstallationDataError(
            f"Installation parameter '{key}' must be text."
        )

    value = value.strip().upper()

    if value not in choices:
        raise InstallationDataError(
            f"Unsupported value '{value}' for installation "
            f"parameter '{key}'. "
            f"Permissible values: {', '.join(choices)}."
        )

    return value


# =============================================================================
# INSTALLATION DATA VALIDATION
# =============================================================================

def validate_installation_data(installation_data):
    """
    Validate motor feeder installation data.

    Parameters
    ----------
    installation_data : dict
        Electrical installation and cable installation data.

    Returns
    -------
    dict
        Validated and normalized installation data.
    """

    if not isinstance(installation_data, dict):
        raise InstallationDataError(
            "Installation data must be provided as a dictionary."
        )

    # -------------------------------------------------------------------------
    # SYSTEM DATA
    # -------------------------------------------------------------------------

    system_voltage_v = _require_positive(
        installation_data,
        "system_voltage_v",
    )

    control_voltage_v = _require_positive(
        installation_data,
        "control_voltage_v",
    )

    control_current_type = _require_choice(
        installation_data,
        "control_current_type",
        (
            "AC",
            "DC",
        ),
    )

    system_frequency_hz = _require_positive(
        installation_data,
        "system_frequency_hz",
    )

    # -------------------------------------------------------------------------
    # CABLE DATA
    # -------------------------------------------------------------------------

    cable_length_m = _require_positive(
        installation_data,
        "cable_length_m",
    )

    conductor_material = _require_choice(
        installation_data,
        "conductor_material",
        CONDUCTOR_MATERIAL_DESCRIPTIONS,
    )

    insulation = _require_choice(
        installation_data,
        "insulation",
        INSULATION_DESCRIPTIONS,
    )

    installation_method = _require_choice(
        installation_data,
        "installation_method",
        INSTALLATION_METHOD_DESCRIPTIONS,
    )

    installation_environment = _require_choice(
        installation_data,
        "installation_environment",
        INSTALLATION_ENVIRONMENT_DESCRIPTIONS,
    )

    loaded_conductors = _require_integer_positive(
        installation_data,
        "loaded_conductors",
    )

    ambient_temperature_c = _require_positive(
        installation_data,
        "ambient_temperature_c",
    )

    grouped_circuits = _require_integer_positive(
        installation_data,
        "grouped_circuits",
    )

    # -------------------------------------------------------------------------
    # CURRENT DEE VERSION LIMITATIONS
    # -------------------------------------------------------------------------

    if conductor_material != "CU":
        raise InstallationDataError(
            "Current DEE cable sizing version supports only "
            "copper conductors (CU)."
        )

    if insulation != "PVC":
        raise InstallationDataError(
            "Current DEE cable sizing version supports only "
            "PVC insulation, 70 deg C."
        )

    if installation_method != "C":
        raise InstallationDataError(
            "Current DEE cable sizing version supports only "
            "installation method C."
        )

    if installation_environment != "AIR":
        raise InstallationDataError(
            "Current DEE cable sizing version supports only "
            "cables installed in air."
        )

    if loaded_conductors != 3:
        raise InstallationDataError(
            "Current DEE cable sizing version supports only "
            "three loaded conductors."
        )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "system_voltage_v": system_voltage_v,
        "system_frequency_hz": system_frequency_hz,
        "control_voltage_v": control_voltage_v,
        "control_current_type": control_current_type,
        "cable_length_m": cable_length_m,

        "conductor_material": conductor_material,
        "conductor_material_description":
            CONDUCTOR_MATERIAL_DESCRIPTIONS[conductor_material],

        "insulation": insulation,
        "insulation_description":
            INSULATION_DESCRIPTIONS[insulation],

        "installation_method": installation_method,
        "installation_method_description":
            INSTALLATION_METHOD_DESCRIPTIONS[installation_method],

        "installation_environment": installation_environment,
        "installation_environment_description":
            INSTALLATION_ENVIRONMENT_DESCRIPTIONS[
                installation_environment
            ],

        "loaded_conductors": loaded_conductors,
        "ambient_temperature_c": ambient_temperature_c,
        "grouped_circuits": grouped_circuits,

        "installation_data_source":
            "USER / PROJECT DATA",

        "installation_data_status":
            "VALID",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_installation_data = {
        "system_voltage_v": 400,
        "system_frequency_hz": 50,

        "cable_length_m": 45.0,

        "conductor_material": "CU",
        "insulation": "PVC",

        "installation_method": "C",
        "installation_environment": "AIR",

        "loaded_conductors": 3,

        "ambient_temperature_c": 40.0,
        "grouped_circuits": 1,
    }

    result = validate_installation_data(
        test_installation_data,
    )

    print("=" * 76)
    print("DEE - MOTOR FEEDER INSTALLATION DATA")
    print("=" * 76)

    print()

    print(
        f"System voltage Un             = "
        f"{result['system_voltage_v']:.0f} V "
        f"(three-phase system line voltage)"
    )

    print(
        f"System frequency fn           = "
        f"{result['system_frequency_hz']:.1f} Hz "
        f"(electrical system frequency)"
    )

    print()

    print(
        f"Cable length L                = "
        f"{result['cable_length_m']:.1f} m "
        f"(one-way motor feeder cable length)"
    )

    print(
        f"Conductor material            = "
        f"{result['conductor_material']} "
        f"({result['conductor_material_description']})"
    )

    print(
        f"Cable insulation              = "
        f"{result['insulation']} "
        f"({result['insulation_description']})"
    )

    print()

    print(
        f"Installation method           = "
        f"{result['installation_method']} "
        f"({result['installation_method_description']})"
    )

    print(
        f"Installation environment      = "
        f"{result['installation_environment']} "
        f"({result['installation_environment_description']})"
    )

    print(
        f"Loaded conductors             = "
        f"{result['loaded_conductors']} "
        f"(current-carrying conductors)"
    )

    print()

    print(
        f"Ambient temperature           = "
        f"{result['ambient_temperature_c']:.1f} deg C "
        f"(ambient air temperature)"
    )

    print(
        f"Grouped circuits              = "
        f"{result['grouped_circuits']} "
        f"(number of grouped circuits)"
    )

    print()

    print(
        f"Installation data source      = "
        f"{result['installation_data_source']} "
        f"(installation conditions data source)"
    )

    print(
        f"Installation data check       = "
        f"{result['installation_data_status']} "
        f"(input data validation status)"
    )

    print("=" * 76)