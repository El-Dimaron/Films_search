import csv
import json
import argparse

csv_file = open("films.csv", "r")
csv_list = csv.reader(csv_file)
dict_reader = csv.DictReader(csv_file)
films_dict = [row for row in dict_reader]

separator = "-" * 40

parser = argparse.ArgumentParser(description="2 execution options: search by title -t/--title [title name] or search by genre -g/--genre")
parser.add_argument("-t", "--title", nargs="+", help = "search by film title (argument [title name] is required)")
parser.add_argument("-g", "--genre", help = "search by film genre (no additional arguments required)", action="store_true", default=False)
arg = parser.parse_args()


def main():
	if arg.title:
		title_search()
	elif arg.genre:
		genre_search()
	else:
		print("Enter -h/--help to see a 'help' message.")


# noinspection PyTypeChecker
def title_search():
	user_film = " ".join(arg.title)
	user_film_search_dict = {f"{film["title"]} ({film["year"]})": film for film in films_dict if user_film.strip().casefold() in film["title"].strip().casefold()}

	if not user_film_search_dict:
		return print(separator, "No films found", sep="\n")
	elif len(user_film_search_dict) == 1:
		print(separator, "Here is info about film:\n", sep="\n")
		for film in user_film_search_dict.values():
			for key_pair in film:
				print(f"\t{key_pair}:\t{film.get(key_pair)}")
	else:
		multi_choice(user_film_search_dict)


def multi_choice(user_film_search_dict):
	film_names = [film["title"] for film in user_film_search_dict.values()]
	counter = 0

	if len(film_names) != len(set(film_names)):
		print("\nLook what we have:")
		for film in user_film_search_dict.values():
			counter += 1
			film.update({"number": counter})
			print(f"{film["number"]} \t {film["title"]} ({film["year"]})")
	else:
		for film in user_film_search_dict.values():
			counter += 1
			print(f"{counter} \t {film["title"]}")
			film.update({"number": counter})
	error_message_title = "Please choose one film to get detail info. Enter number from 1 to {}: "
	user_num = user_number(error_message_title, counter)
	for film in user_film_search_dict.values():
		if film["number"] == user_num:
			film.pop("number")
			user_film_search_dict = film
			result_display(user_film_search_dict)


def result_display(user_film_search_dict):
	print(separator, "Here is info about film:\n", sep="\n")
	for key in user_film_search_dict:
		print(f"\t{key}:\t{user_film_search_dict.get(key)}")


# noinspection PyTypeChecker
def genre_search():
	genre_dict = {}
	print("\nLook what we have:")
	for film in films_dict:
		genre_json = film["gen"].replace("\'", "\"")		# list of genres in json
		genre = json.loads(genre_json)									# list of genres in python dictionary

		for list_ in genre:
			if list_["genre"] in genre_dict:
				genre_dict[list_["genre"]].append(film["title"])
			else:
				genre_dict.update({list_["genre"]: [film["title"]]})

	counter = 0
	genre_list = []
	for genre in genre_dict:
		counter += 1
		genre_list = [genre for genre in genre_dict if genre not in genre_list]
		print(f"{counter} \t {genre} ({len(genre_dict[genre])})")

	error_message_genre = "Please enter a genre number (1 to {}) to get a films list: "
	user_num = user_number(error_message_genre, len(genre_list))
	user_genre = genre_list[user_num - 1]
	print(separator)
	print(f"Here is the list of {user_genre} films:")
	for film in genre_dict.get(user_genre):
		print(film)
	return


def user_number(error_message, max_num):
	while True:
		try:
			user_input = int(input(error_message.format(max_num)))
			if user_input < 1 or user_input > max_num:
				print(f"Please enter a number in range from 1 to {max_num}.", separator, sep="\n")
			else:
				return user_input
		except ValueError:
			print("Please be enter an integer.")


if __name__ == '__main__':
	main()
