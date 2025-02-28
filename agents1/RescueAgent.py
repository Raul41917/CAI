import csv

import numpy as np

from agents1.OfficialAgent import BaselineAgent


class RescueAgent(BaselineAgent):

    def __init__(self, slowdown, condition, name, folder):
        super().__init__(slowdown, condition, name, folder)

    def _trustBelief(self, members, trustBeliefs, folder, receivedMessages):

        etas = [0.5, 0.70, 0.9, 1]
        index_eta = 0
        willing = False

        picked_up_according_to_agent = set()

        for message in receivedMessages:
            if 'Rescue' in message:
                if message == 'Rescue alone':
                    index_eta = 0 if willing else min(3, index_eta + 1)
                    willing = False
                    trustBeliefs[self._human_name]['willingness'] -= (etas[index_eta] * 0.1)
                else:
                    index_eta = 0 if not willing else min(3, index_eta + 1)
                    willing = True
                    trustBeliefs[self._human_name]['willingness'] += (etas[index_eta] + 0.1)
                    trustBeliefs[self._human_name]['competence'] -= 0.1
            elif 'Collect' in message:
                msg_stripped = message.split()
                message_without_room = " ".join(msg_stripped[:-1])
                if message_without_room not in picked_up_according_to_agent:
                    picked_up_according_to_agent.add(message_without_room)
                    trustBeliefs[self._human_name]['competence'] += 0.1
                else:
                    trustBeliefs[self._human_name]['willingness'] -= 0.1

            trustBeliefs[self._human_name]['competence'] = np.clip(trustBeliefs[self._human_name]['competence'], -1,
                                                                       1)
            trustBeliefs[self._human_name]['willingness'] = np.clip(trustBeliefs[self._human_name]['willingness'], -1,
                                                                       1)

        robot_sent_messages = []
        for msg in self._send_messages:
            if "Moving" in msg and "to pick up" in msg:
                robot_sent_messages.append(msg)

        if len(robot_sent_messages) == 8:
            trustBeliefs[self._human_name]['competence'] = -1

        with open(folder + '/beliefs/currentTrustBelief.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['name', 'competence', 'willingness'])
            csv_writer.writerow([self._human_name, trustBeliefs[self._human_name]['competence'],
                                 trustBeliefs[self._human_name]['willingness']])

        return trustBeliefs


