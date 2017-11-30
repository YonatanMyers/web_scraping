from Util.utilFunctions import get_end_score
from Util.utilFunctions import get_half_score
# todo: add connectivity matrix and transitive connectivity graph
# todo: make empty round by marking the game scores as -1 this will indicate to the solver to solve for this round/game


class Round(object):
    """
    A Round of games
    The round is organized as a list of pairs of pairs as follows:
    The outer container is a list of all games.
     Every game is a pair of the the form
     (team A, team A score), (team B, team B score)
     The Round also holds the number of the round.
    """

    def __init__(self, round_n, teem_list, scores_str, end_half):
        """
        The
        Init the Round object
        :param round_n: The index of the Round
        :param teem_list: The list of teams
        :param scores_str: List of goals gained by the teams this is a list of elements of the form 'n(n0)' or '(n0)n'
        n0 is the half time score and is striped away later.
        It is assumed that teams come in pairs so that t0 played t1 and t2 played t3 etc...
        """
        super().__init__()
        self.iter_counter = 0
        self.round_n = round_n
        # strip the elements in the score_str to get the score
        team_score = []
        if end_half == 'end':
            scores = [get_end_score(sc) for sc in scores_str]
            # make the (team, goal) pairs
            team_score = list(zip(teem_list, scores))
        else:
            scores = [get_half_score(sc) for sc in scores_str]
            team_score = list(zip(teem_list, scores))

        self.games = []
        for i in range(0, len(team_score)-1, 2):
            # make the games
            tup = (team_score[i], team_score[i+1])
            self.games.append(tup)

    def print_round(self):
        """
        print the Round to the screen for DBG
        """
        print(self.round_n)
        for g in self.games:
            print(g)

    def __iter__(self):
        self.iter_counter = 0
        return self

    def __next__(self):
        if self.iter_counter >= len(self.games):
            raise StopIteration

        ret_val = self.games[self.iter_counter]
        self.iter_counter += 1

        return ret_val
