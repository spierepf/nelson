from mpf.system.scriptlet import Scriptlet

class CarouselModeCompleteHandler(Scriptlet):
	def on_load(self):
		self.machine.events.add_handler("carousel_mode_complete", self.handle_carousel_mode_complete)
		
	def handle_carousel_mode_complete(self):
		player = self.machine.game.player
		self.log.info("Completed mode: " + str(player.available_modes[player.highlighted_mode_index]))
		del player.available_modes[player.highlighted_mode_index]
		player.highlighted_mode_index = None
