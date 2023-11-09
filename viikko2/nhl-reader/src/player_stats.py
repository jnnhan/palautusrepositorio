from player import Player

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def points(self, player):
        return player.goals + player.assists

    def top_scorers_by_nationality(self, nationality):
        stats = []
        for player in self.reader.players:
            if player.nationality == "FIN":
                stats.append(player)

        stats.sort(key=self.points, reverse=True)
        return stats
