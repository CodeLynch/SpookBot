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
- [ ] **Get Day** - `<prefix> get-day [day_number]` - Displays the movie details and its ratings for a certain day in October. 
- [x] **List** - `<prefix> list` - Shows the movie list
- [ ] **Announce** - `<prefix> announce` - Send a message to announce the movie of the current day. 

### Movie Ratings
- [ ] **Rate** - `<prefix> rate [day_number]` - Send a message to announce the movie details and streaming time of the current day.

### Misc
- [x] **Say** - `<prefix> say [message]` - Send a message
- [x] **Spook** - `<prefix> spook` - Send a random spiel about the spook.

