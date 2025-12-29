class Movie:
    def __init__(
        self,
        day,
        tmdb_id,
        movie_title,
        showing_start,
        showing_end,
        picked_by,
        picker_avatar,
    ) -> None:
        self.day = day
        self.tmdb_id = tmdb_id
        self.movie_title = movie_title
        self.showing_start = showing_start
        self.showing_end = showing_end
        self.picked_by = picked_by
        self.picker_avatar = picker_avatar
