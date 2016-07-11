from __future__ import division
import yaml
import collections
import math

"""
 * The color white.  In the default sRGB space.
"""
WHITE     = (255, 255, 255);

"""
 * The color light gray.  In the default sRGB space.
"""
LIGHT_GRAY = (192, 192, 192);

"""
 * The color gray.  In the default sRGB space.
"""
GRAY      = (128, 128, 128);

"""
 * The color dark gray.  In the default sRGB space.
"""
DARK_GRAY  = (64, 64, 64);

"""
 * The color black.  In the default sRGB space.
"""
BLACK     = (0, 0, 0);

"""
 * The color red.  In the default sRGB space.
"""
RED       = (255, 0, 0);

"""
 * The color pink.  In the default sRGB space.
"""
PINK      = (255, 175, 175);

"""
 * The color orange.  In the default sRGB space.
"""
ORANGE    = (255, 200, 0);

"""
 * The color yellow.  In the default sRGB space.
"""
YELLOW    = (255, 255, 0);

"""
 * The color green.  In the default sRGB space.
"""
GREEN     = (0, 255, 0);

"""
 * The color magenta.  In the default sRGB space.
"""
MAGENTA   = (255, 0, 255);

"""
 * The color cyan.  In the default sRGB space.
"""
CYAN      = (0, 255, 255);

"""
 * The color blue.  In the default sRGB space.
"""
BLUE      = (0, 0, 255);

with open('config/lights.yaml', 'r') as f:
    LEDS = yaml.load(f)["leds"]

def find_leds(prefix):
    leds = []
    for key in sorted(LEDS):
        if key.startswith(prefix):
            leds.append(key)
    return leds

# Input a value 0 to 1 to get a color value.
# The colours are a transition r - g - b - back to r.
def wheel(wheelPos):
    wheelPos = 255/255 - (wheelPos % 1);
    if wheelPos < 85/255:
        return (round((255/255 - wheelPos * 3) * 255), 0, round((wheelPos * 3) * 255));

    if wheelPos < 170/255:
        wheelPos -= 85/255;
        return (0, round((wheelPos * 3) * 255), round((255/255 - wheelPos * 3) * 255));

    wheelPos -= 170/255;
    return (round((wheelPos * 3) * 255), round((255/255 - wheelPos * 3) * 255), 0);

"""
 * Creates a new <code>Color</code> that is a brighter version of this
 * <code>Color</code>.
 * <p>
 * This method applies an arbitrary scale factor to each of the three RGB
 * components of this <code>Color</code> to create a brighter version
 * of this <code>Color</code>. Although <code>brighter</code> and
 * <code>darker</code> are inverse operations, the results of a
 * series of invocations of these two methods might be inconsistent
 * because of rounding errors.
 * @return     a new <code>Color</code> object that is
 *                 a brighter version of this <code>Color</code>.
 * @see        java.awt.Color#darker
 * @since      JDK1.0
"""
def brighter(color, factor=0.7):
    r = color[0]
    g = color[1]
    b = color[2]

    """
    /* From 2D group:
     * 1. black.brighter() should return grey
     * 2. applying brighter to blue will always return blue, brighter
     * 3. non pure color (non zero rgb) will eventually return white
     */
    """
    i = round(1.0/(1.0-factor));
    if r == 0 and g == 0 and b == 0:
       return (i, i, i)

    if r > 0 and r < i:
        r = i;
    if g > 0 and g < i:
        g = i;
    if b > 0 and b < i:
        b = i;

    return (min(round(r/factor), 255),
            min(round(g/factor), 255),
            min(round(b/factor), 255));

"""
 * Creates a new <code>Color</code> that is a darker version of this
 * <code>Color</code>.
 * <p>
 * This method applies an arbitrary scale factor to each of the three RGB
 * components of this <code>Color</code> to create a darker version of
 * this <code>Color</code>.  Although <code>brighter</code> and
 * <code>darker</code> are inverse operations, the results of a series
 * of invocations of these two methods might be inconsistent because
 * of rounding errors.
 * @return  a new <code>Color</code> object that is
 *                    a darker version of this <code>Color</code>.
 * @see        java.awt.Color#brighter
 * @since      JDK1.0
"""
def darker(color, factor = 0.7):
    return (max(round(color[0]*factor), 0),
            max(round(color[1]*factor), 0),
            max(round(color[2]*factor), 0))

def blend(color1, factor, color2):
    contrib1 = darker(color1, factor)
    contrib2 = darker(color2, 1.0-factor)
    return (min(contrib1[0]+contrib2[0], 255), 
            min(contrib1[1]+contrib2[1], 255),
            min(contrib1[2]+contrib2[2], 255))

def rainbow(length):
    retval = []
    for i in range(length):
        retval.append(wheel(i/length))
    return retval

def wave(color, length):
    retval = []
    for i in range(length):
        retval.append(darker(color, (1 + math.cos(2*math.pi * i / length)) / 2))
    return retval
        
def replicate(pattern, count):
    retval = []
    for item in pattern:
        for i in range(count):
            retval.append(item)
    return retval;

def to_hex(color):
    return ''.join('{:02x}'.format(int(x)) for x in color)
    
def gen_frame(leds, pattern):
    items = {}
    i = 0
    for led in leds:
        items[led] = to_hex(pattern[i])
        i = (i + 1) % len(pattern)
    frame = {}
    frame["tocks"] = 1
    frame["leds"] = items
    return frame

def rotate(l,n):
    return l[n:] + l[:n]

def gen_show(leds, pattern, step = 1):
    frames = []
    for i in range(len(pattern)//step):
        frames.append(gen_frame(leds, rotate(pattern, -i * step)))
    return frames

def write_show(name, show):
    with open('shows/'+name+'.yaml', 'w') as outfile:
        outfile.write(yaml.dump(show))

def color_chase(leds, color, black_length=1):
    return gen_show(leds, [color, darker(color)] + [BLACK]*black_length)

def halcon_lighthouse(leds):
    return gen_show(leds, [darker(GREEN), GREEN, darker(GREEN)] + [BLACK]*3 + [darker(MAGENTA), MAGENTA, darker(MAGENTA)] + [BLACK]*3)

def rainbow_chase(leds, length = None):
    return gen_show(leds, rainbow(len(leds))) if length == None else gen_show(leds, rainbow(length)) 

def rainbow_fade(leds):
    return gen_show(leds, replicate(rainbow(60), len(leds)), len(leds))

def color_wave(leds, color):
    return gen_show(l_vendor_bottom, replicate(wave(color, 60), len(l_vendor_bottom)), len(l_vendor_bottom))

def color_flash(leds, color):
    return gen_show(leds, replicate([WHITE, darker(WHITE), BLACK]*2 + [BLACK]*22, len(leds)), len(leds))

l_vendor_bottom = find_leds("l_vendor_bottom")
write_show("vendor_bottom_chase_red", color_chase(l_vendor_bottom, RED))
write_show("vendor_bottom_lighthouse_halcon", halcon_lighthouse(l_vendor_bottom))
write_show("vendor_bottom_chase_rainbow", rainbow_chase(l_vendor_bottom))
write_show("vendor_bottom_fade_rainbow", rainbow_fade(l_vendor_bottom))
write_show("vendor_bottom_wave_red", color_wave(l_vendor_bottom, RED))

l_vendor_left = find_leds("l_vendor_left")
write_show("vendor_left_chase_red", color_chase(l_vendor_left, RED))
write_show("vendor_left_lighthouse_halcon", halcon_lighthouse(l_vendor_left))
write_show("vendor_left_chase_rainbow", rainbow_chase(l_vendor_left))
write_show("vendor_left_fade_rainbow", rainbow_fade(l_vendor_left))
write_show("vendor_left_wave_red", color_wave(l_vendor_left, RED))

l_photos_arrow = find_leds("l_photos_arrow")
write_show("photos_arrow_chase_red", color_chase(l_photos_arrow, RED, 22))
write_show("photos_arrow_chase_rainbow", rainbow_chase(l_photos_arrow, 30))
write_show("photos_arrow_flash_white", color_flash(l_photos_arrow, WHITE))

l_spinner_arrow = find_leds("l_spinner_arrow")
write_show("spinner_arrow_chase_red", color_chase(l_spinner_arrow, RED, 22))
write_show("spinner_arrow_chase_rainbow", rainbow_chase(l_spinner_arrow, 30))
write_show("spinner_arrow_flash_white", color_flash(l_spinner_arrow, WHITE))

l_left_kickout_arrow = find_leds("l_left_kickout_arrow")
write_show("left_kickout_arrow_chase_red", color_chase(l_left_kickout_arrow, RED, 22))
write_show("left_kickout_arrow_chase_rainbow", rainbow_chase(l_left_kickout_arrow, 30))
write_show("left_kickout_arrow_flash_white", color_flash(l_left_kickout_arrow, WHITE))

l_right_kickout_arrow = find_leds("l_right_kickout_arrow")
write_show("right_kickout_arrow_chase_red", color_chase(l_right_kickout_arrow, RED, 22))
write_show("right_kickout_arrow_chase_rainbow", rainbow_chase(l_right_kickout_arrow, 30))
write_show("right_kickout_arrow_flash_white", color_flash(l_right_kickout_arrow, WHITE))
