def return_sorted_files(folder):
    """
    Gather all csv files from a folder and sorts them by their indexing number
    """
    import glob

    # Gather all of the files
    files = glob.glob(f"{folder}/*.csv")

    # Create temporary holding variable
    unsorted_files = dict()

    # Sort them in order 
    for file in files:
        if '/' in file:
            dir = file.split('/')[0:-1]
            file = file.split('/')[-1]
        components = file.split('.csv')[0].split('-')

        if len(components) == 4:
            unsorted_files[int(components[3])] = file
        else:
            unsorted_files[0] = file

    sorted_files = list()

    dir = '/'.join(dir)

    for i, _ in enumerate(unsorted_files):
        file = '/'.join([dir,unsorted_files[i]])
        sorted_files.append(file)

    return sorted_files

def combine_data(files, padding = True, columns = 72):
    """
    Combines multiple csv into one
    """
    import pathlib, pandas

    # If the files have not been merged into one, do so
    if len(files)>1:

        # Combine all the files into a single data structure
        # Combine the data from all csv files 
        for i, file in enumerate(files):

            try:
                if i == 0:
                    # If this is the first file, create a variable
                    data = pandas.read_csv(file, skiprows=2, names=[i for i in range(columns)], usecols=[i for i in range(columns)])
                else:
                    # If not the first file, append to the existing variable
                    if padding:
                        new = pandas.read_csv(file, skiprows=2,header=None, names=[i for i in range(columns)], usecols=[i for i in range(columns)])
                    else:
                        new = pandas.read_csv(file, skiprows=2)

                    # Sometimes labview creates an additional indexing column
                    if '1' in new.columns:
                        new = new.drop(columns='1')

                    new.columns = data.columns
                    data = pandas.concat([data, new], ignore_index=True)
            except Exception as e:
                return combine_data(files, padding=True, columns = 72)
                print(f"Error! {file} \n {e}")
                return None
    return data

def load_data(experiment):
    """
    Loads data from csv file, if multiple files exists, combine them
    """
    import pathlib, pandas

    # Find files within experiment folder
    files = return_sorted_files(experiment)

    # If the files have not been merged into one, do so
    if len(files)>1:

        # Combine all the files into a single data structure
        data = combine_data(files)

        if data is None:
            return None
        else:
            # delete all files
            for file in files:
                pathlib.Path(file).unlink()

            # Save data as a singular large file
            data.to_csv(files[0])

            if not 'Time' in data.columns:
                data = pandas.read_csv(files[0], index_col=0)
    else:
        
        file = files[0]

        try:
            # Load new format file
            #data = pandas.read_csv(file, index_col=0)
        
            data = pandas.read_csv(file, header=1, index_col = 0)

            if not 'Time' in data.columns:
                data = pandas.read_csv(file, index_col=0)
        except:
            
            # If labview format, load it
            data = pandas.read_csv(file, skiprows=2)

            # Delete the file
            pathlib.Path(file).unlink()

            # Save data in new format
            data.to_csv(file)

    
    
    return data

def get_IT_list(site):

    import glob

    # Gather files
    directories = glob.glob(f'{site}/**', recursive=False)

    import datetime

    # Convert directory list to dates
    date_list = list()
    for path in directories:
        date = path.split('/')[-1]
        date_list.append(date)

    # Convert strings to datetime objects
    datetime_list = [datetime.datetime.strptime(date, '%B-%y') for date in date_list]

    # Sort the datetime objects
    sorted_dates = sorted(datetime_list)

    # If you want to convert back to original format after sorting
    sorted_formatted_dates = [date.strftime('%B-%y').upper() for date in sorted_dates]

    sorted_formatted_dates

    sorted_directories = list()
    for date in sorted_formatted_dates:
        sorted_directories.append(f"{site}/{date}")

    return sorted_directories