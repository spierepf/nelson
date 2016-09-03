from mpf.system.mode import Mode
from mpf.system.timing import Timer
import random

class Auction(Mode):
    def mode_init(self):
        self.max_player_bid = 80
        self.max_opponent_bid = 160
        self.opponent_bids = [random.randint(0,self.max_opponent_bid-1) for _ in range(7)]
        self.opponent_bids.sort()
        self.opponent_bids += [self.max_opponent_bid]
        self.timer = Timer(callback=self.tick, frequency=1.0/5.0)
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

    def tick(self, **kwargs):
        player = self.machine.game.player

        player_bid = min(self.max_player_bid, player["player_bid_count"])
        for i in range(0, player_bid / 10):
            self.player_leds[i].color([0,0,255])

        if player_bid < self.max_player_bid:
            self.player_leds[player_bid / 10].color([0,0,25*(player_bid%10)])
            for i in range(1 + (player_bid / 10), len(self.player_leds)):
                self.player_leds[i].color([0,0,0]);
