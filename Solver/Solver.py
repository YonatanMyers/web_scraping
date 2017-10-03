import math
from copy import deepcopy

import numpy as np

from League.League import League


class LeagueSolver(object):
    def __init__(self, league: League):
        super().__init__()
        self.league = league

    def solve_league_no_IRLS(self):
        """
        This function solves the eq:
                A x = b
        """
        # def_dbg = True
        def_dbg = False
        def_plt = True
        # def_plt = False

        team_2_ind_dict = deepcopy(self.league.teem_list)
        """making ind to key dict"""
        # keys_ = team_2_ind_dict.keys()
        # vals_ = team_2_ind_dict.values()
        ind_2_team_dict = {item[1][0]: item[0] for item in team_2_ind_dict.items()}

        num_teams = len(team_2_ind_dict)
        A = []
        b = []
        last_row_in_A = [0 for i in range(num_teams)]
        last_b = [0, 0]
        read_A_start = 0
        for round_ in self.league:
            for game in round_:
                row_in_A = [0 for i in range(num_teams)]
                t0, t1 = game
                row_in_A[team_2_ind_dict[t0[0]][0]] = 1.0
                row_in_A[team_2_ind_dict[t1[0]][0]] = -1.0
                last_row_in_A[team_2_ind_dict[t0[0]][0]] += 1
                last_row_in_A[team_2_ind_dict[t1[0]][0]] += 1
                A.append(deepcopy(row_in_A))
                b_0 = float(t0[1] - t1[1])
                b_1 = float(t0[1] - t1[1])
                last_b[0] += (t0[1] + t1[1])
                if b_1 > 0:
                    b_1 = 1.0
                elif b_1 < 0:
                    b_1 = -1.0
                else:
                    b_1 = 0.0

                b.append([b_0, b_1])
                # b.append(b_0)

            if round_.round_n > 3:
                copy_A_for_solving_round = deepcopy(A)
                copy_A_for_solving_round.append(last_row_in_A)
                copy_b_for_solving_round = deepcopy(b)
                copy_b_for_solving_round.append(last_b)
                np_A = np.array(copy_A_for_solving_round)
                np_b = np.array(copy_b_for_solving_round)
                x, res, qw, asd = np.linalg.lstsq(np_A, np_b)
                for row_ind in range(len(x)):
                    k = ind_2_team_dict[row_ind]
                    self.league.teem_list[k][1].strength.append(list(x[row_ind]))
                for row_in_A, row_in_b in zip(A[read_A_start:], b[read_A_start:]):
                    t0, t1 = LeagueSolver.get_team_names_from_row(row_in_A, ind_2_team_dict)
                    t0_strength = self.league.teem_list[t0][1].strength[-1]
                    t1_strength = self.league.teem_list[t1][1].strength[-1]

                    strength_dx = abs(t0_strength[0] - t1_strength[0])
                    strength_dy = abs(t0_strength[1] - t1_strength[1])

                    if row_in_b[0] == 0:
                        strength_dist = math.sqrt(strength_dx * strength_dx + strength_dy * strength_dy)
                        self.league.teem_list[t0][1].add_tie_dist(strength_dist)
                        self.league.teem_list[t1][1].add_tie_dist(strength_dist)

                        self.league.teem_list[t0][1].add_strength_val(-strength_dx, 'tie',
                                                                      'by_goals')  # for t0 we want to hold t1-t0
                        self.league.teem_list[t1][1].add_strength_val(strength_dx, 'tie',
                                                                      'by_goals')  # for t1 we want to hold t0-t1
                        self.league.teem_list[t0][1].add_strength_val(-strength_dy, 'tie',
                                                                      'by_wins')  # for t0 we want to hold t1-t0
                        self.league.teem_list[t1][1].add_strength_val(strength_dy, 'tie',
                                                                      'by_wins')  # for t1 we want to hold t0-t1
                    elif row_in_b[1] > 0:    # t0 wins  (t1 loos)
                        self.league.teem_list[t0][1].add_strength_val(-strength_dx, 'win',
                                                                      'by_goals')  # for t0 we want to hold t1-t0
                        self.league.teem_list[t0][1].add_strength_val(-strength_dy, 'win',
                                                                      'by_wins')  # for t0 we want to hold t1-t0

                        self.league.teem_list[t1][1].add_strength_val(strength_dx, 'loos',
                                                                      'by_goals')  # for t1 we want to hold t0-t1
                        self.league.teem_list[t1][1].add_strength_val(strength_dy, 'loos',
                                                                      'by_wins')  # for t1 we want to hold t0-t1
                    elif row_in_b[1] < 0:    # t0 loos  (t1 win)
                        self.league.teem_list[t1][1].add_strength_val(-strength_dx, 'win',
                                                                      'by_goals')  # for t0 we want to hold t1-t0
                        self.league.teem_list[t1][1].add_strength_val(-strength_dy, 'win',
                                                                      'by_wins')  # for t0 we want to hold t1-t0

                        self.league.teem_list[t0][1].add_strength_val(strength_dx, 'loos',
                                                                      'by_goals')  # for t1 we want to hold t0-t1
                        self.league.teem_list[t0][1].add_strength_val(strength_dy, 'loos',
                                                                      'by_wins')  # for t1 we want to hold t0-t1
                read_A_start = len(A)
        self.league.print_teems_list_short()

        if def_dbg:
            self.league.print_league()
        if def_plt:
            for team in self.league.teem_list.values():
                team[1].plot_team_wim_loos_tie()
                team[1].plot_team_strength()

    @staticmethod
    def get_team_names_from_row(row_in_A, ind_2_team_dict):
        t0 = ''
        t1 = ''
        for i, val in zip(range(len(row_in_A)), row_in_A):
            if val > 0:
                if t0 == '':
                    t0 = ind_2_team_dict[i]
            elif val < 0:
                t1 = ind_2_team_dict[i]

        return (t0, t1)

    # def make_prediction(self):
    #
