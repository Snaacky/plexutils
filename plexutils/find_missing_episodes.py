import time

import arrow
from loguru import logger
from pyaml_env import parse_config

from plexutils.utils.connections import connect_to_tvdb, connect_to_plex


class FindMissingEpisodes():
    def __init__(self) -> None:
        self.logger = logger.opt(ansi=True)
        self.config = parse_config("../config.yml")
        self.plex = connect_to_plex(baseurl=self.config["plex"]["baseurl"], token=self.config["plex"]["token"])
        self.tvdb = connect_to_tvdb(api_key=self.config["tvdb"]["apikey"], token=self.config["tvdb"]["pin"])
        self.check_library("Anime")

    def check_library(self, library: str) -> None:
        for plex_show in self.plex.library.section(library).all():
            tvdb_id = self.get_tvdbid_for_title(plex_show)
            if not tvdb_id:
                continue

            try:
                tvdb_show = self.tvdb.get_series_extended(tvdb_id)
            except ValueError:
                self.logger.info(f"[??????] {plex_show.title}")
                self.logger.info("  <red> - TVDB ID not found for title, doesn't exist on TVDB?</red>")
                continue

            tvdb_seasons = self.get_clean_tvdb_seasons(tvdb_show)

            tvdb_episodes = []
            for season in tvdb_seasons:
                tvdb_episodes = tvdb_episodes + season["episodes"]

            self.logger.info(f"[{tvdb_id}] {plex_show.title}")

            for season in sorted(tvdb_seasons, key=lambda x: x["number"]):
                if not season["number"]:
                    continue

                if not self.has_season_aired(season):
                    continue

                try:
                    match = plex_show.season(season["number"])
                except Exception:
                    self.logger.info(f"  <yellow> - Missing season {season['number']} on Plex</yellow>")
                    continue

                if len(match.episodes()) != len(season["episodes"]):
                    self.logger.info(
                        f"  <yellow> - Season {season['number']} episode count mismatch "
                        f"Plex: {len(match.episodes())} "
                        f"TVDB: {len(season['episodes'])}</yellow>"
                    )
                else:
                    self.logger.info(f"  <green> - Season {season['number']} episodes match TVDB</green>")

    def has_season_aired(self, season: dict) -> bool:
        """Checks if the release date of the first episode of the season has passed."""
        if not len(season["episodes"]):
            return False
        if not season["episodes"][0]["aired"]:
            return False
        if arrow.get(season["episodes"][0]["aired"]).timestamp() < int(time.time()):
            return True
        return False

    def get_tvdbid_for_title(self, title: str) -> int:
        """Attempts to get the TVDB for the provided Plex title."""
        try:
            return int([guid for guid in title.guids if "tvdb" in guid.id][0].id.replace("tvdb://", ""))
        except IndexError:
            self.logger.info(f"[??????] {title.title}")
            self.logger.info("  <red> - TVDB ID not found for title, not matched on Plex?</red>")

    def get_clean_tvdb_seasons(self, series: dict) -> list:
        """Strips away the dupe seasons by only grabbing the Aired Order seasons."""
        return [
            self.tvdb.get_season_extended(season["id"])
            for season in series["seasons"]
            if season["type"]["name"] == "Aired Order"
        ]


if __name__ == "__main__":
    FindMissingEpisodes()
