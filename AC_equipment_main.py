"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN

Calculation and selection of protection, switching equipment,
and power cable for an existing three-phase asynchronous motor.

Methodological basis:
- Schneider Electric technical documentation;
- Schneider Electric Electrical Installation Guide;
- Schneider Electric TeSys coordination and selection data;
- applicable IEC requirements.

Current development stage:
- motor nameplate data input and validation;
- motor circuit design current calculation;
- motor starting current calculation;
- installation data validation;
- cable current-carrying capacity selection.
"""


# =============================================================================
# IMPORTS
# =============================================================================

from src.reports.ac_motor_feeder_word_report import (
    create_ac_motor_feeder_word_report,
)

from src.ac_motor_feeder.motor_data import (
    validate_motor_data,
    get_connection_description,
    get_duty_description,
    get_efficiency_class_description,
    get_starting_method_description,
)

from src.ac_motor_feeder.design_current import (
    calculate_design_current,
)

from src.ac_motor_feeder.starting_current import (
    calculate_starting_current,
)

from src.ac_motor_feeder.installation_data import (
    validate_installation_data,
)

from src.ac_motor_feeder.cable_current_capacity import (
    select_cable_current_capacity,
)
from src.ac_motor_feeder.voltage_drop import (
    calculate_voltage_drop,
)

from src.ac_motor_feeder.starting_voltage_drop import (
    calculate_starting_voltage_drop,
)

from src.ac_motor_feeder.supply_data import (
    validate_supply_data,
)

from src.ac_motor_feeder.short_circuit_current import (
    calculate_short_circuit_current,
)

from src.ac_motor_feeder.motor_circuit_breaker import (
    select_motor_circuit_breaker,
)

from src.ac_motor_feeder.contactor import (
    select_contactor,
)

from src.ac_motor_feeder.motor_starter_coordination import (
    check_motor_starter_coordination,
)

from src.ac_motor_feeder.motor_starter_coordination_optimizer import (
    optimize_motor_starter_coordination,
)

from src.ac_motor_feeder.final_design_check import (
    check_final_motor_feeder_design,
)

# =============================================================================
# INITIAL MOTOR DATA
# =============================================================================

MOTOR_DATA = {
    # -------------------------------------------------------------------------
    # MOTOR IDENTIFICATION
    # -------------------------------------------------------------------------

    "manufacturer": "REFERENCE MOTOR",
    "motor_type": "TEST AC MOTOR",

    # -------------------------------------------------------------------------
    # RATED MOTOR DATA
    # -------------------------------------------------------------------------

    "rated_power_kw": 15.0,
    "rated_voltage_v": 400,
    "rated_current_a": 28.5,
    "rated_frequency_hz": 50,
    "rated_speed_rpm": 1475,

    "power_factor": 0.86,
    "efficiency": 0.921,

    # -------------------------------------------------------------------------
    # MOTOR CONSTRUCTION AND DUTY
    # -------------------------------------------------------------------------

    "phases": 3,
    "connection": "DELTA",
    "duty": "S1",
    "efficiency_class": "IE3",

    # -------------------------------------------------------------------------
    # STARTING DATA
    # -------------------------------------------------------------------------

    "starting_method": "DOL",
    "starting_current_ratio": 7.5,
    "starting_time_s": 3.5,
}


# =============================================================================
# INITIAL INSTALLATION DATA
# =============================================================================

INSTALLATION_DATA = {
    # -------------------------------------------------------------------------
    # ELECTRICAL SYSTEM
    # -------------------------------------------------------------------------

    "system_voltage_v": 400,
    "system_frequency_hz": 50,
    "control_voltage_v": 220.0,
    "control_current_type": "AC",
    # -------------------------------------------------------------------------
    # MOTOR FEEDER CABLE
    # -------------------------------------------------------------------------

    "cable_length_m": 45.0,

    "conductor_material": "CU",
    "insulation": "PVC",

    "installation_method": "C",
    "installation_environment": "AIR",

    "loaded_conductors": 3,

    # -------------------------------------------------------------------------
    # INSTALLATION CONDITIONS
    # -------------------------------------------------------------------------

    "ambient_temperature_c": 40.0,
    "grouped_circuits": 1,
  }


# =============================================================================
# MOTOR STARTING CALCULATION DATA
# =============================================================================

STARTING_CALCULATION_DATA = {
    "starting_power_factor": 0.35,  
}

# =============================================================================
# ELECTRICAL SUPPLY DATA
# =============================================================================

SUPPLY_DATA = {
    # -------------------------------------------------------------------------
    # SUPPLY SOURCE
    # -------------------------------------------------------------------------

    "supply_source": "TRANSFORMER",

    # -------------------------------------------------------------------------
    # TRANSFORMER DATA
    # -------------------------------------------------------------------------

    "transformer_rated_power_kva": 630.0,

    "transformer_secondary_voltage_v": 400.0,

    "transformer_impedance_percent": 6.0,

    "transformer_load_losses_w": 7100.0,

}

# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():

    print()
    print("=" * 76)
    print("DIGITAL ELECTRICAL ENGINEER (DEE)")
    print("AC MOTOR FEEDER DESIGN")
    print("SCHNEIDER ELECTRIC / IEC")
    print("=" * 76)

    # =========================================================================
    # MOTOR DATA VALIDATION
    # =========================================================================

    motor = validate_motor_data(
        MOTOR_DATA,
    )

    print()
    print("MOTOR NAMEPLATE DATA")
    print("-" * 76)

    print(
        f"Manufacturer                  = "
        f"{motor['manufacturer']} "
        f"(motor manufacturer)"
    )

    print(
        f"Motor type                    = "
        f"{motor['motor_type']} "
        f"(manufacturer motor type or model)"
    )

    print()

    print(
        f"Rated power Pn                = "
        f"{motor['rated_power_kw']:.2f} kW "
        f"(motor rated output power)"
    )

    print(
        f"Rated voltage Un              = "
        f"{motor['rated_voltage_v']:.0f} V "
        f"(motor rated line voltage)"
    )

    print(
        f"Rated current In              = "
        f"{motor['rated_current_a']:.2f} A "
        f"(motor full-load current, FLC)"
    )

    print(
        f"Rated frequency fn            = "
        f"{motor['rated_frequency_hz']:.1f} Hz "
        f"(motor rated supply frequency)"
    )

    print(
        f"Rated speed nn                = "
        f"{motor['rated_speed_rpm']:.0f} rpm "
        f"(motor rated shaft speed)"
    )

    print()

    print(
        f"Efficiency eta                = "
        f"{motor['efficiency']:.3f} "
        f"(motor rated efficiency)"
    )

    print(
        f"Power factor cos(phi)         = "
        f"{motor['power_factor']:.3f} "
        f"(motor rated power factor)"
    )

    print()

    print(
        f"Number of phases              = "
        f"{motor['phases']} "
        f"(three-phase AC motor)"
    )

    print(
        f"Connection                    = "
        f"{motor['connection']} "
        f"({get_connection_description(motor['connection'])})"
    )

    print(
        f"Duty                          = "
        f"{motor['duty']} "
        f"({get_duty_description(motor['duty'])})"
    )

    print(
        f"Efficiency class              = "
        f"{motor['efficiency_class']} "
        f"("
        f"{get_efficiency_class_description(motor['efficiency_class'])}"
        f")"
    )

    print()

    print(
        f"Starting method               = "
        f"{motor['starting_method']} "
        f"("
        f"{get_starting_method_description(motor['starting_method'])}"
        f")"
    )

    print(
        f"Starting current ratio Is/In  = "
        f"{motor['starting_current_ratio']:.2f} "
        f"(starting current to rated current ratio)"
    )

    print(
        f"Starting time ts              = "
        f"{motor['starting_time_s']:.2f} s "
        f"(motor acceleration time)"
    )

    print()

    print(
        f"Motor data source             = "
        f"{motor['motor_data_source']} "
        f"(manufacturer nameplate data)"
    )

    print(
        f"Motor data check              = "
        f"{motor['motor_data_status']} "
        f"(input data validation status)"
    )

    # =========================================================================
    # INSTALLATION DATA VALIDATION
    # =========================================================================

    installation = validate_installation_data(
        INSTALLATION_DATA,
    )

# =========================================================================
    # SUPPLY DATA VALIDATION
    # =========================================================================

    supply = validate_supply_data(
        SUPPLY_DATA,
    )

    print()
    print("INSTALLATION DATA")
    print("-" * 76)

    print(
        f"System voltage Un             = "
        f"{installation['system_voltage_v']:.0f} V "
        f"(three-phase system line voltage)"
    )

    print(
        f"System frequency fn           = "
        f"{installation['system_frequency_hz']:.1f} Hz "
        f"(electrical system frequency)"
    )

    print()

    print(
        f"Cable length L                = "
        f"{installation['cable_length_m']:.1f} m "
        f"(one-way motor feeder cable length)"
    )

    print(
        f"Conductor material            = "
        f"{installation['conductor_material']} "
        f"({installation['conductor_material_description']})"
    )

    print(
        f"Cable insulation              = "
        f"{installation['insulation']} "
        f"({installation['insulation_description']})"
    )

    print()

    print(
        f"Installation method           = "
        f"{installation['installation_method']} "
        f"({installation['installation_method_description']})"
    )

    print(
        f"Installation environment      = "
        f"{installation['installation_environment']} "
        f"({installation['installation_environment_description']})"
    )

    print(
        f"Loaded conductors             = "
        f"{installation['loaded_conductors']} "
        f"(current-carrying conductors)"
    )

    print()

    print(
        f"Ambient temperature           = "
        f"{installation['ambient_temperature_c']:.1f} deg C "
        f"(ambient air temperature)"
    )

    print(
        f"Grouped circuits              = "
        f"{installation['grouped_circuits']} "
        f"(number of grouped circuits)"
    )

    print()

    print(
        f"Installation data source      = "
        f"{installation['installation_data_source']} "
        f"(installation conditions data source)"
    )

    print(
        f"Installation data check       = "
        f"{installation['installation_data_status']} "
        f"(input data validation status)"
    )

    # =========================================================================
    # SECTION 1 - MOTOR DESIGN CURRENT
    # =========================================================================

    design_current = calculate_design_current(
        motor,
    )

    print()
    print("=" * 76)
    print("SECTION 1 - MOTOR DESIGN CURRENT")
    print("=" * 76)

    print()

    print(
        f"Calculated motor current Icalc = "
        f"{design_current['calculated_current_a']:.2f} A "
        f"(control calculation from Pn, Un, eta and cos(phi))"
    )

    print(
        f"Nameplate motor current In     = "
        f"{design_current['nameplate_current_a']:.2f} A "
        f"(manufacturer motor full-load current, FLC)"
    )

    print()

    print(
        f"Current deviation              = "
        f"{design_current['current_deviation_a']:+.2f} A "
        f"(nameplate current minus calculated current)"
    )

    print(
        f"Current deviation              = "
        f"{design_current['current_deviation_percent']:.2f} % "
        f"(absolute current deviation relative to nameplate FLC)"
    )

    print()

    print(
        f"Accepted design current IB     = "
        f"{design_current['design_current_a']:.2f} A "
        f"(motor circuit design current based on nameplate FLC)"
    )

    print(
        f"Current source                 = "
        f"{design_current['current_source']} "
        f"(accepted current data source)"
    )

    print(
        f"Design current status          = "
        f"{design_current['design_current_status']} "
        f"(design current acceptance status)"
    )

    # =========================================================================
    # SECTION 2 - MOTOR STARTING CURRENT
    # =========================================================================

    starting_current = calculate_starting_current(
        motor=motor,
        design_current=design_current,
    )

    print()
    print("=" * 76)
    print("SECTION 2 - MOTOR STARTING CURRENT")
    print("=" * 76)

    print()

    print(
        f"Starting method               = "
        f"{starting_current['starting_method']} "
        f"({starting_current['starting_method_description']})"
    )

    print(
        f"Rated motor current In        = "
        f"{starting_current['rated_current_a']:.2f} A "
        f"(motor nameplate full-load current, FLC)"
    )

    print(
        f"Starting current ratio Is/In  = "
        f"{starting_current['starting_current_ratio']:.2f} "
        f"(manufacturer starting-current ratio)"
    )

    print()

    print(
        f"Starting current Is           = "
        f"{starting_current['starting_current_a']:.2f} A "
        f"(calculated motor starting current)"
    )

    print(
        f"Starting current              = "
        f"{starting_current['starting_current_percent']:.0f} % In "
        f"(starting current relative to rated current)"
    )

    print()

    print(
        f"Starting time ts              = "
        f"{starting_current['starting_time_s']:.2f} s "
        f"(motor acceleration time)"
    )

    print(
        f"Starting time class           = "
        f"{starting_current['starting_time_class']} "
        f"(descriptive starting-time classification)"
    )

    print()

    print(
        f"Starting data source          = "
        f"{starting_current['starting_data_source']} "
        f"(starting parameters data source)"
    )

    print(
        f"Starting current status       = "
        f"{starting_current['starting_current_status']} "
        f"(starting-current calculation status)"
    )

    # =========================================================================
    # SECTION 3 - CABLE CURRENT-CARRYING CAPACITY
    # =========================================================================

    cable = select_cable_current_capacity(
        design_current=design_current,
        installation=installation,
    )

    print()
    print("=" * 76)
    print("SECTION 3 - CABLE CURRENT-CARRYING CAPACITY")
    print("=" * 76)

    print()

    print(
        f"Motor design current IB       = "
        f"{cable['design_current_a']:.2f} A "
        f"(motor feeder design current)"
    )

    print()

    print(
        f"Temperature factor k1         = "
        f"{cable['temperature_factor']:.3f} "
        f"(ambient air temperature correction factor)"
    )

    print(
        f"Grouping factor k4            = "
        f"{cable['grouping_factor']:.3f} "
        f"(grouped circuits correction factor)"
    )

    print(
        f"Total correction factor       = "
        f"{cable['total_correction_factor']:.3f} "
        f"(product of applicable correction factors)"
    )

    print()

    print(
        f"Required tabulated current Iz = "
        f"{cable['required_tabulated_current_a']:.2f} A "
        f"(minimum required table current capacity)"
    )

    print()

    print(
        f"Selected conductor section S  = "
        f"{cable['selected_cross_section_mm2']:.1f} mm2 "
        f"(selected phase conductor cross-section)"
    )

    print(
        f"Tabulated current capacity    = "
        f"{cable['selected_tabulated_current_a']:.2f} A "
        f"(reference current-carrying capacity)"
    )

    print(
        f"Corrected current capacity    = "
        f"{cable['corrected_current_capacity_a']:.2f} A "
        f"(current capacity after correction factors)"
    )

    print()

    print(
        f"Current capacity check        = "
        f"{cable['current_capacity_check']} "
        f"(corrected cable capacity versus motor design current)"
    )

    print(
        f"Cable table source            = "
        f"{cable['cable_table_source']} "
        f"(cable sizing methodology source)"
    )

    print(
        f"Cable selection status        = "
        f"{cable['cable_selection_status']} "
        f"(cable current-capacity selection status)"
    )

    print("=" * 76)

    # =========================================================================
    # SECTION 4 - STEADY-STATE VOLTAGE DROP
    # =========================================================================

    voltage_drop = calculate_voltage_drop(
        motor=motor,
        design_current=design_current,
        cable=cable,
        installation=installation,
    )

    print()
    print("=" * 76)
    print("SECTION 4 - STEADY-STATE VOLTAGE DROP")
    print("=" * 76)

    print()

    print(
        f"Motor design current IB       = "
        f"{voltage_drop['design_current_a']:.2f} A "
        f"(motor feeder design current)"
    )

    print(
        f"System voltage Un             = "
        f"{voltage_drop['system_voltage_v']:.0f} V "
        f"(three-phase line voltage)"
    )

    print(
        f"Cable length L                = "
        f"{voltage_drop['cable_length_m']:.1f} m "
        f"(one-way cable length)"
    )

    print(
        f"Conductor section S           = "
        f"{voltage_drop['cross_section_mm2']:.1f} mm2 "
        f"(selected phase conductor cross-section)"
    )

    print()

    print(
        f"Cable resistance R            = "
        f"{voltage_drop['resistance_ohm_km']:.3f} ohm/km "
        f"(conductor resistance)"
    )

    print(
        f"Cable reactance X             = "
        f"{voltage_drop['reactance_ohm_km']:.3f} ohm/km "
        f"(cable inductive reactance)"
    )

    print()

    print(
        f"Power factor cos(phi)         = "
        f"{voltage_drop['power_factor']:.3f} "
        f"(motor rated power factor)"
    )

    print(
        f"sin(phi)                      = "
        f"{voltage_drop['sin_phi']:.3f} "
        f"(sine of motor phase angle)"
    )

    print()

    print(
        f"Voltage drop delta_U          = "
        f"{voltage_drop['voltage_drop_v']:.2f} V "
        f"(steady-state line voltage drop)"
    )

    print(
        f"Voltage drop delta_U          = "
        f"{voltage_drop['voltage_drop_percent']:.2f} % "
        f"(steady-state voltage drop)"
    )

    print(
        f"Motor terminal voltage        = "
        f"{voltage_drop['motor_terminal_voltage_v']:.2f} V "
        f"(estimated motor terminal voltage)"
    )

    print()

    print(
        f"Maximum voltage drop          = "
        f"{voltage_drop['maximum_voltage_drop_percent']:.2f} % "
        f"(current motor voltage-drop assessment limit)"
    )

    print(
        f"Voltage drop check            = "
        f"{voltage_drop['voltage_drop_check']} "
        f"(steady-state voltage-drop check)"
    )

    print(
        f"Voltage drop source           = "
        f"{voltage_drop['voltage_drop_source']} "
        f"(calculation methodology source)"
    )

    print(
        f"Voltage drop status           = "
        f"{voltage_drop['voltage_drop_status']} "
        f"(voltage-drop calculation status)"
    )

    # =========================================================================
    # SECTION 5 - MOTOR STARTING VOLTAGE DROP
    # =========================================================================

    starting_voltage_drop = calculate_starting_voltage_drop(
        starting_current=starting_current,
        voltage_drop=voltage_drop,
        starting_power_factor=(
            STARTING_CALCULATION_DATA["starting_power_factor"]
        ),
    )

    print()
    print("=" * 76)
    print("SECTION 5 - MOTOR STARTING VOLTAGE DROP")
    print("=" * 76)

    print()

    print(
        f"Starting method               = "
        f"{starting_voltage_drop['starting_method']} "
        f"(Direct-On-Line starting)"
    )

    print(
        f"Starting current Is           = "
        f"{starting_voltage_drop['starting_current_a']:.2f} A "
        f"(motor starting current)"
    )

    print(
        f"Starting time ts              = "
        f"{starting_voltage_drop['starting_time_s']:.2f} s "
        f"(motor acceleration time)"
    )

    print()

    print(
        f"Starting power factor         = "
        f"{starting_voltage_drop['starting_power_factor']:.3f} "
        f"(motor power factor during starting)"
    )

    print(
        f"Starting sin(phi)             = "
        f"{starting_voltage_drop['starting_sin_phi']:.3f} "
        f"(sine of starting phase angle)"
    )

    print()

    print(
        f"Cable length L                = "
        f"{starting_voltage_drop['cable_length_m']:.1f} m "
        f"(one-way cable length)"
    )

    print(
        f"Conductor section S           = "
        f"{starting_voltage_drop['cross_section_mm2']:.1f} mm2 "
        f"(selected phase conductor cross-section)"
    )

    print()

    print(
        f"Starting voltage drop         = "
        f"{starting_voltage_drop['starting_voltage_drop_v']:.2f} V "
        f"(motor feeder voltage drop during starting)"
    )

    print(
        f"Starting voltage drop         = "
        f"{starting_voltage_drop['starting_voltage_drop_percent']:.2f} % "
        f"(starting voltage drop)"
    )

    print(
        f"Starting terminal voltage     = "
        f"{starting_voltage_drop['starting_terminal_voltage_v']:.2f} V "
        f"(estimated motor terminal voltage during starting)"
    )

    print(
        f"Starting terminal voltage     = "
        f"{starting_voltage_drop['starting_terminal_voltage_percent']:.2f} % Un "
        f"(motor starting terminal voltage)"
    )

    print()

    print(
        f"Maximum starting voltage drop = "
        f"{starting_voltage_drop['maximum_starting_voltage_drop_percent']:.2f} % "
        f"(current project assessment limit)"
    )

    print(
        f"Starting voltage-drop check   = "
        f"{starting_voltage_drop['starting_voltage_drop_check']} "
        f"(starting voltage-drop assessment)"
    )

    print(
        f"Starting voltage-drop source  = "
        f"{starting_voltage_drop['starting_voltage_drop_source']} "
        f"(calculation and assessment source)"
    )

    print(
        f"Starting voltage-drop status  = "
        f"{starting_voltage_drop['starting_voltage_drop_status']} "
        f"(starting voltage-drop calculation status)"
    )

    print("=" * 76)

       # =========================================================================
    # SECTION 6 - THREE-PHASE SHORT-CIRCUIT CURRENT
    # =========================================================================

    short_circuit = calculate_short_circuit_current(
        supply=supply,
        voltage_drop=voltage_drop,
    )

    print()
    print("=" * 76)
    print("SECTION 6 - THREE-PHASE SHORT-CIRCUIT CURRENT")
    print("=" * 76)

    print()

    print(
        f"Supply source                 = "
        f"{short_circuit['supply_source']} "
        f"(electrical supply source)"
    )

    print()

    print(
        f"Transformer rated power Sn    = "
        f"{short_circuit['transformer_rated_power_kva']:.1f} kVA "
        f"(transformer rated apparent power)"
    )

    print(
        f"Transformer secondary voltage = "
        f"{short_circuit['transformer_secondary_voltage_v']:.0f} V "
        f"(transformer secondary line voltage)"
    )

    print(
        f"Transformer impedance uk      = "
        f"{short_circuit['transformer_impedance_percent']:.2f} % "
        f"(transformer short-circuit impedance voltage)"
    )

    print(
        f"Transformer load losses PkrT  = "
        f"{short_circuit['transformer_load_losses_w']:.0f} W "
        f"(transformer total load losses)"
    )

    print()

    print(
        f"Transformer rated current InT = "
        f"{short_circuit['transformer_rated_current_a']:.2f} A "
        f"(transformer rated secondary current)"
    )

    print()

    print(
        f"Transformer impedance Ztr     = "
        f"{short_circuit['transformer_impedance_ohm']:.6f} ohm "
        f"(transformer equivalent impedance)"
    )

    print(
        f"Transformer resistance Rtr    = "
        f"{short_circuit['transformer_resistance_ohm']:.6f} ohm "
        f"(transformer winding resistance)"
    )

    print(
        f"Transformer reactance Xtr     = "
        f"{short_circuit['transformer_reactance_ohm']:.6f} ohm "
        f"(transformer leakage reactance)"
    )

    print()

    print(
        f"Transformer terminal Isc      = "
        f"{short_circuit['transformer_short_circuit_current_ka']:.2f} kA "
        f"(three-phase short-circuit current at transformer terminals)"
    )

    print()

    print(
        f"Cable length L                = "
        f"{short_circuit['cable_length_m']:.1f} m "
        f"(one-way feeder cable length)"
    )

    print(
        f"Conductor section S           = "
        f"{short_circuit['cross_section_mm2']:.1f} mm2 "
        f"(selected phase conductor cross-section)"
    )

    print()

    print(
        f"Cable resistance Rc           = "
        f"{short_circuit['cable_resistance_ohm']:.6f} ohm "
        f"(feeder cable resistance)"
    )

    print(
        f"Cable reactance Xc            = "
        f"{short_circuit['cable_reactance_ohm']:.6f} ohm "
        f"(feeder cable reactance)"
    )

    print(
        f"Cable impedance Zc            = "
        f"{short_circuit['cable_impedance_ohm']:.6f} ohm "
        f"(feeder cable impedance)"
    )

    print()

    print(
        f"Total resistance Rtotal       = "
        f"{short_circuit['total_resistance_ohm']:.6f} ohm "
        f"(total series resistance to fault point)"
    )

    print(
        f"Total reactance Xtotal        = "
        f"{short_circuit['total_reactance_ohm']:.6f} ohm "
        f"(total series reactance to fault point)"
    )

    print(
        f"Total impedance Ztotal        = "
        f"{short_circuit['total_impedance_ohm']:.6f} ohm "
        f"(total impedance to fault point)"
    )

    print()

    print(
        f"Feeder-end short-circuit Ik3  = "
        f"{short_circuit['feeder_end_short_circuit_current_ka']:.2f} kA "
        f"(estimated three-phase short-circuit current at motor feeder end)"
    )

    print(
        f"Short-circuit current reduction = "
        f"{short_circuit['short_circuit_current_reduction_percent']:.2f} % "
        f"(fault-current reduction due to feeder impedance)"
    )

    print()

    print(
        f"Calculation model             = "
        f"{short_circuit['short_circuit_calculation_model']} "
        f"(short-circuit calculation model)"
    )

    print(
        f"Short-circuit source          = "
        f"{short_circuit['short_circuit_source']} "
        f"(calculation methodology source)"
    )

    print(
        f"Short-circuit status          = "
        f"{short_circuit['short_circuit_status']} "
        f"(short-circuit calculation status)"
    )

    print("=" * 76)

 # =========================================================================
    # SECTION 7 - MOTOR CIRCUIT BREAKER SELECTION
    # =========================================================================

    motor_circuit_breaker = select_motor_circuit_breaker(
        motor=motor,
        design_current=design_current,
        starting_current=starting_current,
        short_circuit=short_circuit,
        installation=installation,
    )

    print()
    print("=" * 76)
    print("SECTION 7 - MOTOR CIRCUIT BREAKER SELECTION")
    print("=" * 76)

    print()

    print(
        f"Manufacturer                  = "
        f"{motor_circuit_breaker['manufacturer']} "
        f"(selected device manufacturer)"
    )

    print(
        f"Product series                = "
        f"{motor_circuit_breaker['series']} "
        f"(motor protection product family)"
    )

    print(
        f"Selected reference            = "
        f"{motor_circuit_breaker['reference']} "
        f"(Schneider Electric product reference)"
    )

    print()

    print(
        f"Motor rated power Pn          = "
        f"{motor_circuit_breaker['motor_rated_power_kw']:.2f} kW "
        f"(motor rated output power)"
    )

    print(
        f"Motor design current IB       = "
        f"{motor_circuit_breaker['design_current_a']:.2f} A "
        f"(accepted motor feeder design current)"
    )

    print()

    print(
        f"Thermal adjustment range      = "
        f"{motor_circuit_breaker['thermal_min_a']:.2f} ... "
        f"{motor_circuit_breaker['thermal_max_a']:.2f} A "
        f"(motor overload protection adjustment range)"
    )

    print(
        f"Accepted thermal setting Ir   = "
        f"{motor_circuit_breaker['thermal_setting_a']:.2f} A "
        f"(thermal protection setting based on motor FLC)"
    )

    print(
        f"Thermal range check           = "
        f"{motor_circuit_breaker['thermal_range_check']} "
        f"(motor current within thermal adjustment range)"
    )

    print()

    print(
        f"System voltage Un             = "
        f"{motor_circuit_breaker['system_voltage_v']:.0f} V "
        f"(motor feeder system voltage)"
    )

    print(
        f"Device rated voltage Ue       = "
        f"{motor_circuit_breaker['rated_operational_voltage_v']:.0f} V "
        f"(motor circuit breaker rated operational voltage)"
    )

    print(
        f"Voltage check                 = "
        f"{motor_circuit_breaker['voltage_check']} "
        f"(device voltage suitability check)"
    )

    print()

    print(
        f"Calculated short-circuit Ik3  = "
        f"{motor_circuit_breaker['short_circuit_current_ka']:.2f} kA "
        f"(prospective fault current at installation point)"
    )

    print(
        f"Breaking capacity Icu         = "
        f"{motor_circuit_breaker['icu_400v_ka']:.2f} kA "
        f"(ultimate breaking capacity at 400 V)"
    )

    print(
        f"Breaking capacity margin      = "
        f"{motor_circuit_breaker['breaking_capacity_margin_ka']:.2f} kA "
        f"(Icu minus calculated short-circuit current)"
    )

    print(
        f"Breaking capacity check       = "
        f"{motor_circuit_breaker['breaking_capacity_check']} "
        f"(Icu not lower than prospective fault current)"
    )

    print()

    print(
        f"Starting method               = "
        f"{motor_circuit_breaker['starting_method']} "
        f"(Direct-On-Line starting)"
    )

    print(
        f"Motor starting current Is     = "
        f"{motor_circuit_breaker['starting_current_a']:.2f} A "
        f"(calculated motor starting current)"
    )

    print(
        f"Magnetic trip threshold       = "
        f"{motor_circuit_breaker['magnetic_trip_current_a']:.2f} A "
        f"(instantaneous magnetic trip threshold)"
    )

    print(
        f"Magnetic trip margin          = "
        f"{motor_circuit_breaker['magnetic_trip_margin_a']:.2f} A "
        f"(magnetic trip threshold minus starting current)"
    )

    print(
        f"Starting current check        = "
        f"{motor_circuit_breaker['starting_current_check']} "
        f"(starting current below magnetic trip threshold)"
    )

    print()

    print(
        f"Selection source              = "
        f"{motor_circuit_breaker['selection_source']} "
        f"(equipment selection data source)"
    )

    print(
        f"Selection status              = "
        f"{motor_circuit_breaker['selection_status']} "
        f"(motor circuit breaker selection status)"
    )

    print("=" * 76)

    # =========================================================================
    # SECTION 8 - CONTACTOR SELECTION
    # =========================================================================

    contactor = select_contactor(
        motor=motor,
        design_current=design_current,
        installation=installation,
    )

    print()
    print("=" * 76)
    print("SECTION 8 - CONTACTOR SELECTION")
    print("=" * 76)

    print()

    print(
        f"Manufacturer                  = "
        f"{contactor['manufacturer']} "
        f"(selected device manufacturer)"
    )

    print(
        f"Product series                = "
        f"{contactor['series']} "
        f"(contactor product family)"
    )

    print(
        f"Selected reference            = "
        f"{contactor['reference']} "
        f"(Schneider Electric product reference)"
    )

    print()

    print(
        f"Utilisation category          = "
        f"{contactor['utilisation_category']} "
        f"(squirrel-cage motor starting and stopping duty)"
    )

    print()

    print(
        f"Motor rated power Pn          = "
        f"{contactor['motor_rated_power_kw']:.2f} kW "
        f"(motor rated output power)"
    )

    print(
        f"Contactor motor power         = "
        f"{contactor['motor_power_400v_kw']:.2f} kW "
        f"(permissible motor power at 400 V)"
    )

    print(
        f"Motor power margin            = "
        f"{contactor['power_margin_kw']:.2f} kW "
        f"(contactor motor power minus motor rated power)"
    )

    print(
        f"Motor power check             = "
        f"{contactor['power_check']} "
        f"(contactor motor power suitability check)"
    )

    print()

    print(
        f"Motor design current IB       = "
        f"{contactor['design_current_a']:.2f} A "
        f"(accepted motor feeder design current)"
    )

    print(
        f"Contactor operational Ie      = "
        f"{contactor['ie_ac3_a']:.2f} A "
        f"(rated operational current in AC-3)"
    )

    print(
        f"Current margin                = "
        f"{contactor['current_margin_a']:.2f} A "
        f"(contactor operational current minus motor design current)"
    )

    print(
        f"Current check                 = "
        f"{contactor['current_check']} "
        f"(AC-3 operational current suitability check)"
    )

    print()

    print(
        f"System voltage Un             = "
        f"{contactor['system_voltage_v']:.0f} V "
        f"(motor feeder system voltage)"
    )

    print(
        f"Device rated voltage Ue       = "
        f"{contactor['rated_operational_voltage_v']:.0f} V "
        f"(contactor rated operational voltage)"
    )

    print(
        f"Voltage check                 = "
        f"{contactor['voltage_check']} "
        f"(contactor voltage suitability check)"
    )

    print()

    print(
        f"Control circuit voltage Uc    = "
        f"{contactor['control_voltage_v']:.0f} V "
        f"{contactor['control_current_type']} "
        f"(control circuit supply)"
    )

    print(
        f"Selected coil                 = "
        f"{contactor['coil_suffix']} "
        f"({contactor['coil_description']})"
    )

    print()

    print(
        f"Selection source              = "
        f"{contactor['selection_source']} "
        f"(equipment selection data source)"
    )

    print(
        f"Selection status              = "
        f"{contactor['selection_status']} "
        f"(contactor selection status)"
    )

    print("=" * 76)

       # =========================================================================
    # SECTION 9 - MOTOR STARTER COORDINATION
    # =========================================================================

    motor_starter_coordination = check_motor_starter_coordination(
        motor=motor,
        motor_circuit_breaker=motor_circuit_breaker,
        contactor=contactor,
        short_circuit=short_circuit,
        installation=installation,
    )

    # -------------------------------------------------------------------------
    # AUTOMATIC TYPE 2 COORDINATION CORRECTION
    # -------------------------------------------------------------------------

    motor_starter_coordination_optimization = None

    if (
        motor_starter_coordination["coordination_status"]
        != "VERIFIED"
    ):

        motor_starter_coordination_optimization = (
            optimize_motor_starter_coordination(
                motor=motor,
                motor_circuit_breaker=motor_circuit_breaker,
                contactor=contactor,
                short_circuit=short_circuit,
                installation=installation,
            )
        )

    # -------------------------------------------------------------------------
    # SECTION 9 OUTPUT
    # -------------------------------------------------------------------------

    print()
    print("=" * 76)
    print("SECTION 9 - MOTOR STARTER COORDINATION")
    print("=" * 76)

    print()

    print(
        f"Motor circuit breaker         = "
        f"{motor_starter_coordination['motor_circuit_breaker_reference']} "
        f"(selected motor protection device)"
    )

    print(
        f"Contactor                     = "
        f"{motor_starter_coordination['contactor_reference']} "
        f"(selected motor contactor)"
    )

    print()

    print(
        f"System voltage Un             = "
        f"{motor_starter_coordination['system_voltage_v']:.0f} V "
        f"(motor feeder system voltage)"
    )

    if "system_voltage_group" in motor_starter_coordination:

        print(
            f"Coordination voltage group    = "
            f"{motor_starter_coordination['system_voltage_group']} "
            f"(Schneider Electric coordination table voltage group)"
        )

    print(
        f"Calculated short-circuit Ik3  = "
        f"{motor_starter_coordination['short_circuit_current_ka']:.2f} kA "
        f"(prospective fault current at installation point)"
    )

    print()

    print(
        f"Combination check             = "
        f"{motor_starter_coordination['combination_check']} "
        f"(coordination table combination lookup)"
    )

    print(
        f"Coordination type             = "
        f"{motor_starter_coordination['coordination_type']} "
        f"(IEC motor starter coordination type)"
    )

    coordination_short_circuit_ka = (
        motor_starter_coordination[
            "coordination_short_circuit_ka"
        ]
    )

    if coordination_short_circuit_ka is None:

        print(
            f"Coordination short-circuit Iq = "
            f"NOT AVAILABLE "
            f"(coordination table value is not available)"
        )

    else:

        print(
            f"Coordination short-circuit Iq = "
            f"{coordination_short_circuit_ka:.2f} kA "
            f"(Schneider Electric Type 2 coordination table level)"
        )

    print(
        f"Coordination condition        = "
        f"{motor_starter_coordination['short_circuit_coordination_check']} "
        f"(Ik3 <= Iq coordination condition)"
    )

    print()

    print(
        f"Table record status           = "
        f"{motor_starter_coordination['table_record_status']} "
        f"(digitized coordination record status)"
    )

    print(
        f"Coordination source           = "
        f"{motor_starter_coordination['coordination_source']} "
        f"(Schneider Electric source document)"
    )

    print(
        f"Coordination status           = "
        f"{motor_starter_coordination['coordination_status']} "
        f"(motor starter coordination status)"
    )

    # -------------------------------------------------------------------------
    # AUTOMATIC TYPE 2 COORDINATION CORRECTION OUTPUT
    # -------------------------------------------------------------------------

    if motor_starter_coordination_optimization is not None:

        print()
        print("-" * 76)
        print("AUTOMATIC TYPE 2 COORDINATION CORRECTION")
        print("-" * 76)

        print()

        print(
            f"Initial circuit breaker       = "
            f"{motor_starter_coordination_optimization['initial_breaker_reference']} "
            f"(independently selected motor circuit breaker)"
        )

        print(
            f"Initial contactor             = "
            f"{motor_starter_coordination_optimization['initial_contactor_reference']} "
            f"(independently selected contactor)"
        )

        print()

        selected_breaker_reference = (
            motor_starter_coordination_optimization[
                "selected_breaker_reference"
            ]
        )

        selected_contactor_reference = (
            motor_starter_coordination_optimization[
                "selected_contactor_reference"
            ]
        )

        if selected_breaker_reference is None:

            print(
                f"Coordinated circuit breaker   = "
                f"NOT AVAILABLE "
                f"(no coordinated table combination found)"
            )

        else:

            print(
                f"Coordinated circuit breaker   = "
                f"{selected_breaker_reference} "
                f"(Type 2 coordinated motor protection device)"
            )

        if selected_contactor_reference is None:

            print(
                f"Coordinated contactor         = "
                f"NOT AVAILABLE "
                f"(no coordinated table combination found)"
            )

        else:

            print(
                f"Coordinated contactor         = "
                f"{selected_contactor_reference} "
                f"(Type 2 coordinated motor contactor)"
            )

        print()

        optimized_coordination_short_circuit_ka = (
            motor_starter_coordination_optimization[
                "coordination_short_circuit_ka"
            ]
        )

        if optimized_coordination_short_circuit_ka is None:

            print(
                f"Coordination short-circuit Iq = "
                f"NOT AVAILABLE "
                f"(no verified coordination level found)"
            )

        else:

            print(
                f"Coordination short-circuit Iq = "
                f"{optimized_coordination_short_circuit_ka:.2f} kA "
                f"(Schneider Electric Type 2 coordination level)"
            )

        print(
            f"Coordination condition        = "
            f"{motor_starter_coordination_optimization['coordination_condition']} "
            f"(Ik3 <= Iq coordination condition)"
        )

        print(
            f"Combination changed           = "
            f"{motor_starter_coordination_optimization['combination_changed']} "
            f"(initial equipment combination correction status)"
        )

        print()

        print(
            f"Optimization source           = "
            f"{motor_starter_coordination_optimization['optimization_source']} "
            f"(Schneider Electric coordination table source)"
        )

        print(
            f"Optimization status           = "
            f"{motor_starter_coordination_optimization['optimization_status']} "
            f"(coordination optimization result)"
        )

    print("=" * 76)

    # =========================================================================
    # SECTION 10 - FINAL MOTOR FEEDER DESIGN CHECK
    # =========================================================================

    final_design_check = check_final_motor_feeder_design(
        design_current=design_current,
        cable=cable,
        voltage_drop=voltage_drop,
        starting_voltage_drop=starting_voltage_drop,
        short_circuit=short_circuit,
        motor_circuit_breaker=motor_circuit_breaker,
        contactor=contactor,
        motor_starter_coordination=motor_starter_coordination,
        motor_starter_coordination_optimization=(
            motor_starter_coordination_optimization
        ),
    )

        # -------------------------------------------------------------------------
    # SECTION 10 OUTPUT
    # -------------------------------------------------------------------------

    print()
    print("=" * 76)
    print("SECTION 10 - FINAL MOTOR FEEDER DESIGN CHECK")
    print("=" * 76)

    print()

    print(
        f"Motor design current IB       = "
        f"{final_design_check['design_current_a']:.2f} A "
        f"(motor feeder design current)"
    )

    print(
        f"Cable current capacity Iz     = "
        f"{final_design_check['cable_ampacity_a']:.2f} A "
        f"(selected cable current-carrying capacity)"
    )

    print(
        f"Short-circuit current Ik3     = "
        f"{final_design_check['short_circuit_current_ka']:.2f} kA "
        f"(prospective feeder-end short-circuit current)"
    )

    print()

    print(
        f"Cable current capacity        = "
        f"{final_design_check['cable_current_capacity_check']} "
        f"(IB <= Iz current-capacity condition)"
    )

    print(
        f"Cable selection               = "
        f"{final_design_check['cable_selection_check']} "
        f"(cable selection status)"
    )

    print(
        f"Steady-state voltage drop     = "
        f"{final_design_check['steady_state_voltage_drop_check']} "
        f"(steady-state voltage-drop check)"
    )

    print(
        f"Starting voltage drop         = "
        f"{final_design_check['motor_starting_voltage_drop_check']} "
        f"(motor starting voltage-drop check)"
    )

    print(
        f"Circuit breaker selection     = "
        f"{final_design_check['motor_circuit_breaker_selection_check']} "
        f"(motor circuit breaker selection status)"
    )

    print(
        f"Breaking capacity             = "
        f"{final_design_check['breaking_capacity_check']} "
        f"(circuit breaker short-circuit breaking capacity check)"
    )

    print(
        f"Contactor selection           = "
        f"{final_design_check['contactor_selection_check']} "
        f"(motor contactor selection status)"
    )

    print(
        f"Type 2 coordination           = "
        f"{final_design_check['type_2_coordination_check']} "
        f"(Schneider Electric motor starter coordination check)"
    )

    print()

    print(
        f"Initial circuit breaker       = "
        f"{final_design_check['initial_breaker_reference']} "
        f"(initially selected motor protection device)"
    )

    print(
        f"Initial contactor             = "
        f"{final_design_check['initial_contactor_reference']} "
        f"(initially selected motor contactor)"
    )

    print()

    print(
        f"Final circuit breaker         = "
        f"{final_design_check['final_breaker_reference']} "
        f"(final motor protection device reference)"
    )

    print(
        f"Final contactor               = "
        f"{final_design_check['final_contactor_reference']} "
        f"(final motor contactor reference)"
    )

    print(
        f"Final coordination source     = "
        f"{final_design_check['final_coordination_source']} "
        f"(final equipment combination source)"
    )

    print()

    print(
        f"Failed design checks          = "
        f"{final_design_check['failed_design_check_count']} "
        f"(number of failed final design checks)"
    )

    if final_design_check["failed_design_checks"]:

        print(
            f"Failed check list             = "
            f"{', '.join(final_design_check['failed_design_checks'])} "
            f"(final design checks requiring correction)"
        )

    print()

    print(
        f"FINAL DESIGN STATUS           = "
        f"{final_design_check['final_design_status']} "
        f"(final motor feeder design assessment)"
    )

    print("=" * 76)

    # =========================================================================
    # WORD REPORT
    # =========================================================================

    print()
    print("=" * 76)
    print("WORD REPORT")
    print("=" * 76)

    report_path = create_ac_motor_feeder_word_report(
        motor=motor,
        installation=installation,
        supply=supply,
        design_current=design_current,
        starting_current=starting_current,
        cable=cable,
        voltage_drop=voltage_drop,
        starting_voltage_drop=starting_voltage_drop,
        short_circuit=short_circuit,
        motor_circuit_breaker=motor_circuit_breaker,
        contactor=contactor,
        motor_starter_coordination=motor_starter_coordination,
        motor_starter_coordination_optimization=(
            motor_starter_coordination_optimization
        ),
        final_design_check=final_design_check,
    )

    print()

    print(
        f"Word report created           = "
        f"{report_path} "
        f"(AC motor feeder technical calculation report)"
    )

    print("=" * 76)

 # =========================================================================
    # OPEN WORD REPORT
 # =========================================================================

    import os

    os.startfile(report_path)

# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

if __name__ == "__main__":

    main()