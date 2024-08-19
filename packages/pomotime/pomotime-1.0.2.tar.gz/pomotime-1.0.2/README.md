# Pomotime

Pomotime is a simple, customizable terminal-based Pomodoro timer that helps you manage your work and break sessions effectively. It offers flexible settings for session durations, customizable visual styles, fonts and even sound notifications.

## Features

- **Customizable Durations**: Define your own durations for work sessions, short breaks, and long breaks.
- **Customizable Work & Break Sequences**: Set your work and break sequences, for example: "wswl" is "Work, Short Break, Work, Long Break"
- **Flexible Settings**: Choose from different fonts, font styles and colors for the timer display.
- **Sound Alerts**: Configure custom sound notifications to signal the end of each session.
- **Cross-Platform**: Works on macOS, Windows, and Linux.

## Installation

Install via pip:

```bash
pip install pomotime
```

Install via pipx (for Arch and etc.):

```bash
pipx install pomotime
```

## Usage

After installation, you can run `pomotime` from the terminal. Below are some example commands:

- **Start a Pomodoro sequence with the default settings:**

  ```bash
  pomotime
  ```

- **Customize session durations:**

  ```bash
  pomotime -w 30 -s 10 -l 20
  ```

- **Customize Pomodoro sequence and work duration:**

  ```bash
  pomotime -w 45 wlwswl
  ```

- **Disable sound notifications:**

  ```bash
  pomotime --no-sound
  ```

- **Display the paths to the configuration file and sounds folder:**

  ```bash
  pomotime --config
  ```

## Configuration

Pomotime uses a TOML configuration file to store customizable settings. By default, the configuration file is located at:

`~/.config/pomotime/pomotime.toml`

There is full documentation inside of pomotime.toml

### Example Configuration File

```toml
[settings]
block_mode = true
solid_mode = false
font = "block"
text_colour_high_percent = "#FFFFFF"
text_colour_mid_percent = "#888888"
text_colour_low_percent = "#666666"
message_color = "yellow"
timer_high_percent = 0.3
timer_low_percent = 0.15
```

### Custom Sounds

Pomotime allows you to use your own sound files for session notifications. By default, the sound file is located at:

`~/.local/share/pomotime/sound.wav`

You can replace this file with your own `.wav` file, or edit the `pomotime.toml` configuration file to point to a different location.

## Acknowledgements

Pomotime is based on the enhanced version of [timer-cli](https://github.com/1Blademaster/timer-cli) by [1Blademaster](https://github.com/1Blademaster).

Special thanks to the following projects for inspiration:

- [peaclock](https://github.com/octobanana/peaclock) by [octobanana](https://github.com/octobanana)
- [gone](https://github.com/guillaumebreton/gone) by [guillaumebreton](https://github.com/guillaumebreton)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

Pomotime is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/zabojeb">zabojeb</a>
</p>