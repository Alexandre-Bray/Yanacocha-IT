import pathlib
import pandas
import datetime

def return_sorted_files(folder):
    """
    Gather all csv files from a folder and sorts them by their indexing number
    """
    # Convert folder to Path object
    folder_path = pathlib.Path(folder)
    
    # Gather all .csv files
    files = list(folder_path.glob("*.csv"))
    
    # Create temporary holding variable
    unsorted_files = {}
    
    # Sort them by index
    for file in files:
        # Get filename without path
        filename = file.name
        components = filename.split('.csv')[0].split('-')
        
        if len(components) == 4:
            unsorted_files[int(components[3])] = file
        else:
            unsorted_files[0] = file
    
    # Sort files by index and return as list of Path objects
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
                file.unlink()
            
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
            file.unlink()
            
            # Save data in new format
            data.to_csv(file)
    
    return data

def get_IT_list(site):
    """
    Returns a sorted list of directories in the site folder by date
    """
    # Convert site to Path object
    site_path = pathlib.Path(site)
    
    # Gather directories
    directories = [d for d in site_path.iterdir() if d.is_dir()]
    
    # Extract dates from directory names
    date_list = [d.name for d in directories]
    
    # Convert strings to datetime objects
    datetime_list = [datetime.datetime.strptime(date, '%B-%y') for date in date_list]
    
    # Sort by date
    sorted_dates = sorted(datetime_list)
    
    # Convert back to original format
    sorted_formatted_dates = [date.strftime('%B-%y').upper() for date in sorted_dates]
    
    # Create sorted directory paths
    sorted_directories = [site_path / date for date in sorted_formatted_dates]
    
    return sorted_directories