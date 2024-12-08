def player(prev_play, opponent_history=[]):
    # Import necessary libraries for advanced strategy
    import random
    import numpy as np
    from collections import Counter

    # Initialize static variables if they don't exist
    if not hasattr(player, "last_ten"):
        player.last_ten = []
    if not hasattr(player, "total_plays"):
        player.total_plays = 0
    
    # Expand opponent history tracking
    opponent_history.append(prev_play)
    
    # Define strategy weights and transition matrices
    if not hasattr(player, "strategy_weights"):
        player.strategy_weights = {
            "random": 1.0,
            "cycle": 1.0,
            "frequency": 1.0,
            "anti_frequency": 1.0,
            "predict_pattern": 1.0
        }
    
    # Strategies
    def random_strategy():
        return random.choice(["R", "P", "S"])
    
    def cycle_strategy(history):
        # Cycle through R -> P -> S
        if not history:
            return "R"
        last = history[-1]
        if last == "R":
            return "P"
        elif last == "P":
            return "S"
        else:
            return "R"
    
    def frequency_strategy(history):
        # Play what beats the most frequent opponent move
        if not history:
            return "R"
        counts = Counter(history)
        most_common = counts.most_common(1)[0][0]
        beats = {"R": "P", "P": "S", "S": "R"}
        return beats[most_common]
    
    def anti_frequency_strategy(history):
        # Play what beats the least frequent opponent move
        if not history:
            return "S"
        counts = Counter(history)
        least_common = min(counts, key=counts.get)
        beats = {"R": "P", "P": "S", "S": "R"}
        return beats[least_common]
    
    def predict_pattern_strategy(history):
        # Look for repeating sequences
        if len(history) < 4:
            return random_strategy()
        
        # Try to detect and predict 3-move sequences
        sequence_length = 3
        if len(history) >= sequence_length * 2:
            recent = history[-sequence_length:]
            for i in range(len(history) - sequence_length * 2 + 1):
                potential_sequence = history[i:i+sequence_length]
                if potential_sequence == recent:
                    # Predict next move based on pattern
                    next_index = i + sequence_length
                    if next_index < len(history):
                        beats = {"R": "P", "P": "S", "S": "R"}
                        return beats[history[next_index]]
        
        return random_strategy()
    
    # Combine strategies with dynamic weighting
    strategies = [
        random_strategy(),
        cycle_strategy(opponent_history[:-1]),
        frequency_strategy(opponent_history[:-1]),
        anti_frequency_strategy(opponent_history[:-1]),
        predict_pattern_strategy(opponent_history[:-1])
    ]
    
    # Update last ten plays for adaptive learning
    if len(player.last_ten) == 10:
        player.last_ten.pop(0)
    player.last_ten.append(prev_play)
    
    # Increment total plays
    player.total_plays += 1
    
    # Final move selection with adaptive weighting
    if player.total_plays % 50 == 0:  
        player.strategy_weights = {
            key: max(0.1, weight * (random.random() * 0.4 + 0.8))
            for key, weight in player.strategy_weights.items()
        }
    
    # Weighted selection of strategies
    strategy_names = [
        "random", "cycle", "frequency", 
        "anti_frequency", "predict_pattern"
    ]
    
    weights = [
        player.strategy_weights[name] for name in strategy_names
    ]
    
    selected_strategy = random.choices(strategies, weights=weights)[0]
    
    return selected_strategy