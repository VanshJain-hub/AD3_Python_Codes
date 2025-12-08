from machine import Pin, I2C
import neopixel
import time

# --- I2C setup for TCS34725 ---
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
TCS34725_ADDR = 0x29

# --- TCS34725 Registers ---
COMMAND_BIT = 0x80
ENABLE = 0x00
ATIME = 0x01
CONTROL = 0x0F
CDATAL = 0x14
RDATAL = 0x16
GDATAL = 0x18
BDATAL = 0x1A

# --- TCS34725 Settings ---
ENABLE_AEN = 0x02
ENABLE_PON = 0x01

# --- Initialize TCS34725 ---
i2c.writeto_mem(TCS34725_ADDR, COMMAND_BIT | ATIME, bytes([0x00]))  # 700ms integration
i2c.writeto_mem(TCS34725_ADDR, COMMAND_BIT | CONTROL, bytes([0x01])) # 4x gain
i2c.writeto_mem(TCS34725_ADDR, COMMAND_BIT | ENABLE, bytes([ENABLE_PON | ENABLE_AEN]))

time.sleep(0.7)

# --- WS2812B setup ---
NUM_LEDS = 8
np = neopixel.NeoPixel(Pin(2), NUM_LEDS)  # GP2

# --- Helper functions ---
def read16(reg):
    data = i2c.readfrom_mem(TCS34725_ADDR, COMMAND_BIT | reg, 2)
    return data[1] << 8 | data[0]

def get_color():
    c = read16(CDATAL)
    r = read16(RDATAL)
    g = read16(GDATAL)
    b = read16(BDATAL)
    return r, g, b, c

def scale_rgb(r, g, b):
    max_val = max(r, g, b, 1)  # avoid division by zero#1000,100,100 1*255,100/1000*255,
    r_scaled = int(r / max_val * 255)
    g_scaled = int(g / max_val * 255)
    b_scaled = int(b / max_val * 255)
    return r_scaled, g_scaled, b_scaled

def set_leds(r, g, b):#255,100,100
    for i in range(NUM_LEDS):
        np[i] = (r, g, b)
    np.write()

# --- Main interactive loop ---
print("Enter RGB values (0-255) to set LEDs. Type 'exit' to quit.")

while True:
    try:
        inp = input("Enter R,G,B: ")
        if inp.lower() == "exit":
            break
        
        # Parse input
        parts = inp.split(",")
        if len(parts) != 3:
            print("Error: Enter 3 comma-separated values (R,G,B)")
            continue
        r = int(parts[0])
        g = int(parts[1])
        b = int(parts[2])
        mx=max(r,g,b)
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        # Set LEDs
        set_leds(r, g, b)

        # Wait for sensor to read
        time.sleep(0.5)

        # Read sensor and scale
        sr, sg, sb, sc = get_color()
        mxo=max(sr,sg,sb)
        sr_scaled, sg_scaled, sb_scaled = scale_rgb(sr, sg, sb)
        print(f"Sensor reads - R: {sr}, G: {sg}, B: {sb}, C:{sc}")
        print(f"Sensor reads - R: {sr_scaled}, G: {sg_scaled}, B: {sb_scaled}")
        print(f"input ratio :- {r/mx}:{g/mx}:{b/mx}\noutput ratio :- {sr/mxo}:{sg/mxo}:{sb/mxo}")
    except Exception as e:
        print("Error:", e)
