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

    def add_strength_val(self, val, win_loos_tie, goals_wins):
        self.strength_values[win_loos_tie][goals_wins].append(val)
        self.strength_values[win_loos_tie][goals_wins].sort()

        if len(self.strength_values[win_loos_tie][goals_wins]) > 3:
            self.distributions[win_loos_tie][goals_wins]['x'], self.distributions[win_loos_tie][goals_wins]['y']\
                = compute_distribution(self.strength_values[win_loos_tie][goals_wins], 100)

        self.num_games[win_loos_tie] = len(self.strength_values[win_loos_tie][goals_wins])
        self.num_games['total'] = self.num_games['loos'] + self.num_games['tie'] + self.num_games['win']

    def add_tie_dist(self, val):
        self.tie_dist.append(val)
        self.tie_dist.sort()

    def get_probability_of_outcome(self, val_dif_x, val_dif_y):
        # dif_x : goals
        # dif_y : wins
        prob_win_x = self.bayes_law_probability('by_goals', 'win', val_dif_x)
        prob_tie_x = self.bayes_law_probability('by_goals', 'tie', val_dif_x)
        prob_loos_x = self.bayes_law_probability('by_goals', 'loos', val_dif_x)

        prob_win_y = self.bayes_law_probability('by_wins', 'win', val_dif_y)
        prob_tie_y = self.bayes_law_probability('by_wins', 'tie', val_dif_y)
        prob_loos_y = self.bayes_law_probability('by_wins', 'loos', val_dif_y)

    def bayes_law_probability(self, goals_wins, win_tie_loos, in_strength_diff):
        """
        Bayes Law: P(B|A) = P(A|B) * P(B) / P(A)
        :param goals_wins USE GOALS OR WINS
        :param win_tie_loos 0 - win, 1 - tie, 2 - loos
        :param in_strength_diff:
        :return:
        """
        """
        Algo:
        Fetch probability f(B) that is the probability density function of 'win_tie_loos'
        Compute P(A|B) = the probability of  in_strength_diff in the f(B) 
        Compute P(B) = self.num_games[win_tie_loos] / self.num_games['total']
        there is no need to compute P(A) as it is the same for all test cases
        """
        f_b = self.distributions[win_tie_loos][goals_wins]
        p_b = self.num_games[win_tie_loos] / self.num_games['total']
        print(p_b)
        print('total: ' + str(self.num_games['total']))

    def plot_team_wim_loos_tie(self):
        colors = {'win': 'g', 'loos': 'r', 'tie': 'b'}
        plt.figure()
        for w_l_t in self.distributions.keys():
            distribution = self.distributions[w_l_t]
            color = colors[w_l_t]
            plt.plot(distribution['by_goals']['x'], distribution['by_goals']['y'], color)
        plt.title(self.name[::-1] + ' by goals_distribution')
        plt.show()

        plt.figure()
        for w_l_t in self.distributions.keys():
            distribution = self.distributions[w_l_t]
            color = colors[w_l_t]
            plt.plot(distribution['by_wins']['x'], distribution['by_wins']['y'], color)
        plt.title(self.name[::-1] + ' by wins_distribution')
        plt.show()

    def plot_team_strength(self):
        plt.figure()
        x = [coordinates[0] for coordinates in self.strength]
        y = [coordinates[1] for coordinates in self.strength]
        plt.plot(x, y)
        plt.title(self.name[::-1] + ' path')
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
