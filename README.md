# An Anime Game Launcher Flatpak

## Installation

To install the launcher via flatpak you will first have to make sure that you have flathub's remote installed

```sh
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

After installing flathub's remote you install launcher.moe's remote

```sh
flatpak remote-add --if-not-exists launcher.moe https://gol.launcher.moe/gol.launcher.moe.flatpakrepo
```

Now the only thing remaining is to install the launcher

```sh
flatpak install launcher.moe com.gitlab.KRypt0n_.an-anime-game-launcher
```

## Uninstall

To uninstall the launcher including all the files run the following

```sh
flatpak uninstall --delete-data com.gitlab.KRypt0n_.an-anime-game-launcher
```

or to keep the files simply run

```sh
flatpak uninstall com.gitlab.KRypt0n_.an-anime-game-launcher
```

## Additional configuration

### Installing the game in another location

First, create some needed directories: (replace `$GAME_PATH` with where you want the game)

```sh
mkdir -p $GAME_PATH/prefix $GAME_PATH/game $GAME_PATH/temp
```

Then, grant the flatpak permission to access these paths:

```sh
flatpak override --user --filesystem=$GAME_PATH com.gitlab.KRypt0n_.an-anime-game-launcher
```

Finally, edit the launcher's config file in `~/.var/app/com.gitlab.KRypt0n_.an-anime-game-launcher/data/anime-game-launcher/config.yaml` to point to the new paths: (replace the existing `folders:` section)

```yaml
folders:
  prefix: $GAME_PATH/prefix
  game: $GAME_PATH/game
  temp: $GAME_PATH/temp
```

Then, start the launcher and install the game.

### /etc/hosts

Unlike the other packages, the flatpak does _not_ require you to edit /etc/hosts. By default, logging and the optional proxy/cdn servers are blocked. If you want to unblock the optional servers, set the `NO_BLOCK_PROXY` environment variable:

```sh
flatpak override --env=NO_BLOCK_PROXY=true com.gitlab.KRypt0n_.an-anime-game-launcher
```

### MangoHud

To use MangoHud, install the MangoHud Flatpak extension:

```sh
flatpak install flathub org.freedesktop.Platform.VulkanLayer.MangoHud
```

By default, the MangoHud configuration is stored at `~/.var/app/com.gitlab.KRypt0n_.an-anime-game-launcher/config/MangoHud/MangoHud.conf`. To use the config file from the host system instead, run this command:

```sh
flatpak override --filesystem=xdg-config/MangoHud:ro com.gitlab.KRypt0n_.an-anime-game-launcher
```

### Discord RPC

Discord RPC should work out of the box if Discord is also installed as Flatpak. Currently, non-Flatpak Discord isn't supported

### GameMode

GameMode should work out of the box. If you have MangoHud configured to show GameMode status, this won't work due to an [issue with MangoHud](https://github.com/flightlessmango/MangoHud/issues/685). As a workaround, you can run this command:

```sh
flatpak override --talk-name=com.feralinteractive.GameMode com.gitlab.KRypt0n_.an-anime-game-launcher
```
