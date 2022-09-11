# plexutils

A repository of useful Plex and general automation scripts that I've written overtime to streamline the process of automating my Plex.

### find_missing_episodes
* Using the Plex API and the TVDB v4 API, find_missing_episodes will scan over all TV shows in your Plex based on the provided library and check whether there are any missing seasons or episode count mismatches.
* Skips over specials because TVDB lists interviews, movies, commentary segments, and more as specials.
* Skips over seasons that have not aired yet.
