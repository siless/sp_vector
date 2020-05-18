import json
from pathlib import Path


class VectorToJson(object):

    sp_vector = 'sp_vectors.json'

    @staticmethod
    def write_json(data: list) -> None:
        with open(str(Path(VectorToJson.sp_vector)), mode='w') as fp:
            json.dump(data, fp, indent='\t')
