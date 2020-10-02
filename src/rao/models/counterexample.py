
import numpy as np
from . import models

class CounterExampleMDP(models.CCHyperGraphModel):
    """Class representing hand constructed MDP which is intended to give
    an example whereby RAO* fails to find the correct solution."""
    def __init__(self):
        super(CounterExampleMDP,self).__init__()
        self.is_maximization = False #Trying to find shortest path to goal
        self.immutable_actions = False #Actions are not always the same

    def get_state(self, num):
        """
        Returns a proper state representation.
        """
        state_dict = {'s': num}
        return state_dict

    def get_initial_belief(self):
        """
        Proper initial representation of the initial belief state of the search.
        This is an MDP, so the initial state is known.
        """
        belief = {}
        s0 = self.get_state(0)
        belief[self.hash_state(s0)] = [s0,1.0]
        return belief

    def actions(self,state):
        """We can move in any of the available directions, if the state is not
        terminal."""
        if self.is_terminal(state):
            return []
        elif state["s"] in [1, 2]:
            return ["A", "B"]
        else:
            return ["A"]

    def value(self,state,action):
        """Value is the cost of moving."""
        if state['s'] == 0 and action == "A":
            return 3.0
        elif state['s'] == 1 and action == "A":
            return 4.0
        elif state['s'] == 1 and action == "B":
            return 2.0
        elif state['s'] == 2 and action == "A":
            return 2.0
        elif state['s'] == 2 and action == "B":
            return 4.0
        elif state['s'] == 4 and action == "A":
            return 2.0
        elif state['s'] == 5 and action == "A":
            return 10.0
        elif state['s'] == 6 and action == "A":
            return 0.0
        elif state['s'] == 7 and action == "A":
            return 200.0
        else:
            raise Exception("Invalid state action pair")

    def terminal_value(self,state):
        """Value associated with a terminal state."""
        return 0.0

    def heuristic(self,state):
        heur_dict = {
                0: 0.0,
                1: 0.0,
                2: 2.0,
                3: 0.0,
                4: 0.0,
                5: 10.0,
                6: 0.0,
                7: 20.0,
                8: 0.0,
                9: 0.0,
                10: 0.0,
                11: 0.0,
                12: 0.0
                }

        return heur_dict[state["s"]]

    def state_transitions(self,state,action):
        """The agent moves in the desired direction with high probability, or
        slides to the left or right of the desired path."""
        #Set of potential future states
        if action==():
            return [[self.get_state(state),1.0]]
        else:
            if state['s'] == 0 and action == "A":
                return [[self.get_state(1), 0.5], [self.get_state(2), 0.5]]
            if state['s'] == 1 and action == "A":
                return [[self.get_state(3), 0.2], [self.get_state(4), 0.8]]
            if state['s'] == 1 and action == "B":
                return [[self.get_state(5), 1.0]]
            if state['s'] == 2 and action == "A":
                return [[self.get_state(6), 1.0]]
            if state['s'] == 2 and action == "B":
                return [[self.get_state(7), 1.0]]
            if state['s'] == 4 and action == "A":
                return [[self.get_state(8), 1.0]]
            if state['s'] == 5 and action == "A":
                return [[self.get_state(9), 1.0]]
            if state['s'] == 6 and action == "A":
                return [[self.get_state(10), 0.01], [self.get_state(11), 0.99]]
            if state['s'] == 7 and action == "A":
                return [[self.get_state(12), 1.0]]

    def observations(self,state):
        """
        For a fully observable model, the state is the observation.
        """
        meas = id(state)
        return [[meas,1.0]]

    def is_terminal(self,state):
        if state["s"] in [3, 8, 9, 10, 11, 12]:
            return True
        else:
            return False

    def state_risk(self,state):
        """No state risk at the moment."""
        if state['s'] == 3 or state['s'] == 10:
            return 1.0
        else:
            return 0.0

    def execution_risk_heuristic(self,state):
        """
        Admissible estimate of the remaining mission risk.
        """
        return self.state_risk(state)
