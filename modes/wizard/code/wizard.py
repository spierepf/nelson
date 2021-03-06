from mpf.system.mode import Mode
import random

class WizardModeTarget:
    def __init__(self, type_name, name, config):
        self.type_name = type_name
        self.name = name
        self.config = config

    def __repr__(self):
        return "<WizardModeTarget: " + self.name + ">"

    def enable_event_name(self):
    	return self.config["enable_events"].items()[0][0]

    def complete_event_name(self):
        if self.type_name == "shots":
            return self.name + "_wizard_active_hit"
        else:
            return self.name + "_wizard_hit_complete"

class Wizard(Mode):
    def mode_init(self):
        self.wizard_mode_targets = []
        self.current_target = None

        for type_name in ["shots", "shot_groups"]:
            if type_name in self.config:
                for name in self.config[type_name]:
                    if any("wizard_mode_target" in s for s in self.config[type_name][name]["tags"]):
                        target = WizardModeTarget(type_name, name, self.config[type_name][name])
                        self.wizard_mode_targets += [target]

        self.log.info("Wizard Mode Targets: " + str(self.wizard_mode_targets))

    def mode_start(self):
        self.enable_random_target()
        self.machine.events.add_handler("timer_shot_timer_complete", self.target_missed)

    def mode_stop(self):
        self.disable_current_target()
        self.machine.events.remove_handler(self.target_missed)

    def enable_random_target(self):
        last_target = self.current_target
        new_target = random.choice(self.wizard_mode_targets)
        while len(self.wizard_mode_targets) > 1 and last_target == new_target:
            new_target = random.choice(self.wizard_mode_targets)
        self.enable_target(new_target)

    def enable_target(self, target):
        self.disable_current_target()
        self.current_target = target

        self.machine.events.add_handler(target.complete_event_name(), self.target_hit)

        self.log.info("Enabling Wizard Mode Target: " + str(self.current_target))
        self.log.info("Sending Event: " + self.current_target.enable_event_name())
        self.machine.events.post(self.current_target.enable_event_name())

    def disable_current_target(self):
        if self.current_target != None:
            self.machine.events.remove_handler(self.target_hit)
            self.machine.events.post("disable_wizard_mode_shot")
            self.current_target = None

    def target_hit(self, **kwargs):
        self.log.info("Wizard Mode Target Hit: " + str(self.current_target))
        self.enable_random_target()

    def target_missed(self, **kwargs):
        self.log.info("Wizard Mode Target Missed: " + str(self.current_target))
        self.enable_random_target()
