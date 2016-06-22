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

def gen_show(leds, pattern):
    frames = []
    for i in range(len(pattern)):
        frames.append(gen_frame(leds, rotate(pattern, -i)))
    return frames

def write_show(name, show):
    with open('shows/'+name+'.yaml', 'w') as outfile:
        outfile.write(yaml.dump(show))

write_show("popBumper_three_marquee_red", gen_show(find_leds("l_popBumper_three"), [0xff0000, 0x000000, 0x000000]))
