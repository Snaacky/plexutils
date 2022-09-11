import tvdb_v4_official as tvdb
from loguru import logger
from plexapi.server import PlexServer


def connect_to_tvdb(api_key: str, token: str):
    if api_key is None or token is None:
        logger.error("TVDB api_key or token were empty, existing...")
        raise SystemExit
    try:
        connection = tvdb.TVDB(api_key, token)
    except Exception as e:
        logger.error(f"Unable to conect to TVDB, exiting... {e}")
        raise SystemExit
    logger.info("Successfully connected to TVDB with provided information")
    return connection


def connect_to_plex(baseurl: str, token: str):
    if baseurl is None or token is None:
        logger.error("Plex baseurl or token were empty, existing...")
        raise SystemExit
    try:
        connection = PlexServer(baseurl, token)
    except Exception as e:
        logger.error(f"Unable to conect to Plex, exiting... {e}")
        raise SystemExit
    logger.info("Successfully connected to Plex with provided information")
    return connection
