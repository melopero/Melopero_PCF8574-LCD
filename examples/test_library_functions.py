import melopero_lcd as mp
import utime


#create a new LCD object with custom parameters
lcd = mp.LCD(sda_pin=0, scl_pin=1, pcf_address=0x27, 
lines=2, cols=16)

#display a string
lcd.output_string('Hello World!\n:)')

#wait for 1 second (this command is repeated after every function for letting you see its result)
utime.sleep(1)

# clear the screen and set the cursor position to 0,0
lcd.clear()

#display a char and move the cursor forward 
lcd.output_char('a')

utime.sleep(1)

lcd.output_char('b')
utime.sleep(1)

lcd.output_char('c')
utime.sleep(1)


# set the position of the cursor
lcd.set_cursor_position(0,0)

# cursor show/hide and blink functions 
lcd.hide_cursor()

utime.sleep(1)

lcd.show_cursor()

utime.sleep(1)

lcd.blink_cursor_off()

utime.sleep(2)

lcd.blink_cursor_on()

utime.sleep(2)

# shift the text of 1 position
lcd.shift_right()

utime.sleep(1)

lcd.shift_left()

# set the display size
lcd.set_display_size(2, 16)

# turn on/off the backlight
lcd.backlight_off()
utime.sleep(1)
lcd.backlight_on()
utime.sleep(1)

# turn on/off the display
lcd.display_off()
utime.sleep(1)
lcd.display_on()
utime.sleep(1)

lcd.clear()
lcd.output_string('Happy Coding! :)')
