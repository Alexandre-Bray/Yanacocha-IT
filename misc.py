import os
import glob
import pandas
import datetime

def return_sorted_files(folder):
    """
    Gather all csv files from a folder and sorts them by their indexing number
    """
    # Gather all .csv files using glob
    files = glob.glob(os.path.join(folder, "*.csv"))
    
    # Create temporary holding variable
    unsorted_files = {}
    
    # Sort them by index
    for file in files:
        # Get filename without path
        filename = os.path.basename(file)
        components = filename.split('.csv')[0].split('-')
        
        if len(components) == 4:
            unsorted_files[int(components[3])] = file
        else:
            unsorted_files[0] = file
    
    # Sort files by index and return as list
    sorted_files = [unsorted_files[i] for i in sorted(unsorted_files.keys())]
    
    return sorted_files

def combine_data(files, padding=True, columns=72):
    """
    Combines multiple csv files into one
    """
    # If there are multiple files, combine them
    if len(files) > 1:
        for i, file in enumerate(files):
            try:
                if i == 0:
                    # First file: create the data frame
                    data = pandas.read_csv(file, skiprows=2, names=[i for i in range(columns)], 
                                         usecols=[i for i in range(columns)])
                else:
                    # Subsequent files: append to existing data
                    if padding:
                        new = pandas.read_csv(file, skiprows=2, header=None, 
                                            names=[i for i in range(columns)], 
                                            usecols=[i for i in range(columns)])
                    else:
                        new = pandas.read_csv(file, skiprows=2)
                    
                    # Handle potential extra indexing column from LabVIEW
                    if '1' in new.columns:
                        new = new.drop(columns='1')
                    
                    new.columns = data.columns
                    data = pandas.concat([data, new], ignore_index=True)
            except Exception as e:
                print(f"Error! {file} \n {e}")
                # Retry with default padding
                return combine_data(files, padding=True, columns=72)
        return data
    return None

def load_data(experiment):
    """
    Loads data from csv file, if multiple files exist, combine them
    """
    # Find files within experiment folder
    files = return_sorted_files(experiment)
    
    if len(files) > 1:
        # Combine all files into a single data structure
        data = combine_data(files)
        
        if data is None:
            return None
        else:
            # Delete all files
            for file in files:
                os.remove(file)
            
            # Save combined data as a single file
            data.to_csv(files[0])
            
            if 'Time' not in data.columns:
                data = pandas.read_csv(files[0], index_col=0)
    else:
        file = files[0]
        
        try:
            # Load new format file
            data = pandas.read_csv(file, header=1, index_col=0)
            
            if 'Time' not in data.columns:
                data = pandas.read_csv(file, index_col=0)
        except:
            # If LabVIEW format, load it
            data = pandas.read_csv(file, skiprows=2)
            
            # Delete the file
            os.remove(file)
            
            # Save data in new format
            data.to_csv(file)
    
    return data

def get_IT_list(site):
    """
    Returns a sorted list of directories in the site folder by date, with experiment names
    """
    # Gather directories
    directories = [os.path.join(site, d) for d in os.listdir(site) if os.path.isdir(os.path.join(site, d))]
    
    # Extract experiment names and dates
    experiment_names = []
    date_list = []
    
    for path in directories:
        # Extract experiment name from the last component of the path
        experiment_name = os.path.basename(path)
        experiment_names.append(experiment_name)
        date_list.append(experiment_name)
    
    # Convert strings to datetime objects
    try:
        datetime_list = [datetime.datetime.strptime(date, '%B-%y') for date in date_list]
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return [], []
    
    # Sort by date
    sorted_dates = sorted(datetime_list)
    
    # Convert back to original format
    sorted_formatted_dates = [date.strftime('%B-%y').upper() for date in sorted_dates]
    
    # Create sorted directory paths
    sorted_directories = [os.path.join(site, date) for date in sorted_formatted_dates]
    
    return sorted_directories, experiment_names

def process_experiments(site):
    """
    Process experiments and extract names, demonstrating correct path handling with os
    """
    # Get sorted directories and experiment names
    sorted_directories, experiment_names = get_IT_list(site)
    
    # Initialize lists for processing
    processed_experiments = []
    processed_names = []
    
    # Iterate over directories
    for experiment_number, path in enumerate(sorted_directories, start=1):
        # Assign experiment ID
        experiment_id = experiment_number
        
        # Extract experiment name from the path
        experiment_name = os.path.basename(path)
        
        # Append to lists
        processed_names.append(experiment_name)
        processed_experiments.append({
            'id': experiment_id,
            'name': experiment_name,
            'path': path
        })
    
    return processed_experiments, processed_names