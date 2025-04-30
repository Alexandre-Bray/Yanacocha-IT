def segment_cycles(data, minimum_size=100):
    """
    Segment dataset into cycles using 'CCD status'
    """

    # Make a mask to determine where CCD is equal to one
    is_one = data['CCD Status'] == 1

    # Detect segment boundaries and assign number
    group_id = (is_one != is_one.shift()).cumsum()

    # Create segments
    segments = [group for _, group in data[is_one].groupby(group_id[is_one]) if len(group) >= minimum_size]

    return segments

def calculate_elapsed_time(data):
    """
    Calculates elapsed time in seconds, minutes and hours
    """
    from pandas import to_datetime

    # Combine Date and Time into a single string
    data['DateTime'] = data['Date'] + ' ' + data['Time']

    # Convert to datetime
    data['DateTime'] = to_datetime(data['DateTime'], format='%m/%d/%Y %I:%M:%S %p')

    # Set the reference point (first timestamp)
    reference_time = data['DateTime'].iloc[0]

    # Calculate elapsed seconds from the reference point
    data['Elapsed Seconds'] = data['Runtime (hr)']*60*60

    # Calculate elapsed seconds from the reference point
    data['Elapsed Minutes'] = data['Runtime (hr)']*60

    # Calculate elapsed seconds from the reference point
    data['Elapsed Hours'] = data['Runtime (hr)']

    return data

def load_experiment(experiment):
    """
    Loads an .xlsx file in the labview experiment format, and returns the data and cycles
    """
    import misc


    # Load the right file
    data = misc.load_data(experiment)

    try:
        # Remove instances of 'Disabled' data logging
        data = data[data['Time'] != 'DISABLED']
    except:
        data = misc.load_data(experiment)
        data = data[data['Time'] != 'DISABLED']



    # Calculate elapsed time
    data = calculate_elapsed_time(data)

    for time in ['Seconds','Minutes','Hours']:
            data[f'Relative {time}'] = data[f'Elapsed {time}']-data[f'Elapsed {time}'].iloc[0]

    # Segment into cycles
    cycles = segment_cycles(data)

    # Calculate relative time
    for cycle in cycles:
        for time in ['Seconds','Minutes','Hours']:
            cycle[f'Relative {time}'] = cycle[f'Elapsed {time}']-cycle[f'Elapsed {time}'].iloc[0]

    return data, cycles