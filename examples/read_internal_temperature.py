#In this basic example, the Pico will read its internal temperature and show it on the LCD diplay


import machine
import utime

import melopero_lcd as mp

lcd = mp.LCD()

adc = machine.ADC(4)
conversion_factor = 3.3 / (65535)

while True:
    reading = adc.read_u16() * conversion_factor
    temperature = 25 - (reading - 0.706) / 0.001721
    
    lcd.output_string('Temp: ')
    lcd.output_string( str(temperature) )
    
    utime.sleep(2)
    lcd.clear()
