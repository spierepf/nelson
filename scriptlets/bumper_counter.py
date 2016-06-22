from mpf.system.scriptlet import Scriptlet

import logging
import time

class Bumper:
    def __init__(self, machine, leds, event):
        self.machine = machine
        self.hit_count = 0
        self.leds = leds
        self.event = event
        self.colors = [[255,0,255], [0,255,0]]

    @staticmethod
    def current_time_stamp():
        return int(round(time.time() * 1000))

    def reset(self):
        self.hit_count = 0
        for led in self.leds:
            led.color([0,0,0])

    def start(self):
        self.reset()
        self.machine.events.add_handler(self.event, self.hit)
        self.last_hit_time_stamp = Bumper.current_time_stamp()

    def hit(self):
        hit_time_stamp = Bumper.current_time_stamp()
        if hit_time_stamp - self.last_hit_time_stamp > 100:
            self.hit_count += 1
            led = self.leds[self.hit_count%len(self.leds)]
            color = self.colors[(self.hit_count//len(self.leds))%len(self.colors)]
            led.color(color)
            self.last_hit_time_stamp = hit_time_stamp

class BumperCounter(Scriptlet):

    def on_load(self):
        self.log = logging.getLogger("BumperCounter")
        self.machine.events.add_handler('mode_base_started', self.start)
        self.machine.events.add_handler('mode_base_stop', self.stop)
        self.bottom_bumper = Bumper(self.machine,
                             [
                                self.machine.leds['l_vendor_bottom_a'],
                                self.machine.leds['l_vendor_bottom_b'],
                                self.machine.leds['l_vendor_bottom_c'],
                                self.machine.leds['l_vendor_bottom_d'],
                                self.machine.leds['l_vendor_bottom_e'],
                                self.machine.leds['l_vendor_bottom_f'],
                                self.machine.leds['l_vendor_bottom_g'],
                                self.machine.leds['l_vendor_bottom_h'],
                                self.machine.leds['l_vendor_bottom_i'],
                                self.machine.leds['l_vendor_bottom_j'],
                                self.machine.leds['l_vendor_bottom_k'],
                                self.machine.leds['l_vendor_bottom_l'],
                            ],
                            's_popbumper_bottom_active')
        self.right_bumper = Bumper(self.machine,
                             [
                                self.machine.leds['l_vendor_right_a'],
                                self.machine.leds['l_vendor_right_b'],
                                self.machine.leds['l_vendor_right_c'],
                                self.machine.leds['l_vendor_right_d'],
                                self.machine.leds['l_vendor_right_e'],
                                self.machine.leds['l_vendor_right_f'],
                                self.machine.leds['l_vendor_right_g'],
                                self.machine.leds['l_vendor_right_h'],
                                self.machine.leds['l_vendor_right_i'],
                                self.machine.leds['l_vendor_right_j'],
                                self.machine.leds['l_vendor_right_k'],
                                self.machine.leds['l_vendor_right_l'],
                            ],
                            's_popbumper_right_active')

    def reset(self):
        self.bottom_bumper.reset()
        self.right_bumper.reset()

    def start(self):
        self.log.info("Starting BumperCounter")
        self.bottom_bumper.start()
        self.right_bumper.start()

    def stop(self):
        self.log.info("Stopping BumperCounter")
