def find_quiescent_start(series, skip=300, window=3, max_count=10, mean_threshold=0.01, logging=False):
    """
    Finds the start of the quiet period
    """

    if logging:
        log = {'mean':list(),'threshold':list(),'counter':list()}

    # Initialize counter used to determine the quiet period
    count = 0

    for i, _ in enumerate(series):
        if (i < window+skip):
            continue
        else:
            # Create data up until that point
            s = series.iloc[skip:i]

            # Determine variance of data until that point
            v = s.rolling(window).var()

            # If below the mean, increment counter
            mean = v.iloc[:i].mean()

            # Calculate threshold
            threshold = (mean)*mean_threshold

            if logging:
                log['mean'].append(mean)
                log['threshold'].append(threshold)
                log['counter'].append(count)


            if (v.iloc[-1]) < threshold:
                count+=1

                # If mulitple consecutive, the quiet period has started
                if count>=max_count:
                    break
            else:
                # Reset counter
                count = 0
    if logging:
        return i,  threshold, log
    else:
        return i, threshold, None

def find_quiescent_end(series, start, window=3, max_count=10, threshold=0.01):
    """
    Finds the end of the quiet period
    """

    # Initialize counter used to determine the quiet period
    count = 0

    for i, _ in enumerate(series):
        if (i < start+window):
            continue
        else:
            # Create data up until that point
            s = series.iloc[start:i]

            # Determine variance of data until that point
            v = s.rolling(window).var()

            if (v.iloc[-1]) > threshold:
                count+=1

                # If mulitple consecutive, the quiet period has started
                if count>=max_count:
                    break
            else:
                # Reset counter
                count = 0
    
    return i