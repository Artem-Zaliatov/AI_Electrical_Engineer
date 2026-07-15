"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
SCHNEIDER ELECTRIC MOTOR STARTER COORDINATION

This module checks Schneider Electric motor starter coordination.

The coordination check is based on digitized
manufacturer coordination tables.

Current application:

    three-phase asynchronous motor;
    Direct-On-Line starting;
    Schneider Electric TeSys equipment.

IMPORTANT:

Coordination is not calculated from individual
device ratings.

The selected equipment combination must exist
in an official Schneider Electric coordination table.
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
# MOTOR STARTER COORDINATION ERROR
# =============================================================================

class MotorStarterCoordinationError(ValueError):
    """
    Error raised when motor starter coordination
    cannot be checked.
    """

    pass


# =============================================================================
# MOTOR STARTER COORDINATION CHECK
# =============================================================================

def check_motor_starter_coordination(
    motor,
    motor_circuit_breaker,
    contactor,
    short_circuit,
    installation,
):
    """
    Check Schneider Electric motor starter coordination.

    Parameters
    ----------
    motor : dict
        Validated motor data.

    motor_circuit_breaker : dict
        Selected motor circuit breaker data.

    contactor : dict
        Selected contactor data.

    short_circuit : dict
        Short-circuit current calculation results.

    installation : dict
        Validated installation data.

    Returns
    -------
    dict
        Motor starter coordination results.
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

            raise MotorStarterCoordinationError(
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

                raise MotorStarterCoordinationError(
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

    motor_circuit_breaker_reference = str(
        motor_circuit_breaker["reference"]
    ).strip().upper()

    contactor_base_reference = str(
        contactor["base_reference"]
    ).strip().upper()

    contactor_reference = str(
        contactor["reference"]
    ).strip().upper()

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

        raise MotorStarterCoordinationError(
            "Motor rated power must be greater than zero."
        )

    if short_circuit_current_ka <= 0:

        raise MotorStarterCoordinationError(
            "Short-circuit current must be greater than zero."
        )

    if system_voltage_v <= 0:

        raise MotorStarterCoordinationError(
            "System voltage must be greater than zero."
        )

    # -------------------------------------------------------------------------
    # TABLE SEARCH
    # -------------------------------------------------------------------------

    coordination_record = None

    for record in SCHNEIDER_MOTOR_STARTER_COORDINATION_DATA:

        power_match = (
            record["motor_power_kw"]
            == motor_power_kw
        )

        voltage_match = (
            record["system_voltage_v"]
            == system_voltage_v
        )

        starting_method_match = (
            record["starting_method"]
            == starting_method
        )

        breaker_match = (
            record[
                "motor_circuit_breaker_reference"
            ]
            == motor_circuit_breaker_reference
        )

        contactor_match = (
            record[
                "contactor_base_reference"
            ]
            == contactor_base_reference
        )

        if (
            power_match
            and voltage_match
            and starting_method_match
            and breaker_match
            and contactor_match
        ):

            coordination_record = record

            break

    # -------------------------------------------------------------------------
    # TABLE RECORD NOT FOUND
    # -------------------------------------------------------------------------

    if coordination_record is None:

        return {
            "motor_power_kw":
                motor_power_kw,

            "starting_method":
                starting_method,

            "motor_circuit_breaker_reference":
                motor_circuit_breaker_reference,

            "contactor_base_reference":
                contactor_base_reference,

            "contactor_reference":
                contactor_reference,

            "system_voltage_v":
                system_voltage_v,

            "short_circuit_current_ka":
                short_circuit_current_ka,

            "combination_check":
                "NOT FOUND",

            "coordination_type":
                "UNKNOWN",

            "coordination_short_circuit_ka":
                None,

            "short_circuit_coordination_check":
                "NOT CHECKED",

            "table_record_status":
                "NO TABLE RECORD",

            "coordination_source":
                SCHNEIDER_COORDINATION_DATA_SOURCE[
                    "document_title"
                ],

            "coordination_status":
                "NOT VERIFIED",
        }

    # -------------------------------------------------------------------------
    # TABLE RECORD FOUND
    # -------------------------------------------------------------------------

    table_record_status = str(
        coordination_record[
            "table_record_status"
        ]
    ).strip().upper()

    coordination_short_circuit_ka = (
        coordination_record[
            "coordination_short_circuit_ka"
        ]
    )

    # -------------------------------------------------------------------------
    # PENDING SOURCE DIGITIZATION
    # -------------------------------------------------------------------------

    if (
        table_record_status
        != "VERIFIED"
    ):

        return {
            **coordination_record,

            "motor_power_kw":
                motor_power_kw,

            "starting_method":
                starting_method,

            "motor_circuit_breaker_reference":
                motor_circuit_breaker_reference,

            "contactor_base_reference":
                contactor_base_reference,

            "contactor_reference":
                contactor_reference,

            "system_voltage_v":
                system_voltage_v,

            "short_circuit_current_ka":
                short_circuit_current_ka,

            "combination_check":
                "FOUND",

            "short_circuit_coordination_check":
                "NOT CHECKED",

            "coordination_source":
                SCHNEIDER_COORDINATION_DATA_SOURCE[
                    "document_title"
                ],

            "coordination_status":
                "PENDING SOURCE DIGITIZATION",
        }

    # -------------------------------------------------------------------------
    # VERIFIED RECORD CHECK
    # -------------------------------------------------------------------------

    if coordination_short_circuit_ka is None:

        raise MotorStarterCoordinationError(
            "Verified coordination record does not contain "
            "a coordination short-circuit level."
        )

    coordination_short_circuit_ka = float(
        coordination_short_circuit_ka
    )

    if coordination_short_circuit_ka <= 0:

        raise MotorStarterCoordinationError(
            "Coordination short-circuit level must be "
            "greater than zero."
        )

    # -------------------------------------------------------------------------
    # SHORT-CIRCUIT COORDINATION CHECK
    # -------------------------------------------------------------------------

    if (
        short_circuit_current_ka
        <= coordination_short_circuit_ka
    ):

        short_circuit_coordination_check = (
            "PERMISSIBLE"
        )

        coordination_status = (
            "VERIFIED"
        )

    else:

        short_circuit_coordination_check = (
            "NOT PERMISSIBLE"
        )

        coordination_status = (
            "NOT PERMISSIBLE"
        )

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        **coordination_record,

        "motor_power_kw":
            motor_power_kw,

        "starting_method":
            starting_method,

        "motor_circuit_breaker_reference":
            motor_circuit_breaker_reference,

        "contactor_base_reference":
            contactor_base_reference,

        "contactor_reference":
            contactor_reference,

        "system_voltage_v":
            system_voltage_v,

        "short_circuit_current_ka":
            short_circuit_current_ka,

        "combination_check":
            "FOUND",

        "short_circuit_coordination_check":
            short_circuit_coordination_check,

        "coordination_source":
            SCHNEIDER_COORDINATION_DATA_SOURCE[
                "document_title"
            ],

        "coordination_status":
            coordination_status,
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
    }

    test_short_circuit = {
        "feeder_end_short_circuit_current_ka": 1.36,
    }

    test_installation = {
        "system_voltage_v": 400.0,
    }

    result = check_motor_starter_coordination(
        motor=test_motor,

        motor_circuit_breaker=
            test_motor_circuit_breaker,

        contactor=test_contactor,

        short_circuit=test_short_circuit,

        installation=test_installation,
    )

    print("=" * 76)

    print(
        "DEE - MOTOR STARTER COORDINATION"
    )

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

    print()

    print(
        f"Motor circuit breaker         = "
        f"{result['motor_circuit_breaker_reference']} "
        f"(selected motor protection device)"
    )

    print(
        f"Contactor                     = "
        f"{result['contactor_reference']} "
        f"(selected motor contactor)"
    )

    print()

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
        f"Combination check             = "
        f"{result['combination_check']} "
        f"(coordination table combination lookup)"
    )

    print(
        f"Coordination type             = "
        f"{result['coordination_type']} "
        f"(IEC motor starter coordination type)"
    )

    coordination_short_circuit_ka = result[
        "coordination_short_circuit_ka"
    ]

    if coordination_short_circuit_ka is None:

        print(
            f"Coordination short-circuit    = "
            f"NOT AVAILABLE "
            f"(coordination table value is not digitized)"
        )

    else:

        print(
            f"Coordination short-circuit    = "
            f"{coordination_short_circuit_ka:.2f} kA "
            f"(maximum verified coordination fault level)"
        )

    print(
        f"Short-circuit coordination    = "
        f"{result['short_circuit_coordination_check']} "
        f"(calculated Ik3 against coordination table level)"
    )

    print()

    print(
        f"Table record status           = "
        f"{result['table_record_status']} "
        f"(digitized coordination record status)"
    )

    print(
        f"Coordination source           = "
        f"{result['coordination_source']} "
        f"(Schneider Electric source document)"
    )

    print(
        f"Coordination status           = "
        f"{result['coordination_status']} "
        f"(motor starter coordination status)"
    )

    print("=" * 76)