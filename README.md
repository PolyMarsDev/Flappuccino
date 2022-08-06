# Flappuccino

Flappuccino is a game created in 48 hours for the [PyGame Community New Years Jam](https://itch.io/jam/pygame-community-jam) using Python with [Pygame](https://www.pygame.org). 
## Screenshots
![](https://img.itch.zone/aW1hZ2UvODg3MDQ0LzUwMDQzOTkuZ2lm/original/vd0wHu.gif) 

## Background
Information on how to play is available on the game's [itch.io page](https://polymars.itch.io/flappuccino).

## Usage
### Releases
A Windows build of the game is available [here](https://polymars.itch.io/flappuccino).
### Running from source
Grab the latest release of Python from [here](https://www.python.org/downloads/) **and** install Pygame by executing ``pip install pygame``.

**Note:** If the ``pip install pygame`` did not work for you, then try this:
1. Windows:
``python -m pip install pygame``
2. Mac: 
``python3 -m pip install pygame``
3. Linux:
Same as windows.

Ensure ``main.py`` is in the same directory as ``./data`` and execute  ``python main.py``.

### Running from source on unix like systems

**Note:** this project was build on windows, that use codification CF-LF however unix systems uses only LF 
for run from source is necesary install dos2unix and convert the file main.py

1. Mac Os (Using homebrew)
```bash
brew install dos2unix

#after install convert 
dos2unix main.py

#run
./main.py
```

2. Linux (this may change depending of distribution)
```bash
#debian/ubuntu based distros
sudo apt install dos2unix

#arch based distros
sudo pacman -Syu dos2unix

#after install 
dos2unix main.py

#run
./main.py
```


## Contributing
Pull requests are welcome! For major refactors, please open an issue first to discuss what you would like to improve. Feel free to create a fork of this repository and use the code for any noncommercial purposes.
