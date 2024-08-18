# SPDX-FileCopyrightText: 2023 Justus Perlwitz
# SPDX-FileCopyrightText: 2024 Justus Perlwitz
# SPDX-FileCopyrightText: 2021-2023 Bhatihya Perera
#
# SPDX-License-Identifier: MIT
"""Provide utilities for CLI."""

from gettext import gettext

from prompt_toolkit.application.current import get_app


def exit_clicked() -> None:
    get_app().exit()


def gettext_lazy(message: str) -> str:
    return gettext(message)
