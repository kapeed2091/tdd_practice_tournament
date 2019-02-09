class CreateMatchesInTournamentInteractor(object):
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self.tournament_id = -1

    def setup(self, tournament_id):
        self.tournament_id = tournament_id

    def _prepare_matches(self, tournament_data):
        no_of_rounds = tournament_data['no_of_rounds']
        player_usernames = tournament_data['player_usernames']
        matches = []
        for i in range(0, 2**(no_of_rounds-1)):
            matches.append({'player_usernames': player_usernames[2*i:2*i+2]})
        return matches

    def execute(self):
        tournament_data = self.storage.get_tournament_data(self.tournament_id)
        matches = self._prepare_matches(tournament_data)
        self.storage.create_matches(matches)
        return self.presenter.present_create_matches_in_tournament()
