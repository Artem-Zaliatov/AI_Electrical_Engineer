"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
CABLE CURRENT-CARRYING CAPACITY

Methodological basis:
- Schneider Electric Electrical Installation Guide;
- IEC 60364-5-52 cable sizing methodology.

Current supported configuration:
- copper conductor;
- PVC insulation, 70 deg C;
- three loaded conductors;
- installation method C;
- cable installed in air.

Cable sizing sequence:

    IB
     ↓
    ambient temperature correction factor k1
     ↓
    grouping correction factor k4
     ↓
    required tabulated current Iz_required
     ↓
    cable current-carrying capacity table
     ↓
    smallest permissible conductor cross-section

The current-carrying capacity values in this module correspond
to the supported IEC reference configuration defined above.
"""


# =============================================================================
# CABLE SIZING ERROR
# =============================================================================

class CableSizingError(ValueError):
    """
    Error raised when cable sizing cannot be performed.
    """

    pass


# =============================================================================
# AMBIENT AIR TEMPERATURE CORRECTION FACTORS
#
# PVC insulation, 70 deg C
# Reference ambient air temperature = 30 deg C
#
# IEC 60364-5-52 / Schneider Electric Electrical Installation Guide
# =============================================================================

PVC_AIR_TEMPERATURE_FACTORS = {
    10: 1.22,
    15: 1.17,
    20: 1.12,
    25: 1.06,
    30: 1.00,
    35: 0.94,
    40: 0.87,
    45: 0.79,
    50: 0.71,
    55: 0.61,
    60: 0.50,
}


# =============================================================================
# GROUPING CORRECTION FACTORS
#
# Bunched cables / circuits grouped together.
#
# Current DEE implementation uses a conservative grouping-factor table
# for the supported installation configuration.
#
# IMPORTANT:
# Product-specific or installation-specific cases will later be expanded
# using additional Schneider Electric / IEC tables.
# =============================================================================

GROUPING_FACTORS = {
    1: 1.00,
    2: 0.80,
    3: 0.70,
    4: 0.65,
    5: 0.60,
    6: 0.57,
    7: 0.54,
    8: 0.52,
    9: 0.50,
    12: 0.45,
    16: 0.41,
    20: 0.38,
}


# =============================================================================
# CURRENT-CARRYING CAPACITY TABLE
#
# Copper conductors
# PVC insulation, 70 deg C
# Three loaded conductors
# Installation method C
#
# Values: conductor cross-section, mm2 -> current capacity, A
# =============================================================================

CU_PVC_METHOD_C_3_LOADED = {
    1.5: 17.5,
    2.5: 24.0,
    4.0: 32.0,
    6.0: 41.0,
    10.0: 57.0,
    16.0: 76.0,
    25.0: 96.0,
    35.0: 119.0,
    50.0: 144.0,
    70.0: 184.0,
    95.0: 223.0,
    120.0: 259.0,
    150.0: 299.0,
    185.0: 341.0,
    240.0: 403.0,
    300.0: 464.0,
}


# =============================================================================
# LINEAR INTERPOLATION
# =============================================================================

def linear_interpolate(
    x,
    x1,
    y1,
    x2,
    y2,
):
    """
    Perform linear interpolation.
    """

    if x2 == x1:
        return float(y1)

    return (
        y1
        + (
            (y2 - y1)
            * (x - x1)
            / (x2 - x1)
        )
    )


# =============================================================================
# TEMPERATURE FACTOR SELECTION
# =============================================================================

def select_temperature_factor(
    ambient_temperature_c,
):
    """
    Select or interpolate the ambient air temperature
    correction factor for PVC insulated cables.
    """

    temperature = float(
        ambient_temperature_c
    )

    temperatures = sorted(
        PVC_AIR_TEMPERATURE_FACTORS
    )

    minimum_temperature = temperatures[0]
    maximum_temperature = temperatures[-1]

    if not minimum_temperature <= temperature <= maximum_temperature:
        raise CableSizingError(
            f"Ambient temperature {temperature:.1f} deg C is outside "
            f"the supported PVC air correction-factor range "
            f"{minimum_temperature} ... {maximum_temperature} deg C."
        )

    if temperature in PVC_AIR_TEMPERATURE_FACTORS:
        return PVC_AIR_TEMPERATURE_FACTORS[
            temperature
        ]

    for index in range(
        len(temperatures) - 1
    ):
        t1 = temperatures[index]
        t2 = temperatures[index + 1]

        if t1 <= temperature <= t2:
            return linear_interpolate(
                x=temperature,
                x1=t1,
                y1=PVC_AIR_TEMPERATURE_FACTORS[t1],
                x2=t2,
                y2=PVC_AIR_TEMPERATURE_FACTORS[t2],
            )

    raise CableSizingError(
        "Ambient temperature correction factor "
        "could not be determined."
    )


# =============================================================================
# GROUPING FACTOR SELECTION
# =============================================================================

def select_grouping_factor(
    grouped_circuits,
):
    """
    Select the grouping correction factor.

    Exact tabulated values are used.

    Intermediate numbers of circuits are conservatively assigned
    to the next available higher number of grouped circuits.
    """

    circuits = int(
        grouped_circuits
    )

    if circuits <= 0:
        raise CableSizingError(
            "Number of grouped circuits must be greater than zero."
        )

    available_groups = sorted(
        GROUPING_FACTORS
    )

    if circuits > available_groups[-1]:
        raise CableSizingError(
            f"Grouped circuits = {circuits} is outside "
            f"the supported grouping-factor table."
        )

    if circuits in GROUPING_FACTORS:
        return GROUPING_FACTORS[
            circuits
        ]

    for group_number in available_groups:
        if circuits <= group_number:
            return GROUPING_FACTORS[
                group_number
            ]

    raise CableSizingError(
        "Grouping correction factor could not be determined."
    )


# =============================================================================
# CABLE CURRENT CAPACITY SELECTION
# =============================================================================

def select_cable_current_capacity(
    design_current,
    installation,
):
    """
    Select cable cross-section by current-carrying capacity.

    Required tabulated current:

        Iz_required = IB / (k1 * k4)

    where:

        IB - motor circuit design current, A;
        k1 - ambient air temperature correction factor;
        k4 - grouping correction factor.

    The smallest cable cross-section with tabulated current
    capacity not lower than Iz_required is selected.
    """

    # -------------------------------------------------------------------------
    # INPUT DATA CHECK
    # -------------------------------------------------------------------------

    if not isinstance(design_current, dict):
        raise CableSizingError(
            "Design current data must be provided as a dictionary."
        )

    if not isinstance(installation, dict):
        raise CableSizingError(
            "Installation data must be provided as a dictionary."
        )

    if "design_current_a" not in design_current:
        raise CableSizingError(
            "Design current IB is missing."
        )

    required_installation_parameters = (
        "conductor_material",
        "insulation",
        "installation_method",
        "installation_environment",
        "loaded_conductors",
        "ambient_temperature_c",
        "grouped_circuits",
    )

    for parameter in required_installation_parameters:
        if parameter not in installation:
            raise CableSizingError(
                f"Required installation parameter "
                f"'{parameter}' is missing."
            )

    # -------------------------------------------------------------------------
    # SUPPORTED CONFIGURATION CHECK
    # -------------------------------------------------------------------------

    if installation["conductor_material"] != "CU":
        raise CableSizingError(
            "Current cable table supports only copper conductors."
        )

    if installation["insulation"] != "PVC":
        raise CableSizingError(
            "Current cable table supports only PVC insulation."
        )

    if installation["installation_method"] != "C":
        raise CableSizingError(
            "Current cable table supports only installation method C."
        )

    if installation["installation_environment"] != "AIR":
        raise CableSizingError(
            "Current cable table supports only cables installed in air."
        )

    if installation["loaded_conductors"] != 3:
        raise CableSizingError(
            "Current cable table supports only three loaded conductors."
        )

    # -------------------------------------------------------------------------
    # DESIGN CURRENT
    # -------------------------------------------------------------------------

    design_current_a = float(
        design_current["design_current_a"]
    )

    if design_current_a <= 0:
        raise CableSizingError(
            "Design current IB must be greater than zero."
        )

    # -------------------------------------------------------------------------
    # CORRECTION FACTORS
    # -------------------------------------------------------------------------

    temperature_factor = select_temperature_factor(
        installation["ambient_temperature_c"]
    )

    grouping_factor = select_grouping_factor(
        installation["grouped_circuits"]
    )

    total_correction_factor = (
        temperature_factor
        * grouping_factor
    )

    if total_correction_factor <= 0:
        raise CableSizingError(
            "Total cable correction factor must be greater than zero."
        )

    # -------------------------------------------------------------------------
    # REQUIRED TABULATED CURRENT CAPACITY
    # -------------------------------------------------------------------------

    required_tabulated_current_a = (
        design_current_a
        / total_correction_factor
    )

    # -------------------------------------------------------------------------
    # CABLE SELECTION
    # -------------------------------------------------------------------------

    selected_cross_section_mm2 = None
    selected_tabulated_current_a = None

    for (
        cross_section_mm2,
        tabulated_current_a,
    ) in CU_PVC_METHOD_C_3_LOADED.items():

        if (
            tabulated_current_a
            >= required_tabulated_current_a
        ):
            selected_cross_section_mm2 = (
                cross_section_mm2
            )

            selected_tabulated_current_a = (
                tabulated_current_a
            )

            break

    if selected_cross_section_mm2 is None:
        raise CableSizingError(
            f"Required tabulated current capacity "
            f"{required_tabulated_current_a:.2f} A exceeds "
            f"the supported cable table range."
        )

    # -------------------------------------------------------------------------
    # CORRECTED CURRENT-CARRYING CAPACITY
    # -------------------------------------------------------------------------

    corrected_current_capacity_a = (
        selected_tabulated_current_a
        * total_correction_factor
    )

    # -------------------------------------------------------------------------
    # CURRENT CAPACITY CHECK
    # -------------------------------------------------------------------------

    if corrected_current_capacity_a >= design_current_a:
        current_capacity_check = "PERMISSIBLE"
    else:
        current_capacity_check = "NOT PERMISSIBLE"

    # -------------------------------------------------------------------------
    # RESULT
    # -------------------------------------------------------------------------

    result = {
        "design_current_a":
            design_current_a,

        "temperature_factor":
            temperature_factor,

        "grouping_factor":
            grouping_factor,

        "total_correction_factor":
            total_correction_factor,

        "required_tabulated_current_a":
            required_tabulated_current_a,

        "selected_cross_section_mm2":
            selected_cross_section_mm2,

        "selected_tabulated_current_a":
            selected_tabulated_current_a,

        "corrected_current_capacity_a":
            corrected_current_capacity_a,

        "current_capacity_check":
            current_capacity_check,

        "cable_table_source":
            "IEC 60364-5-52 / SCHNEIDER ELECTRIC EIG",

        "cable_selection_status":
            "SELECTED",
    }

    return result


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_design_current = {
        "design_current_a": 28.5,
    }

    test_installation = {
        "conductor_material": "CU",
        "insulation": "PVC",
        "installation_method": "C",
        "installation_environment": "AIR",
        "loaded_conductors": 3,
        "ambient_temperature_c": 40.0,
        "grouped_circuits": 1,
    }

    result = select_cable_current_capacity(
        design_current=test_design_current,
        installation=test_installation,
    )

    print("=" * 76)
    print("DEE - CABLE CURRENT-CARRYING CAPACITY")
    print("=" * 76)

    print()

    print(
        f"Motor design current IB       = "
        f"{result['design_current_a']:.2f} A "
        f"(motor feeder design current)"
    )

    print()

    print(
        f"Temperature factor k1         = "
        f"{result['temperature_factor']:.3f} "
        f"(ambient air temperature correction factor)"
    )

    print(
        f"Grouping factor k4            = "
        f"{result['grouping_factor']:.3f} "
        f"(grouped circuits correction factor)"
    )

    print(
        f"Total correction factor       = "
        f"{result['total_correction_factor']:.3f} "
        f"(product of applicable correction factors)"
    )

    print()

    print(
        f"Required tabulated current Iz = "
        f"{result['required_tabulated_current_a']:.2f} A "
        f"(minimum required table current capacity)"
    )

    print()

    print(
        f"Selected conductor section S  = "
        f"{result['selected_cross_section_mm2']:.1f} mm2 "
        f"(selected phase conductor cross-section)"
    )

    print(
        f"Tabulated current capacity    = "
        f"{result['selected_tabulated_current_a']:.2f} A "
        f"(reference current-carrying capacity)"
    )

    print(
        f"Corrected current capacity    = "
        f"{result['corrected_current_capacity_a']:.2f} A "
        f"(current capacity after correction factors)"
    )

    print()

    print(
        f"Current capacity check        = "
        f"{result['current_capacity_check']} "
        f"(corrected cable capacity versus motor design current)"
    )

    print(
        f"Cable table source            = "
        f"{result['cable_table_source']} "
        f"(cable sizing methodology source)"
    )

    print(
        f"Cable selection status        = "
        f"{result['cable_selection_status']} "
        f"(cable current-capacity selection status)"
    )

    print("=" * 76)