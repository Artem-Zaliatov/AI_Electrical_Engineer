"""
DIGITAL ELECTRICAL ENGINEER (DEE)

SCHNEIDER ELECTRIC DIGITAL PRODUCT DATA

MOTOR STARTER TYPE 2 COORDINATION DATA

This module stores digitized Schneider Electric
motor starter coordination records.

The coordination data are intentionally separated
from calculation and equipment selection algorithms.

Current application:

    three-phase asynchronous motor;
    Direct-On-Line starting;
    Schneider Electric TeSys motor starter;
    Type 2 coordination.

IMPORTANT:

Coordination is a property of the complete tested combination:

    short-circuit protective device
    +
    contactor
    +
    overload protection arrangement

A coordination type must not be inferred only from
individual device current ratings.

Source class:

    Schneider Electric TeSys Selection Guide
    IE3 / IE4 Type 2 Coordination Charts

DEE data status:

    OFFICIAL TABLE DIGITIZATION IN PROGRESS
"""


# =============================================================================
# DATA SOURCE
# =============================================================================

SCHNEIDER_COORDINATION_DATA_SOURCE = {
    "manufacturer":
        "SCHNEIDER ELECTRIC",

    "document_title":
        "TESYS SELECTION GUIDE IE3/IE4 TYPE 2 COORDINATION CHARTS",

    "document_reference":
        "TESYS_SELECTION_GUIDE",

    "coordination_type":
        "TYPE 2",

    "data_status":
        "OFFICIAL TABLE DIGITIZATION IN PROGRESS",
}


# =============================================================================
# MOTOR STARTER COORDINATION DATA
#
# TABLE STRUCTURE
#
# Each record represents one Schneider Electric
# tested motor starter combination.
#
# Fields:
#
# motor_power_kw
#     Motor rated output power at the table voltage.
#
# system_voltage_v
#     Coordination table operational voltage.
#
# starting_method
#     Motor starting method.
#
# motor_circuit_breaker_reference
#     Schneider Electric motor circuit breaker reference.
#
# contactor_base_reference
#     Base contactor reference without coil suffix.
#
# coordination_type
#     IEC coordination type.
#
# coordination_short_circuit_ka
#     Maximum table coordination short-circuit level.
#
# table_record_status
#     VERIFIED only after direct table digitization.
# =============================================================================

SCHNEIDER_MOTOR_STARTER_COORDINATION_DATA = (

    # =========================================================================
    # 400 V - DOL - TYPE 2
    # =========================================================================

    {
        "motor_power_kw": 15.0,

        "system_voltage_v": 400.0,

        "starting_method": "DOL",

        "motor_circuit_breaker_reference": "GV2ME32",

        "contactor_base_reference": "LC1D32",

        "coordination_type": "TYPE 2",

        "coordination_short_circuit_ka": None,

        "table_record_status": "PENDING SOURCE DIGITIZATION",
    },

)