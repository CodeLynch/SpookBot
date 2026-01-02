### SpookBot Goals
Discord bot for managing Spooktober Movie Challenge

Default Prefix - `$pook `

## Pre-requisite
- [x] TMDB API Integration
- [x] SQLITE for storing movie list and ratings

## Commands

### Movie List
- [x] **Search** - `<prefix> search [movie_name]` - search movies in TMDB 
- [x] **Set Day** - `<prefix> set_day [day_number] [stream_start] [movie_tmdb_id] [is_mystery(optional)]` - select a movie for a certain day in October. Overwrites if there is a selected movie for that day. If `is_mystery` is true, `movie_tmdb_id` **argument is ignored** so it doesn't matter what value is inputted for that argument.
- [x] **Get Day** - `<prefix> get_day [day_number]` - displays the movie details for a certain day in October. 
- [x] **Clear Day** - `<prefix> clear_day [day_number]` - clears a certain day in October. 
- [x] **List** - `<prefix> list` - shows the movie list
- [x] **Clear List** - `<prefix> clear_list` - clears the movie list. 
- [x] **Announce** - `<prefix> announce` - send a message to announce the movie of the current day. 

### Movie Ratings
- [x] **Rate** - `<prefix> rate [day_number] [rating] [comment(optional)]` - add a rating of a movie for a particular day.  
- [x] **Ratings** - `<prefix> ratings [day_number]` - check ratings of a movie for a particular day.  
- [x] **Delete Rating** - `<prefix> delete_rating [day_number]` - remove your rating of a movie for a particular day.  

### Misc
- [x] **Say** - `<prefix> say [message]` - send a message.
- [x] **Spook** - `<prefix> spook` - send a random spiel about the spook.
- [x] **Help** - `<prefix> help`- display commands. 
