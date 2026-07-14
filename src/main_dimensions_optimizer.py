"""
Digital Electrical Engineer (DEE)

MAIN DIMENSIONS OPTIMIZER

Automatic optimization of the main dimensions
for Section 1 of the Kopylov asynchronous motor
design method.

The shaft height h is FIXED.

Optimized parameters:

    Da
    Kd
    B_delta
    A

All parameters are varied only within the
permissible ranges obtained from digitized
Kopylov reference data.

The calculated core length is determined
according to Kopylov formula (9.6):

                    P'
    l_delta = -------------------------------
              D^2 * Omega * k_B * kw1 * A * B_delta

where:

    Omega = 2 * pi * f1 / p

    k_B = pi / (2 * sqrt(2))

The coefficient:

    alpha_delta = 2 / pi

is already taken into account in the derivation
of Kopylov formula (9.6) and is not inserted
into the denominator again.
"""

import math


# ================================================================
# DEE MODULES
# ================================================================

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
# KOPYLOV COEFFICIENTS
# ================================================================

ALPHA_DELTA = 2 / math.pi

K_B = math.pi / (
    2 * math.sqrt(2)
)


# ================================================================
# AUXILIARY FUNCTIONS
# ================================================================

def get_selected_value(result):
    """
    Return selected engineering value.
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


def generate_values(
    minimum_value,
    maximum_value,
    number_of_points,
):
    """
    Generate equally spaced values inside
    the permissible engineering range.
    """

    if number_of_points <= 1:

        return [
            minimum_value
        ]

    if math.isclose(
        minimum_value,
        maximum_value,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):

        return [
            minimum_value
        ]

    step = (
        maximum_value
        - minimum_value
    ) / (
        number_of_points
        - 1
    )

    return [
        minimum_value
        + step * index

        for index
        in range(number_of_points)
    ]


# ================================================================
# SINGLE DESIGN VARIANT
# ================================================================

def calculate_design_variant(
    P2,
    poles,
    protection,
    f1,
    kw1,
    h,
    Da,
    Kd,
    B_delta,
    A,
    eta,
    cos_phi,
):
    """
    Calculate one complete design variant
    according to Kopylov formula (9.6).
    """


    # ============================================================
    # KE
    # ============================================================

    Ke_result = select_voltage_coefficient(
        Da=Da,
        poles=poles,
    )

    Ke = get_selected_value(
        Ke_result
    )


    # ============================================================
    # INNER STATOR DIAMETER
    #
    # D = Kd * Da
    # ============================================================

    D = Kd * Da


    # ============================================================
    # POLE PITCH
    #
    # tau = pi * D / 2p
    #
    # poles = 2p
    # ============================================================

    tau = (
        math.pi
        * D
        / poles
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


    # ============================================================
    # SYNCHRONOUS SPEED
    # ============================================================

    pole_pairs = poles / 2

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


    # ============================================================
    # CALCULATED CORE LENGTH
    #
    # KOPYLOV FORMULA (9.6)
    #
    #                 P'
    # l_delta = -------------------------------
    #           D^2 * Omega * k_B * kw1 * A * B_delta
    # ============================================================

    l_delta = (
        P_prime
        / (
            D ** 2
            * Omega
            * K_B
            * kw1
            * A
            * B_delta
        )
    )


    # ============================================================
    # LAMBDA CHECK
    # ============================================================

    lambda_result = check_lambda_ratio(
        h=h,
        l_delta=l_delta,
        tau=tau,
        poles=poles,
        protection=protection,
    )


    # ============================================================
    # RESULT
    # ============================================================

    return {
        "h": h,
        "Da": Da,
        "Kd": Kd,
        "D": D,
        "tau": tau,
        "Ke": Ke,
        "eta": eta,
        "cos_phi": cos_phi,
        "P_prime": P_prime,
        "B_delta": B_delta,
        "A": A,
        "alpha_delta": ALPHA_DELTA,
        "k_B": K_B,
        "kw1": kw1,
        "n1_rpm": n1_rpm,
        "Omega": Omega,
        "l_delta": l_delta,
        "lambda": lambda_result["lambda"],
        "lambda_min": lambda_result["lambda_min"],
        "lambda_max": lambda_result["lambda_max"],
        "status": lambda_result["status"],
        "figure": lambda_result["figure"],
    }


# ================================================================
# MAIN DIMENSIONS OPTIMIZER
# ================================================================

def optimize_main_dimensions(
    P2,
    poles,
    protection,
    h,
    f1=50.0,
    kw1=0.95,
    Da_points=21,
    Kd_points=31,
    B_delta_points=11,
    A_points=11,
    verbose=True,
):
    """
    Search for a permissible design variant.

    FIXED:

        h

    OPTIMIZED:

        Da
        Kd
        B_delta
        A

    PRIMARY OBJECTIVE:

        lambda must be within the permissible
        Kopylov Figure 9.25 range.

    OPTIMAL VARIANT:

        lambda closest to the centre of the
        permissible range.

    SECONDARY OBJECTIVE:

        selected parameters should remain as
        close as possible to the middle of their
        recommended Kopylov ranges.
    """


    # ============================================================
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


    # ============================================================
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


    # ============================================================
    # DA RANGE
    # ============================================================

    Da_result = select_outer_stator_diameter(
        shaft_height_mm=h,
    )

    (
        Da_selected,
        Da_min,
        Da_max,
    ) = get_value_range(
        Da_result
    )

    Da_values = generate_values(
        minimum_value=Da_min,
        maximum_value=Da_max,
        number_of_points=Da_points,
    )


    # ============================================================
    # KD RANGE
    # ============================================================

    Kd_result = select_inner_diameter_coefficient(
        poles=poles,
    )

    (
        Kd_selected,
        Kd_min,
        Kd_max,
    ) = get_value_range(
        Kd_result
    )

    Kd_values = generate_values(
        minimum_value=Kd_min,
        maximum_value=Kd_max,
        number_of_points=Kd_points,
    )


    # ============================================================
    # SEARCH HEADER
    # ============================================================

    if verbose:

        print()
        print("=" * 76)
        print("AUTOMATIC MAIN DIMENSIONS OPTIMIZATION")
        print("=" * 76)

        print()

        print(
            f"Fixed shaft height h"
            f"                    = {h} mm"
        )

        print(
            f"Da permissible range"
            f"                     = "
            f"{Da_min:.4f} ... "
            f"{Da_max:.4f} m"
        )

        print(
            f"Kd permissible range"
            f"                     = "
            f"{Kd_min:.4f} ... "
            f"{Kd_max:.4f}"
        )

        print()

        print(
            f"alpha_delta"
            f"                               = "
            f"{ALPHA_DELTA:.4f}"
        )

        print(
            f"k_B"
            f"                                       = "
            f"{K_B:.4f}"
        )

        print()

        print(
            "Searching permissible design variants..."
        )


    # ============================================================
    # SEARCH VARIABLES
    # ================================================================

    checked_variants = 0

    permissible_variants = 0

    best_variant = None

    best_score = float("inf")

    lambda_achieved_min = float("inf")

    lambda_achieved_max = float("-inf")


    # ============================================================
    # DESIGN SEARCH
    # ================================================================

    for Da in Da_values:


        # ========================================================
        # B_DELTA RANGE FOR CURRENT DA
        # ========================================================

        B_delta_result = select_air_gap_flux_density(
            h=h,
            Da=Da,
            poles=poles,
            protection=protection,
        )

        (
            B_delta_selected,
            B_delta_min,
            B_delta_max,
        ) = get_value_range(
            B_delta_result
        )

        B_delta_values = generate_values(
            minimum_value=B_delta_min,
            maximum_value=B_delta_max,
            number_of_points=B_delta_points,
        )


        # ========================================================
        # A RANGE FOR CURRENT DA
        # ========================================================

        A_result = select_linear_current_loading(
            h=h,
            Da=Da,
            poles=poles,
            protection=protection,
        )

        (
            A_selected,
            A_min,
            A_max,
        ) = get_value_range(
            A_result
        )

        A_values = generate_values(
            minimum_value=A_min,
            maximum_value=A_max,
            number_of_points=A_points,
        )


        # ========================================================
        # RANGE CENTRES
        # ========================================================

        Da_middle = (
            Da_min
            + Da_max
        ) / 2

        Kd_middle = (
            Kd_min
            + Kd_max
        ) / 2

        B_delta_middle = (
            B_delta_min
            + B_delta_max
        ) / 2

        A_middle = (
            A_min
            + A_max
        ) / 2


        # ========================================================
        # PARAMETER SEARCH
        # ========================================================

        for Kd in Kd_values:

            for B_delta in B_delta_values:

                for A in A_values:

                    checked_variants += 1


                    # ============================================
                    # CALCULATE VARIANT
                    # ============================================

                    variant = calculate_design_variant(
                        P2=P2,
                        poles=poles,
                        protection=protection,
                        f1=f1,
                        kw1=kw1,
                        h=h,
                        Da=Da,
                        Kd=Kd,
                        B_delta=B_delta,
                        A=A,
                        eta=eta,
                        cos_phi=cos_phi,
                    )


                    # ============================================
                    # LAMBDA STATISTICS
                    # ============================================

                    lambda_value = variant[
                        "lambda"
                    ]

                    lambda_achieved_min = min(
                        lambda_achieved_min,
                        lambda_value,
                    )

                    lambda_achieved_max = max(
                        lambda_achieved_max,
                        lambda_value,
                    )


                    # ============================================
                    # PERMISSIBILITY CHECK
                    # ============================================

                    if (
                        variant["lambda_min"]
                        <= lambda_value
                        <= variant["lambda_max"]
                    ):

                        permissible_variants += 1


                        # ========================================
                        # TARGET LAMBDA
                        # ========================================

                        lambda_target = (
                            variant["lambda_min"]
                            + variant["lambda_max"]
                        ) / 2


                        # ========================================
                        # PRIMARY SCORE
                        # ========================================

                        lambda_score = abs(
                            lambda_value
                            - lambda_target
                        )


                        # ========================================
                        # NORMALIZED PARAMETER SCORES
                        # ========================================

                        if not math.isclose(
                            Da_max,
                            Da_min,
                        ):

                            Da_score = abs(
                                Da
                                - Da_middle
                            ) / (
                                Da_max
                                - Da_min
                            )

                        else:

                            Da_score = 0.0


                        if not math.isclose(
                            Kd_max,
                            Kd_min,
                        ):

                            Kd_score = abs(
                                Kd
                                - Kd_middle
                            ) / (
                                Kd_max
                                - Kd_min
                            )

                        else:

                            Kd_score = 0.0


                        if not math.isclose(
                            B_delta_max,
                            B_delta_min,
                        ):

                            B_delta_score = abs(
                                B_delta
                                - B_delta_middle
                            ) / (
                                B_delta_max
                                - B_delta_min
                            )

                        else:

                            B_delta_score = 0.0


                        if not math.isclose(
                            A_max,
                            A_min,
                        ):

                            A_score = abs(
                                A
                                - A_middle
                            ) / (
                                A_max
                                - A_min
                            )

                        else:

                            A_score = 0.0


                        # ========================================
                        # SECONDARY SCORE
                        # ========================================

                        parameter_score = (
                            Da_score
                            + Kd_score
                            + B_delta_score
                            + A_score
                        )


                        # ========================================
                        # TOTAL SCORE
                        # ========================================

                        total_score = (
                            lambda_score
                            + 0.001
                            * parameter_score
                        )


                        # ========================================
                        # SAVE BEST VARIANT
                        # ========================================

                        if total_score < best_score:

                            best_score = total_score

                            best_variant = variant.copy()

                            best_variant[
                                "Da_min"
                            ] = Da_min

                            best_variant[
                                "Da_max"
                            ] = Da_max

                            best_variant[
                                "Kd_min"
                            ] = Kd_min

                            best_variant[
                                "Kd_max"
                            ] = Kd_max

                            best_variant[
                                "B_delta_min"
                            ] = B_delta_min

                            best_variant[
                                "B_delta_max"
                            ] = B_delta_max

                            best_variant[
                                "A_min"
                            ] = A_min

                            best_variant[
                                "A_max"
                            ] = A_max

                            best_variant[
                                "lambda_target"
                            ] = lambda_target

                            best_variant[
                                "optimization_score"
                            ] = total_score


    # ============================================================
    # NO SOLUTION
    # ================================================================

    if best_variant is None:

        if verbose:

            print()
            print("-" * 76)

            print(
                f"Checked variants"
                f"                           = "
                f"{checked_variants}"
            )

            print(
                f"Permissible variants"
                f"                       = 0"
            )

            print()

            print(
                f"Achievable lambda range"
                f"                    = "
                f"{lambda_achieved_min:.4f} ... "
                f"{lambda_achieved_max:.4f}"
            )

            print()

            print(
                "NO PERMISSIBLE DESIGN VARIANT FOUND"
            )

            print("=" * 76)

        return None


    # ============================================================
    # SEARCH STATISTICS
    # ================================================================

    best_variant[
        "checked_variants"
    ] = checked_variants

    best_variant[
        "permissible_variants"
    ] = permissible_variants

    best_variant[
        "lambda_achieved_min"
    ] = lambda_achieved_min

    best_variant[
        "lambda_achieved_max"
    ] = lambda_achieved_max


    # ============================================================
    # PRINT OPTIMAL VARIANT
    # ================================================================

    if verbose:

        print()
        print("-" * 76)

        print(
            f"Checked variants"
            f"                           = "
            f"{checked_variants}"
        )

        print(
            f"Permissible variants"
            f"                       = "
            f"{permissible_variants}"
        )

        print()

        print(
            f"Achievable lambda range"
            f"                    = "
            f"{lambda_achieved_min:.4f} ... "
            f"{lambda_achieved_max:.4f}"
        )

        print()

        print("=" * 76)
        print("SELECTED OPTIMAL DESIGN VARIANT")
        print("=" * 76)

        print()

        print(
            f"h"
            f"                                       = "
            f"{best_variant['h']} mm"
        )

        print(
            f"Da"
            f"                                      = "
            f"{best_variant['Da']:.4f} m"
        )

        print(
            f"Kd"
            f"                                      = "
            f"{best_variant['Kd']:.4f}"
        )

        print(
            f"D"
            f"                                       = "
            f"{best_variant['D']:.4f} m"
        )

        print(
            f"tau"
            f"                                     = "
            f"{best_variant['tau']:.4f} m"
        )

        print(
            f"Ke"
            f"                                      = "
            f"{best_variant['Ke']:.4f}"
        )

        print(
            f"B_delta"
            f"                                 = "
            f"{best_variant['B_delta']:.4f} T"
        )

        print(
            f"A"
            f"                                       = "
            f"{best_variant['A']:.0f} A/m"
        )

        print(
            f"Omega"
            f"                                   = "
            f"{best_variant['Omega']:.3f} rad/s"
        )

        print(
            f"l_delta"
            f"                                 = "
            f"{best_variant['l_delta']:.4f} m"
        )

        print()

        print(
            f"lambda"
            f"                                  = "
            f"{best_variant['lambda']:.4f}"
        )

        print(
            f"lambda target"
            f"                           = "
            f"{best_variant['lambda_target']:.4f}"
        )

        print(
            f"lambda permissible range"
            f"                = "
            f"{best_variant['lambda_min']:.4f} ... "
            f"{best_variant['lambda_max']:.4f}"
        )

        print(
            f"status"
            f"                                  = "
            f"{best_variant['status']}"
        )

        print()
        print("=" * 76)


    return best_variant


# ================================================================
# MODULE TEST
# ================================================================

if __name__ == "__main__":

    result = optimize_main_dimensions(
        P2=55.0,
        poles=8,
        protection="IP44",
        h=280,
        f1=50.0,
        kw1=0.95,
        verbose=True,
    )

    print()

    if result is None:

        print(
            "Optimization result: "
            "NO PERMISSIBLE DESIGN"
        )

    else:

        print(
            "Optimization result: "
            "PERMISSIBLE DESIGN FOUND"
        )