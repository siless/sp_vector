from src.vector_to_json import VectorToJson


class Converter(object):
    """Class converts the filecontent of vector files to json
    """
    __ex_eci_pos = "ECI POS (KM)"
    __ex_eci_vel = "ECI VEL (KM/S)"
    __colon = ":"

    def __init__(self):
        self.__data = None

    def set_vector_data(self, data: dict):
        self.__data = data

    def prepare_data_to_json(self):
        if isinstance(self.__data, dict):
            retval = list()
            for key, value in self.__data.items():
                retval.append(self.__dismantel_value(value))

            VectorToJson.write_json(retval)
        else:
            raise TypeError

    def __dismantel_value(self, content: list) -> dict:
        """
        Method dismantel the content of one file
        :param content: all lines of the file as a list
        :return: prepared content as list of dict´s
        """
        prep_vec_content = dict()
        # lines with only two attributes
        prep_vec_content.update(self.__line_with_two_attributes("INT. DES.", content[0]))
        prep_vec_content.update(self.__line_with_two_attributes("EPOCH REV", content[1]))
        prep_vec_content.update(self.__line_with_two_attributes("BDOT (M2/KG-S)", content[6]))
        prep_vec_content.update(self.__line_with_two_attributes("EDR(W/KG)", content[7]))
        prep_vec_content.update(self.__line_with_two_attributes("C.M. OFFSET (M)", content[8]))
        prep_vec_content.update(self.__line_with_two_attributes("IAU 1980 NUTAT", content[11]))
        prep_vec_content.update(self.__line_with_two_attributes("ERROR CONTROL", content[15]))

        # lines with one attribute
        prep_vec_content.update(self.__line_with_one_attributes(content[2]))
        prep_vec_content.update(self.__line_with_one_attributes(content[3]))
        prep_vec_content.update(self.__line_with_one_attributes(content[12]))

        # line with three attributes
        prep_vec_content.update(self.__line_with_three_attributes("DRAG", "LUNAR/SOLAR", content[4]))
        prep_vec_content.update(self.__line_with_three_attributes("SOLID EARTH TIDES", "IN-TRACK THRUST", content[5]))
        prep_vec_content.update(self.__line_with_three_attributes("UT1-UTC (S)", "UT1 RATE (MS/DAY)", content[10]))
        prep_vec_content.update(self.__line_with_three_attributes("COORD SYS", "PARTIALS", content[13]))
        prep_vec_content.update(self.__line_with_three_attributes("FIXED STEP", "STEP SIZE SELECTION", content[14]))

        # line with special values
        prep_vec_content.update(self.__line_with_special_case("F10", "AVERAGE F10", "AVERAGE AP", content[9]))

        return prep_vec_content

    def __line_with_two_attributes(self, nd_part, line) -> dict:
        """
        Method seperates the key, values and adds them to a dict
        :param line: line to prepare
        :param nd_part: second attribute to find in the line
        :return: dict
        """
        line_as_dict = dict()
        idx_sp = line.index(nd_part)  # idx_sp = index second part
        fp = (line[:idx_sp]).strip()  # fp = first part
        idx_colon = fp.index(self.__colon)

        if line.startswith("POLAR MOT"):  # this attrib has two values, therefore we store it as a list
            line_as_dict[(fp[:idx_colon]).strip()] = ((fp[idx_colon + 1:]).strip()).split()
        else:
            line_as_dict[(fp[:idx_colon]).strip()] = (fp[idx_colon + 1:]).strip()

        sp = (line[idx_sp:]).strip()  # sp = second part
        idx_colon = sp.index(self.__colon)
        line_as_dict[(sp[:idx_colon]).strip()] = (sp[idx_colon + 1:]).strip()

        return line_as_dict

    def __line_with_one_attributes(self, line) -> dict:
        """
        Method seperates the key, values and adds them to a dict
        :param line: line to prepare
        :return: dict
        """
        line_as_dict = dict()
        idx_colon = line.index(self.__colon)
        if line.startswith(self.__ex_eci_pos) or line.startswith(self.__ex_eci_vel):
            line_as_dict[(line[:idx_colon]).strip()] = ((line[idx_colon + 1:]).strip()).split()
        else:
            line_as_dict[(line[:idx_colon]).strip()] = ((line[idx_colon + 1:]).strip())

        return line_as_dict

    def __line_with_three_attributes(self, nd_part, rd_part, line) -> dict:
        """
        Method prepares line with three key-values
        :param nd_part: second key-value
        :param rd_part: third key-value
        :param line: line to prepare
        :return: dict
        """
        line_as_dict = dict()
        idx_fp = line.index(nd_part)
        idx_sp = line.index(rd_part)
        fs = (line[:idx_fp]).strip()  # fs = first slot
        ss = (line[idx_fp:idx_sp]).strip()  # ss = second slot
        ts = (line[idx_sp:]).strip()  # ts = third slot

        for slot in [fs, ss, ts]:
            line_as_dict.update(self.__line_with_one_attributes(slot))

        return line_as_dict

    def __line_with_special_case(self, nd_part, rd_part, fth_part, line) -> dict:
        """
        Method prepares the "SOLAR FLUX" line
        :param nd_part: key-value of F10
        :param rd_part: key-value of AVG F10
        :param fth_part: key-value of AVG AP
        :param line: line to prepare
        :return: dict
        """
        line_as_dict = dict()
        idx_fs = line.index(nd_part)
        idx_colon = line.index(self.__colon)
        line_as_dict[(line[:idx_colon]).strip()] = self.__line_with_three_attributes(rd_part, fth_part, (line[idx_fs:]).strip())

        return line_as_dict
