import csv

import numpy as np

from agents1.OfficialAgent import BaselineAgent


class NEVER_TRUST(BaselineAgent):

    def __init__(self, slowdown, condition, name, folder):
        super().__init__(slowdown, condition, name, folder)

    def _trustBelief(self, members, trustBeliefs, folder, receivedMessages):
        trustBeliefs[self._human_name]['competence'] = -1
        trustBeliefs[self._human_name]['willingness'] = -1


        with open(folder + '/beliefs/currentTrustBelief.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['name', 'competence', 'willingness'])
            csv_writer.writerow([self._human_name, trustBeliefs[self._human_name]['competence'],
                                 trustBeliefs[self._human_name]['willingness']])
        return trustBeliefs


class ALWAYS_TRUST(BaselineAgent):

    def __init__(self, slowdown, condition, name, folder):
        super().__init__(slowdown, condition, name, folder)

    def _trustBelief(self, members, trustBeliefs, folder, receivedMessages):
        trustBeliefs[self._human_name]['competence'] = 1
        trustBeliefs[self._human_name]['willingness'] = 1

        return trustBeliefs

class RANDOM_TRUST(BaselineAgent):

    def __init__(self, slowdown, condition, name, folder):
        super().__init__(slowdown, condition, name, folder)

    def _trustBelief(self, members, trustBeliefs, folder, receivedMessages):
        np.random.rand(42)
        trustBeliefs[self._human_name]['competence'] = 0.55
        trustBeliefs[self._human_name]['willingness'] = -0.14

        with open(folder + '/beliefs/currentTrustBelief.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['name', 'competence', 'willingness'])
            csv_writer.writerow([self._human_name, trustBeliefs[self._human_name]['competence'],
                                 trustBeliefs[self._human_name]['willingness']])
        return trustBeliefs
