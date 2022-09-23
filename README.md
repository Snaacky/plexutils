# plexutils

A repository of useful Plex and general automation scripts that I've written overtime to streamline the process of automating my Plex.

### find_missing_episodes
* Scans over TV shows in a library using the Plex and TVDB v4 APIs and check whether there are any missing seasons or episode mismatches.
* Skips over specials because TVDB lists interviews, movies, commentary segments, and more as specials.
* Skips over seasons that have not aired yet.
* Takes about ~30 minutes per 1000 titles because TVDB's API is rather slow.
<img src="https://i.imgur.com/hbOLOco.png" style="width:75%;height:50%">

### find_duplicate_files
* Scans over TV shows in a library using the Plex API and checks if any episodes have more than one file location.
<img src="https://i.imgur.com/OYzUJuv.png" style="width:75%;height:50%">

