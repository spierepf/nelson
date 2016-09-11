from mpf.system.mode import Mode
from mpf.system.timing import Timer
from mpf.devices.ball_save import BallSave

class Base(Mode):
    def mode_init(self):
        self.log.info("Initializing Base Mode")
        self.leds = [
            self.machine.leds['l_ball_save_s'],
            self.machine.leds['l_ball_save_r'],
            self.machine.leds['l_ball_save_q'],
            self.machine.leds['l_ball_save_p'],
            self.machine.leds['l_ball_save_o'],
            self.machine.leds['l_ball_save_n'],
            self.machine.leds['l_ball_save_m'],
            self.machine.leds['l_ball_save_l'],
            self.machine.leds['l_ball_save_k'],
            self.machine.leds['l_ball_save_j'],
            self.machine.leds['l_ball_save_i'],
            self.machine.leds['l_ball_save_h'],
            self.machine.leds['l_ball_save_g'],
            self.machine.leds['l_ball_save_f'],
            self.machine.leds['l_ball_save_e'],
            self.machine.leds['l_ball_save_d'],
            self.machine.leds['l_ball_save_c'],
            self.machine.leds['l_ball_save_b'],
            self.machine.leds['l_ball_save_a'],
        ]

    def mode_start(self, **kwargs):
        self.log.info("Starting Base Mode")
        self.machine.events.add_handler('player_base_ball_save_tick', self.tick)
        for led in self.leds:
            led.color([255, 0, 0])

    def mode_stop(self, **kwargs):
        self.log.info("Stopping Base Mode")
        self.machine.events.remove_handler_by_event('player_base_ball_save_tick', self.tick)

    def tick(self, **kwargs):
        for i in range(len(self.leds)):
            if i < kwargs['value']:
                self.leds[i].color([255, 0, 0])
            else:
                self.leds[i].color([0, 0, 0])
