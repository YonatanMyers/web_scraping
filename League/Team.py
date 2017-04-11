import matplotlib.pyplot as plt
from Util.utilFunctions import compute_distribution

# todo: best predictor counter x, y
# todo: team predictor counter
# todo: Bayesian result predictor
# todo: best predictor by interval
# todo: dominant team


class Team(object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.num_games = {'total': 0, 'win': 0, 'loos': 0, 'tie': 0}

        self.strength = [[0, 0]]
        self.strength_values = {'win': {'by_goals': [], 'by_wins': []}, 'loos': {'by_goals': [], 'by_wins': []},
                                'tie': {'by_goals': [], 'by_wins': []}}

        self.tie_dist = []

        self.distributions = {'win': {'by_goals': {'x': [], 'y': []}, 'by_wins': {'x': [], 'y': []}},
                              'loos': {'by_goals': {'x': [], 'y': []}, 'by_wins': {'x': [], 'y': []}},
                              'tie': {'by_goals': {'x': [], 'y': []}, 'by_wins': {'x': [], 'y': []}}}
        # self.win_x_distribution = []
        # self.loos_x_distribution = []
        # self.tie_x_distribution = []
        #
        # self.win_y_distribution = []
        # self.loos_y_distribution = []
        # self.tie_y_distribution = []
        #
        # self.win_x_distribution_x = []
        # self.loos_x_distribution_x = []
        # self.tie_x_distribution_x = []
        #
        # self.win_y_distribution_x = []
        # self.loos_y_distribution_x = []
        # self.tie_y_distribution_x = []

    # def add_strength(self, in_strength):
    #     self.strength.append(in_strength)

    def add_strength_val(self, val, win_loos_tie, goals_wins):
        self.strength_values[win_loos_tie][goals_wins].append(val)
        self.strength_values[win_loos_tie][goals_wins].sort()

        if len(self.strength_values[win_loos_tie][goals_wins]) > 3:
            self.distributions[win_loos_tie][goals_wins]['x'], self.distributions[win_loos_tie][goals_wins]['y']\
                = compute_distribution(self.strength_values[win_loos_tie][goals_wins], 100)

        self.num_games['win_loos_tie'] = len(self.strength_values[win_loos_tie][goals_wins])
        self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']

    # def add_win_x(self, val):
    #     self.win_x.append(val)
    #     self.win_x.sort()
    #     if len(self.win_x) > 3:
    #         self.win_x_distribution_x, self.win_x_distribution = compute_distribution(self.win_x, 100)
    #     self.num_games['win'] = len(self.win_x)
    #     self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']
    #
    # def add_loos_x(self, val):
    #     self.loos_x.append(val)
    #     self.loos_x.sort()
    #     if len(self.loos_x) > 3:
    #         self.loos_x_distribution_x, self.loos_x_distribution = compute_distribution(self.loos_x, 100)
    #     self.num_games['loos'] = len(self.loos_x)
    #     self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']
    #
    # def add_tie_x(self, val):
    #     self.tie_x.append(val)
    #     self.tie_x.sort()
    #     if len(self.tie_x) > 3:
    #         self.tie_x_distribution_x, self.tie_x_distribution = compute_distribution(self.tie_x, 100)
    #     self.num_games['tie'] = len(self.tie_x)
    #     self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']
    #
    # def add_win_y(self, val):
    #     self.win_y.append(val)
    #     self.win_y.sort()
    #     if len(self.win_y) > 3:
    #         self.win_y_distribution_x, self.win_y_distribution = compute_distribution(self.win_y, 100)
    #     self.num_games['win'] = len(self.win_y)
    #     self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']
    #
    # def add_loos_y(self, val):
    #     self.loos_y.append(val)
    #     self.loos_y.sort()
    #     if len(self.loos_y) > 3:
    #         self.loos_y_distribution_x, self.loos_y_distribution = compute_distribution(self.loos_y, 100)
    #     self.num_games['loos'] = len(self.loos_y)
    #     self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']
    #
    # def add_tie_y(self, val):
    #     self.tie_y.append(val)
    #     self.tie_y.sort()
    #     if len(self.tie_y) > 3:
    #         self.tie_y_distribution_x, self.tie_y_distribution = compute_distribution(self.tie_y, 100)
    #     self.num_games['tie'] = len(self.tie_y)
    #     self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']
    #
    def add_tie_dist(self, val):
        self.tie_dist.append(val)
        self.tie_dist.sort()

    def get_probability_of_outcome(self, val_dif_x, val_dif_y):
        pass
    #     prob_win_x = self.bayes_law_probability(0, val_dif_x)
    #     prob_tie_x = self.bayes_law_probability(1, val_dif_x)
    #     prob_loos_x = self.bayes_law_probability(2, val_dif_x)
    #
    #     prob_win_y = self.bayes_law_probability(0, val_dif_y)
    #     prob_tie_y = self.bayes_law_probability(1, val_dif_y)
    #     prob_loos_y = self.bayes_law_probability(2, val_dif_y)

    # def bayes_law_probability(self, win_tie_loos, in_strength_diff):
    #     """
    #     Bayes Law: P(B|A) = P(A|B) * P(B) / P(A)
    #     :param win_tie_loos 0 - win, 1 - tie, 2 - loos
    #     :param in_strength_diff:
    #     :return:
    #     """
    #     if  win_tie_loos == 0:
    #         prob_x = self.
    #     elif win_tie_loos == 1:
    #     elif win_tie_loos == 2:
    #     else:

    def plot_team_wim_loos_tie(self):
        colors = {'win': 'g', 'loos': 'r', 'tie': 'b'}
        plt.figure()
        for w_l_t in self.distributions.keys():
            distribution = self.distributions[w_l_t]
            color = colors[w_l_t]
            plt.plot(distribution['by_goals']['x'], distribution['by_goals']['y'], color)
        plt.title(self.name + ' by goals_distribution')
        plt.show()

        plt.figure()
        for w_l_t in self.distributions.keys():
            distribution = self.distributions[w_l_t]
            color = colors[w_l_t]
            plt.plot(distribution['by_wins']['x'], distribution['by_wins']['y'], color)
        plt.title(self.name + ' by wins_distribution')
        plt.show()

    def plot_team_strength(self):
        plt.figure()
        x = [coordinates[0] for coordinates in self.strength]
        y = [coordinates[1] for coordinates in self.strength]
        plt.plot(x, y)
        plt.title(self.name + ' path')
        plt.show()

    def print_team(self):
        print('Team:')
        print('Name: ', self.name)
        print('Strength: ', self.strength)
        for itm in self.strength_values.items():
            print(itm[0])
            for iner_itm in itm[1].items():
                print(iner_itm[0])
                print(iner_itm[1])
            print()
