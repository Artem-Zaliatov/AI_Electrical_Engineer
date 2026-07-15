"""
DIGITAL ELECTRICAL ENGINEER (DEE)

SCHNEIDER ELECTRIC DIGITAL PRODUCT DATA

MOTOR STARTER TYPE 2 COORDINATION DATA

This module stores digitized Schneider Electric
motor starter Type 2 coordination records.

Application:

    three-phase asynchronous motor;
    Direct-On-Line starting;
    Schneider Electric TeSys motor starter;
    IEC Type 2 coordination.

IMPORTANT:

Coordination is a property of the complete tested combination:

    motor circuit breaker
    +
    contactor

The coordination short-circuit current Iq must be taken
from the Schneider Electric coordination table.

It must not be inferred from individual device ratings.

Source:

    Schneider Electric
    TeSys IE3 / IE4 Type 2 Coordination Charts

Coordination standard:

    IEC 60947-4-1
"""


# =============================================================================
# DATA SOURCE
# =============================================================================

SCHNEIDER_COORDINATION_DATA_SOURCE = {
    "manufacturer":
        "SCHNEIDER ELECTRIC",

    "document_title":
        "TESYS IE3/IE4 TYPE 2 COORDINATION CHARTS",

    "document_reference":
        "TESYS_SELECTION_GUIDE",

    "coordination_standard":
        "IEC 60947-4-1",

    "coordination_type":
        "TYPE 2",

    "data_status":
        "VERIFIED SOURCE TABLE DATA",
}


# =============================================================================
# MOTOR STARTER TYPE 2 COORDINATION DATA
#
# 400 / 415 V
#
# Starting method:
#
#     DOL - Direct-On-Line
#
# Protection:
#
#     motor circuit breaker with built-in overload protection
#
# Contactor:
#
#     Schneider Electric TeSys contactor
#
# Iq:
#
#     coordination short-circuit current according
#     to the Schneider Electric Type 2 coordination table
# =============================================================================

SCHNEIDER_MOTOR_STARTER_COORDINATION_DATA = (

    # -------------------------------------------------------------------------
    # 1.5 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 1.5,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME08",
        "contactor_base_reference": "LC1D09",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 130.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 2.2 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 2.2,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME10",
        "contactor_base_reference": "LC1D09",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 130.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 3.0 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 3.0,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME14",
        "contactor_base_reference": "LC1D09",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 130.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 4.0 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 4.0,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME14",
        "contactor_base_reference": "LC1D09",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 130.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 5.5 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 5.5,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME16",
        "contactor_base_reference": "LC1D25",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 130.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 7.5 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 7.5,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME20",
        "contactor_base_reference": "LC1D25",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 50.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 9.0 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 9.0,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME21",
        "contactor_base_reference": "LC1D25",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 50.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 11.0 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 11.0,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME22",
        "contactor_base_reference": "LC1D25",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 50.0,
        "table_record_status": "VERIFIED",
    },

    # -------------------------------------------------------------------------
    # 15.0 kW
    # -------------------------------------------------------------------------

    {
        "motor_power_kw": 15.0,
        "system_voltage_group": "400/415 V",
        "system_voltage_min_v": 400.0,
        "system_voltage_max_v": 415.0,
        "starting_method": "DOL",
        "motor_circuit_breaker_reference": "GV2ME32",
        "contactor_base_reference": "LC1D32",
        "coordination_type": "TYPE 2",
        "coordination_short_circuit_ka": 35.0,
        "table_record_status": "VERIFIED",
    },

)