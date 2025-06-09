
temperature_compensation_values = (-7.0603196042813465, 304.6208427571597)

"""
(Slope, Intercept)
Values from test in Golden, CO (GRL138) February 2025
"""
conductivity_compensation_values = (6.10587651312185, 61.63512345974522)


def normalize_concentrate_pressure(temperature, conductivity, pressure, model='linear'):
    """
    Temperature and Conductivity normalization for concentrate pressure 
    Only use for Integrity Test data
    """

    if model == 'legacy':
        temperature_normalized_pressure = temperature_pressure_correction_legacy(temperature,pressure)
        return conductivity_pressure_correction_legacy(conductivity, temperature_normalized_pressure)
    elif model == 'ratio':

        temperature_normalized_pressure = temperature_pressure_correction_ratio(temperature,pressure)
        return conductivity_pressure_correction_ratio(conductivity, temperature_normalized_pressure)
        
    elif model == 'linear':
        temperature_normalized_pressure = temperature_pressure_correction_linear(temperature,pressure)
        return conductivity_pressure_correction_linear(conductivity, temperature_normalized_pressure)

def temperature_correction(temperature, pressure, model='linear'):
    if model == 'legacy':
        return temperature_pressure_correction_legacy(temperature,pressure)
    elif model == 'ratio':
        return temperature_pressure_correction_ratio(temperature,pressure)
    elif model == 'linear':
        return temperature_pressure_correction_linear(temperature,pressure)
    
def conductivity_correction(conductivity, pressure, model='linear'):
    if model == 'legacy':
        return conductivity_pressure_correction_legacy(conductivity,pressure)
    elif model == 'ratio':
        return conductivity_pressure_correction_ratio(conductivity,pressure)
    elif model == 'linear':
        return conductivity_pressure_correction_linear(conductivity,pressure)


def conductivity_pressure_correction_legacy(conductivity, pressure, reference_conductivity=1):
    """
    Conductivity-based pressure correction for concentrate pressure, intended for Integrity Test data.
    This is a legacy implementation using a deviation-based correction method.

    Parameters:
    - conductivity: Measured conductivity (float, assumed in units like mS/cm).
    - pressure: Measured pressure (float, assumed in units consistent with model, e.g., kPa).
    - reference_conductivity: Reference conductivity for normalization (default = 1 mS/cm).

    Linear Model (from March 31, 2025 dataset):
    - Slope: 5.1304346421771
    - Intercept: 61.29198474607597
    - R-squared: 0.996466747755096

    Returns:
    - normalized_pressure: Pressure adjusted to account for conductivity effects (float).

    Notes:
    - Uses a two-step correction: first adjusts based on deviation from a model, then normalizes to a reference.
    - Only suitable for scalar inputs; not vectorized for Pandas Series.
    """
    
    # Define the linear model coefficients derived from the March 31, 2025 dataset
    slope = 5.1304346421771      # Slope of the conductivity-pressure relationship
    intercept = 61.29198474607597 # Intercept of the linear model when conductivity is zero

    # Calculate the expected pressure at the reference conductivity using the linear model
    # Formula: P_ref = slope * reference_conductivity + intercept
    reference_pressure = reference_conductivity * slope + intercept

    # Compute the predicted pressure based on the measured conductivity
    # Formula: P_model = slope * conductivity + intercept
    model = conductivity * slope + intercept

    # Calculate the relative deviation of the measured pressure from the model prediction
    # Formula: deviation = 1 - (P_measured / P_model)
    # - If P_measured = P_model, deviation = 0
    # - If P_measured < P_model, deviation > 0
    # - If P_measured > P_model, deviation < 0
    deviation_from_model = 1 - (pressure / model)

    # Compute a pressure adjustment based on the deviation
    # Formula: P_deviation = P_measured * deviation_from_model
    # This scales the deviation by the measured pressure to create a correction term
    deviation_pressure = pressure * deviation_from_model

    # Apply the initial correction to the measured pressure
    # Formula: P_corrected = P_measured + P_deviation
    # Simplified: P_corrected = P_measured * (2 - P_measured / P_model)
    # This adjusts the pressure but may amplify deviations rather than aligning to the model
    corrected_pressure = pressure + deviation_pressure

    # Calculate the relative deviation of the corrected pressure from the reference pressure
    # Formula: deviation_ref = 1 - (P_corrected / P_ref)
    # Similar to deviation_from_model, but compares to the reference condition
    deviation_from_ref = 1 - corrected_pressure / reference_pressure

    # Compute a second correction term based on the deviation from the reference
    # Formula: correction_ref = deviation_ref * P_corrected
    # This scales the reference deviation by the corrected pressure
    correction_from_ref = deviation_from_ref * corrected_pressure

    # Apply the final correction to the original measured pressure
    # Formula: P_normalized = P_measured + correction_ref
    # This is the final output, intended to normalize the pressure to reference conditions
    normalized_pressure = pressure + correction_from_ref

    # Return the normalized pressure value
    return normalized_pressure

def temperature_pressure_correction_legacy(temperature, pressure, reference_temperature=20):
    """
    Temperature-based pressure correction for concentrate pressure.
    This is a legacy implementation using a deviation-based correction method.

    Parameters:
    - temperature: Measured temperature (float, assumed in °C).
    - pressure: Measured pressure (float, assumed in units like psi).
    - reference_temperature: Reference temperature for normalization (default = 20°C).

    Linear Model (from March 19, 2025 dataset, 98% fit):
    - Slope: -1.4399933561082126
    - Intercept: 116.47030556331322

    Historical Models:
    - Initial: Slope = -1.217276959542105, Intercept = 102.8411543501525
    - March 20: Slope = -1.3305002495295128, Intercept = 113.9134756029711 (95% fit)
    - March 20: Slope = -1.4399933561082126, Intercept = 116.47030556331322 (98% fit)

    Returns:
    - normalized_pressure: Pressure adjusted to account for temperature effects (float).

    Notes:
    - Applies a two-stage correction: first based on deviation from the model, then from the reference.
    - Only suitable for scalar inputs; not designed for Pandas Series.
    - May amplify deviations due to its mathematical structure.
    """
    
    # Define the linear model coefficients from the March 19, 2025 dataset (98% fit)
    slope = -1.4399933561082126      # Slope of the temperature-pressure relationship (negative, pressure decreases with temperature)
    intercept = 116.47030556331322    # Intercept of the model when temperature is 0°C

    # Calculate the expected pressure at the reference temperature using the linear model
    # Formula: P_ref = slope * reference_temperature + intercept
    # Example: At 20°C, P_ref ≈ 87.67 psi
    reference_pressure = reference_temperature * slope + intercept

    # Compute the predicted pressure at the measured temperature based on the model
    # Formula: P_model = slope * temperature + intercept
    # Example: At 25°C, P_model ≈ 80.47 psi
    model = temperature * slope + intercept

    # Calculate the relative deviation of the measured pressure from the model prediction
    # Formula: deviation = 1 - (P_measured / P_model)
    # - If P_measured = P_model, deviation = 0
    # - If P_measured < P_model, deviation > 0 (positive correction needed)
    # - If P_measured > P_model, deviation < 0 (negative correction)
    deviation_from_model = 1 - (pressure / model)

    # Compute a pressure adjustment based on the deviation
    # Formula: P_deviation = P_measured * deviation_from_model
    # This scales the deviation by the measured pressure, creating a correction term
    deviation_pressure = pressure * deviation_from_model

    # Apply the initial correction to the measured pressure
    # Formula: P_corrected = P_measured + P_deviation
    # Simplified: P_corrected = P_measured * (2 - P_measured / P_model)
    # Note: This can amplify deviations rather than aligning to the model
    corrected_pressure = pressure + deviation_pressure

    # Calculate the relative deviation of the corrected pressure from the reference pressure
    # Formula: deviation_ref = 1 - (P_corrected / P_ref)
    # Assesses how far the corrected pressure is from the reference condition
    deviation_from_ref = 1 - corrected_pressure / reference_pressure

    # Compute a second correction term based on the deviation from the reference
    # Formula: correction_ref = deviation_ref * P_corrected
    # Scales the reference deviation by the corrected pressure for a final adjustment
    correction_from_ref = deviation_from_ref * corrected_pressure

    # Apply the final correction to the original measured pressure
    # Formula: P_normalized = P_measured + correction_ref
    # This is the output, intended to normalize pressure to the reference temperature
    normalized_pressure = pressure + correction_from_ref

    # Return the normalized pressure value
    return normalized_pressure

def temperature_pressure_correction_linear(temperature, pressure, reference_temperature=20):
    """
    Temperature-based pressure correction for concentrate pressure.

    Parameters:
    - temperature: Measured temperature (float or pd.Series, assumed in degrees Celsius).
    - pressure: Measured pressure (float or pd.Series, assumed in units consistent with model, e.g., psi).
    - reference_temperature: Reference temperature for normalization (default = 20°C).

    Linear Model (from March 19, 2025 dataset, 98% fit):
    - Slope: -1.4399933561082126
    - Intercept: 116.47030556331322

    Returns:
    - corrected_pressure: Pressure corrected to reference temperature conditions (float or pd.Series).

    Notes:
    - Assumes pressure is non-negative.
    - Handles both scalar and Pandas Series inputs.
    """

    import pandas as pd
    import numpy as np

    
    # Model coefficients
    slope = -1.4399933561082126
    intercept = 116.47030556331322

    # Convert scalars to Series if necessary for consistent handling
    if not isinstance(temperature, pd.Series):
        temperature = pd.Series([temperature])
    if not isinstance(pressure, pd.Series):
        pressure = pd.Series([pressure])

    # Calculate correction factor based on temperature difference
    temperature_difference = temperature - reference_temperature
    pressure_correction = temperature_difference * slope

    # Apply correction to measured pressure
    corrected_pressure = pressure - pressure_correction

    # Ensure corrected pressure remains non-negative
    corrected_pressure = corrected_pressure.clip(lower=0)

    return corrected_pressure


def conductivity_pressure_correction_linear(conductivity, pressure, reference_conductivity=1):
    """
    Conductivity-based pressure correction for concentrate pressure, intended for Integrity Test data.

    Parameters:
    - conductivity: Measured conductivity (float or pd.Series, assumed in units like mS/cm).
    - pressure: Measured pressure (float or pd.Series, assumed in units consistent with model, e.g., kPa).
    - reference_conductivity: Reference conductivity for normalization (default = 1 mS/cm).

    Linear Model (from March 31, 2025 dataset):
    - Slope: 5.1304346421771
    - Intercept: 61.29198474607597
    - R-squared: 0.996466747755096

    Slope: 5.771015481273857
    Intercept: 62.84748675157308
    R-squared: 0.9990941177157482

    Returns:
    - corrected_pressure: Pressure corrected to reference conductivity conditions (float or pd.Series).

    Notes:
    - Assumes pressure and conductivity are non-negative.
    - Adjusts pressure linearly based on conductivity deviation from reference.
    """

    import pandas as pd
    import numpy as np

    
    # Model coefficients
    slope = 5.771015481273857
    intercept = 62.84748675157308

    # Convert scalars to Series if necessary for consistent handling
    if not isinstance(conductivity, pd.Series):
        conductivity = pd.Series([conductivity])
    if not isinstance(pressure, pd.Series):
        pressure = pd.Series([pressure])

    # Calculate correction factor based on conductivity difference
    # This adjusts pressure linearly to what it would be at reference conductivity
    conductivity_difference = conductivity - reference_conductivity

    # Slope gives pressure change per conductivity unit
    pressure_correction = conductivity_difference * slope  

    # Apply correction to measured pressure
    corrected_pressure = pressure - pressure_correction

    # Ensure corrected pressure remains non-negative
    corrected_pressure = corrected_pressure.clip(lower=0)

    return corrected_pressure

def conductivity_pressure_correction_ratio(conductivity, pressure, reference_conductivity=1):
    """
    Conductivity-based pressure correction using a ratio method.

    Parameters:
    - conductivity: Measured conductivity (float or pd.Series, in mS/cm or consistent units).
    - pressure: Measured pressure (float or pd.Series, in kPa or consistent units).
    - reference_conductivity: Reference conductivity (default = 5 mS/cm).

    Linear Model:
    Slope: 6.10587651312185
    Intercept: 61.63512345974522
    R-squared: 0.9986141566315516

    
    Returns:
    - corrected_pressure: Pressure adjusted to reference conductivity (float or pd.Series).

    Raises:
    - ValueError: If pressure or conductivity is negative.
    """

    import pandas as pd
    import numpy as np


    # Model coefficients
    slope = 6.10587651312185
    intercept = 61.63512345974522

    # Convert inputs to Series
    if not isinstance(conductivity, pd.Series):
        conductivity = pd.Series([conductivity])
    if not isinstance(pressure, pd.Series):
        pressure = pd.Series([pressure])

    # Input validation
    if (pressure < 0).any():
        raise ValueError("Pressure must be non-negative.")
    if (conductivity < 0).any():
        raise ValueError("Conductivity must be non-negative.")

    # Model pressure at reference conductivity
    P_ref = slope * reference_conductivity + intercept 
    
    # Model pressure at measured conductivity
    P_meas = slope * conductivity + intercept

    # Correction ratio
    ratio = P_ref / P_meas

    # Corrected pressure
    corrected_pressure = pressure * ratio

    return corrected_pressure


def temperature_pressure_correction_ratio(temperature, pressure, reference_temperature=20):
    """
    Temperature-based pressure correction for concentrate pressure using a ratio method.

    Parameters:
    - temperature: Measured temperature (float or pd.Series, assumed in degrees Celsius).
    - pressure: Measured pressure (float or pd.Series, assumed in units consistent with model, e.g., psi).
    - reference_temperature: Reference temperature for normalization (default = 20°C).

    Linear Model (from March 19, 2025 dataset, 98% fit):
    - Slope: -1.4399933561082126
    - Intercept: 116.47030556331322

    April 28 Yanacocha
    Slope: -7.0603196042813465
    Intercept: 304.6208427571597
    R-squared: 0.9871420897167897

    Returns:
    - corrected_pressure: Pressure corrected to reference temperature conditions (float or pd.Series).

    Notes:
    - Assumes pressure is non-negative.
    - Handles both scalar and Pandas Series inputs.
    - Uses ratio of model pressures (reference / measured) to scale the pressure.
    """
    import pandas as pd
    import numpy as np

    
    # Model coefficients
    slope = -7.0603196042813465
    intercept = 304.6208427571597
    
    # Temperature threshold where model pressure = 0
    temp_threshold = -intercept / slope  # Approximately 80.88°C

    # Convert scalars to Series if necessary for consistent handling
    if not isinstance(temperature, pd.Series):
        temperature = pd.Series([temperature])
    if not isinstance(pressure, pd.Series):
        pressure = pd.Series([pressure])

    # Input validation
    if (pressure < 0).any():
        raise ValueError("Pressure must be non-negative; found negative values.")
    if (temperature >= temp_threshold).any():
        raise ValueError(f"Temperature must be < {temp_threshold:.2f}°C to ensure positive model pressure.")

    # Model pressure at reference temperature
    P_ref = slope * reference_temperature + intercept  # Scalar value, e.g., ~87.67 psi at 20°C
    if P_ref <= 0:
        raise ValueError("Reference temperature results in non-positive model pressure.")

    # Model pressure at measured temperature
    P_meas = slope * temperature + intercept

    # Correction ratio: P_ref / P_meas
    # Scales pressure to what it would be at reference temperature per the model
    ratio = P_ref / P_meas

    # Apply correction to measured pressure
    corrected_pressure = pressure * ratio

    # Ensure corrected pressure remains non-negative
    corrected_pressure = corrected_pressure.clip(lower=0)

    return corrected_pressure
