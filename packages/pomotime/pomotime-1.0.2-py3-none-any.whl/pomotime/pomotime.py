#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pomotime: A simple terminal-based Pomodoro timer with configurable settings.
Author: https://github.com/zabojeb
License: Apache 2.0 License

This script allows you to run work and break sessions based on the Pomodoro technique,
with customizable settings for durations, colors, fonts, and sounds. The configuration 
is loaded from a TOML file located at ~/.config/pomotime/pomotime.toml.

Pomotime is based on an enhanced version of timer-cli (https://github.com/1Blademaster/timer-cli) by 1Blademaster
And inspired by:
- peaclock (https://github.com/octobanana/peaclock) by octobanana
- gone (https://github.com/guillaumebreton/gone) by guillaumebreton

Dependencies:
- art: for ASCII art rendering
- rich: for terminal output styling
- click: for command-line interface handling
- toml: for loading the configuration file
"""

import math
import os
import sys
import time
import shutil
import toml
from typing import Union

import click
from art import text2art  # For rendering timer as ASCII art
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.measure import Measurement
import appdirs

# Application name
appname = "pomotime"

# Define paths to user directories
user_config_dir = appdirs.user_config_dir(appname)
user_data_dir = appdirs.user_data_dir(appname)

# Paths to configuration and sound files
USER_CONFIG_PATH = os.path.join(user_config_dir, 'pomotime.toml')
USER_SOUND_PATH = os.path.join(user_data_dir, 'sound.wav')

# Path to the default configuration and sound files
DEFAULT_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), 'config', 'pomotime.toml')
DEFAULT_SOUND_PATH = os.path.join(os.path.dirname(__file__), 'sound.wav')

# Create directories if they don't exist
os.makedirs(user_config_dir, exist_ok=True)
os.makedirs(user_data_dir, exist_ok=True)

# Copy default configuration and sound files if user files do not exist
if not os.path.exists(USER_CONFIG_PATH):
    shutil.copy(DEFAULT_CONFIG_PATH, USER_CONFIG_PATH)

if not os.path.exists(USER_SOUND_PATH):
    shutil.copy(DEFAULT_SOUND_PATH, USER_SOUND_PATH)

# Load configuration
config = toml.load(USER_CONFIG_PATH)

# CLI context settings
CONTEXT_SETTINGS: dict = dict(help_option_names=["-h", "--help"])

# Constants loaded from the configuration file
BLOCK_MODE: bool = config["settings"]["block_mode"]
SOLID_MODE: bool = config["settings"]["solid_mode"]
FONT: str = config["settings"]["font"]
TEXT_COLOUR_HIGH_PERCENT: str = config["settings"]["text_colour_high_percent"]
TEXT_COLOUR_MID_PERCENT: str = config["settings"]["text_colour_mid_percent"]
TEXT_COLOUR_LOW_PERCENT: str = config["settings"]["text_colour_low_percent"]
MESSAGE_COLOR: str = config["settings"]["message_color"]
TIMER_HIGH_PERCENT: float = config["settings"]["timer_high_percent"]
TIMER_LOW_PERCENT: float = config["settings"]["timer_low_percent"]
PATH_TO_SOUND: str = USER_SOUND_PATH

Number = Union[int, float]  # Type alias for numbers (int or float)

# Mapping of session types to their default names and durations
SESSION_TYPES = {
    "w": ("Work", 25),  # Work session (25 minutes by default)
    "s": ("Short Break", 5),  # Short break (5 minutes by default)
    "l": ("Long Break", 15),  # Long break (15 minutes by default)
}


def standardize_time_str(num: Number) -> str:
    """
    Converts a number to a two-digit string format. Ensures that single-digit numbers are padded with a leading zero.

    Args:
        num (Number): The number to be converted.

    Returns:
        str: A two-digit string representation of the number.
    """
    num = round(num)
    if num <= 0:
        return "00"
    time_str = str(num)
    if len(time_str) == 1:
        time_str = f"0{time_str}"
    return time_str


def createTimeString(hrs: Number, mins: Number, secs: Number) -> str:
    """
    Creates a time string in the format HH:MM:SS.

    Args:
        hrs (Number): Hours.
        mins (Number): Minutes.
        secs (Number): Seconds.

    Returns:
        str: The formatted time string.
    """
    time_hrs = standardize_time_str(hrs)
    time_mins = standardize_time_str(mins)
    time_secs = standardize_time_str(secs)
    return f"{time_hrs}:{time_mins}:{time_secs}"


def play_sound():
    """
    Plays the configured sound file depending on the platform.
    Supports macOS, Windows, and Linux.
    """
    if sys.platform == "darwin":  # macOS
        os.system(f"afplay {PATH_TO_SOUND}")
    elif sys.platform == "win32":  # Windows
        os.system(
            f"powershell -c (New-Object Media.SoundPlayer '{PATH_TO_SOUND}').PlaySync();")
    else:  # Assume Linux or other UNIX-like systems
        os.system(f"aplay {PATH_TO_SOUND}")


def run_timer(console, duration_secs: int, message: str, no_sound: bool) -> None:
    """
    Runs the timer and updates the console display with the remaining time.

    Args:
        console (Console): The Rich console object used for display.
        duration_secs (int): The duration of the timer in seconds.
        message (str): The session message to display.
        no_sound (bool): Whether to disable sound notifications at the end of the session.
    """
    start_time = math.floor(time.time())
    target_time = start_time + duration_secs
    time_difference_secs = duration_secs

    try:
        with Live(screen=True) as live:
            while round(target_time) > round(time.time()):
                remaining_time = math.floor(
                    target_time) - math.floor(time.time())
                remaining_time_string = createTimeString(
                    remaining_time // 3600,
                    (remaining_time // 60) % 60,
                    remaining_time % 60,
                )

                # Render the timer as ASCII art, replacing characters if BLOCK_MODE is enabled
                if SOLID_MODE:
                    remaining_time_text = Text(
                        text2art(remaining_time_string + "\n\n", font=FONT)
                        .replace("#", "██")
                        .replace(" ", "  ")
                    )
                elif BLOCK_MODE:
                    remaining_time_text = Text(
                        text2art(remaining_time_string + "\n\n",
                                 font=FONT).replace("#", "█")
                    )
                else:
                    remaining_time_text = Text(
                        text2art(remaining_time_string + "\n\n", font=FONT))

                # Adjust the color of the timer based on the remaining time percentage
                time_difference_percentage = remaining_time / time_difference_secs
                if TIMER_HIGH_PERCENT < time_difference_percentage <= 1:
                    remaining_time_text.stylize(TEXT_COLOUR_HIGH_PERCENT)
                elif TIMER_LOW_PERCENT < time_difference_percentage <= TIMER_HIGH_PERCENT:
                    remaining_time_text.stylize(TEXT_COLOUR_MID_PERCENT)
                else:
                    remaining_time_text.stylize(TEXT_COLOUR_LOW_PERCENT)

                # Create and align the message text
                message_text = Text(message, style=MESSAGE_COLOR)
                message_text.align(
                    "center",
                    Measurement.get(console, console.options,
                                    remaining_time_text)
                    .normalize()
                    .maximum,
                )

                # Combine the timer and message text for display
                display_text = Text.assemble(remaining_time_text, message_text)
                display = Align.center(
                    display_text, vertical="middle", height=console.height + 1
                )
                live.update(display)
                time.sleep(1)

        # Play sound if no_sound is not enabled
        if not no_sound:
            play_sound()

    except KeyboardInterrupt:
        console.print("[red]Quitting...[/red]")
        sys.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name="pomotime")
@click.argument("sequence", type=str, required=False, default="wswl")
@click.option("-w", type=int, default=25, help="Duration of work sessions in minutes")
@click.option("-s", type=int, default=5, help="Duration of short breaks in minutes")
@click.option("-l", type=int, default=15, help="Duration of long breaks in minutes")
@click.option(
    "--no-sound",
    default=False,
    is_flag=True,
    help="Do not play a sound once a session is over",
)
@click.option(
    "--config",
    default=False,
    is_flag=True,
    help="Display the path to the configuration file and sounds folder",
)
def pomotime(sequence: str, w: int, s: int, l: int, no_sound: bool, config: bool) -> None:
    """
    Starts a series of Pomodoro sessions based on the given sequence.

    SEQUENCE is a string of characters defining the order of work (w), short break (s),
    and long break (l) sessions. For example, 'wswl' means one work session, followed by
    a short break, another work session, and then a long break.

    Args:
        sequence (str): The sequence of session types.
        w (int): Duration of work sessions in minutes.
        s (int): Duration of short breaks in minutes.
        l (int): Duration of long breaks in minutes.
        no_sound (bool): Whether to disable sound notifications.
        config (bool): Whether to display the path to the configuration file.
    """
    if config:
        print(f"Configuration file path: {USER_CONFIG_PATH}")
        print(f"Sound file path: {USER_SOUND_PATH}")
        sys.exit()

    # Initialize console for output
    console = Console()

    # Update session durations based on command-line arguments
    SESSION_TYPES["w"] = ("Work", w)
    SESSION_TYPES["s"] = ("Short Break", s)
    SESSION_TYPES["l"] = ("Long Break", l)

    # Process the sequence and run the timer for each session
    for session_type in sequence.lower():
        if session_type not in SESSION_TYPES:
            console.print(
                f"[red]Invalid session type '{session_type}' in sequence[/red]")
            sys.exit(1)

        session_name, duration = SESSION_TYPES[session_type]
        duration_seconds = duration * 60
        message = f"{session_name} - {duration} minutes"

        console.print(f"[green]Starting {session_name}...[/green]")
        run_timer(console, duration_seconds,
                  message, no_sound)

    console.print("[bold green]All sessions complete![/bold green]")


if __name__ == "__main__":
    pomotime()
