import tarfile
from pathlib import Path


class DecompressTar(object):
    """Class manages and handels the tar-archive.
    Attributes:
    untar -- relative Path after decompression
    """
    untar = "mnt/scratch/SP_VEC"

    def __init__(self):
        """Constructor"""
        self.__tarfile = None

    def decompress(self):
        """Method decompresses a tarfile to current dir
        :return: None
        """
        if self.__tarfile is not None and tarfile.is_tarfile(self.__tarfile):
            with tarfile.open(self.__tarfile, mode='r:*') as tf:
                tf.extractall()
        else:
            raise FileNotFoundError('File not found or no tarfile')

    def set_tarfile(self, file: Path) -> None:
        """Set the filename of the tarfile
        :param file: file
        :return: None
        """
        if isinstance(file, Path):
            self.__tarfile = file
        else:
            self.__tarfile = Path(file)

    @classmethod
    def get_sp_vec(cls) -> dict:
        """Method reads file content and generates a dict with filename as key
        :return: dict
        """
        if Path(DecompressTar.untar).exists():
            sat_id = dict()
            for noradid in Path(DecompressTar.untar).iterdir():
                for f in Path(noradid).iterdir():
                    with open(str(f)) as vec:
                        sat_id[f.stem] = vec.readlines()[:-1]
            return sat_id
