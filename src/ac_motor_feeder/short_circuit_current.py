"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
THREE-PHASE SHORT-CIRCUIT CURRENT

This module calculates the estimated three-phase short-circuit
current at the motor feeder end.

Methodological basis:
- Schneider Electric Electrical Installation Guide;
- IEC low-voltage short-circuit calculation methodology.

The electrical network is divided into series components.

For each component:

    Z^2 = R^2 + X^2

Transformer impedance:

    Ztr = (U2^2 / Sn) * (uk / 100)

Transformer winding resistance from total load losses:

    Rtr = PkrT / (3 * InT^2)

Transformer reactance:

    Xtr = sqrt(Ztr^2 - Rtr^2)

Cable resistance and reactance:

    Rc = R * L

    Xc = X * L

Total resistance and reactance:

    Rtotal = Rtr + Rc

    Xtotal = Xtr + Xc

Total impedance:

    Ztotal = sqrt(Rtotal^2 + Xtotal^2)

Three-phase short-circuit current:

    Ik3 = U2 / (sqrt(3) * Ztotal)
"""


# =============================================================================
# IMPORTS
# =============================================================================

from math import sqrt


# =============================================================================
# SHORT-CIRCUIT CALCULATION ERROR
# =============================================================================

class ShortCircuitCurrentError(ValueError):
    """
    Error raised when short-circuit current
    cannot be calculated.
    """

    pass


# =============================================================================
# SHORT-CIRCUIT CURRENT CALCULATION
# =============================================================================

def calculate_short_circuit_current(
    supply,
    voltage_drop,
):
    """
    Calculate three-phase short-circuit current
    at the motor feeder end.

    Parameters
    ----------
    supply : dict
        Validated electrical supply system data.

    voltage_drop : dict
        Cable electrical data and feeder length.

    Returns
    -------
    dict
        Three-phase short-circuit calculation results.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(
        supply,
        dict,
    ):
        raise ShortCircuitCurrentError(
            "Supply data must be provided as a dictionary."
        )

    if not isinstance(
        voltage_drop,
        dict,
    ):
        raise ShortCircuitCurrentError(
            "Voltage-drop data must be provided as a dictionary."
        )

    required_supply_parameters = (
        "supply_source",
        "transformer_rated_power_kva",
        "transformer_secondary_voltage_v",
        "transformer_impedance_percent",
        "transformer_load_losses_w",
    )

    required_cable_parameters = (
        "cable_length_m",
        "cable_length_km",
        "cross_section_mm2",
        "resistance_ohm_km",
        "reactance_ohm_km",
    )

    for parameter in required_supply_parameters:
        if parameter not in supply:
            raise ShortCircuitCurrentError(
                f"Required supply parameter "
                f"'{parameter}' is missing."
            )

    for parameter in required_cable_parameters:
        if parameter not in voltage_drop:
            raise ShortCircuitCurrentError(
                f"Required cable parameter "
                f"'{parameter}' is missing."
            )

    # -------------------------------------------------------------------------
    # INPUT VALUES
    # -------------------------------------------------------------------------

    supply_source = str(
        supply["supply_source"]
    ).strip().upper()

    transformer_rated_power_kva = float(
        supply["transformer_rated_power_kva"]
    )

    transformer_secondary_voltage_v = float(
        supply["transformer_secondary_voltage_v"]
    )

    transformer_impedance_percent = float(
        supply["transformer_impedance_percent"]
    )

    transformer_load_losses_w = float(
        supply["transformer_load_losses_w"]
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

    # -------------------------------------------------------------------------
    # SUPPLY SOURCE CHECK
    # -------------------------------------------------------------------------

    if supply_source != "TRANSFORMER":
        raise ShortCircuitCurrentError(
            f"Supply source '{supply_source}' is not supported. "
            f"Current supported supply source: TRANSFORMER."
        )

    # -------------------------------------------------------------------------
    # NUMERICAL DATA CHECK
    # -------------------------------------------------------------------------

    positive_values = {
        "transformer_rated_power_kva":
            transformer_rated_power_kva,

        "transformer_secondary_voltage_v":
            transformer_secondary_voltage_v,

        "transformer_impedance_percent":
            transformer_impedance_percent,

        "transformer_load_losses_w":
            transformer_load_losses_w,

        "cable_length_km":
            cable_length_km,
    }

    for parameter, value in positive_values.items():
        if value <= 0:
            raise ShortCircuitCurrentError(
                f"Parameter '{parameter}' must be greater than zero."
            )

    if resistance_ohm_km < 0:
        raise ShortCircuitCurrentError(
            "Cable resistance cannot be negative."
        )

    if reactance_ohm_km < 0:
        raise ShortCircuitCurrentError(
            "Cable reactance cannot be negative."
        )

    # -------------------------------------------------------------------------
    # TRANSFORMER RATED VALUES
    # -------------------------------------------------------------------------

    transformer_rated_power_va = (
        transformer_rated_power_kva
        * 1000.0
    )

    transformer_rated_current_a = (
        transformer_rated_power_va
        / (
            sqrt(3.0)
            * transformer_secondary_voltage_v
        )
    )

    # -------------------------------------------------------------------------
    # TRANSFORMER IMPEDANCE
    # -------------------------------------------------------------------------

    transformer_impedance_ohm = (
        transformer_secondary_voltage_v ** 2
        / transformer_rated_power_va
        * (
            transformer_impedance_percent
            / 100.0
        )
    )

    # -------------------------------------------------------------------------
    # TRANSFORMER RESISTANCE
    # -------------------------------------------------------------------------

    transformer_resistance_ohm = (
        transformer_load_losses_w
        / (
            3.0
            * transformer_rated_current_a ** 2
        )
    )

    # -------------------------------------------------------------------------
    # TRANSFORMER REACTANCE
    # -------------------------------------------------------------------------

    transformer_reactance_square = (
        transformer_impedance_ohm ** 2
        - transformer_resistance_ohm ** 2
    )

    if transformer_reactance_square < 0:
        raise ShortCircuitCurrentError(
            "Transformer resistance is greater than transformer "
            "impedance. Check transformer uk and load-loss data."
        )

    transformer_reactance_ohm = sqrt(
        transformer_reactance_square
    )

    # -------------------------------------------------------------------------
    # TRANSFORMER TERMINAL SHORT-CIRCUIT CURRENT
    # -------------------------------------------------------------------------

    transformer_short_circuit_current_a = (
        transformer_secondary_voltage_v
        / (
            sqrt(3.0)
            * transformer_impedance_ohm
        )
    )

    transformer_short_circuit_current_ka = (
        transformer_short_circuit_current_a
        / 1000.0
    )

    # -------------------------------------------------------------------------
    # CABLE IMPEDANCE COMPONENTS
    # -------------------------------------------------------------------------

    cable_resistance_ohm = (
        resistance_ohm_km
        * cable_length_km
    )

    cable_reactance_ohm = (
        reactance_ohm_km
        * cable_length_km
    )

    cable_impedance_ohm = sqrt(
        cable_resistance_ohm ** 2
        + cable_reactance_ohm ** 2
    )

    # -------------------------------------------------------------------------
    # TOTAL RESISTANCE AND REACTANCE
    # -------------------------------------------------------------------------

    total_resistance_ohm = (
        transformer_resistance_ohm
        + cable_resistance_ohm
    )

    total_reactance_ohm = (
        transformer_reactance_ohm
        + cable_reactance_ohm
    )

    total_impedance_ohm = sqrt(
        total_resistance_ohm ** 2
        + total_reactance_ohm ** 2
    )

    if total_impedance_ohm <= 0:
        raise ShortCircuitCurrentError(
            "Total short-circuit impedance must be greater than zero."
        )

    # -------------------------------------------------------------------------
    # THREE-PHASE SHORT-CIRCUIT CURRENT AT FEEDER END
    # -------------------------------------------------------------------------

    feeder_end_short_circuit_current_a = (
        transformer_secondary_voltage_v
        / (
            sqrt(3.0)
            * total_impedance_ohm
        )
    )

    feeder_end_short_circuit_current_ka = (
        feeder_end_short_circuit_current_a
        / 1000.0
    )

    # -------------------------------------------------------------------------
    # SHORT-CIRCUIT CURRENT REDUCTION
    # -------------------------------------------------------------------------

    short_circuit_current_reduction_percent = (
        (
            transformer_short_circuit_current_a
            - feeder_end_short_circuit_current_a
        )
        / transformer_short_circuit_current_a
        * 100.0
    )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "supply_source":
            supply_source,

        "transformer_rated_power_kva":
            transformer_rated_power_kva,

        "transformer_secondary_voltage_v":
            transformer_secondary_voltage_v,

        "transformer_impedance_percent":
            transformer_impedance_percent,

        "transformer_load_losses_w":
            transformer_load_losses_w,

        "transformer_rated_current_a":
            transformer_rated_current_a,

        "transformer_impedance_ohm":
            transformer_impedance_ohm,

        "transformer_resistance_ohm":
            transformer_resistance_ohm,

        "transformer_reactance_ohm":
            transformer_reactance_ohm,

        "transformer_short_circuit_current_a":
            transformer_short_circuit_current_a,

        "transformer_short_circuit_current_ka":
            transformer_short_circuit_current_ka,

        "cable_length_m":
            cable_length_m,

        "cross_section_mm2":
            cross_section_mm2,

        "cable_resistance_ohm":
            cable_resistance_ohm,

        "cable_reactance_ohm":
            cable_reactance_ohm,

        "cable_impedance_ohm":
            cable_impedance_ohm,

        "total_resistance_ohm":
            total_resistance_ohm,

        "total_reactance_ohm":
            total_reactance_ohm,

        "total_impedance_ohm":
            total_impedance_ohm,

        "feeder_end_short_circuit_current_a":
            feeder_end_short_circuit_current_a,

        "feeder_end_short_circuit_current_ka":
            feeder_end_short_circuit_current_ka,

        "short_circuit_current_reduction_percent":
            short_circuit_current_reduction_percent,

        "short_circuit_calculation_model":
            "SEPARATE R/X SERIES IMPEDANCE SUMMATION",

        "short_circuit_source":
            "SCHNEIDER ELECTRIC EIG / IEC METHODOLOGY",

        "short_circuit_status":
            "CALCULATED",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_supply = {
        "supply_source": "TRANSFORMER",
        "transformer_rated_power_kva": 630.0,
        "transformer_secondary_voltage_v": 400.0,
        "transformer_impedance_percent": 6.0,
        "transformer_load_losses_w": 7100.0,
    }

    test_voltage_drop = {
        "cable_length_m": 45.0,
        "cable_length_km": 0.045,
        "cross_section_mm2": 6.0,
        "resistance_ohm_km": 3.69,
        "reactance_ohm_km": 0.08,
    }

    result = calculate_short_circuit_current(
        supply=test_supply,
        voltage_drop=test_voltage_drop,
    )

    print("=" * 76)
    print("DEE - THREE-PHASE SHORT-CIRCUIT CURRENT")
    print("=" * 76)

    print()

    print(
        f"Supply source                 = "
        f"{result['supply_source']} "
        f"(electrical supply source)"
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
        f"Transformer rated current InT = "
        f"{result['transformer_rated_current_a']:.2f} A "
        f"(transformer rated secondary current)"
    )

    print()

    print(
        f"Transformer impedance Ztr     = "
        f"{result['transformer_impedance_ohm']:.6f} ohm "
        f"(transformer equivalent impedance)"
    )

    print(
        f"Transformer resistance Rtr    = "
        f"{result['transformer_resistance_ohm']:.6f} ohm "
        f"(transformer winding resistance)"
    )

    print(
        f"Transformer reactance Xtr     = "
        f"{result['transformer_reactance_ohm']:.6f} ohm "
        f"(transformer leakage reactance)"
    )

    print()

    print(
        f"Transformer terminal Isc      = "
        f"{result['transformer_short_circuit_current_ka']:.2f} kA "
        f"(three-phase short-circuit current at transformer terminals)"
    )

    print()

    print(
        f"Cable length L                = "
        f"{result['cable_length_m']:.1f} m "
        f"(one-way feeder cable length)"
    )

    print(
        f"Conductor section S           = "
        f"{result['cross_section_mm2']:.1f} mm2 "
        f"(selected phase conductor cross-section)"
    )

    print()

    print(
        f"Cable resistance Rc           = "
        f"{result['cable_resistance_ohm']:.6f} ohm "
        f"(feeder cable resistance)"
    )

    print(
        f"Cable reactance Xc            = "
        f"{result['cable_reactance_ohm']:.6f} ohm "
        f"(feeder cable reactance)"
    )

    print(
        f"Cable impedance Zc            = "
        f"{result['cable_impedance_ohm']:.6f} ohm "
        f"(feeder cable impedance)"
    )

    print()

    print(
        f"Total resistance Rtotal       = "
        f"{result['total_resistance_ohm']:.6f} ohm "
        f"(total series resistance to fault point)"
    )

    print(
        f"Total reactance Xtotal        = "
        f"{result['total_reactance_ohm']:.6f} ohm "
        f"(total series reactance to fault point)"
    )

    print(
        f"Total impedance Ztotal        = "
        f"{result['total_impedance_ohm']:.6f} ohm "
        f"(total impedance to fault point)"
    )

    print()

    print(
        f"Feeder-end short-circuit Ik3  = "
        f"{result['feeder_end_short_circuit_current_ka']:.2f} kA "
        f"(estimated three-phase short-circuit current at motor feeder end)"
    )

    print(
        f"Short-circuit current reduction = "
        f"{result['short_circuit_current_reduction_percent']:.2f} % "
        f"(fault-current reduction due to feeder impedance)"
    )

    print()

    print(
        f"Calculation model             = "
        f"{result['short_circuit_calculation_model']} "
        f"(short-circuit calculation model)"
    )

    print(
        f"Short-circuit source          = "
        f"{result['short_circuit_source']} "
        f"(calculation methodology source)"
    )

    print(
        f"Short-circuit status          = "
        f"{result['short_circuit_status']} "
        f"(short-circuit calculation status)"
    )

    print("=" * 76)