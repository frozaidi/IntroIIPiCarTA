import time
from robot_hat import ADC


class GrayscaleSensor(object):
    def __init__(self):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")

    def get_grayscale_data(self):
        """
        Function calls the ADC channels instantiated by class and returns an
        array of three values, corresponding to the three grayscale sensors
        """
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

    def sensor_bus(self, bus, delay):
        """
        Function to run the sensor class in a loop using a broadcast bus to
        write sensor value messages for each loop
        :param bus: The bus class
        :param delay: The time delay in seconds between each loop
        """
        while True:
            adc_list = self.get_grayscale_data()
            bus.write(adc_list)
            time.sleep(delay)