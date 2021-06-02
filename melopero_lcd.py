
import pcf8574
import utime
from machine import I2C, Pin

ENABLE_MASK = 0x04
READ_MASK = 0x02
REGISTER_SELECT_MASK = 0x01

LCD_CLEAR_CMD = 0x01
LCD_HOME_CMD = 0x02

LCD_RESET_CMD = 0x30
LCD_4BIT_CMD = 0x20
LCD_2LINES_CMD = 0x08

LCD_DISPLAY_OFF_CMD = 0x08          
LCD_DISPLAY_ON_CMD = 0x04 | LCD_DISPLAY_OFF_CMD

LCD_CURSOR_ON_CMD = 0x02 | LCD_DISPLAY_ON_CMD
LCD_CURSOR_OFF_CMD = LCD_DISPLAY_ON_CMD
LCD_CURSOR_BLINK_ON_CMD = 0x01 | LCD_CURSOR_ON_CMD 

LCD_ENTRY_MODE_CMD = 0x04 
LCD_ENTRY_INC_CMD = 0x02

LCD_BACKLIGHT_ON = 0x08
LCD_BACKLIGHT_OFF = 0

LCD_SHIFT_LEFT = 0x18
LCD_SHIFT_RIGHT = 0x04 | LCD_SHIFT_LEFT 
LCD_SET_DDRAM_CMD = 0x80

class LCD():
    # writing to DDRAM determines where the cursor is 
    # writing to CGRAM determines what to display
    
    def __init__(self, sda_pin=0, scl_pin=1, pcf_address=0x27, lines=2, cols=16):
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.pcf =  pcf8574.PCF8574(self.i2c, pcf_address)

        # Send reset command 3 times
        self._write_nibble(LCD_RESET_CMD)
        utime.sleep_ms(5)    # need to delay at least 4.1 msec
        self._write_nibble(LCD_RESET_CMD)
        utime.sleep_ms(1)
        self._write_nibble(LCD_RESET_CMD)
        utime.sleep_ms(1)

        # Put LCD into 4 bit mode
        self._write_nibble(LCD_4BIT_CMD)
        utime.sleep_ms(1)

        self.cursor_x = 0
        self.cursor_y = 0
        self.backlight = LCD_BACKLIGHT_ON

        self.set_display_size(lines, cols)

        self.display_off()
        self.backlight_on()
        self.clear()
        #self._write_byte(LCD_ENTRY_MODE_CMD | LCD_ENTRY_INC_CMD)
        self.hide_cursor()
        self.display_on()

        self._write_byte(LCD_4BIT_CMD | LCD_2LINES_CMD)

    def _write_nibble(self, nibble):
        # this function writes only a nibble and is used during initialization of the device
        self.pcf.port = (nibble & 0xF0) | ENABLE_MASK
        self.pcf.port = (nibble & 0xF0) # why? not really sure


    def _write_byte(self, byte, rs=False, write=True):
        # a byte is transmitted in two 4 bit transmission 
        # the connected pins are actually 8 but 3 are used for enable, rs and write pin
        # the data pins are actually only 4.
        flags = self.backlight
        flags |= REGISTER_SELECT_MASK if rs else 0
        flags |= READ_MASK if (not write) else 0

        self.pcf.port = flags | (byte & 0xF0)  | ENABLE_MASK # send first high order bits
        self.pcf.port = flags | (byte & 0xF0)  # why? not really sure 
        self.pcf.port = flags | ((byte & 0x0F) << 4) | ENABLE_MASK # then low order bits
        self.pcf.port = flags | ((byte & 0x0F) << 4)  # why? not really sure


    def set_display_size(self, lines, columns):
        if (not (0 < lines < 5)) or (not (0 < columns < 41)):
            raise ValueError("Lines must be between 1 and 4 and columns between 1 and 40")

        self.clear()
        self.num_lines = lines
        self.num_columns = columns
        self.set_cursor_position(0,0)


    def backlight_on(self):
        self.pcf.port = LCD_BACKLIGHT_ON
        self.backlight = LCD_BACKLIGHT_ON

    def backlight_off(self):
        self.pcf.port = LCD_BACKLIGHT_OFF
        self.backlight = LCD_BACKLIGHT_OFF

    
    def display_on(self):
        self._write_byte(LCD_DISPLAY_ON_CMD)

    
    def display_off(self):
        self._write_byte(LCD_DISPLAY_OFF_CMD)


    def clear(self):
        self.cursor_x = 0
        self.cursor_y = 0
        self._write_byte(LCD_CLEAR_CMD)
        utime.sleep_ms(5)
        self._write_byte(LCD_HOME_CMD)
        utime.sleep_ms(5)


    def hide_cursor(self):
        self._write_byte(LCD_CURSOR_OFF_CMD)

    def show_cursor(self):
        self._write_byte(LCD_CURSOR_ON_CMD)

    def blink_cursor_on(self):
        self._write_byte(LCD_CURSOR_BLINK_ON_CMD)

    def blink_cursor_off(self):
        self.show_cursor()

    def shift_left(self):
        self._write_byte(LCD_SHIFT_LEFT)

    def shift_right(self):
        self._write_byte(LCD_SHIFT_RIGHT)

    def set_cursor_position(self, x, y):
        self.cursor_x = x % self.num_columns
        self.cursor_y = y % self.num_lines

        addr = x & 0x3f
        if y & 1:
            addr += 0x40    # Lines 1 & 3 add 0x40
        if y & 2: 
            addr += self.num_columns   # Lines 2 & 3 add number of columns

        self._write_byte(LCD_SET_DDRAM_CMD | addr)


    def output_char(self, char):
        if char == '\n':
            self.cursor_y += 1
            self.cursor_x = 0
        else:
            self._write_byte(ord(char), rs=True)
            self.cursor_x += 1

        if self.cursor_x >= self.num_columns:
            self.cursor_x = 0
            self.cursor_y += 1

        self.cursor_y %= self.num_lines

        self.set_cursor_position(self.cursor_x, self.cursor_y)


    def output_string(self, string):
        for char in string:
            self.output_char(char)
    
