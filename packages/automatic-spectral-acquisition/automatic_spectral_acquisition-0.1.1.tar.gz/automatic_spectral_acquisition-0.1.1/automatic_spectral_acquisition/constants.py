############################# Debug options #############################
DEBUG:bool = False # Changes how exceptions are dealt with.
IGNORE_CONNECTIONS:bool = False # Ignore connections and fakes parts in order to test the program without the hardware.
IGNORE_REQUESTS:bool = False # Ignore requests.

############################# Arduino connection #############################
ARDUINO_BAUDRATE = 9600 # Baudrate for the arduino
ARDUINO_TIMEOUT = 0.1 # Timeout for the arduino

############################# Arduino commands #############################
GOTO    = "GOTO"     # Send
DONE    = "DONE"     # Receive - completed request
INVALID = "INVALID"  # Receive - invalid request
RUNNING = "RUNNING"  # Receive - motor is moving
STOP    = "STOP"     # Receive - stop button was pressed

############################# Oscilloscope settings #############################
OSCILLOSCOPE_TIMEOUT:float = 1000 # Timeout for the oscilloscope (ms)
OSCILLOSCOPE_HORIZONTAL_SCALE:float = 100e-3 # Time scale for the oscilloscope
OSCILLOSCOPE_VERTICAL_SCALE:float = 5e-3 # Vertical scale for the oscilloscope
OSCILLOSCOPE_OFFSET:float = 0 # Offset for the oscilloscope
OSCILLOSCOPE_SCALES = [5e-3, 10e-3, 20e-3, 50e-3, 100e-3, 200e-3, 500e-3, 1000e-3] # List of vertical scales for the oscilloscope

############################# Measurements options #############################
DEFAULT_NUMBER_OF_MEASUREMENTS:int = 3 # Default number of measurements to take for take for each wavelength.
WAVELENGTH_MIN:float = 200 # Minimum wavelength that can be measured.
WAVELENGTH_MAX:float = 1050 # Maximum wavelength that can be measured.
DEFAULT_POSITION:float = 0 # Default position for the motor.
CALIBRATION_POSITIONS:list[float] = [-4000 ,-2000 , 0, 2000, 4000] # Position of wavelengths used for calibration.

############################# File options #############################
OUTPUT_DIRECTORY:str = 'automatic_spectral_acquisition/output' # Directory to save the output files.
TEMP_DIRECTORY:str = 'automatic_spectral_acquisition/temp' # Directory to save the temporary files.
OUTPUT_FILE:str = 'output_{time}.csv' # Name of the output file. {time} will be replaced by the current time.
TIME_FORMAT:str = '%Y-%m-%d_%H-%M-%S' # Time format for the output file.
LOG_FILE:str = 'log.txt' # Name of the log file.
CONFIG_FILE:str = 'config.pkl' # Name of the configuration file.
DEFAULT_HEADER:list[str]=['wavelength(nm)', 'voltage(mV)', 'uncertainty(mV)'] # Default header for the output file.
