from chrome_trex import DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN

# Create a new game that runs with at most 'fps' frames per second.
# Use fps=0 for unlimited fps.
game = DinoGame(60)

# Go to the next frame and take the action 'action'
# (ACTION_UP, ACTION_FORWARD or ACTION_DOWN).

while(not game.game_over):
    game.step(ACTION_UP)

    # Get a list of floats representing the game state
    # (positions of the obstacles and game speed).
    game.get_state()

    # Get the game score.
    game.get_score()

    # Reset the game.
game.reset()

    # Close the game.
game.close()