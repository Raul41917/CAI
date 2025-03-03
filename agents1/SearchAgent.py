import numpy as np

from agents1.OfficialAgent import BaselineAgent


class SearchAgent(BaselineAgent):
    def __init__(self, slowdown, condition, name, folder):
        super().__init__(slowdown, condition, name, folder)

    def _trustBelief(self, members, trustBeliefs, folder, receivedMessages):

        etas_search = [0.5, 0.7, 0.9, 1]
        index_eta_search = 0

        etas_remove = [0.5, 0.7, 0.9, 1]
        index_eta_remove = 0

        search_set = set()
        help_remove = set()
        victims = set()

        competency = trustBeliefs[self._human_name]['competency']
        willingness = trustBeliefs[self._human_name]['willingness']

        latest_search_room = -1

        for message in receivedMessages:
            if 'Search' in message:
                area_to_search = int(message.split()[-1])
                latest_search_room = area_to_search
                if area_to_search in search_set:
                    willingness -= 0.2
                    competency -= 0.1
                else:
                    search_set.add(area_to_search)
                    willingness += 0.1

            elif 'Remove' in message:
                  area_to_remove = int(message.split()[-1])
                  if area_to_remove in search_set:
                      if area_to_remove not in help_remove:
                          help_remove.add(area_to_remove)
                          willingness += 0.1
                          competency -= 0.1
                      else:
                          willingness -= etas_remove[index_eta_remove] * 0.1
                          index_eta_remove = min(3, index_eta_remove + 1)
                  else:
                      willingness -= 0.1

            elif 'Found' in message:
                broken_message = message.split()
                victim = " ".join(broken_message[1: -2])
                area_of_found_victim = broken_message[-1]

                if victim not in victims:
                    competency += 0.1
                else:
                    willingness -= etas_search[index_eta_search]
                    index_eta_search = min(3, index_eta_search + 1)

                if area_of_found_victim not in search_set:
                    willingness -= etas_search[index_eta_search] * 0.1
                    index_eta_search = min(3, index_eta_search + 1)
                elif latest_search_room == area_of_found_victim:
                    willingness += 0.1

            competency = np.clip(competency, -1, 1)
            willingness = np.clip(willingness, -1, 1)

        trustBeliefs[self._human_name]['competency'] = competency
        trustBeliefs[self._human_name]['willingness'] = willingness

        return trustBeliefs