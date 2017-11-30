from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.spatial

from League.Team import Team


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
        more = 1
        while more !=0:
            team_1_ind = int(input('Enter team 1: '))
            team_2_ind = int(input('Enter team 2: '))

            team_1_str = self.ind_2_team_dict[team_1_ind]
            team_2_str = self.ind_2_team_dict[team_2_ind]

            team_1 = self.teem_list[team_1_str][1]
            team_2 = self.teem_list[team_2_str][1]

            # plot the data so we can look at it and get intuition#
            plt.figure()
            colors = ['green', 'red', 'blue']
            for color, win_loos_tie in zip(colors, ['win', 'loos', 'tie']):
                team_x = []
                team_y = []
                points = []
                # team_1.plot_team_wim_loos_tie()
                # team_1.plot_team_strength()
                for coords in team_1.results_coordinates_diffs[win_loos_tie]:
                    team_x.append(coords[0] + team_1.strength[-1][0])
                    team_y.append(coords[1] + team_1.strength[-1][1])
                    points.append([team_x[-1], team_y[-1]])
                if len(points) >= 3:
                    points_ch = np.array(points)
                    hull = scipy.spatial.ConvexHull(points_ch)
                    points_ch = hull.points[[hull.vertices]]
                else:
                    points_ch = points

                plt.plot([p[0] for p in points], [p[1] for p in points], color=color, linestyle='None', marker='x')
                xs = [p[0] for p in points_ch]
                ys = [p[1] for p in points_ch]
                if len(ys) > 0:
                    xs.append(xs[0])
                    ys.append(ys[0])
                plt.plot(xs, ys, color)
                # plt.plot(points_ch, color)
                plt.plot(team_1.strength[-1][0], team_1.strength[-1][1], 'ro')
                team_1.plot_team_strength_no_fig()
                team_x = []
                team_y = []
                points = []
                # team_2.plot_team_wim_loos_tie()
                # team_2.plot_team_strength()
                for coords in team_2.results_coordinates_diffs[win_loos_tie]:
                    team_x.append(coords[0] + team_2.strength[-1][0])
                    team_y.append(coords[1] + team_2.strength[-1][1])
                    points.append([team_x[-1], team_y[-1]])
                if len(points) >= 3:
                    points_ch = np.array(points)
                    hull = scipy.spatial.ConvexHull(points_ch)
                    points_ch = hull.points[[hull.vertices]]
                else:
                    points_ch = points
                plt.plot([p[0] for p in points], [p[1] for p in points], color=color, linestyle='None', marker='.')
                xs = [p[0] for p in points_ch]
                ys = [p[1] for p in points_ch]
                if len(ys) > 0:
                    xs.append(xs[0])
                    ys.append(ys[0])
                plt.plot(xs, ys, linestyle='--', color=color)
                # plt.plot(team_x, team_y, linestyle='--', color=color)
                plt.plot(team_2.strength[-1][0], team_2.strength[-1][1], 'go')
                team_2.plot_team_strength_no_fig()
            plt.show()

            strength_1 = team_1.strength[-1]
            strength_2 = team_2.strength[-1]

            val_dif_for_team_1_x = strength_2[0] - strength_1[0]
            val_dif_for_team_1_y = strength_2[1] - strength_1[1]

            # val_dif_for_team_1_x - by goals
            # val_dif_for_team_1_y - by wins
            team_1.get_probability_of_outcome(val_dif_for_team_1_x, val_dif_for_team_1_y)

            more = int(input('More? '))

    def __iter__(self):
        self.iter_counter = 0
        return self

    def __next__(self):
        if self.iter_counter >= len(self.rounds):
            raise StopIteration

        ret_val = self.rounds[self.iter_counter]
        self.iter_counter += 1

        return ret_val
