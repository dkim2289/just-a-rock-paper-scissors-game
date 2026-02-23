# just-a-rock-paper-scissors-game
It's just a rock-paper-scissors game.

## Background
I initially wanted to make something practical, something I might use in my everyday life, like a simple app that shows real-time arrival of buses 200 and 207 at stop 19531 in Melbourne CBD. But Transport Victoria OpenData's API was very difficult to get (I'm still waiting for your reply Transport Victoria!). Hence, this rock-paper-scissors game for lack of my creativity.

## Features
- Classic rock-paper-scissors game
- Hall of Fame - Leave your name if you achieve the highest win streak
- Win streak tracking with life bonuses at streak 2

## Requirements
- Python 3.6 or later
- Required packages:
  - `colorama` (for colored text)
  - `pyfiglet` (for ASCII art title)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/dkim2289/just-a-rock-paper-scissors-game.git
```

2. Navigate to the project directory
```bash
cd just-a-rock-paper-scissors-game
```

3. (Optional) Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install required packages
```bash
pip install colorama pyfiglet
```

5. Run the game
```bash
python3 main.py
```

## Note
- It was fun making it more than I thought it would be. I hope you enjoy the game!
- If you beat the record, you can share your achievement with everyone, you can fork the repository first and create a pull request with your updated hall_of_fame.json file
```bash
git add hall_of_fame.json
git commit -m "Update hall_of_fame"
git push origin main
```
