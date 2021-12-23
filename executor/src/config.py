# TODO - Make singleton
# TODO - Create this based on DB value
class Config:
    def __init__(self, work_dir_root="/tmp/test"):
        self.__work_dir_root = work_dir_root

    @property
    def work_dir_root(self) -> str:
        return self.__work_dir_root
