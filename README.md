# Melopero 
A MicroPython library for interfacing the <b>Raspberry Pi Pico</b> with the I2C LCD display included in the <b>Melopero Raspberry Pi Pico STARTER KIT</b>
<br> If you want to purchase the Melopero Raspberry Pi Pico starter kit click [HERE](https://www.melopero.com/shop/raspberry-pi/kits/raspberry-pi-pico-starter-kit/)

![melopero logo](images/i2c-lcd-1602-display.jpg)


# Pinout and connections

<table style="width:100%">
  <tr>
    <th>I2C LCD display</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>GND</td>
    <td>Ground pin</td>
  </tr>
  <tr>
    <td>VDD</td>
    <td>Input power pin. Connect to 5V on the Raspberry Pi Pico (pin 40 - VBUS)</td>
  </tr>
  <tr>
    <td>SDA</td>
    <td>I2C Serial DAta pin, connecto to Pico pin 1 (GP0)</td>
  </tr>
  <tr>
    <td>SCL</td>
    <td>I2C Serial CLock pin, connecto to Pico pin 2 (GP1)</td>
  </tr>
 
</table>

![Image](images/melopero-lcd-display-raspberry-pi-pico-connections.jpg)


### Install the library
We’ve created a downloadable UF2 file to let you install MicroPython with our LCD library included more easily:
<br>1. Download the uf2 file here: www.melopero.com/melopero-pico-kit.uf2 
<br>2. Push and hold the BOOTSEL button and plug your Pico into the USB port of your Raspberry Pi or other computer. Release the BOOTSEL button after your Pico is connected.
<br>3. It will mount as a Mass Storage Device called RPI-RP2.
<br>4. Drag and drop the MicroPython UF2 file onto the RPI-RP2 volume. Your Pico will reboot. You are now running MicroPython with our library included




## Example
```MicroPython
#In this basic example, the Pico will read its internal temperature and output on the LCD diplay


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

  
```


## Library Functions
```MicroPython
#create a new LCD object with default parameters
lcd = mp.LCD() 

#create a new LCD object with custom parameters
lcd = mp.LCD(sda_pin=0, scl_pin=1, pcf_address=0x27, 
lines=2, cols=16)

#display a string
lcd.output_string('Hello World!\n:)')

#display a char and move the cursor forward 
lcd.output_char('a')


# clear the screen and set the cursor position to 0,0
lcd.clear()

# set the position of the cursor
lcd.set_cursor_position(0,0)

# cursor show/hide and blink functions 
lcd.hide_cursor()
lcd.show_cursor()
lcd.blink_cursor_off()
lcd.blink_cursor_on()

# shift the text of 1 position
lcd.shift_right()
lcd.shift_left()

# set the display size
lcd.set_display_size(2, 16)

# turn on/off the backlight
lcd.backlight_off()
lcd.backlight_on()

# turn on/off the display
lcd.display_off()
lcd.display_on()
```

