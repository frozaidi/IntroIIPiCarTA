import time
import numpy as np
from sensor import GrayscaleSensor


class Interpreter(object):
    def __init__(self, sensitivity=0, polarity=1):
        """
        Instantiate the interpreter class, which processes information from the
        grayscale data
        :param sensitivity: The tolerance of the edge detection [0,1]
        :param polarity: Whether or not the line is lighter than the ground (1)
        or darker than the ground (-1)
        """
        self.sensitivity = sensitivity
        self.polarity = polarity

    def edge_detect(self, gry_list):
        """
        Function to process the grayscale data and detect the relative location
        of the line to follow
        :param gry_list: The array of grayscale data from the module
        """
        # Normalize the array to the maximum value obtained
        gry_list_norm = [float(i)/max(gry_list) for i in gry_list]
        # Get the difference between the max and min of the normalized values
        gry_list_diff = max(gry_list_norm)-min(gry_list_norm)
        # If the difference is larger than the tolerance, try to detect an edge
        if gry_list_diff > self.sensitivity:
            # The base relative direction should be based on the left and right
            # grayscale sensor values
            rel_dir = gry_list_norm[0]-gry_list_norm[2]
            # Calculate the amount of error to make a more continuous relative
            # direction. The deviation of the max or min value from the avg is
            # determined to be the error.
            if self.polarity == 1:
                error = (max(gry_list_norm)-np.mean(gry_list_norm))*(2/3)
            elif self.polarity == -1:
                error = (min(gry_list_norm)-np.mean(gry_list_norm))*(2/3)
            # The relative direction is then multiplied by error and polarity
            # to make a distinction between "just off-centered" and "very off-
            # centered"
            rel_dir_pol = rel_dir*error*self.polarity
        else:
            rel_dir_pol = 0

        return rel_dir_pol

    def interpret_bus(self, sens_bus, inter_bus, delay):
        """
        Function to run the interpret class in a loop using the sensor bus to
        read sensor value messages, and the interpreter bus to write direction
        messages for each loop
        :param sens_bus: The sensor bus class, containing sensor messages
        :param inter_bus: The interpreter bus class, containing direction
        messages
        :param delay: The time delay in seconds between each loop
        """
        while True:
            gry_list = sens_bus.read()
            rel_dir = self.edge_detect(gry_list)
            inter_bus.write(rel_dir)
            time.sleep(delay)


if __name__ == '__main__':
    sens = GrayscaleSensor()
    inter = Interpreter(0.0, -1)

    while True:
        list = sens.get_grayscale_data()
        rel_dir = inter.edge_detect(list)
        print("{:.3f}".format(rel_dir))
        time.sleep(1)