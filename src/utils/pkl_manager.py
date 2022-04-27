import pickle


class Pkl_Manager:
    def __init__(self) -> None:
        pass

    def read_file(path):
        with open(path, "rb") as file:
            return pickle.load(file)

    def write_file(data, path):
        with open(path, "wb") as albums_file:
            pickle.dump(data, albums_file)
            albums_file.close()


# style = 'organic'
# print(Pkl_Manager.read_file(f"src/data/by_category/{style}.pkl"))
