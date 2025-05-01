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
    Returns a sorted list of directories in the site folder by date and number suffix,
    with experiment names. Supports names like 'May-01', 'MAY-01=1', 'APRIL-30=2_OVERNIGHT'.
    Sorts primarily by date, secondarily by number after '='.
    """
    # Gather directories
    directories = [os.path.join(site, d) for d in os.listdir(site) if os.path.isdir(os.path.join(site, d))]
    
    # Extract experiment names, dates, and numbers
    experiment_info = []
    current_year = datetime.datetime.now().year  # Use current year (2025)
    
    for path in directories:
        # Extract experiment name from the last component of the path
        experiment_name = os.path.basename(path)
        try:
            # Replace underscores with hyphens for consistency
            normalized_name = experiment_name.replace('_', '-')
            # Split on '=' to separate date and number parts
            parts = normalized_name.split('=')
            if len(parts) < 1:
                raise ValueError("Experiment name does not contain a valid format")
            
            # Get the date part (before '=' or entire name if no '=')
            date_part = parts[0]
            # Split date part on '-' to get month and day
            date_components = date_part.split('-')
            if len(date_components) < 2:
                raise ValueError("Experiment name does not contain a valid date format")
            
            # Construct date string (e.g., 'APRIL-30')
            date_str = f"{date_components[0]}-{date_components[1]}"
            # Normalize case for parsing (e.g., 'APRIL-30' to 'April-30')
            normalized_date = date_str.title()
            date = datetime.datetime.strptime(normalized_date, '%B-%d')
            # Assign the current year to the date
            date = date.replace(year=current_year)
            
            # Extract number after '=' if present, default to 0
            number = 0
            if len(parts) > 1:
                # Take the part after '=' and before any additional '-' (e.g., '2-OVERNIGHT' -> '2')
                number_part = parts[1].split('-')[0]
                try:
                    number = int(number_part)
                except ValueError:
                    raise ValueError(f"Invalid number format in '{experiment_name}'")
            
            experiment_info.append({
                'name': experiment_name,  # Preserve original name
                'date': date,
                'number': number,
                'path': path
            })
        except ValueError as e:
            print(f"Warning: Could not parse date or number from '{experiment_name}'. Skipping. Error: {e}")
            continue
    
    # Sort by date (primary) and number (secondary)
    sorted_info = sorted(experiment_info, key=lambda x: (x['date'], x['number']))
    
    # Extract sorted directories and experiment names
    sorted_directories = [info['path'] for info in sorted_info]
    experiment_names = [info['name'] for info in sorted_info]
    
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

def format_names(experiment_names):
    names = list()
    for name in experiment_names:
        names.append('\n'.join(name.split('_')))
    return names