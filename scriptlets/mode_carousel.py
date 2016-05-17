from mpf.system.scriptlet import Scriptlet

class ModeCarouselItem:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<ModeCarouselItem: " + self.name + ">"
 
class ModeCarousel(Scriptlet):

    def on_load(self):
        self.items = [ModeCarouselItem('cosplay'), ModeCarouselItem('vendors'), ModeCarouselItem('auction'), ModeCarouselItem('photos'), ModeCarouselItem('gaming'), ModeCarouselItem('stargazer')]
        self.start_events = ['ball_started']
        self.next_item_events = ['sw_mode_carousel_next_item']
        self.select_item_events = ['sw_mode_carousel_select_item', 'balldevice_plungerLane_ball_left']

        self.register_handlers(self.start_events, self.begin)
    
    def register_handlers(self, events, handler):
        for event in events:
            self.machine.events.add_handler(event, handler)

    def deregister_handlers(self, events, handler):
        for event in events:
            self.machine.events.remove_handler_by_event(event, handler)

    def highlighted_mode(self):
        player = self.machine.game.player
        return player.available_modes[self.highlighted_mode_index]

    def update_highlighted_mode(self):
        self.log.info("Highlighted mode: " + str(self.highlighted_mode()))

        self.machine.events.post(self.highlighted_mode().name + "_highlighted")


    def begin(self, **kwargs):
        self.deregister_handlers(self.start_events, self.begin)
        self.register_handlers(self.next_item_events, self.next_item)
        self.register_handlers(self.select_item_events, self.select_item)

        player = self.machine.game.player
        if not player.is_player_var('available_modes'):
            player.available_modes = self.items
        self.highlighted_mode_index = 0

        self.update_highlighted_mode()

    def next_item(self, **kwargs):
        player = self.machine.game.player

        self.highlighted_mode_index += 1
        if self.highlighted_mode_index >= len(player.available_modes):
            self.highlighted_mode_index = 0

        self.update_highlighted_mode()

    def select_item(self, **kwargs):
        self.log.info("Selected mode: " + str(self.highlighted_mode()))

        self.deregister_handlers(self.next_item_events, self.next_item)
        self.deregister_handlers(self.select_item_events, self.select_item)

        self.machine.events.post(self.highlighted_mode().name + "_selected")
        self.machine.events.post("mode_selected")
