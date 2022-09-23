from loguru import logger
from pyaml_env import parse_config

from plexutils.utils.connections import connect_to_plex


class FindDuplicateFiles():
    def __init__(self) -> None:
        self.logger = logger.opt(ansi=True)
        self.config = parse_config("./config.yml")
        self.plex = connect_to_plex(baseurl=self.config["plex"]["baseurl"], token=self.config["plex"]["token"])
        self.check_library("Anime")

    def check_library(self, library: str) -> None:
        for plex_show in self.plex.library.section(library).all():
            tvdb_id = self.get_tvdbid_for_title(plex_show)
            self.logger.info(f"[{tvdb_id}] {plex_show.title}")

            episodes = plex_show.episodes()
            for episode in episodes:
                if len(episode.locations) > 1:
                    self.logger.info(
                        "<yellow>"
                        f"  - S{episode.seasonNumber:0>2}E{episode.episodeNumber:0>2} "
                        f"has {len(episode.locations)} files.</yellow>"
                    )

    def get_tvdbid_for_title(self, title: str) -> int:
        """Attempts to get the TVDB for the provided Plex title."""
        try:
            return int([guid for guid in title.guids if "tvdb" in guid.id][0].id.replace("tvdb://", ""))
        except IndexError:
            self.logger.info(f"[??????] {title.title}")
            self.logger.info("  <red> - TVDB ID not found for title, not matched on Plex?</red>")


if __name__ == "__main__":
    FindDuplicateFiles()
