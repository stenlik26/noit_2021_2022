# TODO - Make singleton
# TODO - Create this based on DB value
class Config:
    def __init__(self):
        self.__work_dir_root = "/tmp/code"

    @property
    def work_dir_root(self) -> str:
        return self.__work_dir_root
