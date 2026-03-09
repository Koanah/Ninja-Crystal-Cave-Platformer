## Ninja Crystal Cave Platformer

A fast-paced platformer game featuring a nimble ninja character navigating through crystal-filled caves while avoiding enemies.

## 🎮 Game Features

- **Ninja Character** with smooth animations (walking, jumping, idle)
- **Two Enemy Types**: Flying bats and patrolling  slimes
- **Animated Sprites**: All characters have movement and idle animations
- **Sound Effects & Music**: Jump sounds, collision effects, crystal collection, and background music
- **Main Menu**: Clickable buttons for Start, Sound/Music toggles, and Exit
- **Win/Lose Conditions**: Reach the goal or get caught by enemies
- **Score System**: Collect crystals for bonus points
- **Clean OOP Design**: Well-structured classes following Python best practices

## Controls

| Action | Key |
|--------|-----|
| Move Left/Right | LEFT/RIGHT ARROW |
| Jump | UP ARROW or SPACEBAR |
| Menu Navigation | Mouse Click |

## Prerequisites
- Pygame Zero (pgzero)
- Python 3.6+

### Installation

1. **Clone the repository into your local enviroment**
```bash
git clone 
```
2. **Install Pygame Zero**
```bash
pip install pgzero
```
3. **Run the game on your terminal instead of your regular Python compile-run**
```bash
pgzrun main.py
```
Or alternatively:
```bash
python -m pgzero main.py
```

## Project Structure:
All sprites and sounds were generated programmatically using Python (Pillow for images, wave module for audio) to ensure completely original assets.
```
Game/
├── images/     # ninja, bat, and slime sprites
└── sounds/             # Sound effects
    ├── background.wav
    ├── click.wav
    ├── collect.wav
    ├── hit.wav
    ├── jump.wav
    └── win.wav
├── .gitignore
├── Main.py     # Main game file
├── README.MD   # Game instructions
├── requirements.txt   # packages to install
  
```

## Gameplay

**Objective**: Guide your ninja to the top-right platform while avoiding enemies and collecting crystals!

- Jump from platform to platform
- Avoid flying bats that patrol horizontally
- Watch out for walking slimes on platforms
- Collect blue crystals for bonus points (10 points each)
- Reach the goal platform to win!

## License
This project is open source and available under the MIT License.

### Built With
- **Pillow (PIL) library** : For Sprite generation
- **Pygame Zero**: Simple game framework for Python
- **Python Standard Library**: 'random' for game logic

## 👨‍💻 Author
Akhona Nzimande

**Made with ❤️ and Python**
