"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
SCHNEIDER ELECTRIC MOTOR STARTER COORDINATION OPTIMIZER

This module searches for a permissible Schneider Electric
Type 2 coordinated motor starter combination.

Current application:

    three-phase asynchronous motor;
    Direct-On-Line starting;
    Schneider Electric TeSys equipment;
    IEC Type 2 coordination.

The optimizer is used when the independently selected
motor circuit breaker and contactor combination is not found
in the digitized Schneider Electric coordination table.

IMPORTANT:

The optimizer does not infer or calculate a manufacturer
coordination combination.

Only combinations explicitly stored in the digitized
Schneider Electric coordination table may be selected.
"""


# =============================================================================
# IMPORTS
# =============================================================================

try:
    from src.ac_motor_feeder.schneider_data.motor_starter_coordination_data import (
        SCHNEIDER_COORDINATION_DATA_SOURCE,
        SCHNEIDER_MOTOR_STARTER_COORDINATION_DATA,
    )

except ModuleNotFoundError:
    from schneider_data.motor_starter_coordination_data import (
        SCHNEIDER_COORDINATION_DATA_SOURCE,
        SCHNEIDER_MOTOR_STARTER_COORDINATION_DATA,
    )


# =============================================================================
# COORDINATION OPTIMIZER ERROR
# =============================================================================

class MotorStarterCoordinationOptimizerError(ValueError):
    """
    Error raised when coordinated motor starter optimization fails.
    """

    pass


# =============================================================================
# COORDINATED MOTOR STARTER SEARCH
# =============================================================================

def optimize_motor_starter_coordination(
    motor,
    motor_circuit_breaker,
    contactor,
    short_circuit,
    installation,
):
    """
    Search for a permissible Schneider Electric
    Type 2 coordinated motor starter combination.

    Parameters
    ----------
    motor : dict
        Validated motor data.

    motor_circuit_breaker : dict
        Initially selected motor circuit breaker data.

    contactor : dict
        Initially selected contactor data.

    short_circuit : dict
        Short-circuit calculation results.

    installation : dict
        Validated installation data.

    Returns
    -------
    dict
        Coordination optimization results.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    input_data = {
        "motor":
            motor,

        "motor_circuit_breaker":
            motor_circuit_breaker,

        "contactor":
            contactor,

        "short_circuit":
            short_circuit,

        "installation":
            installation,
    }

    for data_name, data in input_data.items():

        if not isinstance(
            data,
            dict,
        ):

            raise MotorStarterCoordinationOptimizerError(
                f"{data_name} data must be provided "
                f"as a dictionary."
            )

    # -------------------------------------------------------------------------
    # REQUIRED PARAMETERS
    # -------------------------------------------------------------------------

    required_parameters = {
        "motor": (
            "rated_power_kw",
            "starting_method",
        ),

        "motor_circuit_breaker": (
            "reference",
        ),

        "contactor": (
            "base_reference",
            "reference",
            "coil_suffix",
            "coil_description",
        ),

        "short_circuit": (
            "feeder_end_short_circuit_current_ka",
        ),

        "installation": (
            "system_voltage_v",
        ),
    }

    for data_name, parameters in required_parameters.items():

        data = input_data[
            data_name
        ]

        for parameter in parameters:

            if parameter not in data:

                raise MotorStarterCoordinationOptimizerError(
                    f"Required parameter '{parameter}' "
                    f"is missing in {data_name} data."
                )

    # -------------------------------------------------------------------------
    # INPUT VALUES
    # -------------------------------------------------------------------------

    motor_power_kw = float(
        motor["rated_power_kw"]
    )

    starting_method = str(
        motor["starting_method"]
    ).strip().upper()

    initial_breaker_reference = str(
        motor_circuit_breaker["reference"]
    ).strip().upper()

    initial_contactor_base_reference = str(
        contactor["base_reference"]
    ).strip().upper()

    initial_contactor_reference = str(
        contactor["reference"]
    ).strip().upper()

    coil_suffix = str(
        contactor["coil_suffix"]
    ).strip().upper()

    coil_description = str(
        contactor["coil_description"]
    ).strip()

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

    if motor_power_kw <= 0:

        raise MotorStarterCoordinationOptimizerError(
            "Motor rated power must be greater than zero."
        )

    if short_circuit_current_ka <= 0:

        raise MotorStarterCoordinationOptimizerError(
            "Short-circuit current must be greater than zero."
        )

    if system_voltage_v <= 0:

        raise MotorStarterCoordinationOptimizerError(
            "System voltage must be greater than zero."
        )

    # -------------------------------------------------------------------------
    # SEARCH ALL APPLICABLE TABLE RECORDS
    # -------------------------------------------------------------------------

    applicable_records = []

    for record in SCHNEIDER_MOTOR_STARTER_COORDINATION_DATA:

        power_match = (
            record["motor_power_kw"]
            == motor_power_kw
        )

        voltage_match = (
            record["system_voltage_min_v"]
            <= system_voltage_v
            <= record["system_voltage_max_v"]
        )

        starting_method_match = (
            record["starting_method"]
            == starting_method
        )

        verified_record_check = (
            str(
                record["table_record_status"]
            ).strip().upper()
            == "VERIFIED"
        )

        coordination_level = (
            record[
                "coordination_short_circuit_ka"
            ]
        )

        coordination_level_available = (
            coordination_level is not None
        )

        if (
            power_match
            and voltage_match
            and starting_method_match
            and verified_record_check
            and coordination_level_available
        ):

            coordination_level = float(
                coordination_level
            )

            short_circuit_check = (
                short_circuit_current_ka
                <= coordination_level
            )

            if short_circuit_check:

                applicable_records.append(
                    record
                )

    # -------------------------------------------------------------------------
    # NO COORDINATED COMBINATION FOUND
    # -------------------------------------------------------------------------

    if not applicable_records:

        return {
            "motor_power_kw":
                motor_power_kw,

            "starting_method":
                starting_method,

            "system_voltage_v":
                system_voltage_v,

            "short_circuit_current_ka":
                short_circuit_current_ka,

            "initial_breaker_reference":
                initial_breaker_reference,

            "initial_contactor_base_reference":
                initial_contactor_base_reference,

            "initial_contactor_reference":
                initial_contactor_reference,

            "selected_breaker_reference":
                None,

            "selected_contactor_base_reference":
                None,

            "selected_contactor_reference":
                None,

            "coordination_type":
                None,

            "coordination_short_circuit_ka":
                None,

            "coordination_condition":
                "NOT CHECKED",

            "combination_changed":
                "NOT APPLICABLE",

            "optimization_source":
                SCHNEIDER_COORDINATION_DATA_SOURCE[
                    "document_title"
                ],

            "optimization_status":
                "NO COORDINATED COMBINATION FOUND",
        }

    # -------------------------------------------------------------------------
    # SELECT COORDINATED COMBINATION
    #
    # Current selection principle:
    #
    # 1. exact motor power;
    # 2. applicable voltage group;
    # 3. applicable starting method;
    # 4. verified table record;
    # 5. Iq >= Ik3;
    # 6. lowest sufficient coordination short-circuit level.
    #
    # The final equipment references remain manufacturer table references.
    # -------------------------------------------------------------------------

    selected_record = min(
        applicable_records,
        key=lambda record: (
            float(
                record[
                    "coordination_short_circuit_ka"
                ]
            ),
            record[
                "motor_circuit_breaker_reference"
            ],
            record[
                "contactor_base_reference"
            ],
        ),
    )

    # -------------------------------------------------------------------------
    # SELECTED REFERENCES
    # -------------------------------------------------------------------------

    selected_breaker_reference = str(
        selected_record[
            "motor_circuit_breaker_reference"
        ]
    ).strip().upper()

    selected_contactor_base_reference = str(
        selected_record[
            "contactor_base_reference"
        ]
    ).strip().upper()

    selected_contactor_reference = (
        selected_contactor_base_reference
        + coil_suffix
    )

    coordination_short_circuit_ka = float(
        selected_record[
            "coordination_short_circuit_ka"
        ]
    )

    # -------------------------------------------------------------------------
    # COMBINATION CHANGE CHECK
    # -------------------------------------------------------------------------

    breaker_changed = (
        selected_breaker_reference
        != initial_breaker_reference
    )

    contactor_changed = (
        selected_contactor_base_reference
        != initial_contactor_base_reference
    )

    if (
        breaker_changed
        or contactor_changed
    ):

        combination_changed = (
            "YES"
        )

    else:

        combination_changed = (
            "NO"
        )

    # -------------------------------------------------------------------------
    # COORDINATION CONDITION
    # -------------------------------------------------------------------------

    coordination_condition = (
        "PERMISSIBLE"
        if short_circuit_current_ka
        <= coordination_short_circuit_ka
        else "NOT PERMISSIBLE"
    )

    # -------------------------------------------------------------------------
    # OPTIMIZATION STATUS
    # -------------------------------------------------------------------------

    optimization_status = (
        "COORDINATED COMBINATION SELECTED"
        if coordination_condition
        == "PERMISSIBLE"
        else "NO COORDINATED COMBINATION FOUND"
    )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        **selected_record,

        "motor_power_kw":
            motor_power_kw,

        "starting_method":
            starting_method,

        "system_voltage_v":
            system_voltage_v,

        "short_circuit_current_ka":
            short_circuit_current_ka,

        "initial_breaker_reference":
            initial_breaker_reference,

        "initial_contactor_base_reference":
            initial_contactor_base_reference,

        "initial_contactor_reference":
            initial_contactor_reference,

        "selected_breaker_reference":
            selected_breaker_reference,

        "selected_contactor_base_reference":
            selected_contactor_base_reference,

        "selected_contactor_reference":
            selected_contactor_reference,

        "coil_suffix":
            coil_suffix,

        "coil_description":
            coil_description,

        "coordination_condition":
            coordination_condition,

        "breaker_changed":
            breaker_changed,

        "contactor_changed":
            contactor_changed,

        "combination_changed":
            combination_changed,

        "optimization_source":
            SCHNEIDER_COORDINATION_DATA_SOURCE[
                "document_title"
            ],

        "optimization_status":
            optimization_status,
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_motor = {
        "rated_power_kw": 15.0,
        "starting_method": "DOL",
    }

    test_motor_circuit_breaker = {
        "reference": "GV2ME32",
    }

    test_contactor = {
        "base_reference": "LC1D32",
        "reference": "LC1D32M7",
        "coil_suffix": "M7",
        "coil_description": "220 V AC 50/60 Hz",
    }

    test_short_circuit = {
        "feeder_end_short_circuit_current_ka": 1.36,
    }

    test_installation = {
        "system_voltage_v": 400.0,
    }

    result = optimize_motor_starter_coordination(
        motor=test_motor,
        motor_circuit_breaker=test_motor_circuit_breaker,
        contactor=test_contactor,
        short_circuit=test_short_circuit,
        installation=test_installation,
    )

    print("=" * 76)
    print("DEE - MOTOR STARTER COORDINATION OPTIMIZER")
    print("=" * 76)

    print()

    print(
        f"Motor rated power Pn          = "
        f"{result['motor_power_kw']:.2f} kW "
        f"(motor rated output power)"
    )

    print(
        f"Starting method               = "
        f"{result['starting_method']} "
        f"(motor starting method)"
    )

    print(
        f"System voltage Un             = "
        f"{result['system_voltage_v']:.0f} V "
        f"(motor feeder system voltage)"
    )

    print(
        f"Calculated short-circuit Ik3  = "
        f"{result['short_circuit_current_ka']:.2f} kA "
        f"(prospective fault current at installation point)"
    )

    print()

    print(
        f"Initial circuit breaker       = "
        f"{result['initial_breaker_reference']} "
        f"(independently selected motor circuit breaker)"
    )

    print(
        f"Initial contactor             = "
        f"{result['initial_contactor_reference']} "
        f"(independently selected contactor)"
    )

    print()

    selected_breaker_reference = result[
        "selected_breaker_reference"
    ]

    selected_contactor_reference = result[
        "selected_contactor_reference"
    ]

    if selected_breaker_reference is None:

        print(
            "Selected circuit breaker      = "
            "NOT AVAILABLE "
            "(no coordinated table combination found)"
        )

    else:

        print(
            f"Selected circuit breaker      = "
            f"{selected_breaker_reference} "
            f"(Type 2 coordinated motor protection device)"
        )

    if selected_contactor_reference is None:

        print(
            "Selected contactor            = "
            "NOT AVAILABLE "
            "(no coordinated table combination found)"
        )

    else:

        print(
            f"Selected contactor            = "
            f"{selected_contactor_reference} "
            f"(Type 2 coordinated motor contactor)"
        )

    print()

    coordination_short_circuit_ka = result[
        "coordination_short_circuit_ka"
    ]

    if coordination_short_circuit_ka is None:

        print(
            "Coordination short-circuit Iq = "
            "NOT AVAILABLE "
            "(no verified coordination level found)"
        )

    else:

        print(
            f"Coordination short-circuit Iq = "
            f"{coordination_short_circuit_ka:.2f} kA "
            f"(Schneider Electric Type 2 coordination level)"
        )

    print(
        f"Coordination condition        = "
        f"{result['coordination_condition']} "
        f"(Ik3 <= Iq coordination condition)"
    )

    print()

    print(
        f"Combination changed           = "
        f"{result['combination_changed']} "
        f"(initial equipment combination correction status)"
    )

    print(
        f"Optimization source           = "
        f"{result['optimization_source']} "
        f"(Schneider Electric coordination table source)"
    )

    print(
        f"Optimization status           = "
        f"{result['optimization_status']} "
        f"(coordination optimization result)"
    )

    print("=" * 76)