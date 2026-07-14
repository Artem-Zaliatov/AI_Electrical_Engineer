"""
Digital Electrical Engineer (DEE)

Asynchronous Motor Design
Kopylov Design Method

SECTION 1
SELECTION OF MAIN DIMENSIONS

The program performs:

    1. Initial data input.
    2. Selection of main dimensions.
    3. Lambda ratio check.
    4. Automatic optimization if required.
    5. Microsoft Word report generation.
"""

import math


# ================================================================
# DEE CALCULATION MODULES
# ================================================================

from src.p01_h_shaft_height import (
    select_shaft_height,
)

from src.p02_Da_stator_outer_diameter import (
    select_outer_stator_diameter,
)

from src.p03_Kd_inner_diameter_coefficient import (
    select_inner_diameter_coefficient,
)

from src.p04_Ke_coefficient import (
    select_voltage_coefficient,
)

from src.p05_eta_efficiency import (
    select_efficiency,
)

from src.p06_cos_phi_power_factor import (
    select_power_factor,
)

from src.p07_Bdelta_air_gap_flux_density import (
    select_air_gap_flux_density,
)

from src.p08_A_linear_current_loading import (
    select_linear_current_loading,
)

from src.p09_lambda_ratio_check import (
    check_lambda_ratio,
)

from src.main_dimensions_optimizer import (
    optimize_main_dimensions,
)


# ================================================================
# DEE REPORT MODULES
# ================================================================

from src.reports.section01_word_report import (
    create_section01_word_report,
)


# ================================================================
# INITIAL DATA
# ================================================================

P2 = 37.0
U1 = 380
poles = 6
protection = "IP23"
f1 = 50.0


# ================================================================
# PRELIMINARY KOPYLOV COEFFICIENTS
# ================================================================

alpha_delta = 2 / math.pi

k_B = math.pi / (
    2 * math.sqrt(2)
)

kw1 = 0.95


# ================================================================
# AUXILIARY FUNCTIONS
# ================================================================

def get_selected_value(result):
    """
    Return the selected engineering value.

    Supported result formats:

        value

    or:

        (value, minimum, maximum)
    """

    if isinstance(result, tuple):

        return result[0]

    return result


def get_value_range(result):
    """
    Return:

        selected
        minimum
        maximum
    """

    if isinstance(result, tuple):

        if len(result) >= 3:

            return (
                result[0],
                result[1],
                result[2],
            )

        if len(result) == 2:

            return (
                result[0],
                result[1],
                result[1],
            )

        if len(result) == 1:

            return (
                result[0],
                result[0],
                result[0],
            )

    return (
        result,
        result,
        result,
    )


# ================================================================
# MAIN CALCULATION
# ================================================================

def main():

    # ============================================================
    # PROGRAM HEADER
    # ============================================================

    print()

    print("=" * 76)

    print(
        "DIGITAL ELECTRICAL ENGINEER (DEE)"
    )

    print(
        "ASYNCHRONOUS MOTOR DESIGN"
    )

    print(
        "KOPYLOV DESIGN METHOD"
    )

    print("=" * 76)


    # ============================================================
    # INITIAL DATA
    # ============================================================

    print()

    print(
        "INITIAL DATA"
    )

    print("-" * 76)

    print(
        f"Rated output power P2"
        f"          = {P2:.2f} kW"
    )

    print(
        f"Rated line voltage U1"
        f"          = {U1} V"
    )

    print(
        f"Number of poles 2p"
        f"             = {poles}"
    )

    print(
        f"Protection degree"
        f"              = {protection}"
    )

    print(
        f"Supply frequency f1"
        f"            = {f1:.1f} Hz"
    )


    # ============================================================
    # SECTION 1
    # ============================================================

    print()

    print("=" * 76)

    print(
        "SECTION 1 - SELECTION OF MAIN DIMENSIONS"
    )

    print("=" * 76)

    print()


    # ============================================================
    # P01
    # SHAFT HEIGHT
    # ============================================================

    h_result = select_shaft_height(
        power_kw=P2,
        poles=poles,
        protection=protection,
    )

    h = get_selected_value(
        h_result
    )

    print(
        f"01. Shaft height h"
        f"                         = {h} mm"
    )


    # ============================================================
    # P02
    # STATOR OUTER DIAMETER
    # ============================================================

    Da_result = select_outer_stator_diameter(
        shaft_height_mm=h,
    )

    (
        Da,
        Da_min,
        Da_max,
    ) = get_value_range(
        Da_result
    )

    print(
        f"02. Stator outer diameter Da"
        f"                 = {Da:.3f} m"
    )

    print(
        f"    Recommended Da range"
        f"                          = "
        f"{Da_min:.3f} ... "
        f"{Da_max:.3f} m"
    )


    # ============================================================
    # P03
    # INNER DIAMETER COEFFICIENT
    # ============================================================

    Kd_result = select_inner_diameter_coefficient(
        poles=poles,
    )

    (
        Kd,
        Kd_min,
        Kd_max,
    ) = get_value_range(
        Kd_result
    )

    print(
        f"03. Inner diameter coefficient Kd"
        f"              = {Kd:.2f}"
    )

    print(
        f"    Recommended Kd range"
        f"                          = "
        f"{Kd_min:.2f} ... "
        f"{Kd_max:.2f}"
    )


    # ============================================================
    # STATOR INNER DIAMETER
    #
    # D = Kd * Da
    # ============================================================

    D = (
        Kd
        * Da
    )

    print(
        f"    Stator inner diameter D = Kd * Da"
        f"            = {D:.3f} m"
    )


    # ============================================================
    # POLE PITCH
    #
    # tau = pi * D / 2p
    # ============================================================

    tau = (
        math.pi
        * D
        / poles
    )

    print(
        f"    Pole pitch tau = pi * D / 2p"
        f"               = {tau:.3f} m"
    )


    # ============================================================
    # P04
    # VOLTAGE COEFFICIENT KE
    # ============================================================

    Ke_result = select_voltage_coefficient(
        Da=Da,
        poles=poles,
    )

    Ke = get_selected_value(
        Ke_result
    )

    print(
        f"04. Voltage coefficient Ke"
        f"                    = {Ke:.3f}"
    )


    # ============================================================
    # P05
    # PRELIMINARY EFFICIENCY
    # ============================================================

    eta_result = select_efficiency(
        power_kw=P2,
        poles=poles,
        protection=protection,
    )

    eta = get_selected_value(
        eta_result
    )

    print(
        f"05. Preliminary efficiency eta"
        f"                = {eta:.3f}"
    )


    # ============================================================
    # P06
    # PRELIMINARY POWER FACTOR
    # ============================================================

    cos_phi_result = select_power_factor(
        power_kw=P2,
        poles=poles,
        protection=protection,
    )

    cos_phi = get_selected_value(
        cos_phi_result
    )

    print(
        f"06. Preliminary power factor cos(phi)"
        f"           = {cos_phi:.3f}"
    )


    # ============================================================
    # CALCULATED POWER
    #
    # P' = P2 * Ke / (eta * cos_phi)
    # ============================================================

    P_prime = (
        P2
        * 1000
        * Ke
        / (
            eta
            * cos_phi
        )
    )

    print()

    print(
        f"    Calculated power P'"
        f"                          = {P_prime:.0f} VA"
    )


    # ============================================================
    # P07
    # AIR-GAP FLUX DENSITY
    # ============================================================

    B_delta_result = select_air_gap_flux_density(
        h=h,
        Da=Da,
        poles=poles,
        protection=protection,
    )

    (
        B_delta,
        B_delta_min,
        B_delta_max,
    ) = get_value_range(
        B_delta_result
    )

    print()

    print(
        f"07. Air-gap flux density B_delta"
        f"               = {B_delta:.3f} T"
    )

    print(
        f"    Recommended B_delta range"
        f"                    = "
        f"{B_delta_min:.3f} ... "
        f"{B_delta_max:.3f} T"
    )


    # ============================================================
    # P08
    # LINEAR CURRENT LOADING
    # ============================================================

    A_result = select_linear_current_loading(
        h=h,
        Da=Da,
        poles=poles,
        protection=protection,
    )

    (
        A,
        A_min,
        A_max,
    ) = get_value_range(
        A_result
    )

    print()

    print(
        f"08. Linear current loading A"
        f"                   = {A:.0f} A/m"
    )

    print(
        f"    Recommended A range"
        f"                          = "
        f"{A_min:.0f} ... "
        f"{A_max:.0f} A/m"
    )


    # ============================================================
    # KOPYLOV PRELIMINARY COEFFICIENTS
    # ============================================================

    print()

    print(
        f"    Air-gap flux curve coefficient alpha_delta"
        f"      = {alpha_delta:.3f}"
    )

    print(
        f"    Magnetic field form coefficient k_B"
        f"          = {k_B:.3f}"
    )

    print(
        f"    Preliminary winding factor kw1"
        f"              = {kw1:.3f}"
    )


    # ============================================================
    # SYNCHRONOUS SPEED
    # ============================================================

    pole_pairs = (
        poles
        / 2
    )

    n1_rpm = (
        60
        * f1
        / pole_pairs
    )


    # ============================================================
    # SYNCHRONOUS ANGULAR FREQUENCY
    #
    # Omega = 2 * pi * f1 / p
    # ============================================================

    Omega = (
        2
        * math.pi
        * f1
        / pole_pairs
    )

    print()

    print(
        f"    Synchronous speed n1"
        f"                          = {n1_rpm:.0f} rpm"
    )

    print(
        f"    Synchronous angular frequency Omega"
        f"             = {Omega:.3f} rad/s"
    )


    # ============================================================
    # CALCULATED CORE LENGTH
    #
    # KOPYLOV FORMULA (9.6)
    #
    #                 P'
    # l_delta = -------------------------------
    #           D^2 * Omega * k_B * kw1 * A * B_delta
    #
    # alpha_delta = 2 / pi is already included
    # in the derivation of formula (9.6).
    # ============================================================

    l_delta = (
        P_prime
        / (
            D ** 2
            * Omega
            * k_B
            * kw1
            * A
            * B_delta
        )
    )

    print()

    print(
        f"    Calculated core length l_delta"
        f"                 = {l_delta:.3f} m"
    )


    # ============================================================
    # P09
    # LAMBDA CHECK
    # ============================================================

    lambda_result = check_lambda_ratio(
        h=h,
        l_delta=l_delta,
        tau=tau,
        poles=poles,
        protection=protection,
    )

    print()

    print(
        f"09. Lambda ratio lambda = l_delta / tau"
        f"           = "
        f"{lambda_result['lambda']:.3f}"
    )

    print(
        f"    Permissible lambda range"
        f"                      = "
        f"{lambda_result['lambda_min']:.3f} ... "
        f"{lambda_result['lambda_max']:.3f}"
    )

    print(
        f"    Lambda check status"
        f"                           = "
        f"{lambda_result['status']}"
    )

    print(
        f"    Kopylov diagram"
        f"                                = "
        f"{lambda_result['figure']}"
    )


    # ============================================================
    # INITIAL FINAL RESULT
    # ============================================================

    final_result = None


    # ============================================================
    # INITIAL DESIGN IS PERMISSIBLE
    # ============================================================

    if lambda_result["status"] == "PERMISSIBLE":

        final_result = {

            "h": h,

            "Da": Da,

            "Da_min": Da_min,

            "Da_max": Da_max,

            "Kd": Kd,

            "Kd_min": Kd_min,

            "Kd_max": Kd_max,

            "D": D,

            "tau": tau,

            "Ke": Ke,

            "eta": eta,

            "cos_phi": cos_phi,

            "P_prime": P_prime,

            "B_delta": B_delta,

            "B_delta_min": B_delta_min,

            "B_delta_max": B_delta_max,

            "A": A,

            "A_min": A_min,

            "A_max": A_max,

            "alpha_delta": alpha_delta,

            "k_B": k_B,

            "kw1": kw1,

            "n1_rpm": n1_rpm,

            "Omega": Omega,

            "l_delta": l_delta,

            "lambda": lambda_result[
                "lambda"
            ],

            "lambda_min": lambda_result[
                "lambda_min"
            ],

            "lambda_max": lambda_result[
                "lambda_max"
            ],

            "status": lambda_result[
                "status"
            ],

            "figure": lambda_result[
                "figure"
            ],

            "optimized": False,
        }


    # ============================================================
    # INITIAL DESIGN IS NOT PERMISSIBLE
    # ============================================================

    else:

        print()

        print(
            "Initial design is NOT PERMISSIBLE."
        )

        print(
            "Starting automatic parameter optimization..."
        )

        final_result = optimize_main_dimensions(
            P2=P2,
            poles=poles,
            protection=protection,
            h=h,
            f1=f1,
            kw1=kw1,
            verbose=True,
        )

        if final_result is not None:

            final_result[
                "optimized"
            ] = True


    # ============================================================
    # SECTION 1 RESULTS
    # ============================================================

    print()

    print("=" * 76)

    print(
        "SECTION 1 RESULTS"
    )

    print("=" * 76)


    # ============================================================
    # NO PERMISSIBLE DESIGN
    # ============================================================

    if final_result is None:

        print()

        print(
            "NO PERMISSIBLE DESIGN VARIANT FOUND"
        )

        print()

        print(
            "SECTION 1 DESIGN FAILED"
        )

        print("=" * 76)

        print()

        print(
            "WORD REPORT"
        )

        print("-" * 76)

        print(
            "Word report was NOT created."
        )

        print(
            "Reason: Section 1 has no permissible "
            "design result."
        )

        print("=" * 76)

        return


    # ============================================================
    # RESULT SOURCE
    # ============================================================

    print()

    if final_result["optimized"]:

        print(
            "RESULT SOURCE   = AUTOMATIC OPTIMIZATION"
        )

    else:

        print(
            "RESULT SOURCE   = INITIAL KOPYLOV SELECTION"
        )

    print()


    # ============================================================
    # PRINT FINAL RESULT
    # ============================================================

    print(
        f"h               = "
        f"{final_result['h']} mm"
    )

    print(
        f"Da              = "
        f"{final_result['Da']:.4f} m"
    )

    print(
        f"Da range        = "
        f"{final_result['Da_min']:.4f} ... "
        f"{final_result['Da_max']:.4f} m"
    )

    print(
        f"Kd              = "
        f"{final_result['Kd']:.4f}"
    )

    print(
        f"Kd range        = "
        f"{final_result['Kd_min']:.4f} ... "
        f"{final_result['Kd_max']:.4f}"
    )

    print(
        f"D               = "
        f"{final_result['D']:.4f} m"
    )

    print(
        f"tau             = "
        f"{final_result['tau']:.4f} m"
    )

    print(
        f"Ke              = "
        f"{final_result['Ke']:.4f}"
    )

    print(
        f"eta             = "
        f"{final_result['eta']:.4f}"
    )

    print(
        f"cos_phi         = "
        f"{final_result['cos_phi']:.4f}"
    )

    print(
        f"P'              = "
        f"{final_result['P_prime']:.0f} VA"
    )

    print(
        f"B_delta         = "
        f"{final_result['B_delta']:.4f} T"
    )

    print(
        f"B_delta range   = "
        f"{final_result['B_delta_min']:.4f} ... "
        f"{final_result['B_delta_max']:.4f} T"
    )

    print(
        f"A               = "
        f"{final_result['A']:.0f} A/m"
    )

    print(
        f"A range         = "
        f"{final_result['A_min']:.0f} ... "
        f"{final_result['A_max']:.0f} A/m"
    )

    print(
        f"alpha_delta     = "
        f"{final_result['alpha_delta']:.4f}"
    )

    print(
        f"k_B             = "
        f"{final_result['k_B']:.4f}"
    )

    print(
        f"kw1             = "
        f"{final_result['kw1']:.4f}"
    )

    print(
        f"n1              = "
        f"{final_result['n1_rpm']:.0f} rpm"
    )

    print(
        f"Omega           = "
        f"{final_result['Omega']:.3f} rad/s"
    )

    print(
        f"l_delta         = "
        f"{final_result['l_delta']:.4f} m"
    )

    print(
        f"lambda          = "
        f"{final_result['lambda']:.4f}"
    )

    print(
        f"lambda range    = "
        f"{final_result['lambda_min']:.4f} ... "
        f"{final_result['lambda_max']:.4f}"
    )

    print(
        f"lambda check    = "
        f"{final_result['status']}"
    )

    print("=" * 76)


    # ============================================================
    # WORD REPORT GENERATION
    # ============================================================

    print()

    print(
        "WORD REPORT"
    )

    print("-" * 76)

    try:

        report_path = create_section01_word_report(
            result=final_result,
            P2=P2,
            U1=U1,
            poles=poles,
            protection=protection,
            f1=f1,
        )

        print(
            "Section 1 Word report created successfully."
        )

        print(
            f"File: {report_path}"
        )

    except Exception as error:

        print(
            "ERROR: Word report could not be created."
        )

        print(
            f"Reason: {error}"
        )

        raise

    print("=" * 76)


# ================================================================
# PROGRAM START
# ================================================================

if __name__ == "__main__":

    main()