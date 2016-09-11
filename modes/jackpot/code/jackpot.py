from mpf.system.mode import Mode
import random

class JackpotModeTarget:
    def __init__(self, type_name, name, config):
        self.type_name = type_name
        self.name = name
        self.config = config

    def __repr__(self):
        return "<JackpotModeTarget: " + self.name + ">"

    def enable_event_name(self):
        return self.config["enable_events"].items()[0][0]

    def disable_event_name(self):
        return self.config["disable_events"].items()[0][0]

    def complete_event_name(self):
        if self.type_name == "shots":
            return self.name + "_jackpot_active_hit"
        else:
            return self.name + "_jackpot_hit_complete"

class Jackpot(Mode):
    def mode_init(self, **kwargs):
        self.jackpot_mode_targets = []
        self.current_target = None

        for type_name in ["shots", "shot_groups"]:
            if type_name in self.config:
                for name in self.config[type_name]:
                    if any("jackpot_shot" in s for s in self.config[type_name][name]["tags"]):
                        target = JackpotModeTarget(type_name, name, self.config[type_name][name])
                        self.jackpot_mode_targets += [target]

        self.log.info("Jackpot Mode Targets: " + str(self.jackpot_mode_targets))

    def mode_start(self, **kwargs):
        self.enable_random_target()
        self.machine.events.add_handler("timer_shot_timer_complete", self.target_missed)

    def mode_stop(self, **kwargs):
        self.disable_current_target()
        self.machine.events.remove_handler(self.target_missed)

    def enable_random_target(self):
        last_target = self.current_target
        new_target = random.choice(self.jackpot_mode_targets)
        while len(self.jackpot_mode_targets) > 1 and last_target == new_target:
            new_target = random.choice(self.jackpot_mode_targets)
        self.enable_target(new_target)

    def enable_target(self, target):
        self.disable_current_target()
        self.current_target = target

        self.machine.events.add_handler(target.complete_event_name(), self.target_hit)

        self.log.info("Enabling Jackpot Mode Target: " + str(self.current_target))
        self.log.info("Sending Event: " + self.current_target.enable_event_name())
        self.machine.events.post(self.current_target.enable_event_name())

    def disable_current_target(self):
        if self.current_target != None:
            self.machine.events.remove_handler(self.target_hit)
            self.machine.events.post("disable_jackpot_mode_shot")
            self.current_target = None

    def target_hit(self, **kwargs):
        self.log.info("Jackpot Mode Target Hit: " + str(self.current_target))
        self.machine.events.post("jackpot_hit")

    def target_missed(self, **kwargs):
        self.log.info("Jackpot Mode Target Missed: " + str(self.current_target))
