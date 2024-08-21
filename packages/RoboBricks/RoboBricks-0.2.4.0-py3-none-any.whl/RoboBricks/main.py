#from .constants_lib import RoboBricksConst
import smbus

class Motor:
    
    # Addresses of motors on the bus
    BIG_RED = 0x03
    BIG_GREEN = 0x04
    BIG_BLUE = 0x05
    BIG_YELLOW = 0x06
    #BIG_YELLOW = 0x0C
    
    # State of motors
    STATE_UNDEFINED = 0
    STATE_STOP = 1
    STATE_LOOP = 2
    STATE_ANGLE = 3
    
    # Direction of rotation
    DIRECTION_UNDEFINED = 0
    DIRECTION_FORWARD = 1
    DIRECTION_BACKWARD = 2
    
    def __init__(self, address, bus=1):
        if address >= self.BIG_RED and address <= self.BIG_YELLOW:
            self.address = address
            self.bus = smbus.SMBus(bus)
        else:
            print('Invalid color for motor')
    
    def debug_read(self):
        return self.bus.read_i2c_block_data(self.address, 0, 10)
    
    def debug_write(self, data):
        self.bus.write_i2c_block_data(self.address, 0, data)
    
    '''
    State:
    Direction:
    Speed: 0-100%
    Angle: 0-65535 deg
    '''
    def set_state(self, state, direction=0, speed=0, angle = 0):
        self.state = state
        self.direction = direction
        self.speed = speed
        self.angle = angle
        
        if self.state == self.STATE_STOP:
            self.__state_stop()
        elif self.state == self.STATE_LOOP:
            self.__state_loop()
        elif self.state == self.STATE_ANGLE:
            self.__state_angle(self.angle)
    
    def get_state(self):
        data = self.bus.read_i2c_block_data(self.address, 0, 10)
        return ((data[4] << 8) + data[5])
    
    '''
    Пакет для привода:
    [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9]
    b0 - параметр для служебных функций: 0 - нормальная работа
    b1 - направление вращения: 0 или 1
    b2 - скорость вращения: от 0 до 100
    b3 - старший байт угла
    b4 - младший байт угла
    '''
    def __state_stop(self):
        data = [0,self.state,0,0,0,0,0,0,0,0]
        self.bus.write_i2c_block_data(self.address, 0, data)
        
    def __state_loop(self):
        data = [0,self.state,self.direction,self.speed,0,0,0,0,0,0]
        self.bus.write_i2c_block_data(self.address, 0, data)
        
    def __state_angle(self, angle):
        angleh = angle >> 8
        anglel = angle
        data = [0,self.state,self.direction,self.speed,angleh,anglel,0,0,0,0]
        self.bus.write_i2c_block_data(self.address, 0, data)
        

class Button:
    
    # Addresses of buttons on the bus
    RED = 0x0D
    GREEN = 0x0E
    BLUE = 0x0F
    YELLOW = 0x10
    BLACK = 0x11
    #BLACK = 0x16
    
    # Button states
    STATE_RELEASED = 0
    STATE_CLICKED = 1
    STATE_PRESSED = 2
    
    def __init__(self, address, bus=1):
        if address >= self.RED and address <= self.BLACK:
            self.address = address
            self.bus = smbus.SMBus(bus)
        else:
            print('Invalid color for button')
        
    def get_state(self):
        res = self.__get_data_button()
        if res == self.STATE_RELEASED:
            return 'released'
        elif res == self.STATE_PRESSED:
            return 'pressed'
        
    def __get_data_button(self):
        return self.bus.read_byte_data(self.address, 1)
    