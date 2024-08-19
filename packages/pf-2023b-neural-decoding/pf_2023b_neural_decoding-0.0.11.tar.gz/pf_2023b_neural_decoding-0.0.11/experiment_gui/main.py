from json_parser import JsonParser
import pygame
import numpy as np
    

def run(json_path, output_path, driver): 
    """
    Executes a data collection and recording procedure using the specified BCI driver.

    This function initializes a connection with the BCI driver, starts streaming data, 
    and collects samples based on the states defined in the provided JSON configuration. 
    It then writes the collected data, along with markers, to a specified output file.

    Args:
        json_path (str): The file path to the JSON configuration file that defines the machine states 
                         and associated parameters for the data collection.
        output_path (str): The file path where the collected data will be saved. The data will be 
                           written in a tab-delimited format with each line containing sensor values 
                           followed by the associated marker.
        driver (object): An instance of a BCI driver class (e.g., CytonDaisyBCIDriver) that handles 
                          the connection and data acquisition from the BCI device.

    Raises:
        Exception: Raises exceptions related to connection issues, data retrieval errors, or 
                   file writing issues.

    Example:
        # Create a driver instance
        driver = drivers.CytonDaisyBCIDriver(buffer_size, 'COM4')
        
        # Run the data collection procedure
        run('path/to/config.json', 'path/to/output.txt', driver)
    """

    pygame.init()
    pygame.mouse.set_visible(False)
       
    parser = JsonParser(json_path)
    initial_state = parser.get_machine_state()


    current_state = initial_state[0]
    first = True
    experiment_data = {}
    
    driver.connect()
    driver.start_stream()

    while current_state != None:
        if first: 
            current_state.show()
            first = False     

        expected_samples = int(current_state.duration * driver.sampling_frequency)
        if driver.get_board_data_count() >= expected_samples:
            retrieved_data = driver.get_board_data()
            if current_state.has_marker():
                experiment_data[current_state.get_marker()] = retrieved_data[:, :expected_samples]
            current_state = current_state.next_state
            first = True

    driver.stop_stream()
    driver.release_session()
    pygame.quit()
    
    with open(output_path, 'w') as file: 
        for k,v in experiment_data.items ():
            for line in np.transpose(v):
                list = []
                list.extend(line.tolist())
                list.append(k)
                file.write('\t'.join(map(str, list)) + '\n')
    file.close()
