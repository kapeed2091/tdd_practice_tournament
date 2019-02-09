from django.db import models


class Tournament(models.Model):
    STATUS_MAX_LENGTH = 20
    NAME_MAX_LENGTH = 50

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    user_id = models.PositiveIntegerField()
    total_rounds = models.PositiveIntegerField()
    start_datetime = models.DateTimeField()
    status = models.CharField(max_length=STATUS_MAX_LENGTH)

    @classmethod
    def create_tournament(cls, user_id, total_rounds, start_datetime):
        from .user import User
        User.validate_user_id(user_id=user_id)

        cls._validate_total_rounds(total_rounds=total_rounds)

        cls._validate_start_datetime(start_datetime=start_datetime)

        from ..constants.general import TournamentStatus
        cls.objects.create(
            user_id=user_id,
            total_rounds=total_rounds,
            start_datetime=start_datetime,
            status=TournamentStatus.CAN_JOIN.value
        )

    @classmethod
    def get_all_tournament_details(cls):
        details = []
        # todo: feedback function should descend only one level of abstraction
        for each_obj in cls.objects.all():
            details.append(each_obj.convert_to_dict())

        # todo: feedback function should only one thing
        details = sorted(details, key=lambda k: k['start_datetime'])
        return details

    # todo: get this function down
    def convert_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "total_rounds": self.total_rounds,
            "start_datetime": self.start_datetime,
            "status": self.status
        }

    @classmethod
    def get_players_count_in_a_round(cls, tournament_id, round_number):
        total_rounds = cls.get_total_rounds_in_tournament(
            tournament_id=tournament_id
        )
        # todo: feedback function should only one thing
        # todo: feedback more clarity in the calculation
        total_players = 2 ** (total_rounds + 1 - round_number)

        return total_players

    @classmethod
    def get_total_rounds_in_tournament(cls, tournament_id):
        obj = cls.get_tournament_by_id(tournament_id=tournament_id)
        return obj.total_rounds

    @classmethod
    def get_tournament_by_id(cls, tournament_id):
        obj = cls.objects.get(id=tournament_id)
        return obj

    def update_status(self, status):
        self.status = status
        self.save()

    @classmethod
    def validate_tournament_id(cls, tournament_id):
        tournament_exists = cls.objects.filter(id=tournament_id).exists()

        # todo: feedback negative conditionals
        if not tournament_exists:
            from ..exceptions.custom_exceptions import InvalidTournamentId
            raise InvalidTournamentId

    # todo: feedback obscured intent
    def validate_tournament_status(self):
        from ..constants.general import TournamentStatus
        from ..exceptions.custom_exceptions import \
            InvalidFullYetToStartRegister, \
            InvalidInProgresstRegister, InvalidCompletedRegister

        if self.status == TournamentStatus.FULL_YET_TO_START.value:
            raise InvalidFullYetToStartRegister

        elif self.status == TournamentStatus.IN_PROGRESS.value:
            raise InvalidInProgresstRegister

        elif self.status == TournamentStatus.COMPLETED.value:
            raise InvalidCompletedRegister

    # todo: feedback more proper name standards
    def validate_if_status_is_completed(self):
        from tournaments.constants.general import TournamentStatus
        if self.status == TournamentStatus.IN_PROGRESS.value:
            from tournaments.exceptions.custom_exceptions import \
                TournamentInProgress
            raise TournamentInProgress

        elif self.status != TournamentStatus.COMPLETED.value:
            from tournaments.exceptions.custom_exceptions import \
                TournamentNotYetStarted
            raise TournamentNotYetStarted

    @staticmethod
    def _validate_total_rounds(total_rounds):
        if total_rounds < 1:
            from ..exceptions.custom_exceptions import InvalidTotalRounds
            raise InvalidTotalRounds

    @staticmethod
    def _validate_start_datetime(start_datetime):
        from ib_common.date_time_utils.get_current_local_date_time import \
            get_current_local_date_time
        now = get_current_local_date_time()

        # todo: feedback encapsulating conditionals
        if start_datetime <= now:
            from ..exceptions.custom_exceptions import InvalidStartDateTime
            raise InvalidStartDateTime
