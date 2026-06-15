# import libraries, modules, and functions here:
import pandas 
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM 
import astropy.units as un
import numpy as np

cosmo = FlatLambdaCDM(H0=70 * un.km / un.s / un.Mpc, Tcmb0=2.725 * un.K, Om0=0.3)

def print_stats(data_column):
    '''
    prints out the minimum, maximum, and median 
    values of a pandas data frame column.
    
    Parameters:
    -----------
    data_column: pandas.DataFrame()
        the data for which statistics should be printed
        
    Returns:
    -----------
    None
    
    '''
    print(f"The minimum is {data_column.min()}")
    print(f"The maximum is {data_column.max()}")
    print(f"The median is {data_column.median()}")
    print(f"The mean is {data_column.mean()}")
    
def plot_histogram(data_column, plot_title, x_label):
    '''
    Displays a histogram of the input data 
    frame column.
    
    Parameters:
    -----------
    data_column: pandas.DataFrame()
        the data to plot on the histogram
    plot_title: string
        The title of the histogram plot
    x_label: string
        The label for the x-axis of the plot
    
    Returns:
    -----------
    None
    '''
    plt.figure(figsize=(6, 4), dpi=100) #The figure size is given in inches. Play with the figure size. 
                                        #Play with the dots-per-inch (dpi) to vary resolution 
    plt.hist(data_column) #tip: type help(np.hist) in a separate cell to see more plotting options for this function
    plt.title(plot_title)

    plt.xlabel(x_label) 

    plt.show()
    
    
def convert_redshift_to_distance(galaxy_redshifts): #this function needs redshift values to convert
    '''
    Converts input redshifts to distances in 
    lightyears using the universe cosmology (cosmo) 
    pre-defined by the user.
    
    Parameters:
    -----------
    
    
    Returns:
    -----------
    
    '''
    
    lightyears_per_parsec = 3.26156 # lightyears per parsec

    luminosity_distance_Mpc = cosmo.luminosity_distance(galaxy_redshifts).value # in units of Mega parsecs (Mpc)
    
    luminosity_distance_pc = luminosity_distance_Mpc*(1e6) #convert from Mpc to parsecs (pc)
    
    luminosity_distance_lightyears = luminosity_distance_pc*lightyears_per_parsec #convert from pc to lightyears
        
    return luminosity_distance_lightyears #add a return variable so we can use these distances elsewhere in our code

def plot_scatter(data_column_x, data_column_y, plot_title, x_label, y_label):
    '''
    Displays a histogram of the input data 
    frame columns.
    
    Parameters:
    -----------
    data_column_x: pandas.DataFrame()
        The x-axis data of the scatter plot
    data_column_y: pandas.DataFrame()
        The y-axis data of the scatter plot
    plot_title: string
        The title of the histogram plot
    x_label: string
        The label for the x-axis of the plot
    y_label: string
        The label for the y-axis of the plot
    Returns:
    -----------
    '''
    plt.figure(figsize=(6, 4), dpi=100) #The figure size is given in inches. Play with the figure size. 
                                        #Play with the dots-per-inch (dpi) to vary resolution 
    plt.scatter(data_column_x, data_column_y, c='red')
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    plt.show()
    
file_names = ['Data/Random-SF-Galaxies-PortsmouthGroup_properties.csv',
              'Data/Random-SB-Galaxies-PortsmouthGroup_properties.csv', 
              'Data/Random-AGN-Galaxies-PortsmouthGroup_properties.csv']

# your code here
for file in file_names:
    print('file name = ', file)
    
    # 1. read in the file
    # recall that we used the pandas library to read in a CSV file during the last workshop
    galaxies_df = pandas.read_csv(file, comment='#') #remove this line
    
    
    # 2. display the min, max, and median values of 'logMass' and 'SFR' (star formation rate) columns
    print('STATISTICS:')
    print('log10 of the Stellar mass:')
    print_stats(galaxies_df['logMass'])
    
    print('Star formation rates:')
    print_stats(galaxies_df['SFR'])
    
    
    # 3. display a histogram of the 'logMass' and 'SFR' values
    
    print('Displaying the distributions of logMass values...')
    plot_histogram(galaxies_df['logMass'], 'Stellar Masses of Galaxies', 'log(Stellar Mass/Solar Mass)')
    
    
    print('Displaying the distributions of star formation rate values...')
    plot_histogram(np.log10(galaxies_df['SFR']), 'SFRs of Galaxies', 'log(SFR) units: Solar Mass/year')
    
    print('Converting redshifts to distances in lightyears...')
    distances_lyr = convert_redshift_to_distance(galaxies_df['z'])
    
    print('Taking the logarithm of distances and SFRs...')
    log_distances = np.log10(distances_lyr)
    log_SFRs = np.log10(galaxies_df['SFR'])
    
    print('Displaying the logMass vs log10 of distance...')
    plot_scatter(log_distances, galaxies_df['logMass'], 'logMass vs logDistance', 'logDistance (lightyears)', 'logMass (Stellar Mass/Solar Mass)')

    print('Displaying the logSFR vs log10 of distance...')
    plot_scatter(log_distances, log_SFRs, 'logSFR vs logDistance', 'logDistance (lightyears)', 'log SFR (Solar Mass/year)')
    print('==================================================')
    
    
    filtered_galaxies_df = galaxies_df[galaxies_df['SFR']>2]
    
    print('Taking the logarithm of filtered distances and SFRs...')
    filtered_distances_lyr = convert_redshift_to_distance(filtered_galaxies_df['z'])
    filtered_log_distances = np.log10(filtered_distances_lyr)
    filtered_log_SFRs = np.log10(filtered_galaxies_df['SFR'])

    print('Displaying the filtered logSFR vs log10 of distance...')
    plot_scatter(filtered_log_distances, filtered_log_SFRs, 'logSFR vs logDistance', 'logDistance (lightyears)', 'log SFR (Solar Mass/year)')

    print('==================================================')