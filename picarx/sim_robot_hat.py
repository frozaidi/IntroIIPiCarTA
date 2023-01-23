import math, time


class Servo(object):
    """
    Simulated Servo class, returns any angle it's given
    """
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50

    def __init__(self, pwm):
        super().__init__()
        self.pwm = pwm

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        if not (isinstance(angle, int) or isinstance(angle, float)):
            raise ValueError("Angle value should be int or float value, not %s" % type(angle))
        if angle < -90:
            angle = -90
        if angle > 90:
            angle = 90
        return angle


class PWM():
    """
    Simulated PWM class
    """
    REG_CHN = 0x20
    REG_FRE = 0x30
    REG_PSC = 0x40
    REG_ARR = 0x44

    ADDR = 0x14

    CLOCK = 72000000

    def __init__(self, channel, debug="critical"):
        pass
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError("PWM channel should be between [P1, P14], not {0}".format(channel))

        self.debug = debug
        self.channel = channel
        self.timer = int(channel/4)
        self._pulse_width = 0
        self._freq = 50
        self.freq(50)

    def freq(self, *freq):
        if len(freq) == 0:
            return self._freq
        else:
            self._freq = int(freq[0])
            # [prescaler,arr] list
            result_ap = []
            # accuracy list
            result_acy = []
            # middle value for equal arr prescaler
            st = int(math.sqrt(self.CLOCK/self._freq))
            # get -5 value as start
            st -= 5
            # prevent negetive value
            if st <= 0:
                st = 1
            for psc in range(st, st+10):
                arr = int(self.CLOCK/self._freq/psc)
                result_ap.append([psc, arr])
                result_acy.append(abs(self._freq-self.CLOCK/psc/arr))
            i = result_acy.index(min(result_acy))
            psc = result_ap[i][0]
            arr = result_ap[i][1]
            self.prescaler(psc)
            self.period(arr)

    def prescaler(self, *prescaler):
        if len(prescaler) == 0:
            return self._prescaler
        else:
            self._prescaler = int(prescaler[0]) - 1
            reg = self.REG_PSC + self.timer

    def period(self, *arr):
        timer = [
            {
                "arr": 0
            }
        ] * 4
        if len(arr) == 0:
            return timer[self.timer]["arr"]
        else:
            timer[self.timer]["arr"] = int(arr[0]) - 1
            reg = self.REG_ARR + self.timer

    def pulse_width(self, *pulse_width):
        if len(pulse_width) == 0:
            return self._pulse_width
        else:
            self._pulse_width = int(pulse_width[0])
            reg = self.REG_CHN + self.channel

    def pulse_width_percent(self, *pulse_width_percent):
        timer = [
            {
                "arr": 0
            }
        ] * 4
        if len(pulse_width_percent) == 0:
            return self._pulse_width_percent
        else:
            self._pulse_width_percent = pulse_width_percent[0]
            temp = self._pulse_width_percent / 100.0
            # print(temp)
            pulse_width = temp * timer[self.timer]["arr"]
            self.pulse_width(pulse_width)


class Pin(object):
    """
    Simulated Pin class
    """
    PULL_NONE = None

    _dict = {
        "BOARD_TYPE": 12,
    }

    _dict_1 = {
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  19,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,
    }

    _dict_2 = {
        "D0":  17,
        "D1":   4,  # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,  # Removed
        "D7":   4,  # Removed
        "D8":   5,  # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25,  # Changed
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5,  # Changed
    }

    def __init__(self, *value):
        pass

    def init(self, mode, pull=PULL_NONE):
        self._pull = pull
        self._mode = mode

    def dict(self, *_dict):
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict)

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):
        if len(value) == 0:
            self.mode(self.IN)
            result = 1
            return result
        else:
            value = value[0]
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        if len(value) == 0:
            return self._mode
        else:
            mode = value[0]
            self._mode = mode

    def pull(self, *value):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.mode(self.IN)

    def name(self):
        return "GPIO%s" % self._pin

    def names(self):
        return [self.name, self._board_name]

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4 = 4
        GPIO5 = 5
        GPIO6 = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass


class ADC():
    """
    Simulated ADC class
    """
    ADDR = 0x14

    def __init__(self, chn):
        super().__init__()
        if isinstance(chn, str):
            if chn.startswith("A"):
                chn = int(chn[1:])
            else:
                raise ValueError("ADC channel should be between [A0, A7], not {0}".format(chn))
        if chn < 0 or chn > 7:
            self._error('Incorrect channel range')
        chn = 7 - chn
        self.chn = chn | 0x10
        self.reg = 0x40 + self.chn

    def read(self):
        self.send([self.chn, 0, 0], self.ADDR)

        value_h = self.recv(1, self.ADDR)[0]
        value_l = self.recv(1, self.ADDR)[0]

        value = (value_h << 8) + value_l
        return value

    def read_voltage(self):
        return self.read*3.3/4095


class fileDB(object):
    """
    Simulated file database class
    """

    def __init__(self, db:str, mode:str=None, owner:str=None):
        '''Init the db_file is a file to save the datas.'''

        # Check if db_file is defined
        if db != None:
            self.db = db
        else:
            self.db = "config"

    def get(self, name, default_value=0):
        return default_value

    def set(self, name, value):
        pass

class Ultrasonic():
    def __init__(self, trig, echo, timeout=0.02):
        self.trig = trig
        self.echo = echo
        self.timeout = timeout

    def _read(self):
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.00001)
        self.trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        return cm

    def read(self, times=10):
        for i in range(times):
            a = self._read()
            if a != -1:
                return a
        return -1

class Grayscale_Module(object):
    def __init__(self, pin0, pin1, pin2, reference=1000):
        self.chn_0 = ADC(pin0)
        self.chn_1 = ADC(pin1)
        self.chn_2 = ADC(pin2)
        self.reference = reference

    def get_line_status(self,fl_list):

        if fl_list[0] > self.reference and fl_list[1] > self.reference and fl_list[2] > self.reference:
            return 'stop'
            
        elif fl_list[1] <= self.reference:
            return 'forward'
        
        elif fl_list[0] <= self.reference:
            return 'right'

        elif fl_list[2] <= self.reference:
            return 'left'

    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list