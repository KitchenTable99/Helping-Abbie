# -*- coding: utf-8 -*-
# Caleb Bitting created the framework to read and graph x,y data contained in a csv file
'''
Example python data input and plotting code.
'''
import os
import sys
import matplotlib.pyplot as plt

def validate_graph_input(f):
    '''Decorator: makes sure that the inputs are in valid form
    
    Args:
        f (func): decorated function
    
    Returns:
        unbound method: same as f in args
    '''
    def wrapper(*args, **kwargs):
        '''Validates inputs
        
        Args:
            *args: all args of f
            **kwargs: all kwargs of f
        
        Raises:
            TypeError: If the form of any input is not correct, alerts user to this problem
        '''
        # check each dataset
        for arg in args:
            if not isinstance(arg, list):         # make sure it's a list
                raise TypeError('Each argument passed must be a list')                          # alert user
            else:
                good_form = True
                for coord_pair in arg:            # check that each item in the list is also a list of length two
                    if not isinstance(coord_pair, list) or len(coord_pair) != 2:
                        good_form = False
        if not good_form:
            raise TypeError('The coordinate pairs are not in the correct form of [x1, y1]')     # alert user
        else:
            return f(*args, **kwargs)

    return wrapper

def csvImport(csv_name, include_headers=False):
    '''Imports two-column csv data. The data is assumed to represent (x, y) coordinate pairs where the first column stores the x-values and the second column, the y-values. The csv must be in the working directory.
    
    Args:
        csv_name (str): the name of the csv that contains the data
        include_headers (bool, optional): whether or not to include the header names in the returned list. Defaults to False.
    
    Returns:
        2D list: The list will be in the form [[x(1), y(1)], [x(2), y(2)], ... [x(n-1), y(n-1)], [x(n), y(n)]] with a csv of n columns
    '''
    # csv_name into csv_path
    if '.csv' not in csv_name:
        csv_name += '.csv'

    # read contents of the csv
    with open(csv_name, 'r') as fp:
        if not include_headers:
            fp.readline()
        raw_csv_contents = fp.read()

    # process contents    
    raw_csv_contents = raw_csv_contents.split('\n')
    csv_contents = [item for item in raw_csv_contents if item != '']
    processed_csv_contents = [list(map(float, coord_pair.split(','))) for coord_pair in csv_contents]


    return processed_csv_contents

@validate_graph_input
def graphData(*args, parameters={}):
    '''Visualizes data
    
    Args:
        *args: A variable length arguement. Each argument should be a list of the form returned by csvImport() above.
        parameters (dict, optional): A dictionary of visualization parameters in the form {unbound plt method: desired paramter, ...} (e.g {plt.title: 'Absorbance v. Wavelength', plt.xlim: [220, 700]}
    '''
    # create list of axes to graph
    x_axes = [[pair[0] for pair in dataset] for dataset in args]    # a list of lists of the form [[ax1, ax2, ax3, ...], [bx1, bx2, bx3, ...], ...] where the letters represent the different datasets
    y_axes = [[pair[1] for pair in dataset] for dataset in args]    # a list of lists of the form [[ay1, ay2, ay3, ...], [by1, by2, by3, ...], ...] where the letters represent the different datasets
    
    # plot each graph
    for x, y in zip(x_axes, y_axes):
        plt.plot(x, y)

    # implementing the visualization parameters if passed
    for key, value in parameters.items():
        key(value)

    # display plot
    plt.show()

def main():
    # make sure the csv_name is passed
    try:
        csv_name = sys.argv[1]
    except Exception as e:
        raise Exception('Make sure to pass the desired csv name as a command-line argument.')

    # import the csv data
    csv_data = csvImport(csv_name)
    # example data processing
    csv_data2 = [[point[0], point[1]*2] for point in csv_data]

    # example visualization parameters
    vis = {}
    vis[plt.title] = 'Absorbance v. Wavelength'
    vis[plt.ylabel] = 'Absorbance (OD)'
    vis[plt.xlabel] = 'Wavelength (nm)'
    vis[plt.ylim] = [-0.05, 1.15]
    vis[plt.xlim] = [220, 700]

    # graphing the processed data
    graphData(csv_data, csv_data2, parameters=vis)

if __name__ == '__main__':
    main()






