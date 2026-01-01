### SpookBot Goals
Discord bot for managing Spooktober Movie Challenge

Default Prefix - `$pook `

## Pre-requisite
- [x] TMDB API Integration
- [x] SQLITE for storing movie list and ratings

## Commands

### Movie List
- [x] **Search** - `<prefix> search [movie_name]` - search movies in TMDB 
- [x] **Set Day** - `<prefix> set_day [day_number] [stream_start] [movie_tmdb_id] ` - select a movie for a certain day in October. Overwrites if there is a selected movie for that day.
- [x] **Get Day** - `<prefix> get_day [day_number]` - displays the movie details for a certain day in October. 
- [x] **Clear Day** - `<prefix> clear_day [day_number]` - clears a certain day in October. 
- [x] **List** - `<prefix> list` - shows the movie list
- [x] **Clear List** - `<prefix> clear_list` - clears the movie list. 
- [x] **Announce** - `<prefix> announce` - send a message to announce the movie of the current day. 

### Movie Ratings
- [ ] **Rate** - `<prefix> rate [day_number] [rating]` - add a rating to a movie of a particular day.
- [ ] **Ratings** - `<prefix> ratings [day_number]` - check ratings of a movie of a particular day.  

### Misc
- [x] **Say** - `<prefix> say [message]` - send a message.
- [x] **Spook** - `<prefix> spook` - send a random spiel about the spook.
- [x] **Help** - `<prefix> help`- display commands. 
