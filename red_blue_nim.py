#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

# Evaluation function to evaluate the state of the game
def evaluate_state(red_marbles, blue_marbles, version_type):
    red_score = 2 * red_marbles
    blue_score = 3 * blue_marbles
    if version_type == "misere":
        return red_score + blue_score
    else:
        return -(red_score + blue_score)

# This method is to get possible moves of the game
def get_possible_moves(red_marbles, blue_marbles):
    moves = []
    if red_marbles >= 2:
        moves.append(("red", 2))
    if blue_marbles >= 2:
        moves.append(("blue", 2))
    if red_marbles >= 1:
        moves.append(("red", 1))
    if blue_marbles >= 1:
        moves.append(("blue", 1))
    return moves
  
# This method is to get the best move for the computer player
def get_best_move(red_marbles, blue_marbles, version_type, depth):
    best_move = None
    best_eval = float('-inf') if version_type == 'standard' else float('inf')
    alpha_value = float('-inf')
    beta_value = float('inf')

    for i in range(1, 3):
        for color in ['red', 'blue']:
            if color == 'red' and red_marbles >= i:
                eval = minimax_pruning(red_marbles - i, blue_marbles, depth, False, alpha_value, beta_value, version_type)
            elif color == 'blue' and blue_marbles >= i:
                eval = minimax_pruning(red_marbles, blue_marbles - i, depth, False, alpha_value, beta_value, version_type)

            if (version_type == 'standard' and eval > best_eval) or (version_type == 'misere' and eval < best_eval):
                best_eval = eval
                best_move = (color, i)

    return best_move  

# Minimax algorithm with alpha-beta pruning
def minimax_pruning(red_marbles, blue_marbles, depth, maximizing_player, alpha_value, beta_value, version_type):
    if red_marbles == 0 or blue_marbles == 0:
        return evaluate_state(red_marbles, blue_marbles, version_type)

    if depth == 0:
        return 0 
     
    if maximizing_player:
        max_eval = float("-inf")
        for move in get_possible_moves(red_marbles, blue_marbles):
            pile, num_marbles = move
            if pile == "red":
                new_red = red_marbles - num_marbles
                new_blue = blue_marbles
            else:
                new_red = red_marbles
                new_blue = blue_marbles - num_marbles
            # This will recursively evaluate the next state
            eval = minimax_pruning(new_red, new_blue, depth - 1, False, alpha_value, beta_value, version_type)
            max_eval = max(max_eval, eval)
            alpha_value = max(alpha_value, eval)
            # This will perform alpha-beta pruning
            if beta_value <= alpha_value:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(red_marbles, blue_marbles):
            pile, num_marbles = move
            if pile == "red":
                new_red = red_marbles - num_marbles
                new_blue = blue_marbles
            else:
                new_red = red_marbles
                new_blue = blue_marbles - num_marbles
            # This will recursively evaluate the next state
            eval = minimax_pruning(new_red, new_blue, depth - 1, True, alpha_value, beta_value, version_type)
            min_eval = min(min_eval, eval)
            beta_value = min(beta_value, eval)
            # This will perform alpha-beta pruning
            if beta_value <= alpha_value:
                break
        return min_eval

# This is the Main function to control the game flow
def main():
    if len(sys.argv) < 3:
        print("Usage: red_blue_nim.py <num-red> <num-blue> <version> [<first-player> <depth>]")
        sys.exit(1)

    red_marbles = int(sys.argv[1])
    blue_marbles = int(sys.argv[2])
    version_type = 'standard' if len(sys.argv) < 4 else sys.argv[3]
    first_player = 'computer' if len(sys.argv) < 5 else sys.argv[4]
    depth = 3 if len(sys.argv) < 6 else int(sys.argv[5])

    while red_marbles > 0 and blue_marbles > 0:
        if first_player == 'computer':
            move = get_best_move(red_marbles, blue_marbles, version_type, depth)
            color, amount = move
            print(f"Computer picks {amount} {color} marble(s)")
            if color == 'red':
                red_marbles -= amount
            else:
                blue_marbles -= amount

        else:
            print(f"Remaining marbles - Red: {red_marbles}, Blue: {blue_marbles}")
            while True:
                try:
                    color = input("Your turn: Choose a color (red/blue): ").lower()
                    amount = int(input("Choose number of marbles (1/2): "))
                    if color not in ['red', 'blue'] or amount not in [1, 2]:
                        raise ValueError
                    if (color == 'red' and amount > red_marbles) or (color == 'blue' and amount > blue_marbles):
                        raise ValueError("Invalid move, not enough marbles!")
                    break
                except ValueError as e:
                    print("Invalid input. Please try again.", e)
            if color == 'red':
                red_marbles -= amount
            else:
                blue_marbles -= amount

        first_player = 'computer' if first_player == 'human' else 'human'

    print("Game over!")
    score = evaluate_state(red_marbles, blue_marbles, version_type)
    if version_type == "standard":
        if first_player == 'computer':
            print("Computer wins!")
            print("Human loses with a score of", abs(score))
        else:
            print("Human wins!")
            print("Computer loses with a score of", abs(score))   
    elif version_type == "misere":
        if first_player == 'computer':
            print("Human wins with a score of", score)
            print("Computer loses!")
        else:
            print("Computer wins with a score of", score)
            print("Human loses!")
        

if __name__ == "__main__":
    main()

