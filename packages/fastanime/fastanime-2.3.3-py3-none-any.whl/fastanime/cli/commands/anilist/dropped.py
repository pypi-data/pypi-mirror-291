from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from fastanime.cli.config import Config


@click.command(help="View anime you dropped")
@click.pass_obj
def dropped(config: "Config"):
    from ....anilist import AniList
    from ...interfaces import anilist_interfaces
    from ...utils.tools import FastAnimeRuntimeState, exit_app

    if not config.user:
        print("Not authenticated")
        print("Please run: fastanime anilist loggin")
        exit_app()
    anime_list = AniList.get_anime_list("DROPPED")
    if not anime_list:
        return
    if not anime_list[0] or not anime_list[1]:
        return
    media = [
        mediaListItem["media"]
        for mediaListItem in anime_list[1]["data"]["Page"]["mediaList"]
    ]  # pyright:ignore
    anime_list[1]["data"]["Page"]["media"] = media  # pyright:ignore
    fastanime_runtime_state = FastAnimeRuntimeState()
    fastanime_runtime_state.anilist_data = anime_list[1]
    anilist_interfaces.anilist_results_menu(config, fastanime_runtime_state)
