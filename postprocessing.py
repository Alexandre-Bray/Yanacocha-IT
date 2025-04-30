def temperature_pressure_correction(temperature,pressure,reference_temperature=20):
    """
    Temperature based pressure correction

    Using: 

    Slope: -1.217276959542105
    Intercept: 102.8411543501525


    MARCH 20
    slope = -1.3305002495295128
    intercept = 113.9134756029711
    95% fit

    slope = -1.4399933561082126
    intercept = 116.47030556331322
    98% fit

    Dataset from  March 19 2025
    """
    
    slope = -1.4399933561082126
    intercept = 116.47030556331322

    reference_pressure = reference_temperature*slope+intercept

    model = (temperature*slope+intercept)

    deviation_from_model = 1-(pressure/model)

    deviation_pressure = pressure*deviation_from_model

    corrected_pressure = pressure+deviation_pressure

    deviation_from_ref = 1-corrected_pressure/reference_pressure

    correction_from_ref = deviation_from_ref*corrected_pressure

    normalized_pressure = pressure+correction_from_ref

    return normalized_pressure

def temperature_correction_factor(T):
    """
    Calculates Temperature Correction Factor

    Temperature in C
    """
    from numpy import exp 

    if T == 25:
        return 1
    else:
        a = 1/298
        b = 1/(273+T)
        c = a-b
        if T > 25:
            return exp( 2640*c )
        elif T < 25:
            return exp( 3020*c )
        
def legacy_temperature_correction(temperature,pressure):
    return pressure*temperature_correction_factor(temperature)