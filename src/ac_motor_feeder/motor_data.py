"""
DIGITAL ELECTRICAL ENGINEER (DEE)

AC MOTOR FEEDER DESIGN
MOTOR NAMEPLATE DATA

This module stores and validates the input data of an existing
three-phase asynchronous motor.

The motor is considered as an existing electrical machine.
The module does not design the motor.

The validated motor data will later be used for:

- design current calculation;
- starting current calculation;
- cable sizing;
- voltage-drop calculation;
- short-circuit calculations;
- protection requirements;
- Schneider Electric equipment selection;
- Schneider Electric coordination checks.
"""


# =============================================================================
# PARAMETER DESCRIPTIONS
# =============================================================================

CONNECTION_DESCRIPTIONS = {
    "DELTA": "Delta connection",
    "STAR": "Star connection",
}


DUTY_DESCRIPTIONS = {
    "S1": "Continuous duty",
    "S2": "Short-time duty",
    "S3": "Intermittent periodic duty",
    "S4": "Intermittent periodic duty with starting",
    "S5": "Intermittent periodic duty with electric braking",
    "S6": "Continuous-operation periodic duty",
    "S7": "Continuous-operation periodic duty with electric braking",
    "S8": "Continuous-operation periodic duty with related load and speed changes",
    "S9": "Duty with non-periodic load and speed variations",
    "S10": "Duty with discrete constant loads and speeds",
}


EFFICIENCY_CLASS_DESCRIPTIONS = {
    "IE1": "Standard efficiency",
    "IE2": "High efficiency",
    "IE3": "Premium efficiency",
    "IE4": "Super premium efficiency",
    "IE5": "Ultra premium efficiency",
}


STARTING_METHOD_DESCRIPTIONS = {
    "DOL": "Direct-On-Line starting",
    "STAR_DELTA": "Star-Delta starting",
    "SOFT_START": "Soft starter",
    "VFD": "Variable Frequency Drive",
}


# =============================================================================
# MOTOR DATA ERROR
# =============================================================================

class MotorDataError(ValueError):
    """
    Error raised when motor input data are invalid.
    """

    pass


# =============================================================================
# AUXILIARY FUNCTIONS
# =============================================================================

def _require_value(data, key):
    """
    Check that a required parameter exists and is not None.
    """

    if key not in data:
        raise MotorDataError(
            f"Required motor parameter '{key}' is missing."
        )

    if data[key] is None:
        raise MotorDataError(
            f"Required motor parameter '{key}' is None."
        )

    return data[key]


def _require_positive(data, key):
    """
    Check that a numerical parameter is greater than zero.
    """

    value = _require_value(data, key)

    if not isinstance(value, (int, float)):
        raise MotorDataError(
            f"Motor parameter '{key}' must be numerical."
        )

    if value <= 0:
        raise MotorDataError(
            f"Motor parameter '{key}' must be greater than zero."
        )

    return float(value)


def _require_integer_positive(data, key):
    """
    Check that a parameter is a positive integer.
    """

    value = _require_value(data, key)

    if not isinstance(value, int):
        raise MotorDataError(
            f"Motor parameter '{key}' must be an integer."
        )

    if value <= 0:
        raise MotorDataError(
            f"Motor parameter '{key}' must be greater than zero."
        )

    return value


def _require_range(data, key, minimum, maximum):
    """
    Check that a numerical parameter is inside the specified range.
    """

    value = _require_positive(data, key)

    if not minimum <= value <= maximum:
        raise MotorDataError(
            f"Motor parameter '{key}' = {value} is outside "
            f"the permissible range {minimum} ... {maximum}."
        )

    return value


def _require_choice(data, key, choices):
    """
    Check that a text parameter belongs to the permissible choices.
    """

    value = _require_value(data, key)

    if not isinstance(value, str):
        raise MotorDataError(
            f"Motor parameter '{key}' must be text."
        )

    value = value.strip().upper()

    if value not in choices:
        raise MotorDataError(
            f"Unsupported value '{value}' for motor parameter '{key}'. "
            f"Permissible values: {', '.join(choices)}."
        )

    return value


def _require_text(data, key):
    """
    Check that a text parameter is not empty.
    """

    value = _require_value(data, key)

    if not isinstance(value, str):
        raise MotorDataError(
            f"Motor parameter '{key}' must be text."
        )

    value = value.strip()

    if not value:
        raise MotorDataError(
            f"Motor parameter '{key}' must not be empty."
        )

    return value


# =============================================================================
# MOTOR DATA VALIDATION
# =============================================================================

def validate_motor_data(motor_data):
    """
    Validate motor nameplate and starting data.

    Parameters
    ----------
    motor_data : dict
        Input data of an existing asynchronous motor.

    Returns
    -------
    dict
        Validated and normalized motor data.
    """

    if not isinstance(motor_data, dict):
        raise MotorDataError(
            "Motor data must be provided as a dictionary."
        )

    # -------------------------------------------------------------------------
    # MOTOR IDENTIFICATION
    # -------------------------------------------------------------------------

    manufacturer = _require_text(
        motor_data,
        "manufacturer",
    )

    motor_type = _require_text(
        motor_data,
        "motor_type",
    )

    # -------------------------------------------------------------------------
    # RATED MOTOR DATA
    # -------------------------------------------------------------------------

    rated_power_kw = _require_positive(
        motor_data,
        "rated_power_kw",
    )

    rated_voltage_v = _require_positive(
        motor_data,
        "rated_voltage_v",
    )

    rated_current_a = _require_positive(
        motor_data,
        "rated_current_a",
    )

    rated_frequency_hz = _require_positive(
        motor_data,
        "rated_frequency_hz",
    )

    rated_speed_rpm = _require_positive(
        motor_data,
        "rated_speed_rpm",
    )

    power_factor = _require_range(
        motor_data,
        "power_factor",
        0.01,
        1.00,
    )

    efficiency = _require_range(
        motor_data,
        "efficiency",
        0.01,
        1.00,
    )

    # -------------------------------------------------------------------------
    # MOTOR CONSTRUCTION AND DUTY
    # -------------------------------------------------------------------------

    phases = _require_integer_positive(
        motor_data,
        "phases",
    )

    if phases != 3:
        raise MotorDataError(
            "Current DEE AC motor feeder module supports only "
            "three-phase asynchronous motors."
        )

    connection = _require_choice(
        motor_data,
        "connection",
        CONNECTION_DESCRIPTIONS,
    )

    duty = _require_choice(
        motor_data,
        "duty",
        DUTY_DESCRIPTIONS,
    )

    if duty != "S1":
        raise MotorDataError(
            f"Motor duty '{duty}' is recognized but is not supported "
            "in the current DEE version. Current supported duty: S1."
        )

    efficiency_class = _require_choice(
        motor_data,
        "efficiency_class",
        EFFICIENCY_CLASS_DESCRIPTIONS,
    )

    # -------------------------------------------------------------------------
    # STARTING DATA
    # -------------------------------------------------------------------------

    starting_method = _require_choice(
        motor_data,
        "starting_method",
        STARTING_METHOD_DESCRIPTIONS,
    )

    if starting_method != "DOL":
        raise MotorDataError(
            f"Starting method '{starting_method}' is recognized but is not "
            "supported in the current DEE version. "
            "Current supported starting method: DOL."
        )

    starting_current_ratio = _require_positive(
        motor_data,
        "starting_current_ratio",
    )

    starting_time_s = _require_positive(
        motor_data,
        "starting_time_s",
    )

    # -------------------------------------------------------------------------
    # FORM VALIDATED DATA
    # -------------------------------------------------------------------------

    validated_data = {
        "manufacturer": manufacturer,
        "motor_type": motor_type,

        "rated_power_kw": rated_power_kw,
        "rated_voltage_v": rated_voltage_v,
        "rated_current_a": rated_current_a,
        "rated_frequency_hz": rated_frequency_hz,
        "rated_speed_rpm": rated_speed_rpm,

        "power_factor": power_factor,
        "efficiency": efficiency,

        "phases": phases,
        "connection": connection,
        "duty": duty,
        "efficiency_class": efficiency_class,

        "starting_method": starting_method,
        "starting_current_ratio": starting_current_ratio,
        "starting_time_s": starting_time_s,

        "motor_data_source": "NAMEPLATE",
        "motor_data_status": "VALID",
    }

    return validated_data


# =============================================================================
# DESCRIPTION FUNCTIONS
# =============================================================================

def get_connection_description(connection):
    """
    Return motor connection description.
    """

    return CONNECTION_DESCRIPTIONS.get(
        connection,
        "Unknown connection",
    )


def get_duty_description(duty):
    """
    Return motor duty description.
    """

    return DUTY_DESCRIPTIONS.get(
        duty,
        "Unknown duty",
    )


def get_efficiency_class_description(efficiency_class):
    """
    Return motor efficiency class description.
    """

    return EFFICIENCY_CLASS_DESCRIPTIONS.get(
        efficiency_class,
        "Unknown efficiency class",
    )


def get_starting_method_description(starting_method):
    """
    Return motor starting method description.
    """

    return STARTING_METHOD_DESCRIPTIONS.get(
        starting_method,
        "Unknown starting method",
    )


# =============================================================================
# MODULE TEST
# =============================================================================

if __name__ == "__main__":

    test_motor_data = {
        # ---------------------------------------------------------------------
        # MOTOR IDENTIFICATION
        # ---------------------------------------------------------------------

        "manufacturer": "REFERENCE MOTOR",
        "motor_type": "TEST AC MOTOR",

        # ---------------------------------------------------------------------
        # RATED MOTOR DATA
        # ---------------------------------------------------------------------

        "rated_power_kw": 15.0,
        "rated_voltage_v": 400,
        "rated_current_a": 28.5,
        "rated_frequency_hz": 50,
        "rated_speed_rpm": 1475,

        "power_factor": 0.86,
        "efficiency": 0.921,

        # ---------------------------------------------------------------------
        # MOTOR CONSTRUCTION AND DUTY
        # ---------------------------------------------------------------------

        "phases": 3,
        "connection": "DELTA",
        "duty": "S1",
        "efficiency_class": "IE3",

        # ---------------------------------------------------------------------
        # STARTING DATA
        # ---------------------------------------------------------------------

        "starting_method": "DOL",
        "starting_current_ratio": 7.5,
        "starting_time_s": 3.5,
    }

    result = validate_motor_data(
        test_motor_data,
    )

    print("=" * 76)
    print("DEE - AC MOTOR NAMEPLATE DATA VALIDATION")
    print("=" * 76)

    print()
    print(
        f"Manufacturer                  = "
        f"{result['manufacturer']}"
    )

    print(
        f"Motor type                    = "
        f"{result['motor_type']}"
    )

    print()
    print(
        f"Rated power Pn                = "
        f"{result['rated_power_kw']:.2f} kW "
        f"(motor rated output power)"
    )

    print(
        f"Rated voltage Un              = "
        f"{result['rated_voltage_v']:.0f} V "
        f"(motor rated line voltage)"
    )

    print(
        f"Rated current In              = "
        f"{result['rated_current_a']:.2f} A "
        f"(motor full-load current, FLC)"
    )

    print(
        f"Rated frequency fn            = "
        f"{result['rated_frequency_hz']:.1f} Hz "
        f"(motor rated supply frequency)"
    )

    print(
        f"Rated speed nn                = "
        f"{result['rated_speed_rpm']:.0f} rpm "
        f"(motor rated shaft speed)"
    )

    print()
    print(
        f"Efficiency eta                = "
        f"{result['efficiency']:.3f} "
        f"(motor rated efficiency)"
    )

    print(
        f"Power factor cos(phi)         = "
        f"{result['power_factor']:.3f} "
        f"(motor rated power factor)"
    )

    print()
    print(
        f"Number of phases              = "
        f"{result['phases']} "
        f"(three-phase AC motor)"
    )

    print(
        f"Connection                    = "
        f"{result['connection']} "
        f"({get_connection_description(result['connection'])})"
    )

    print(
        f"Duty                          = "
        f"{result['duty']} "
        f"({get_duty_description(result['duty'])})"
    )

    print(
        f"Efficiency class              = "
        f"{result['efficiency_class']} "
        f"({get_efficiency_class_description(result['efficiency_class'])})"
    )

    print()
    print(
        f"Starting method               = "
        f"{result['starting_method']} "
        f"({get_starting_method_description(result['starting_method'])})"
    )

    print(
        f"Starting current ratio Is/In  = "
        f"{result['starting_current_ratio']:.2f} "
        f"(starting current to rated current ratio)"
    )

    print(
        f"Starting time ts              = "
        f"{result['starting_time_s']:.2f} s "
        f"(motor acceleration time)"
    )

    print()
    print(
        f"Motor data source             = "
        f"{result['motor_data_source']} "
        f"(manufacturer nameplate data)"
    )

    print(
        f"Motor data check              = "
        f"{result['motor_data_status']} "
        f"(input data validation status)"
    )

    print("=" * 76)