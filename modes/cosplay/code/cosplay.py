from mpf.system.mode import Mode

class Cosplay(Mode):
	def mode_start(self, **kwargs):
		self.machine.events.add_handler("cosplay_kickout_hit_me_active_hit", self.remove_mode_from_available_modes)

	def mode_stop(self, **kwargs):
		self.machine.events.remove_handler_by_event("cosplay_kickout_hit_me_active_hit", self.remove_mode_from_available_modes)

	def remove_mode_from_available_modes(self, **kwargs):
		player = self.machine.game.player
		player.available_modes = [x for x in player.available_modes if x.name != "cosplay"]
