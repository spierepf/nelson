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
                                self.machine.leds['l_popBumper_bottom_0'],
                                self.machine.leds['l_popBumper_bottom_1'],
                                self.machine.leds['l_popBumper_bottom_2'],
                                self.machine.leds['l_popBumper_bottom_3'],
                                self.machine.leds['l_popBumper_bottom_4'],
                                self.machine.leds['l_popBumper_bottom_5'],
                                self.machine.leds['l_popBumper_bottom_6'],
                                self.machine.leds['l_popBumper_bottom_7'],
                                self.machine.leds['l_popBumper_bottom_8'],
                                self.machine.leds['l_popBumper_bottom_9'],
                                self.machine.leds['l_popBumper_bottom_10'],
                                self.machine.leds['l_popBumper_bottom_11'],
                            ],
                            's_popbumper_bottom_active')
        self.right_bumper = Bumper(self.machine,
                             [
                                self.machine.leds['l_popBumper_right_0'],
                                self.machine.leds['l_popBumper_right_1'],
                                self.machine.leds['l_popBumper_right_2'],
                                self.machine.leds['l_popBumper_right_3'],
                                self.machine.leds['l_popBumper_right_4'],
                                self.machine.leds['l_popBumper_right_5'],
                                self.machine.leds['l_popBumper_right_6'],
                                self.machine.leds['l_popBumper_right_7'],
                                self.machine.leds['l_popBumper_right_8'],
                                self.machine.leds['l_popBumper_right_9'],
                                self.machine.leds['l_popBumper_right_10'],
                                self.machine.leds['l_popBumper_right_11'],
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
