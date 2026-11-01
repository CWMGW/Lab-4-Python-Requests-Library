import json
import logging
import requests

logging.basicConfig(filename='logs/lab4.log', level=logging.INFO)

def rank_to_value(card_value):
    mapping = {'JACK': 11, 'QUEEN': 12, 'KING': 13, 'ACE': 14}
    if card_value in mapping:
        return mapping[card_value]
    try:
        return int(card_value)
    except ValueError:
        return 0

def main():
    try:
        # Create deck
        deck_resp = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1', timeout=10)
        deck_data = deck_resp.json()
        deck_id = deck_data['deck_id']
        logging.info("LAB4_DECK_CREATE_OK")
        
        # Get player count
        try:
            num_players = int(input("Enter number of players (>= 2): "))
            if num_players < 2:
                raise ValueError
        except ValueError:
            logging.error("LAB4_ERR")
            print("Invalid player count.")
            return

        players = [f"Player {i+1}" for i in range(num_players)]
        active_players = players.copy()
        
        rounds_history = []
        round_num = 1
        winner = None

        while not winner:
            draw_resp = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={len(active_players)}', timeout=10)
            draw_data = draw_resp.json()
            logging.info("LAB4_DRAW_OK")
            
            round_results = {}
            max_val = -1
            
            for idx, player in enumerate(active_players):
                card = draw_data['cards'][idx]
                val = rank_to_value(card['value'])
                round_results[player] = {'card': f"{card['value']} of {card['suit']}", 'value': val}
                if val > max_val:
                    max_val = val
            
            # Find tied top players
            top_players = [p for p, data in round_results.items() if data['value'] == max_val]
            
            rounds_history.append({
                "round": round_num,
                "results": round_results,
                "top_players": top_players
            })
            
            if len(top_players) == 1:
                winner = top_players[0]
            else:
                logging.info("LAB4_TIE_ROUND")
                active_players = top_players
                round_num += 1

        # Save results
        summary = f"Final Winner: {winner}\nTotal Rounds: {round_num}\n"
        with open("data/high_card_result.txt", "w") as f:
            f.write(summary)
            
        with open("data/high_card_rounds.json", "w") as f:
            json.dump(rounds_history, f, indent=4)
            
        logging.info("LAB4_GAME_END")
        print(f"Game over! Winner: {winner}")

    except requests.RequestException:
        logging.error("LAB4_ERR")
        print("Network error occurred during high card game.")

if __name__ == "__main__":
    main()