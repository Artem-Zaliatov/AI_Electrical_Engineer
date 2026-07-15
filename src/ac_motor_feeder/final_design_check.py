"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
FINAL MOTOR FEEDER DESIGN CHECK

This module performs the final technical assessment
of the AC motor feeder design.

The final check combines results of:

    motor design current;
    cable current-carrying capacity selection;
    steady-state voltage drop;
    motor starting voltage drop;
    short-circuit calculation;
    motor circuit breaker selection;
    contactor selection;
    motor starter Type 2 coordination.

The module does not perform primary equipment selection.

It evaluates previously calculated and selected
motor feeder design results.
"""


# =============================================================================
# FINAL DESIGN CHECK ERROR
# =============================================================================

class FinalDesignCheckError(ValueError):
    """
    Error raised when the final motor feeder design
    cannot be checked.
    """

    pass


# =============================================================================
# FINAL MOTOR FEEDER DESIGN CHECK
# =============================================================================

def check_final_motor_feeder_design(
    design_current,
    cable,
    voltage_drop,
    starting_voltage_drop,
    short_circuit,
    motor_circuit_breaker,
    contactor,
    motor_starter_coordination,
    motor_starter_coordination_optimization=None,
):
    """
    Perform the final AC motor feeder design check.

    Parameters
    ----------
    design_current : dict
        Motor design current calculation results.

    cable : dict
        Selected cable and cable current-capacity results.

    voltage_drop : dict
        Steady-state voltage-drop calculation results.

    starting_voltage_drop : dict
        Motor starting voltage-drop calculation results.

    short_circuit : dict
        Short-circuit calculation results.

    motor_circuit_breaker : dict
        Selected motor circuit breaker results.

    contactor : dict
        Selected contactor results.

    motor_starter_coordination : dict
        Initial motor starter coordination check results.

    motor_starter_coordination_optimization : dict or None
        Automatic coordination optimization results.

    Returns
    -------
    dict
        Final motor feeder design assessment.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    required_dictionaries = {
        "design_current":
            design_current,

        "cable":
            cable,

        "voltage_drop":
            voltage_drop,

        "starting_voltage_drop":
            starting_voltage_drop,

        "short_circuit":
            short_circuit,

        "motor_circuit_breaker":
            motor_circuit_breaker,

        "contactor":
            contactor,

        "motor_starter_coordination":
            motor_starter_coordination,
    }

    for data_name, data in required_dictionaries.items():

        if not isinstance(
            data,
            dict,
        ):

            raise FinalDesignCheckError(
                f"{data_name} data must be provided "
                f"as a dictionary."
            )

    if (
        motor_starter_coordination_optimization
        is not None
        and not isinstance(
            motor_starter_coordination_optimization,
            dict,
        )
    ):

        raise FinalDesignCheckError(
            "Motor starter coordination optimization data "
            "must be provided as a dictionary or None."
        )

    # -------------------------------------------------------------------------
    # REQUIRED PARAMETERS
    #
    # IMPORTANT:
    #
    # Parameter names correspond to the actual DEE module interfaces.
    # -------------------------------------------------------------------------

    required_parameters = {
        "design_current": (
            "design_current_a",
        ),

        "cable": (
            "corrected_current_capacity_a",
            "current_capacity_check",
            "cable_selection_status",
        ),

        "voltage_drop": (
            "voltage_drop_check",
        ),

        "starting_voltage_drop": (
            "starting_voltage_drop_check",
        ),

        "short_circuit": (
            "feeder_end_short_circuit_current_ka",
        ),

        "motor_circuit_breaker": (
            "reference",
            "breaking_capacity_check",
            "selection_status",
        ),

        "contactor": (
            "reference",
            "selection_status",
        ),

        "motor_starter_coordination": (
            "coordination_status",
        ),
    }

    for data_name, parameters in required_parameters.items():

        data = required_dictionaries[
            data_name
        ]

        for parameter in parameters:

            if parameter not in data:

                raise FinalDesignCheckError(
                    f"Required parameter '{parameter}' "
                    f"is missing in {data_name} data."
                )

    # -------------------------------------------------------------------------
    # BASIC VALUES
    # -------------------------------------------------------------------------

    design_current_a = float(
        design_current[
            "design_current_a"
        ]
    )

    cable_current_capacity_a = float(
        cable[
            "corrected_current_capacity_a"
        ]
    )

    short_circuit_current_ka = float(
        short_circuit[
            "feeder_end_short_circuit_current_ka"
        ]
    )

    motor_circuit_breaker_reference = str(
        motor_circuit_breaker[
            "reference"
        ]
    ).strip().upper()

    contactor_reference = str(
        contactor[
            "reference"
        ]
    ).strip().upper()

    # -------------------------------------------------------------------------
    # NUMERICAL DATA CHECK
    # -------------------------------------------------------------------------

    if design_current_a <= 0:

        raise FinalDesignCheckError(
            "Motor design current must be greater than zero."
        )

    if cable_current_capacity_a <= 0:

        raise FinalDesignCheckError(
            "Cable corrected current capacity "
            "must be greater than zero."
        )

    if short_circuit_current_ka <= 0:

        raise FinalDesignCheckError(
            "Short-circuit current must be greater than zero."
        )

    # -------------------------------------------------------------------------
    # CABLE CURRENT-CAPACITY CHECK
    #
    # Basic current condition:
    #
    #     IB <= IZ
    #
    # IB - motor feeder design current
    # IZ - corrected cable current-carrying capacity
    # -------------------------------------------------------------------------

    cable_current_capacity_check = (
        "PERMISSIBLE"
        if design_current_a
        <= cable_current_capacity_a
        else "NOT PERMISSIBLE"
    )

    # -------------------------------------------------------------------------
    # CABLE MODULE CHECK
    # -------------------------------------------------------------------------

    cable_module_current_capacity_check = str(
        cable[
            "current_capacity_check"
        ]
    ).strip().upper()

    cable_selection_status = str(
        cable[
            "cable_selection_status"
        ]
    ).strip().upper()

    # -------------------------------------------------------------------------
    # STEADY-STATE VOLTAGE-DROP CHECK
    # -------------------------------------------------------------------------

    steady_state_voltage_drop_check = str(
        voltage_drop[
            "voltage_drop_check"
        ]
    ).strip().upper()

    # -------------------------------------------------------------------------
    # MOTOR STARTING VOLTAGE-DROP CHECK
    # -------------------------------------------------------------------------

    motor_starting_voltage_drop_check = str(
        starting_voltage_drop[
            "starting_voltage_drop_check"
        ]
    ).strip().upper()

    # -------------------------------------------------------------------------
    # MOTOR CIRCUIT BREAKER CHECK
    # -------------------------------------------------------------------------

    motor_circuit_breaker_selection_check = str(
        motor_circuit_breaker[
            "selection_status"
        ]
    ).strip().upper()

    breaking_capacity_check = str(
        motor_circuit_breaker[
            "breaking_capacity_check"
        ]
    ).strip().upper()

    # -------------------------------------------------------------------------
    # CONTACTOR CHECK
    # -------------------------------------------------------------------------

    contactor_selection_check = str(
        contactor[
            "selection_status"
        ]
    ).strip().upper()

    # -------------------------------------------------------------------------
    # MOTOR STARTER TYPE 2 COORDINATION CHECK
    #
    # Priority:
    #
    # 1. verified initial combination;
    # 2. coordinated combination selected by optimizer;
    # 3. coordination not verified.
    # -------------------------------------------------------------------------

    initial_coordination_status = str(
        motor_starter_coordination[
            "coordination_status"
        ]
    ).strip().upper()

    if initial_coordination_status == "VERIFIED":

        type_2_coordination_check = (
            "VERIFIED"
        )

        final_coordination_source = (
            "INITIAL EQUIPMENT COMBINATION"
        )

        final_breaker_reference = (
            motor_circuit_breaker_reference
        )

        final_contactor_reference = (
            contactor_reference
        )

    elif (
        motor_starter_coordination_optimization
        is not None
        and str(
            motor_starter_coordination_optimization.get(
                "optimization_status",
                "",
            )
        ).strip().upper()
        == "COORDINATED COMBINATION SELECTED"
        and str(
            motor_starter_coordination_optimization.get(
                "coordination_condition",
                "",
            )
        ).strip().upper()
        == "PERMISSIBLE"
    ):

        type_2_coordination_check = (
            "VERIFIED"
        )

        final_coordination_source = (
            "AUTOMATIC COORDINATION CORRECTION"
        )

        final_breaker_reference = str(
            motor_starter_coordination_optimization[
                "selected_breaker_reference"
            ]
        ).strip().upper()

        final_contactor_reference = str(
            motor_starter_coordination_optimization[
                "selected_contactor_reference"
            ]
        ).strip().upper()

    else:

        type_2_coordination_check = (
            "NOT VERIFIED"
        )

        final_coordination_source = (
            "NO VERIFIED COORDINATED COMBINATION"
        )

        final_breaker_reference = (
            motor_circuit_breaker_reference
        )

        final_contactor_reference = (
            contactor_reference
        )

    # -------------------------------------------------------------------------
    # INDIVIDUAL DESIGN CHECKS
    # -------------------------------------------------------------------------

    design_checks = {
        "cable_current_capacity":
            cable_current_capacity_check,

        "cable_module_current_capacity":
            cable_module_current_capacity_check,

        "cable_selection":
            cable_selection_status,

        "steady_state_voltage_drop":
            steady_state_voltage_drop_check,

        "motor_starting_voltage_drop":
            motor_starting_voltage_drop_check,

        "motor_circuit_breaker_selection":
            motor_circuit_breaker_selection_check,

        "breaking_capacity":
            breaking_capacity_check,

        "contactor_selection":
            contactor_selection_check,

        "type_2_coordination":
            type_2_coordination_check,
    }

    # -------------------------------------------------------------------------
    # PERMISSIBLE STATUS VALUES
    # -------------------------------------------------------------------------

    permissible_status_values = {
        "PERMISSIBLE",
        "SELECTED",
        "ACCEPTED",
        "VERIFIED",
    }

    # -------------------------------------------------------------------------
    # FAILED DESIGN CHECKS
    # -------------------------------------------------------------------------

    failed_design_checks = []

    for check_name, check_status in design_checks.items():

        normalized_status = str(
            check_status
        ).strip().upper()

        if (
            normalized_status
            not in permissible_status_values
        ):

            failed_design_checks.append(
                check_name
            )

    # -------------------------------------------------------------------------
    # FINAL DESIGN STATUS
    # -------------------------------------------------------------------------

    if failed_design_checks:

        final_design_status = (
            "NOT ACCEPTED"
        )

    else:

        final_design_status = (
            "ACCEPTED"
        )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "design_current_a":
            design_current_a,

        "cable_current_capacity_a":
            cable_current_capacity_a,

        "cable_ampacity_a":
            cable_current_capacity_a,

        "short_circuit_current_ka":
            short_circuit_current_ka,

        "cable_current_capacity_check":
            cable_current_capacity_check,

        "cable_module_current_capacity_check":
            cable_module_current_capacity_check,

        "cable_selection_check":
            cable_selection_status,

        "steady_state_voltage_drop_check":
            steady_state_voltage_drop_check,

        "motor_starting_voltage_drop_check":
            motor_starting_voltage_drop_check,

        "motor_circuit_breaker_selection_check":
            motor_circuit_breaker_selection_check,

        "breaking_capacity_check":
            breaking_capacity_check,

        "contactor_selection_check":
            contactor_selection_check,

        "type_2_coordination_check":
            type_2_coordination_check,

        "initial_breaker_reference":
            motor_circuit_breaker_reference,

        "initial_contactor_reference":
            contactor_reference,

        "final_breaker_reference":
            final_breaker_reference,

        "final_contactor_reference":
            final_contactor_reference,

        "final_coordination_source":
            final_coordination_source,

        "design_checks":
            design_checks,

        "failed_design_checks":
            failed_design_checks,

        "failed_design_check_count":
            len(
                failed_design_checks
            ),

        "final_design_status":
            final_design_status,

        "final_check_source":
            "DEE MOTOR FEEDER DESIGN ASSESSMENT",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_design_current = {
        "design_current_a": 28.50,
    }

    test_cable = {
        "corrected_current_capacity_a": 36.00,
        "current_capacity_check": "PERMISSIBLE",
        "cable_selection_status": "SELECTED",
    }

    test_voltage_drop = {
        "voltage_drop_check": "PERMISSIBLE",
    }

    test_starting_voltage_drop = {
        "starting_voltage_drop_check": "PERMISSIBLE",
    }

    test_short_circuit = {
        "feeder_end_short_circuit_current_ka": 1.36,
    }

    test_motor_circuit_breaker = {
        "reference": "GV2ME32",
        "breaking_capacity_check": "PERMISSIBLE",
        "selection_status": "SELECTED",
    }

    test_contactor = {
        "reference": "LC1D32M7",
        "selection_status": "SELECTED",
    }

    test_motor_starter_coordination = {
        "coordination_status": "VERIFIED",
    }

    result = check_final_motor_feeder_design(
        design_current=test_design_current,
        cable=test_cable,
        voltage_drop=test_voltage_drop,
        starting_voltage_drop=test_starting_voltage_drop,
        short_circuit=test_short_circuit,
        motor_circuit_breaker=test_motor_circuit_breaker,
        contactor=test_contactor,
        motor_starter_coordination=test_motor_starter_coordination,
        motor_starter_coordination_optimization=None,
    )

    print("=" * 76)
    print("DEE - FINAL MOTOR FEEDER DESIGN CHECK")
    print("=" * 76)

    print()

    print(
        f"Motor design current IB       = "
        f"{result['design_current_a']:.2f} A "
        f"(motor feeder design current)"
    )

    print(
        f"Cable current capacity Iz     = "
        f"{result['cable_current_capacity_a']:.2f} A "
        f"(corrected cable current-carrying capacity)"
    )

    print(
        f"Short-circuit current Ik3     = "
        f"{result['short_circuit_current_ka']:.2f} kA "
        f"(prospective feeder-end short-circuit current)"
    )

    print()

    print(
        f"Cable current capacity        = "
        f"{result['cable_current_capacity_check']} "
        f"(IB <= Iz current-capacity condition)"
    )

    print(
        f"Cable module current check    = "
        f"{result['cable_module_current_capacity_check']} "
        f"(cable selection module current-capacity result)"
    )

    print(
        f"Cable selection               = "
        f"{result['cable_selection_check']} "
        f"(cable selection status)"
    )

    print(
        f"Steady-state voltage drop     = "
        f"{result['steady_state_voltage_drop_check']} "
        f"(steady-state voltage-drop check)"
    )

    print(
        f"Starting voltage drop         = "
        f"{result['motor_starting_voltage_drop_check']} "
        f"(motor starting voltage-drop check)"
    )

    print(
        f"Circuit breaker selection     = "
        f"{result['motor_circuit_breaker_selection_check']} "
        f"(motor circuit breaker selection status)"
    )

    print(
        f"Breaking capacity             = "
        f"{result['breaking_capacity_check']} "
        f"(circuit breaker short-circuit breaking capacity check)"
    )

    print(
        f"Contactor selection           = "
        f"{result['contactor_selection_check']} "
        f"(motor contactor selection status)"
    )

    print(
        f"Type 2 coordination           = "
        f"{result['type_2_coordination_check']} "
        f"(Schneider Electric motor starter coordination check)"
    )

    print()

    print(
        f"Final circuit breaker         = "
        f"{result['final_breaker_reference']} "
        f"(final motor protection device reference)"
    )

    print(
        f"Final contactor               = "
        f"{result['final_contactor_reference']} "
        f"(final motor contactor reference)"
    )

    print(
        f"Final coordination source     = "
        f"{result['final_coordination_source']} "
        f"(final equipment combination source)"
    )

    print()

    print(
        f"Failed design checks          = "
        f"{result['failed_design_check_count']} "
        f"(number of failed final design checks)"
    )

    print()

    print(
        f"FINAL DESIGN STATUS           = "
        f"{result['final_design_status']} "
        f"(final motor feeder design assessment)"
    )

    print("=" * 76)