class Review:
    def __init__(
        self, rater_id, day, score, rater_name, rater_avatar, comment=None
    ) -> None:
        self.rater_id = rater_id
        self.day = day
        self.score = score
        self.rater_name = rater_name
        self.rater_avatar = rater_avatar
        self.comment = comment
