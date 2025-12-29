### SpookBot Goals
Discord bot for managing Spooktober Movie Challenge

Default Prefix - `$pook `

## Pre-requisite
- [x] TMDB API Integration
- [x] SQLITE for storing movie list and ratings

## Commands

### Movie List
- [x] **Search** - `<prefix> search [movie_name]` - Search movies in TMDB 
- [x] **Set Day** - `<prefix> set_day [day_number] [stream_start] [movie_tmdb_id] ` - Select a movie for a certain day in October. Overwrites if there is a selected movie for that day.
- [x] **Get Day** - `<prefix> get_day [day_number]` - Displays the movie details and its ratings for a certain day in October. 
- [x] **Clear Day** - `<prefix> clear_day [day_number]` - clears a certain day in October. 
- [x] **List** - `<prefix> list` - Shows the movie list
- [x] **Clear List** - `<prefix> clear_day` - clears the movie list. 
- [x] **Announce** - `<prefix> announce` - Send a message to announce the movie of the current day. 

### Movie Ratings
- [ ] **Rate** - `<prefix> rate [day_number] [rating]` - Add a rating to a movie of a particular day.

### Misc
- [x] **Say** - `<prefix> say [message]` - Send a message.
- [x] **Spook** - `<prefix> spook` - Send a random spiel about the spook.
- [ ] **Help** - `<prefix> help`- Display commands. 
