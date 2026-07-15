"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
SUPPLY SYSTEM DATA

This module stores and validates the electrical supply source data
required for short-circuit current calculation.

Current supported supply source:

    TRANSFORMER

Current calculation model:

    one MV/LV distribution transformer
    feeding a low-voltage three-phase system.

Required transformer data:

    Sn  - transformer rated apparent power, kVA;
    U2  - transformer secondary line voltage, V;
    uk  - transformer short-circuit impedance voltage, %.

The transformer rated secondary current is:

    InT = Sn / (sqrt(3) * U2)

The simplified three-phase short-circuit current
at the transformer secondary terminals is:

    IscT = InT * 100 / uk

Methodological basis:
- Schneider Electric Electrical Installation Guide;
- IEC low-voltage short-circuit calculation methodology.
"""


# =============================================================================
# SUPPLY DATA ERROR
# =============================================================================

class SupplyDataError(ValueError):
    """
    Error raised when supply system data are invalid.
    """

    pass


# =============================================================================
# SUPPLY SOURCE DESCRIPTIONS
# =============================================================================

SUPPLY_SOURCE_DESCRIPTIONS = {
    "TRANSFORMER":
        "Single MV/LV distribution transformer",
}


# =============================================================================
# AUXILIARY FUNCTIONS
# =============================================================================

def _require_value(
    data,
    key,
):
    """
    Check that a required parameter exists and is not None.
    """

    if key not in data:
        raise SupplyDataError(
            f"Required supply parameter '{key}' is missing."
        )

    if data[key] is None:
        raise SupplyDataError(
            f"Required supply parameter '{key}' is None."
        )

    return data[key]


def _require_positive(
    data,
    key,
):
    """
    Check that a numerical parameter is greater than zero.
    """

    value = _require_value(
        data,
        key,
    )

    if not isinstance(
        value,
        (int, float),
    ):
        raise SupplyDataError(
            f"Supply parameter '{key}' must be numerical."
        )

    value = float(
        value
    )

    if value <= 0:
        raise SupplyDataError(
            f"Supply parameter '{key}' must be greater than zero."
        )

    return value


def _require_choice(
    data,
    key,
    choices,
):
    """
    Check that a text parameter belongs to permissible choices.
    """

    value = _require_value(
        data,
        key,
    )

    if not isinstance(
        value,
        str,
    ):
        raise SupplyDataError(
            f"Supply parameter '{key}' must be text."
        )

    value = value.strip().upper()

    if value not in choices:
        raise SupplyDataError(
            f"Unsupported value '{value}' for supply "
            f"parameter '{key}'. "
            f"Permissible values: {', '.join(choices)}."
        )

    return value


# =============================================================================
# SUPPLY DATA VALIDATION
# =============================================================================

def validate_supply_data(
    supply_data,
):
    """
    Validate electrical supply system data.

    Parameters
    ----------
    supply_data : dict
        Supply source and transformer data.

    Returns
    -------
    dict
        Validated and normalized supply system data.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(
        supply_data,
        dict,
    ):
        raise SupplyDataError(
            "Supply data must be provided as a dictionary."
        )

    # -------------------------------------------------------------------------
    # SUPPLY SOURCE
    # -------------------------------------------------------------------------

    supply_source = _require_choice(
        supply_data,
        "supply_source",
        SUPPLY_SOURCE_DESCRIPTIONS,
    )

    # -------------------------------------------------------------------------
    # CURRENT DEE VERSION LIMITATION
    # -------------------------------------------------------------------------

    if supply_source != "TRANSFORMER":
        raise SupplyDataError(
            "Current DEE short-circuit calculation version "
            "supports only a transformer supply source."
        )

    # -------------------------------------------------------------------------
    # TRANSFORMER DATA
    # -------------------------------------------------------------------------

    transformer_rated_power_kva = _require_positive(
        supply_data,
        "transformer_rated_power_kva",
    )

    transformer_secondary_voltage_v = _require_positive(
        supply_data,
        "transformer_secondary_voltage_v",
    )

    transformer_impedance_percent = _require_positive(
        supply_data,
        "transformer_impedance_percent",
    )
    
    transformer_load_losses_w = _require_positive(
        supply_data,
        "transformer_load_losses_w",
    )
    # -------------------------------------------------------------------------
    # ENGINEERING CHECKS
    # -------------------------------------------------------------------------

    if transformer_impedance_percent >= 100.0:
        raise SupplyDataError(
            "Transformer short-circuit impedance voltage "
            "must be lower than 100 percent."
        )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "supply_source":
            supply_source,

        "supply_source_description":
            SUPPLY_SOURCE_DESCRIPTIONS[
                supply_source
            ],

        "transformer_rated_power_kva":
            transformer_rated_power_kva,

        "transformer_secondary_voltage_v":
            transformer_secondary_voltage_v,

        "transformer_impedance_percent":
            transformer_impedance_percent,

        "transformer_load_losses_w":
            transformer_load_losses_w,

        "supply_data_source":
            "USER / PROJECT DATA",

        "supply_data_status":
            "VALID",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_supply_data = {
        "supply_source": "TRANSFORMER",

        "transformer_rated_power_kva": 630.0,
        "transformer_secondary_voltage_v": 400.0,
        "transformer_impedance_percent": 6.0,
         "transformer_load_losses_w": 7100.0,
    }

    result = validate_supply_data(
        test_supply_data,
    )

    print("=" * 76)
    print("DEE - SUPPLY SYSTEM DATA")
    print("=" * 76)

    print()

    print(
        f"Supply source                 = "
        f"{result['supply_source']} "
        f"({result['supply_source_description']})"
    )

    print()

    print(
        f"Transformer rated power Sn    = "
        f"{result['transformer_rated_power_kva']:.1f} kVA "
        f"(transformer rated apparent power)"
    )

    print(
        f"Transformer secondary voltage = "
        f"{result['transformer_secondary_voltage_v']:.0f} V "
        f"(transformer secondary line voltage)"
    )

    print(
        f"Transformer impedance uk      = "
        f"{result['transformer_impedance_percent']:.2f} % "
        f"(transformer short-circuit impedance voltage)"
    )

    print(
        f"Transformer load losses PkrT  = "
        f"{result['transformer_load_losses_w']:.0f} W "
        f"(transformer total load losses)"
    )
    print()

    print(
        f"Supply data source            = "
        f"{result['supply_data_source']} "
        f"(electrical supply data source)"
    )

    print(
        f"Supply data check             = "
        f"{result['supply_data_status']} "
        f"(input data validation status)"
    )

    print("=" * 76)