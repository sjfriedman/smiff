from functools import reduce

def power_consumption(file_name):
    '''
        This contains all the functions related part 1, which are built in one function
        And the part 2 (delta and omega) is implemented via recursive method
        Parameters
        ----------
        file_name - input file to use
    '''
    with open(file_name, 'r') as f:
        # opens file and strips spaces around each line
        lines = [entry.strip() for entry in f.readlines()]

    def part_1(lines):
        '''
        Compute alpha rate and beta rate and return the power consumption
        Parameters
        ----------
        lines - array representing the lines in the problem set

        Returns
        -------
        power consumption, in base 10, which is alpha * beta
        '''

        # sets empty array to be filled by alpha values
        alpha_list = []

        # gets number of cols
        number_cols = len(lines[0])

        # appends alpha_list to get the list of the number that appears most in each column
        for num in range(0, number_cols): alpha_list.append(int(len(list(filter(lambda x: int(x[num]) == 1, lines))) >= len(lines) / 2))

        # converts alpha to base 10
        alpha = int(''.join(str(x) for x in alpha_list),2)

        # gets an array of all the opposites of alpha(since the opposite would be least popular number in column)
        # converts sigma to base 10
        sigma = int(''.join(str(x) for x in list(map(lambda x: 1 - int(x), alpha_list))), 2)

        # returns power consumption alpha*sigma
        return alpha * sigma

    def part_2(lines):
        '''
        Compute delta and omega via recursive methods, documented in each function and return delta * omega
        Parameters
        ----------
        lines - array representing the lines in the problem set

        Returns
        -------
        delta * omega, in base 10
        '''

        def delta(lines):
            '''
            Compute the delta rate recursively by going bit by bit down the chain reducing each
            list to the lines that are for the favorite bit
            Parameters
            ----------
            lines - string array to process

            Returns
            -------
            Array of strings meeting criteria of having the most common value in the first bit
            '''

            # case if empty string
            if lines == ['']:
                return []
            # case if only one solution left but still more bits
            elif len(lines) == 1:
                return lines

            # gets the delta rate of the least common element in the first column of lines
            # because this is recursive each time this function is called, it gets the following column
            popular = int(len(list(filter(lambda x: int(x[0]) == 1, lines))) >= len(lines) / 2)

            # the parameter in part 3 can be broken into two parts
            # the filter gets all the lines that start with the popular number
            # the map makes the array move to the next column; deletes the first index of every item
            # the list just converts the map type to a list type
            # the popular in [] adds the popular number to the return arrary
            return [popular] + delta(list(map(lambda y: y[1:], filter(lambda x: int(x[0]) == popular, lines))))

        def omega(lines):
            '''
            Compute the omega rate recursively by going bit by bit down the chain reducing each
            list to the lines that are for the favorite bit
            Parameters
            ----------
            lines - string array to process

            Returns
            -------
            Array of strings meeting criteria of having the most common value in the first bit
            '''

            # case if empty string
            if lines == ['']:
                return []
            # case if only one solution left but still more bits
            elif len(lines) == 1:
                return list(lines[0])

            # gets the omega rate of the most unpopular element in the first column of lines
            # because this is recursive each time this function is called, it gets the following column
            unpopular = 1 - int(len(list(filter(lambda x: int(x[0]) == 1, lines))) >= len(lines) / 2)

            # the parameter in part 3 can be broken into two parts
            # the filter gets all the lines that start with the unpopular number
            # the map makes the array move to the next column; deletes the first index of every item
            # the list just converts the map type to a list type
            # the unpopular in [] adds the unpopular number to the return arrary
            return [unpopular] + omega(list(map(lambda y: y[1:], filter(lambda x: int(x[0]) == unpopular, lines))))

        # For both delta and omega use reduce to convert array to convert to string, then int to convert base 10 number
        base_10_delta = int(reduce(lambda x,y: str(x) + str(y), delta(lines)), 2)
        base_10_omega = int(reduce(lambda x,y: str(x) + str(y), omega(lines)), 2)

        return base_10_delta * base_10_omega

    # prints alpha * sigma
    print("Part One:", part_1(lines))
    # print delta * omega
    print("Part Two:", part_2(lines))

# invokes the function that will compute and print the results for part 1 and part 2
power_consumption('logic_input.txt')
