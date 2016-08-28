from mpf.system.mode import Mode

class Vendors(Mode):

    def mode_init(self):
        self.bottom_bumper = [
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
                            ]

    def mode_start(self, **kwargs):
        self.machine.events.add_handler('timer_tick', self.tick)
        for led in self.bottom_bumper:
            led.color = [0,0,0]

    def mode_stop(self, **kwargs):
        self.machine.events.remove_handler_by_event('timer_tick', self.tick)
        for led in self.bottom_bumper:
            led.color = [0,0,0]

    def tick(self, **kwargs):
        player = self.machine.game.player
        for i in range(0, len(self.bottom_bumper) - player.vendor_bottom_hits_count):
            self.bottom_bumper[i].color = [0, 0, 255]

        for i in range(len(self.bottom_bumper) - player.vendor_bottom_hits_count, len(self.bottom_bumper)):
            if(self.bottom_bumper[i].color == [0, 0, 0]):
                self.bottom_bumper[i].color = [0, 0, 255]
            else:
            	self.bottom_bumper[i].color = [0, 0, 0]
