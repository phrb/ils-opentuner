from opentuner.search import technique
import random
import math

class IteratedLocalSearch(technique.SequentialSearchTechnique):
    def probabilistic_improvement(self, start, max_step, acceptance):
        param = random.choice(self.manipulator.parameters(start.data))

        if param.is_primitive():
            unit_value = param.get_unit_value(start.data)
            proposal = self.manipulator.copy(start.data)
            new_unit_value = unit_value - (random.random() * max_step)

            if new_unit_value < 0.0:
                new_unit_value = min(1.0, unit_value + (random.random() * max_step))

            param.set_unit(proposal, new_unit_value)
            proposal = driver.get_configuration(proposal)

        difference = self.objective.compare(proposal, start)
        acceptance_prob = math.exp(difference / acceptance)

        if random.random() <= acceptance_prob or self.objective.lt(proposal, start):
            return proposal
        else:
            return start

    def main_generator(self):
        objective   = self.objective
        driver      = self.driver
        manipulator = self.manipulator
        acceptance  = 0.5
        max_step    = 0.25
        iterations  = 50

        # start at a random position
        start = driver.get_configuration(manipulator.random())
        yield start

        # initial step size is arbitrary
        step_size = 0.1

        while True:
            param = random.choice(self.manipulator.parameters(start.data))

            if param.is_primitive():
                unit_value = param.get_unit_value(start.data)
                proposal = self.manipulator.copy(start.data)
                new_unit_value = unit_value - (random.random() * max_step)

                if new_unit_value < 0.0:
                    new_unit_value = min(1.0, unit_value + (random.random() * max_step))

                param.set_unit(proposal, new_unit_value)
                proposal = driver.get_configuration(proposal)

            for i in range(iterations):
                proposal = self.probabilistic_improvement(proposal, max_step, acceptance)
                yield start

            difference = self.objective.compare(proposal, start)
            acceptance_prob = math.exp(difference / acceptance)

            if random.random() <= acceptance_prob or self.objective.lt(proposal, start):
                start = proposal

            yield start

technique.register(IteratedLocalSearch())
