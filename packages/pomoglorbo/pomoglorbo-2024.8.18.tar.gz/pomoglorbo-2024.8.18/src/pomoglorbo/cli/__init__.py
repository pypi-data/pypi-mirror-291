#!/usr/bin/env python

# SPDX-FileCopyrightText: 2021-2023 Bhatihya Perera
# SPDX-FileCopyrightText: 2023 Justus Perlwitz
# SPDX-FileCopyrightText: 2024 Justus Perlwitz
#
# SPDX-License-Identifier: MIT
"""Pomoglorbo's CLI package."""

import gettext
import subprocess
import threading
from importlib import resources

from pomoglorbo import messages
from pomoglorbo.cli.layout import make_user_interface
from pomoglorbo.cli.render import render_tomato
from pomoglorbo.cli.util import gettext_lazy as _
from pomoglorbo.core import sound
from pomoglorbo.core.config import create_configuration
from pomoglorbo.core.tomato import tomato_interact
from pomoglorbo.core.util import (
    every,
)
from pomoglorbo.types import UserInterface


def draw(interface: UserInterface) -> None:
    tomato_interact(interface.tomato, "update")
    result = render_tomato(interface.tomato)
    layout = interface.layout
    layout.text_area.text = result.text


def run(interface: UserInterface) -> None:
    draw(interface)
    threading.Thread(
        target=lambda: every(1, lambda: draw(interface)),
        daemon=True,
    ).start()
    interface.application.run()


def main() -> None:
    path = resources.files(messages)
    with resources.as_file(path) as path:
        gettext.bindtextdomain("messages", localedir=path)
    gettext.textdomain("messages")

    config = create_configuration()
    if config.audio_check:
        # WHY twice: to catch more issues
        print(_("Playing alarm once..."))
        sound.play(config.audio_file, block=True)
        print(_("Playing alarm twice..."))
        sound.play(config.audio_file, block=True)
        print(_("Have a nice day"))
        return
    ui = make_user_interface(config)
    run(ui)
    if config.exit_cmd:
        subprocess.run(config.exit_cmd)


if __name__ == "__main__":
    # Profiling method 1)
    # import pstats
    # import cProfile
    # pr = cProfile.Profile()
    # pr.enable()
    # main()
    # pr.disable()
    # sortby = pstats.SortKey.CUMULATIVE
    # with open("profile.txt", "w") as fd:
    #     ps = pstats.Stats(pr, stream=fd).sort_stats(sortby)
    #     ps.print_stats()
    #
    # Profiling method 2)
    # https://github.com/sumerc/yappi/blob/master/doc/api.md
    # import yappi

    # yappi.set_clock_type("cpu")
    # yappi.start()
    main()
    # with open("profile.txt", "w") as fd:
    #     stats = yappi.get_func_stats()
    #     stats.save("profile.pstat", "pstat")
    # then snakeviz profile.pstat
