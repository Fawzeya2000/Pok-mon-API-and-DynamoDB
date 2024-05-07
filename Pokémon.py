
```python
import random
import requests
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PokemonCollection')

def get_random_pokemon():
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url)
    pokemons = response.json()['results']
    random_pokemon = random.choice(pokemons)['name']
    return random_pokemon

def download_pokemon_details(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)
    return response.json()

def check_pokemon_in_db(pokemon_name):
    response = table.get_item(Key={'PokemonName': pokemon_name})
    return 'Item' in response

def save_pokemon_to_db(pokemon_details):
    response = table.put_item(Item=pokemon_details)
    return response

def main():
    while True:
        user_input = input("Would you like to draw a Pokémon? (yes/no): ")
        if user_input.lower() == 'yes':
            pokemon_name = get_random_pokemon()
            if check_pokemon_in_db(pokemon_name):
                pokemon_details = download_pokemon_details(pokemon_name)
                print("Pokemon details:")
                print(pokemon_details)
                print("This Pokemon is already in our database!")
            else:
                pokemon_details = download_pokemon_details(pokemon_name)
                save_pokemon_to_db(pokemon_details)
                print("Pokemon details:")
                print(pokemon_details)
                print("Pokemon saved to the database.")
        else:
            print("Farewell! Exiting the program.")
            break

if __name__ == "__main__":
    main()

