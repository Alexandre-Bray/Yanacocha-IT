def calculate_statistics(channels, site, recovery=30, exclude = [],conductivity_compensation=True,temperature_compensation=True,model='ratio'):
    """
    Calculate Statistics for the Box plots for IT test data
    """
    import misc, preprocessing, os, pandas
    
    # Initialize empty lists to store experiment names and their corresponding summary data
    experiment_names = list()
    experiment_summaries = list()

    # Retrieve a list of directories (experiments) for the specified site using a custom function
    directories, _ = misc.get_IT_list(site)

    datasets = dict()
    all_cycles = dict()

    # Iterate through each directory, assigning an experiment number and extracting data
    for experiment_number, path in enumerate(directories):
        # Assign the current experiment number as the ID
        experiment_id = experiment_number
        # Extract the experiment name from the last component of the directory path
        experiment_name = os.path.basename(path)
        # Append the experiment name to the list
        experiment_names.append(experiment_name)

        # Attempt to load experiment data and cycles from the directory
        try:
            data, cycles = preprocessing.load_experiment(path)
        # Handle any exceptions during data loading, print the error, and retry loading
        except Exception as e:
            print(e, experiment_id, experiment_name)
            data, cycles = preprocessing.load_experiment(path)

        # Apply compensation to data
        cycles = preprocessing.apply_pressure_correction_all_cycles(cycles, exclude, 
                                                                    conductivity_compensation, 
                                                                    temperature_compensation, 
                                                                    model)
        
        # Calculate Permeate Ratio
        for cycle in cycles:
            P1 = cycle['Permeate 1 Flow (L/min)']
            P3 = cycle['Permeate 3 Flow (L/min)']
            cycle['Permeate Ratio (P1/P3)'] = P1/P3

        # Iterate through each specified channel to process data
        datapoints = dict()
        for channel in channels:
            # Initialize an empty list to store datapoints for the current channel
            datapoints[channel] = list()

            # Process each cycle in the experiment, gathering data at specified conditions
            for i, cycle in enumerate(cycles):
                # Skip cycles marked for exclusion
                if i in exclude:
                    continue
                else:
                    # Attempt to apply corrections and extract data
                    try:
                        preprocessing.apply_pressure_correction(cycle,
                                                                conductivity_compensation,
                                                                temperature_compensation,
                                                                model)

                        # Extract the first datapoint for the target channel where Cycle Recovery is at least 30%
                        datapoint = cycle[cycle['Cycle Recovery (%)'] >= recovery].iloc[0][channel]

                        # Append the datapoint to the channel's list
                        datapoints[channel].append(datapoint)

                    # Handle any exceptions during data processing, print the error, and stop processing the current cycle
                    except Exception as e:
                        print(e)
                        break

        # Create a DataFrame from the collected datapoints for the current experiment
        summary = pandas.DataFrame(datapoints)

        # Append the summary DataFrame to the list of experiment summaries
        experiment_summaries.append(summary)

        datasets[experiment_name] = data
<<<<<<< HEAD
    return experiment_summaries, experiment_names, datasets

def days_until_clean(val1, val2, clean_val=100):
    big = max([val1,val2])
    smol = min([val1, val2])
    return round((clean_val-big)/(big-smol)), round(big-smol,3)
=======
        all_cycles[experiment_name] = cycles
    return experiment_summaries, experiment_names, datasets, all_cycles
>>>>>>> 5f69020b04129965fbfed9785ceb144f61c89709
