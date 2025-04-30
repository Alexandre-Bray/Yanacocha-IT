"""
Scripts for Calculating Equations relating to Turbidity Experiments 
"""


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

def effective_pressure( feed_pressure, permeate_pressure, device_pressure_drop, osmotic_pressure):
    """
    Calculating the Normalized Effective Pressure in bar

    feed_pressure : Vessel Feed Pressure, bar
    permeate_pressure : Permeate Pressure, bar
    device_pressure_drop : Device Pressure Drop, bar
    osmotic_pressure : Osmotic Pressure, bar
    """

    # Calculate Effective Pressure
    return feed_pressure - permeate_pressure - (device_pressure_drop/2) - osmotic_pressure

def normalized_effective_pressure(feed_pressure, permeate_pressure, device_pressure_drop, temperature_correction_factor, osmotic_pressure):
    """
    Calculating the Normalized Effective Pressure in bar

    feed_pressure : Vessel Feed Pressure, bar
    permeate_pressure : Permeate Pressure, bar
    device_pressure_drop : Device Pressure Drop, bar
    temperature_correction_factor : Temperature Correction Factor
    osmotic_pressure : Osmotic Pressure, bar
    """

    # Calculate Normalized Effective Pressure
    return temperature_correction_factor*effective_pressure(feed_pressure, permeate_pressure, device_pressure_drop, osmotic_pressure)

def pressure_drop(feed_pressure, concentrate_pressure):
    """
    Calculating the Device Pressure Pressure in bar

    P_feed : Vessel Feed Pressure, bar
    P_con :  Concentrate Pressure, bar
    """

    # Return Pressure Drop
    return feed_pressure - concentrate_pressure

def concentration_factor(water_recovery, rejection = 1):
    """
    Calculating the concentration factor
    """

    recovery_number = water_recovery/100

    return 1/((1 - recovery_number)**rejection)