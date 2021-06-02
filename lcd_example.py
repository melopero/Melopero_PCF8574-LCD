
import melopero_lcd as mp


lcd = mp.LCD() # uses the lcd default address 0x27 and the pins 0 and 1
# lcd = mp.LCD(sda_pin=0, scl_pin=1, pcf_address=0x27, lines=2, cols=16)

# display a string
lcd.output_string('Hello World!\n:)')

# displays a char and advances the cursor
lcd.output_char('a')

# clears the screen and sets the cursor position to 0,0
lcd.clear()

# sets the position of the cursor
lcd.set_cursor_position(0,0)

# cursor show and blink function 
lcd.hide_cursor()
lcd.show_cursor()
lcd.blink_cursor_off()
lcd.blink_cursor_on()

# shift functions
lcd.shift_right()
lcd.shift_left()

# set the display size (doesnt affect shifting now...)
lcd.set_display_size(2, 16)

# display and backlight functions
lcd.backlight_off()
lcd.backlight_on()
lcd.display_off()
lcd.display_on()



lcd.clear()
lcd.output_string('Happy Coding! :)')