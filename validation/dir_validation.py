import os

class ValidDir:

    def path_exists(directory, path):
            if not os.path.exists(path+directory):
                os.makedirs(path+directory)
            return path+directory
