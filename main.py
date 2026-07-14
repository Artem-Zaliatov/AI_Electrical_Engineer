"""
Digital Electrical Engineer (DEE)

Asynchronous Motor Design
Kopylov Design Method

SECTION 1
SELECTION OF MAIN DIMENSIONS
"""

import math


# ================================================================
# DEE MODULES
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


# ================================================================
# INITIAL DATA
# KOPYLOV REFERENCE EXAMPLE
# ================================================================

P2 = 15.0
U1 = 380
poles = 4
protection = "IP44"
f1 = 50.0


# ================================================================
# PRELIMINARY VALUES
# ================================================================

kw1 = 0.95


# ================================================================
# AUXILIARY FUNCTION
# ================================================================

def get_selected_value(result):
    """
    Returns the selected engineering value.

    If a DEE module returns:
        value

    the value is returned directly.

    If a DEE module returns:
        (value, minimum, maximum)

    the first element is returned.
    """

    if isinstance(result, tuple):
        return result[0]

    return result


# ================================================================
# MAIN CALCULATION
# ================================================================

def main():

    print()
    print("=" * 76)
    print("DIGITAL ELECTRICAL ENGINEER (DEE)")
    print("ASYNCHRONOUS MOTOR DESIGN")
    print("KOPYLOV DESIGN METHOD")
    print("=" * 76)

    print()
    print("INITIAL DATA")
    print("-" * 76)

    print(f"Rated output power P2          = {P2:.2f} kW")
    print(f"Rated line voltage U1          = {U1} V")
    print(f"Number of poles 2p             = {poles}")
    print(f"Protection degree              = {protection}")
    print(f"Supply frequency f1            = {f1:.1f} Hz")

    print()
    print("=" * 76)
    print("SECTION 1 - SELECTION OF MAIN DIMENSIONS")
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

    h = get_selected_value(h_result)

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

    if isinstance(Da_result, tuple):

        Da = Da_result[0]

        if len(Da_result) >= 3:
            Da_min = Da_result[1]
            Da_max = Da_result[2]
        else:
            Da_min = Da
            Da_max = Da

    else:

        Da = Da_result
        Da_min = Da
        Da_max = Da

    print(
        f"02. Stator outer diameter Da"
        f"                 = {Da:.3f} m"
    )

    print(
        f"    Recommended Da range"
        f"                          = "
        f"{Da_min:.3f} ... {Da_max:.3f} m"
    )


    # ============================================================
    # P03
    # INNER DIAMETER COEFFICIENT
    # ============================================================

    Kd_result = select_inner_diameter_coefficient(
        poles=poles,
    )

    Kd = get_selected_value(Kd_result)

    print(
        f"03. Inner diameter coefficient Kd"
        f"              = {Kd:.2f}"
    )


    # ============================================================
    # STATOR INNER DIAMETER
    #
    # D = Kd * Da
    # ============================================================

    D = Kd * Da

    print(
        f"    Stator inner diameter D = Kd * Da"
        f"            = {D:.3f} m"
    )


    # ============================================================
    # POLE PITCH
    #
    # tau = pi * D / 2p
    # ============================================================

    tau = math.pi * D / poles

    print(
        f"    Pole pitch tau = pi * D / 2p"
        f"               = {tau:.3f} m"
    )


    # ============================================================
    # P04
    # VOLTAGE COEFFICIENT Ke
    # ============================================================

    Ke_result = select_voltage_coefficient(
        Da=Da,
        poles=poles,
    )

    Ke = get_selected_value(Ke_result)

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

    eta = get_selected_value(eta_result)

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

    cos_phi = get_selected_value(cos_phi_result)

    print(
        f"06. Preliminary power factor cos(phi)"
        f"           = {cos_phi:.3f}"
    )


    # ============================================================
    # CALCULATED POWER P'
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
    #
    # Da selected previously in P02
    # ============================================================

    (
        B_delta,
        B_delta_min,
        B_delta_max,
    ) = select_air_gap_flux_density(
        h=h,
        Da=Da,
        poles=poles,
        protection=protection,
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
    #
    # Da selected previously in P02
    # ============================================================

    (
        A,
        A_min,
        A_max,
    ) = select_linear_current_loading(
        h=h,
        Da=Da,
        poles=poles,
        protection=protection,
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
    # SYNCHRONOUS SPEED
    # ============================================================

    p = poles / 2

    n1_rpm = 60 * f1 / p

    n1 = n1_rpm / 60


    # ============================================================
    # CALCULATED CORE LENGTH
    # ============================================================

    l_delta = (
        P_prime
        / (
            math.pi ** 2
            * D ** 2
            * n1
            * A
            * B_delta
            * kw1
        )
    )

    print()

    print(
        f"    Winding factor kw1"
        f"                            = {kw1:.3f}"
    )

    print(
        f"    Synchronous speed n1"
        f"                          = {n1_rpm:.0f} rpm"
    )

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
    # SECTION 1 RESULTS
    # ============================================================

    print()
    print("=" * 76)
    print("SECTION 1 RESULTS")
    print("=" * 76)

    print(f"h               = {h} mm")
    print(f"Da              = {Da:.3f} m")

    print(
        f"Da range        = "
        f"{Da_min:.3f} ... {Da_max:.3f} m"
    )

    print(f"Kd              = {Kd:.2f}")
    print(f"D               = {D:.3f} m")
    print(f"tau             = {tau:.3f} m")
    print(f"Ke              = {Ke:.3f}")
    print(f"eta             = {eta:.3f}")
    print(f"cos_phi         = {cos_phi:.3f}")
    print(f"P'              = {P_prime:.0f} VA")

    print(f"B_delta         = {B_delta:.3f} T")

    print(
        f"B_delta range   = "
        f"{B_delta_min:.3f} ... "
        f"{B_delta_max:.3f} T"
    )

    print(f"A               = {A:.0f} A/m")

    print(
        f"A range         = "
        f"{A_min:.0f} ... "
        f"{A_max:.0f} A/m"
    )

    print(f"kw1             = {kw1:.3f}")
    print(f"n1              = {n1_rpm:.0f} rpm")
    print(f"l_delta         = {l_delta:.3f} m")

    print(
        f"lambda          = "
        f"{lambda_result['lambda']:.3f}"
    )

    print(
        f"lambda range    = "
        f"{lambda_result['lambda_min']:.3f} ... "
        f"{lambda_result['lambda_max']:.3f}"
    )

    print(
        f"lambda check    = "
        f"{lambda_result['status']}"
    )

    print("=" * 76)


# ================================================================
# PROGRAM START
# ================================================================

if __name__ == "__main__":
    main()