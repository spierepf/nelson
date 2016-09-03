from mpf.system.mode import Mode
from mpf.system.timing import Timer
import random

class Auction(Mode):
    def mode_init(self):
        self.timer = Timer(callback=self.tick, frequency=1.0/5.0)

        self.max_player_bid = 80.0
        self.player_leds = [
            self.machine.leds['l_player_bid_a'],
            self.machine.leds['l_player_bid_b'],
            self.machine.leds['l_player_bid_c'],
            self.machine.leds['l_player_bid_d'],
            self.machine.leds['l_player_bid_e'],
            self.machine.leds['l_player_bid_f'],
            self.machine.leds['l_player_bid_g'],
            self.machine.leds['l_player_bid_h']
        ]

        self.max_opponent_bid = 160.0
        self.opponent_leds = [
            self.machine.leds['l_opponent_bid_a'],
            self.machine.leds['l_opponent_bid_b'],
            self.machine.leds['l_opponent_bid_c'],
            self.machine.leds['l_opponent_bid_d'],
            self.machine.leds['l_opponent_bid_e'],
            self.machine.leds['l_opponent_bid_f'],
            self.machine.leds['l_opponent_bid_g'],
            self.machine.leds['l_opponent_bid_h']
        ]

    def mode_start(self, **kwargs):
        self.machine.timing.add(self.timer)

    def mode_stop(self, **kwargs):
        self.machine.timing.remove(self.timer)

    def show_fraction(self, fraction, leds, color):
        count = len(leds) * fraction
        for i in range(0, int(count)):
            leds[i].color(color)
        if fraction < 1.0:
            partial = [int(i * (count % 1)) for i in color]
            leds[int(count)].color(partial)
            for i in range(int(count) + 1, len(leds)):
                leds[i].color([0, 0, 0])

    def tick(self, **kwargs):
        player = self.machine.game.player

        fraction = min(self.max_player_bid, player["player_bid_count"]) / self.max_player_bid
        self.show_fraction(fraction, self.player_leds, [0, 255, 0])

        fraction = min(self.max_opponent_bid, player["auction_opponent_bid_tick"]) / self.max_opponent_bid
        self.show_fraction(fraction, self.opponent_leds, [255, 0, 255])
