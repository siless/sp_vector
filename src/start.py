import sys
from pathlib import Path

from src.converter import Converter
from src.decompress_tar import DecompressTar


def run(archive: str):
    decom = DecompressTar()
    decom.set_tarfile(Path(archive))
    decom.decompress()

    cvt = Converter()
    cvt.set_vector_data(decom.get_sp_vec())
    cvt.prepare_data_to_json()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        sys.exit("Archive is missing or too many arguments:")
