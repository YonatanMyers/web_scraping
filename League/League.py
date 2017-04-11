from copy import deepcopy
from League.Team import Team
from operator import itemgetter, attrgetter

class League(object):
    def __init__(self, team_2_ind, rounds):
        super().__init__()
        self.teem_list = deepcopy(team_2_ind)
        self.ind_2_team_dict = {item[1]: item[0] for item in team_2_ind.items()}
        for key, e in self.teem_list.items():
            self.teem_list[key] = [e, Team(key)]
        self.rounds = deepcopy(rounds)
        self.iter_counter = 0

    def print_league(self):
        print(self.teem_list)
        for r in self.rounds:
            r.print_round()
        for t in self.teem_list:
            self.teem_list[t][1].print_team()

    def print_teems_list_short(self):
        teem_list_as_list = [t[1] for t in self.teem_list.values()]
        teem_list_as_list_s_0 = sorted(teem_list_as_list, key=lambda teem: teem.strength[-1][0], reverse=True)
        teem_list_as_list_s_1 = sorted(teem_list_as_list, key=lambda teem: teem.strength[-1][1], reverse=True)

        ind = 1
        print('Teams by goals:')
        for t in teem_list_as_list_s_0:
            print(ind, end='')
            print('. ' + t.name + ' ', end='')
            print(t.strength[-1][0])
            ind += 1

        ind = 1
        print()
        print('Teams by wins:')
        for t in teem_list_as_list_s_1:
            print(ind, end='')
            print('. ' + t.name + ' ', end='')
            print(t.strength[-1][1])
            ind += 1

    def print_teem_list_short(self):
        for t in self.teem_list.items():
            print(t[0], t[1][0])

    def guess_results(self):
        """
        input teems and print the odds of win loos by all kinds of calculation
        :return: 
        """
        # todo: input validation
        team_1_ind = int(input('Enter team 1: '))
        team_2_ind = int(input('Enter team 2: '))

        team_1_str = self.ind_2_team_dict[team_1_ind]
        team_2_str = self.ind_2_team_dict[team_2_ind]

        team_1 = self.teem_list[team_1_str][1]
        team_2 = self.teem_list[team_2_str][1]

        strength_1 = team_1.strength[-1]
        strength_2 = team_2.strength[-1]

        val_dif_for_team_1_x = strength_2[0] - strength_1[0]
        val_dif_for_team_1_y = strength_2[1] - strength_1[1]

        team_1.get_probability_of_outcome(self, val_dif_for_team_1_x, val_dif_for_team_1_y)

    def __iter__(self):
        self.iter_counter = 0
        return self

    def __next__(self):
        if self.iter_counter >= len(self.rounds):
            raise StopIteration

        ret_val = self.rounds[self.iter_counter]
        self.iter_counter += 1

        return ret_val
