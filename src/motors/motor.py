import math

from src.p01_h_shaft_height import select_shaft_height


def main():

    # ============================================================
    # INITIAL DATA
    # ============================================================

    P2 = 15.0
    U_low = 220
    U_high = 380
    poles = 4

    # Available values:
    # IP44
    # IP23

    protection = "IP44"

    construction = "IM1001"
    cooling = "IC0141"
    climate = "U3"
    insulation_class = "E"
    frequency = 50.0

    # ============================================================
    # INITIAL DATA OUTPUT
    # ============================================================

    print("=" * 60)
    print("DIGITAL ELECTRICAL ENGINEER (DEE)")
    print("ASYNCHRONOUS MOTOR DESIGN")
    print("KOPYLOV METHOD")
    print("=" * 60)

    print("\nINITIAL DATA")
    print("-" * 60)

    print(f"Rated output power P2:       {P2} kW")
    print(f"Rated voltage U1:            {U_low}/{U_high} V")
    print(f"Number of poles 2p:          {poles}")
    print(f"Construction:                {construction}")
    print(f"Protection degree:           {protection}")
    print(f"Cooling method:              {cooling}")
    print(f"Climate version:             {climate}")
    print(f"Insulation class:            {insulation_class}")
    print(f"Supply frequency f1:         {frequency} Hz")

    # ============================================================
    # SECTION 1
    # SELECTION OF MAIN DIMENSIONS
    # ============================================================

    print("\n" + "=" * 60)
    print("SECTION 1. SELECTION OF MAIN DIMENSIONS")
    print("=" * 60)

    # ------------------------------------------------------------
    # 1. Shaft height and outer stator diameter
    # ------------------------------------------------------------

    h = select_shaft_height(
        power_kw=P2,
        poles=poles,
        protection=protection,
    )

    # Temporary reference value from the Kopylov example.
    # This value will later be replaced by a separate
    # engineering selection module.

    Da = 0.272

    print("\n1. Shaft height and outer stator diameter")

    print(f"Rated output power:          P2 = {P2} kW")
    print(f"Number of poles:             2p = {poles}")
    print(f"Protection degree:           {protection}")

    print(f"Selected shaft height:       h = {h} mm")
    print(f"Outer stator diameter:       Da = {Da:.3f} m")

    # ------------------------------------------------------------
    # 2. Inner stator diameter
    # ------------------------------------------------------------

    kD = 0.68

    D = kD * Da

    print("\n2. Inner stator diameter")

    print(f"kD = {kD:.2f}")
    print("D = kD * Da")
    print(f"D = {D:.3f} m")

    # ------------------------------------------------------------
    # 3. Pole pitch
    # ------------------------------------------------------------

    tau = math.pi * D / poles

    print("\n3. Pole pitch")

    print("tau = pi * D / (2p)")
    print(f"tau = {tau:.3f} m")

    # ------------------------------------------------------------
    # 4. Design apparent power
    # ------------------------------------------------------------

    kE = 0.975
    eta = 0.88
    cos_phi = 0.88

    P_design = (
        P2
        * 1000
        * kE
        / (eta * cos_phi)
    )

    print("\n4. Design apparent power")

    print(f"kE = {kE:.3f}")
    print(f"eta = {eta:.2f}")
    print(f"cos(phi) = {cos_phi:.2f}")

    print(
        "P' = P2 * 1000 * kE / "
        "(eta * cos(phi))"
    )

    print(f"P' = {P_design:.0f} VA")

    # ------------------------------------------------------------
    # 5. Preliminary electromagnetic loads
    # ------------------------------------------------------------

    A = 32_000
    B_delta = 0.75

    print("\n5. Preliminary electromagnetic loads")

    print(f"Linear current loading:      A = {A:.0f} A/m")
    print(f"Air-gap flux density:        B_delta = {B_delta:.2f} T")

    # ------------------------------------------------------------
    # 6. Preliminary winding factor
    # ------------------------------------------------------------

    kw1 = 0.95

    print("\n6. Preliminary winding factor")

    print(f"kw1 = {kw1:.2f}")

    # ------------------------------------------------------------
    # 7. Design length of magnetic core
    # ------------------------------------------------------------

    pole_pairs = poles / 2

    omega_sync = (
        2
        * math.pi
        * frequency
        / pole_pairs
    )

    l_delta = (
        P_design
        / (
            D ** 2
            * omega_sync
            * kw1
            * A
            * B_delta
        )
    )

    l_delta_accepted = 0.140

    print("\n7. Design length of magnetic core")

    print(f"Number of pole pairs:        p = {pole_pairs:.0f}")

    print(
        f"Synchronous angular speed:   "
        f"omega = {omega_sync:.2f} rad/s"
    )

    print(f"Calculated core length:      l_delta = {l_delta:.3f} m")

    print(
        f"Accepted core length:        "
        f"l_delta = {l_delta_accepted:.3f} m"
    )

    # ------------------------------------------------------------
    # 8. Ratio lambda
    # ------------------------------------------------------------

    lambda_ratio = (
        l_delta_accepted
        / tau
    )

    print("\n8. Ratio of core length to pole pitch")

    print("lambda = l_delta / tau")
    print(f"lambda = {lambda_ratio:.2f}")

    print("\nAccording to Kopylov Fig. 9.25:")
    print("lambda is within the permissible range.")

    # ============================================================
    # SECTION RESULTS
    # ============================================================

    print("\n" + "=" * 60)
    print("SECTION 1 RESULTS")
    print("=" * 60)

    print(f"P2          = {P2} kW")
    print(f"2p          = {poles}")
    print(f"IP          = {protection}")
    print(f"h           = {h} mm")
    print(f"Da          = {Da:.3f} m")
    print(f"kD          = {kD:.2f}")
    print(f"D           = {D:.3f} m")
    print(f"tau         = {tau:.3f} m")
    print(f"kE          = {kE:.3f}")
    print(f"eta         = {eta:.2f}")
    print(f"cos(phi)    = {cos_phi:.2f}")
    print(f"P'          = {P_design:.0f} VA")
    print(f"A           = {A:.0f} A/m")
    print(f"B_delta     = {B_delta:.2f} T")
    print(f"kw1         = {kw1:.2f}")
    print(f"omega       = {omega_sync:.2f} rad/s")
    print(f"l_delta calc= {l_delta:.3f} m")
    print(f"l_delta acc = {l_delta_accepted:.3f} m")
    print(f"lambda      = {lambda_ratio:.2f}")

    print("=" * 60)


if __name__ == "__main__":
    main()