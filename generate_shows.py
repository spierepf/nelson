from __future__ import division
import yaml
import collections

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
        return (255/255 - wheelPos * 3, 0, wheelPos * 3);

    if wheelPos < 170/255:
        wheelPos -= 85/255;
        return (0, wheelPos * 3, 255/255 - wheelPos * 3);

    wheelPos -= 170/255;
    return (wheelPos * 3, 255/255 - wheelPos * 3, 0);


def rainbow(length):
    retval = [];
    for i in range(length):
        retval.append(wheel(i/length))
    return retval;

def replicate(pattern, count):
    retval = []
    for item in pattern:
        for i in range(count):
            retval.append(item)
    return retval;

def gen_frame(leds, pattern):
    items = {}
    i = 0
    for led in leds:
        items[led] = pattern[i]
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

write_show("popBumper_three_chase_red", gen_show(find_leds("l_popBumper_three"), [(1,0,0), (0,0,0), (0,0,0)]))

write_show("popBumper_three_chase_rainbow", gen_show(find_leds("l_popBumper_three"), rainbow(len(find_leds("l_popBumper_three")))))

write_show("popBumper_three_fade_rainbow", gen_show(find_leds("l_popBumper_three"), replicate(rainbow(60), len(find_leds("l_popBumper_three"))), len(find_leds("l_popBumper_three"))))

