class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0
        self.score = ""

        self.MAX_POINTS = 4
        self.points = {
            0: "Love",
            1: "Fifteen",
            2: "Thirty",
            3: "Forty"
        }

    def won_point(self, player_name):
        if player_name == "player1":
            self.m_score1 = self.m_score1 + 1
        else:
            self.m_score2 = self.m_score2 + 1

    def _same_scores(self):
        if self.m_score1 < 3:
            self.score = self.points[self.m_score1] + "-All"
        else:
            self.score = "Deuce"

    def _advantage_scores(self):
        minus_result = self.m_score1 - self. m_score2

        if minus_result == 1:
            self.score = "Advantage player1"
        elif minus_result == -1:
            self.score = "Advantage player2"
        elif minus_result >= 2:
            self.score = "Win for player1"
        else:
            self.score = "Win for player2"

    def get_score(self):
        self.score = ""
        temp_score = 0

        if self.m_score1 == self.m_score2:
            self._same_scores()
        elif self.m_score1 >= self.MAX_POINTS or self.m_score2 >= self.MAX_POINTS:
            self._advantage_scores()
        else:
            self.score = self.points[self.m_score1] + "-" + self.points[self.m_score2]
        return self.score
