import os

from load import SAVE_EXT, LEVEL_EXT


class FileBase:
    def __init__(self, directory):
        self.directory = directory
        self.level_base = LevelBase(directory + "\\level")
        self.save_base = SaveBase(directory + "\\save")

    def get_levels(self):
        return self.level_base.levels

    def get_level(self, hash_code):
        return self.level_base.get_level(hash_code)

    def get_saves(self):
        return self.save_base.get_saves()

    def new_save(self, save_name):
        save = Save(save_name, self.directory + "\\save\\" + save_name + SAVE_EXT)
        self.save_base.write(save)

    def del_save(self, name):
        del self.save_base[name]


class LevelBase:
    def __init__(self, directory):
        self.directory = directory

        self.levels = list()
        for filename in os.listdir(directory):
            if filename.endswith(LEVEL_EXT):
                self.levels.append(Level(filename[0:-len(LEVEL_EXT)], directory + "\\" + filename))

    def get_levels(self):
        return self.levels

    def get_level(self, hash_code):
        for level in self.levels:
            if hash(level) == hash_code:
                return level
        return None

    def __getitem__(self, item):
        return self.levels[item]


class Level:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.map = list()
        max_len = 0

        with open(filename, mode="r", encoding="utf-8") as file:
            while True:
                line = file.readline().strip()
                if line == '':
                    break
                max_len = max(max_len, len(line))

        line = self.name
        with open(filename, mode="r", encoding="utf-8") as file:
            for line in file.readlines():
                row = list()
                for cell in line.strip():
                    line += cell
                    row.append(cell)
                if len(row) < max_len:
                    row.extend((" " for _ in range(max_len - len(row))))
                self.map.append(row)
        self.hash = hash(line)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_map(self):
        return self.map

    def __hash__(self):
        return self.hash


class SaveBase:
    def __init__(self, directory):
        self.directory = directory

        self.saves = dict()
        for filename in os.listdir(directory):
            if filename.endswith(SAVE_EXT):
                save = Save(filename[0:-len(SAVE_EXT)], directory + "\\" + filename)
                self.saves[save.name] = save

    def get_saves(self):
        return self.saves

    def __getitem__(self, item):
        return self.saves[item]

    def __delitem__(self, key):
        del self.saves[key]

    def write(self, new_save):
        self.saves[new_save.name] = new_save
        with open(new_save.filename, mode="w", encoding="utf-8") as file:
            file.write(" ".join(map(str, new_save.passed_levels)))


class Save:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                self.passed_levels = list(map(int, (num for num in file.readline().strip().split(" ") if num.isdigit())))
        except FileNotFoundError:
            self.passed_levels = list()

    def get_passed_levels(self):
        return self.passed_levels

    def new_passed_level(self, level):
        if hash(level) not in self.passed_levels:
            self.passed_levels.append(hash(level))

    def is_passed(self, level):
        return hash(level) in self.passed_levels

    def get_name(self):
        return self.name
