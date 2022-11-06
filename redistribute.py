"""
    My code is a redistribution through recursion, thus redistributing one item at time
    We prioritize redistribute to the numbers less than minimum first
    Why?    Because this better handles the case with 0 values
            as they have no proportionality to everything else until they hav
    Each iteration proportionately redistributes
"""

def redistribute(weights, min : float = 0.02, max : float = 0.25):
    """
    Recursive redistribution
    Parameters
    weights : array of values to redistribute
    min : Min value allowed, default to 0.02 per assignment
    max : Max value allowed, default to 0.25 per assignment
    Returns
    -------
    [ [Redistributed array] , sum of array ]
    """

    def distribute(weights, max, min):
        '''
        Returns the current distribution
        Parameters
        ----------
            weights : array of values to redistribute
            min : Min value allowed, default to 0.02 per assignment
            max : Max value allowed, default to 0.25 per assignment
        '''

        # List over max, sorted largest to smallest
        over_list = sorted( filter(lambda x: x > max, weights), reverse=True )
        # List under min, sorted smallest to largest (process 0's first)
        under_list = sorted( filter(lambda x: x < min, weights), reverse=False )


        # If completely processed just return current weights.
        if len(under_list) == 0 and len(over_list) == 0:
            return weights

        # Prioritize handling items that are under our minimum and take from everyone else
        elif len(under_list) > 0:
            # Remove the smallest number < min
            weights.remove(under_list[0])
            # We need the total of the subset to do proper redistribution, do not take from those at or below minimum
            total = sum(list(filter(lambda i: i > min, weights)))
            # The amount to take from others
            spread = min - under_list[0]
            # For each number
            for i, weight in enumerate(weights):
                if weight > min:
                    # Remove the amount needed to redistribute, zero case has no weight so will not go negative
                    weights[i] = weight - (spread * (weight / total))
            # Add back in our the low number with the minimum
            weights.append(min)
            # process again
            return distribute(weights, max, min)

        # We have items over our max, cap them at max and redistribute their value
        # But only to others who are below the max
        else:
            # Remove the largest number > max
            weights.remove(over_list[0])
            # We need the total of the subset which are less than max to do proper redistribution
            total = sum(list(filter(lambda i: i < max, weights)))
            # The amount to distribute
            spread = over_list[0] - max
            # For each number
            for i, weight in enumerate(weights):
                if weight < max  :
                    # Add to all redistribute the over max value
                    weights[i] = weight + (spread * (weight / total))
            # Add back in our the high number with the maximum
            weights.append(max)
            # process again
            return distribute(weights, max, min)

    # Can't distribute more than we have
    if len(weights)*min>1:
        print("Invalid Inputs: All solutions would be less than minimum required")
        return [None, None]

    # Assignment calls for distributing with sum greater than one
    if sum(weights) > 1:
        print ("Invalid Inputs: Input array sums to greater than one")
        return [ None, None ]

    # Start our recursion with passed in values
    x = distribute(weights, max, min )

    return ([x, sum(x)])

print(redistribute([0.056, 0.219, 0.322, 0.025, 0.012, 0.048, .105, .097, .065, .051]))
