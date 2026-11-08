# G8 Traffic System

Grade 8 tech design project. A Raspberry Pi watches one approach of an intersection with an Adafruit VL53L0X distance sensor. Three RGB LEDs stand in for the traffic signals on three approaches, and an 8-pixel NeoPixel strip stands in for the fourth. When a vehicle comes close enough, the program counts it and then runs one full signal cycle.

## How a vehicle is detected

The VL53L0X runs in continuous mode over I2C. `sensor.range` is the distance in millimetres.

The main loop keeps a count of close readings:

- A reading of **25 mm or less** counts as one vehicle.
- After each count the program waits **1.5 seconds**, so one vehicle is not counted again immediately. The current count is printed.
- Each new count restarts a **15 second** timer.

The signal cycle in `lightLoop()` runs when either of these happens:

- the count reaches **4**, or
- **15 seconds** pass since the last count (or since the timer started).

The count is then reset to 0 and the timer starts again. On startup, before any vehicle is seen, all three RGB LEDs and the NeoPixel strip are red.

## How the lights change

`lightLoop()` walks the intersection one approach at a time. Each approach gets green, then amber, then red, before the next approach turns green. Times below are how long that step is held.

| Step | LED 1 | LED 2 | LED 3 | NeoPixels | Hold |
| --- | --- | --- | --- | --- | --- |
| 1 | Green | Red | Red | Red | 5 s |
| 2 | Amber | Red | Red | Red | 4 s |
| 3 | Red | Green | Red | Red | 5 s |
| 4 | Red | Amber | Red | Red | 4 s |
| 5 | Red | Red | Green | Red | 5 s |
| 6 | Red | Red | Amber | Red | 4 s |
| 7 | Red | Red | Red | Green | 5 s |
| 8 | Red | Red | Red | Amber | 4 s |
| 9 | Red | Red | Red | Red | — |

RGB colours used by the three LEDs:

- Red `(1, 0, 0)`
- Amber `(1, 0.15, 0)`
- Green `(0, 1, 0)`

NeoPixel colours (GRB, one colour across all 8 pixels):

- Red `0x100000`
- Green `0x00FF00`
- Amber `0xFF5B00`

Distance is read during the cycle, but those readings do not change the sequence. The cycle always runs in the order above.

## Hardware

- Raspberry Pi with I2C and SPI enabled
- [Adafruit VL53L0X](https://www.adafruit.com/product/3317) time-of-flight sensor (library: `adafruit_vl53l0x.VL53L0X`)
- 3 RGB LEDs, driven with `gpiozero.RGBLED` (BCM pin numbers)
- 8 NeoPixels on SPI, driven with `neopixel_spi` (`NeoPixel_SPI`, pixel order GRB)

### RGB LED pins

| Signal | Red | Green | Blue |
| --- | --- | --- | --- |
| LED 1 | GPIO 12 | GPIO 19 | GPIO 26 |
| LED 2 | GPIO 6 | GPIO 22 | GPIO 27 |
| LED 3 | GPIO 18 | GPIO 23 | GPIO 24 |

`gpiozero` uses BCM numbering. Each colour pin is the matching leg of that RGB LED.

### Sensor and NeoPixels

| Part | Connection |
| --- | --- |
| VL53L0X SDA | GPIO 2 (I2C SDA) |
| VL53L0X SCL | GPIO 3 (I2C SCL) |
| VL53L0X power | 3.3 V and GND |
| NeoPixel data | SPI MOSI, GPIO 10 (`board.SPI()`) |
| NeoPixel power | 5 V and a common GND with the Pi |

The sensor is created with `board.I2C()` and `VL53L0X(i2c)`, then `start_continuous()`. The strip is 8 pixels: `NeoPixel_SPI(spi, 8, pixel_order=GRB, auto_write=True)`.

## Software

Runs on Raspberry Pi OS with Python 3. Enable I2C and SPI (`sudo raspi-config`, then reboot) before the first run.

Libraries imported by `main.py`:

```bash
pip3 install adafruit-blinka adafruit-circuitpython-vl53l0x adafruit-circuitpython-neopixel-spi gpiozero RPi.GPIO
```

`gpiozero` and `RPi.GPIO` are usually already installed on Raspberry Pi OS. Blinka is what provides the `board` module (`board.I2C()` and `board.SPI()`).

## Run

```bash
python3 main.py
```

Leave the sensor aimed across the approach you want to watch. When something is within 25 mm, the printed count increases. After 4 counts, or after 15 seconds, the LEDs and the NeoPixel strip run the cycle in the table above, then the program waits for the next vehicle.
