import urllib.request
import os
import zipfile

def main():
    # Open the file
    with open('data.txt', 'r') as file:
        split_file = file.read().split('\n')

    # Parse the file
    # List of arrays structured like so: [id, name, url]
    poke_data_list = []
    for file_line in split_file:
        first_space = file_line.index(' ')
        comma = file_line.index(',')
        poke_data = [
            file_line[1:first_space],
            file_line[first_space + 1:comma],
            file_line[comma + 1:]
        ]
        poke_data_list.append(poke_data)

    # Make the directory, download the zip, unzip
    path = os.getcwd() + "/pokemon/"
    i = 0
    for pokemon in poke_data_list:
        # Just for testing, this check will ensure you only download one file
        i = i + 1
        if (i > 1):
            break

        pokemon_path = path + pokemon[0]
        pokemon_filename = path + pokemon[0] + '/' + pokemon[1] + '.zip'
        # Debugging in case you want to see what you're downloading
        # print(pokemon_path)
        try:
            os.mkdir(pokemon_path)
            urllib.request.urlretrieve(pokemon[2], pokemon_filename)
            with zipfile.ZipFile(pokemon_filename, 'r') as zip_ref:
                zip_ref.extractall(pokemon_path)

        except OSError:
            print ("Creation of the directory %s failed" % path)

main()