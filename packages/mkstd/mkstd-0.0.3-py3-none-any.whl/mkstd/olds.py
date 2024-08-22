from pydantic import BaseModel, Field


import .formats.xml as xml


class Standard:
    """Create standards from a pydantic model.

    Attrs:
        model:
            The pydantic model.
    """

    def __init__(self, model: BaseModel):
        self.model = model

    def to_hdf5(self, filename: str):
        data = dict(self.model)
        hdfdict.dump(data, filename)

    @staticmethod
    def from_hdf5(filename: str):
        data = hdfdict.load(filename)
        return SSRData.parse_obj(data)

    def to_json(self, filename: str):
        data = self.model.model_dump_json(indent=2)
        with open(filename, 'w') as f:
            f.write(data)

    @staticmethod
    def from_json(filename: str):
        with open(filename, 'r') as f:
            data = f.read()
        return SSRData.model_validate_json(data)

    def to_yaml(self, filename: str):
        data = pydantic_yaml.to_yaml_str(self.model)
        with open(filename, 'w') as f:
            f.write(data)

    @staticmethod
    def from_yaml(filename: str):
        with open(filename, 'r') as f:
            data = f.read()
        return pydantic_yaml.parse_yaml_raw_as(SSRData, data)

    def to_xml(self, filename: str):
        data = pydantic_xmlmodel.model_dump_xml(self.model)
        with open(filename, 'w') as f:
            f.write(data)

    @staticmethod
    def from_xml(filename: str):
        with open(filename, 'r') as f:
            data = f.read()
        return pydantic_xmlmodel.model_validate_xml(SSRData, data)
