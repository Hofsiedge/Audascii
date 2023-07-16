This project is a WIP

Note that this project is intended to be used from a `devShell` of the nix flake due to a number of external dependencies.

If you have `nix` installed and configured to use `flakes`, you can enter a dev shell with all the dependencies with the command:
```bash
nix develop
```

I might pack the executables to be used out-of-the-box in the future, if there's any interest in the project.


It extends `audascii`'s terminal recording capability with audio recording capability.

For now, there is only Python API available (usage is shown in `src/example.py`).

The recordings can be played with HTML player (`player/player.html`).
The recording has to be put in the same directory as `player.html`.
After that, you can run any static server to serve the player.

For example,

```bash
python -m http.server --directory player 3000
```
can be used to serve the player.


To record a session, tweak the parameters in `src/example.py`, then run the file with python

```bash
python src/example.py
```


# Missing features

- Executables
- CLI
- CLI player
- A complete js player library
- Editor
