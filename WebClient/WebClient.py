from League.Round import Round
from League.League import League

from selenium import webdriver

# todo: improve web scraper to start at: http://sports.walla.co.il/category/157 and read all rounds
# todo: this ^ must be done as well as reading everything in the existing "isr_league.pickle" or from
# "http://sports.walla.co.il/leagueround/201' + str(i) + '?leagueId=2343"


class WebClient(object):
    """
    The Client class is responsible to the communication with the www.
    We scrape the www using selenium as this solves all (?) the loading and java-script problems.
    The browser opens the page and runs all the JS and we come along after it is all over and read the resulting HTML
    """

    def __init__(self):
        """
        Init the connection with the browser
        """
        super().__init__()
        self.driverPath = r"E:\instalesAndDownloads\WebDriver\chromedriver.exe"
        self.chrome = webdriver.Chrome(self.driverPath)

    def collect_league(self, teems_x_path, score_x_path):
        """
        Open the page
        :param teems_x_path: the Xpathe to the team name in teh www
        :param score_x_path: Xpathe to the score in the www
        """

        round_counter = 0
        rounds = []
        team_2_ind = {}
        teem_list = ''
        urls = [[55, 27, 'http://sports.walla.co.il/leagueround/201', 'str(i)', '?leagueId=2343'],
                [157, 7, 'http://sports.walla.co.il/category/', 'str(i)']]
        for url_i in urls:
            for i in range(url_i[0], url_i[0] + url_i[1]):
                url = self.make_url(url_i, i)
                self.chrome.get(url)
                teem_list = self.get_all(teems_x_path)
                scores_str = self.get_all(score_x_path)
                if len(team_2_ind) == 0:
                    for team, team_i in zip(teem_list, range(len(teem_list))):
                        team_2_ind[team] = team_i
                if len(scores_str) > 0:
                    round_counter += 1
                    rounds.append(Round(round_counter, teem_list, scores_str))

        return League(team_2_ind, rounds)

    def get_all(self, x_path):
        """
        This function gets elements by Xpath.
        :param x_path: This function gets elements by Xpath.
        :return: The elements in a list
        """
        raw_elements = self.chrome.find_elements_by_xpath(x_path)
        elements = [e.text for e in raw_elements]
        return elements

    def make_url(self, url_i, i):
        url_i = url_i[2:]
        url_strs = [elem if elem != 'str(i)' else str(i) for elem in url_i]
        url = ''
        for ix in range(len(url_strs)):
            url += url_strs[ix]
        return url