from __future__ import division
import yaml
import collections
import math

COLORS = {}

"""
 * The color white.  In the default sRGB space.
"""
COLORS['white']     = (255, 255, 255);

"""
 * The color light gray.  In the default sRGB space.
"""
COLORS['lightgray'] = (192, 192, 192);

"""
 * The color gray.  In the default sRGB space.
"""
COLORS['gray']      = (128, 128, 128);

"""
 * The color dark gray.  In the default sRGB space.
"""
COLORS['darkgray']  = (64, 64, 64);

"""
 * The color black.  In the default sRGB space.
"""
COLORS['black']     = (0, 0, 0);

"""
 * The color red.  In the default sRGB space.
"""
COLORS['red']       = (255, 0, 0);

"""
 * The color pink.  In the default sRGB space.
"""
COLORS['pink']      = (255, 175, 175);

"""
 * The color orange.  In the default sRGB space.
"""
COLORS['oragne']    = (255, 200, 0);

"""
 * The color yellow.  In the default sRGB space.
"""
COLORS['yellow']    = (255, 255, 0);

"""
 * The color green.  In the default sRGB space.
"""
COLORS['green']     = (0, 255, 0);

"""
 * The color magenta.  In the default sRGB space.
"""
COLORS['magenta']   = (255, 0, 255);

"""
 * The color cyan.  In the default sRGB space.
"""
COLORS['cyan']      = (0, 255, 255);

"""
 * The color blue.  In the default sRGB space.
"""
COLORS['blue']      = (0, 0, 255);

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


'''*************************************************************************************************'''

class LedsIterator(object):
    def __init__(self, leds):
        self.leds = leds
        self.i = 0
        
    def next(self):
        if self.i >= len(self.leds):
            raise StopIteration
        else:
            retval = self.leds[self.i]
            self.i += 1
            return retval
        
class Leds(object):
    def __init__(self, leds_name, start_index=None, end_index=None):
        self.leds_name = leds_name
        self.leds = find_leds("l_"+self.leds_name)
        if end_index != None:
            self.leds = self.leds[:end_index]
        if start_index != None:
            self.leds = self.leds[start_index:]

    def __str__(self):
        return self.leds_name            
    
    def __len__(self):
        return len(self.leds)
        
    def __iter__(self):
        return LedsIterator(self)
    
    def __getitem__(self, key):
        return self.leds[key % len(self.leds)]
        
'''*************************************************************************************************'''

class Show(object):
    def __init__(self, leds):
        self.leds = leds
        
    def write(self):
        write_show(self.name(), self.show()) 

'''*************************************************************************************************'''

class ColorChase(Show):
    def __init__(self, leds_name, color_name, back_length = 1, back_color_name = 'black'):
        super(ColorChase, self).__init__(leds_name)
        self.color_name = color_name
        self.back_length = back_length
        self.back_color_name = back_color_name

    def show(self):
        color = COLORS[self.color_name]
        return gen_show(self.leds, [color] + [COLORS[self.back_color_name]]*self.back_length)
    
    def name(self):
        return str(self.leds) + "_chase_" + self.color_name

'''*************************************************************************************************'''

class LighthouseHalcon(Show):
    def __init__(self, leds_name):
        super(LighthouseHalcon, self).__init__(leds_name)

    def show(self):
        return gen_show(self.leds, [darker(COLORS['green']), COLORS['green'], darker(COLORS['green'])] + [COLORS['black']]*3 + [darker(COLORS['magenta']), COLORS['magenta'], darker(COLORS['magenta'])] + [COLORS['black']]*3)
    
    def name(self):
        return str(self.leds) + "_lighthouse_halcon"

'''*************************************************************************************************'''

class RainbowChase(Show):
    def __init__(self, leds_name, length=None):
        super(RainbowChase, self).__init__(leds_name)
        self.length = len(self.leds) if length==None else length

    def show(self):
        return gen_show(self.leds, rainbow(self.length)) 
    
    def name(self):
        return str(self.leds) + "_chase_rainbow"

'''*************************************************************************************************'''

class RainbowChaseCCW(Show):
    def __init__(self, leds_name, length=None):
        super(RainbowChaseCCW, self).__init__(leds_name)
        self.length = len(self.leds) if length==None else length

    def show(self):
        return gen_show(self.leds, rainbow(self.length), -1) 
    
    def name(self):
        return str(self.leds) + "_chase_ccw_rainbow"

'''*************************************************************************************************'''

class RainbowFade(Show):
    def __init__(self, leds_name, length=60):
        super(RainbowFade, self).__init__(leds_name)
        self.length = length

    def show(self):
        return gen_show(self.leds, replicate(rainbow(self.length), len(self.leds)), len(self.leds))
    
    def name(self):
        return str(self.leds) + "_fade_rainbow"

'''*************************************************************************************************'''

class ColorWave(Show):
    def __init__(self, leds_name, color_name, length=60):
        super(ColorWave, self).__init__(leds_name)
        self.color_name = color_name
        self.length = length

    def show(self):
        color = COLORS[self.color_name]
    	return gen_show(self.leds, replicate(wave(color, self.length), len(self.leds)), len(self.leds))
    
    def name(self):
        return str(self.leds) + "_wave_" + self.color_name

'''*************************************************************************************************'''

class ColorFlash(Show):
    def __init__(self, leds_name, color_name):
        super(ColorFlash, self).__init__(leds_name)
        self.color_name = color_name

    def show(self):
        color = COLORS[self.color_name]
        return gen_show(self.leds, replicate([color, darker(color), COLORS['black']]*2 + [COLORS['black']]*22, len(self.leds)), len(self.leds))
    
    def name(self):
        return str(self.leds) + "_flash_" + self.color_name

'''*************************************************************************************************'''

for leds_name in ["vendor_left", "vendor_right", "vendor_bottom"]:
	ColorChase(Leds(leds_name), "red").write()
	LighthouseHalcon(Leds(leds_name)).write()
	RainbowChase(Leds(leds_name)).write()
	RainbowFade(Leds(leds_name)).write()
	ColorWave(Leds(leds_name), "red").write()

for leds_name in ["photos_arrow", "spinner_arrow", "left_kickout_arrow", "right_kickout_arrow"]:
	ColorChase(Leds(leds_name), "red", 22).write()
	RainbowChase(Leds(leds_name), 30).write()
	ColorFlash(Leds(leds_name), "white").write()

for leds_name in ["xp_multiplier_2", "xp_multiplier_3", "xp_multiplier_5"]:
    RainbowChase(Leds(leds_name, 1)).write()
    RainbowChaseCCW(Leds(leds_name, 1)).write()
    RainbowFade(Leds(leds_name)).write()

for leds_name in ["admissions", "gaming_drop_target", "cosplay_drop_target"]:
    ColorChase(Leds(leds_name), "blue", 2, "gray").write()
    ColorChase(Leds(leds_name), "green", 2, "gray").write()
    ColorChase(Leds(leds_name), "magenta", 2, "gray").write()

RainbowChase(Leds("main_stage_edge")).write()
