import pickle

from Solver.Solver import LeagueSolver
from WebClient.WebClient import WebClient


# import jsonpickle
# import json


def main():
    stored_file_name = 'isr_league.pickle'
    # stored_file_name = 'isr_league.pickle_1'
    teems_x_path = """//*/h4/a"""
    score_x_path = """//*/div/p[@class="score"]"""

    load = False
    # load = True

    if not load:
        web_client = WebClient()
        isr = web_client.collect_league(teems_x_path, score_x_path)
    else:
        with open(stored_file_name, 'rb') as fp:
            isr = pickle.load(fp)

    with open(stored_file_name, 'wb') as fp:
        pickle.dump(isr, fp)

    # isr.print_league()
    solver = LeagueSolver(isr)
    solver.solve_league_no_IRLS()
    isr.print_teem_list_short()
    isr.guess_results()

    # TODO: MUST DO count dominant teem
    # TODO: MUST DO count dominant x, y in team


if __name__ == "__main__":
    main()
