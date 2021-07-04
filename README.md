# Dino Game AI #
## Game ##
The game itself was developed with the Pygame module
```bash
pip install pygame
```
You can also play it yourself by making the dino jump with the space bar.

## AI ##
The AI was programmed using the neat module.
```bash
pip install neat-python
```
The neural network has two inputs, the y-coordinate of the dino and the x-coordinate of the next cactus, and one output, whether the dinosaur should jump or not.

Settings of the AI can be changed in the [configuration file](https://github.com/kilian-kier/Dino-Game-AI/blob/master/neat-config.txt), e.g. how many dinos are trained per generation.

With how many generations the AI trains can be changed in the start menu by entering the desired number.

[ai-example.pkl](https://github.com/kilian-kier/Dino-Game-AI/blob/master/ai-example.pkl) is a neural network that was trained with 100 generations. Rename it to ai.pkl so that the AI can play with it again
