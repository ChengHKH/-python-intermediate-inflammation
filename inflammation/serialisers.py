import json

from inflammation import models

class PatientSerialiser:
    model = models.Patient

    @classmethod
    def serialise(cls, instances):
        return [{
            'name': instance.name,
            'observations': instance.observations,
        } for instance in instances]

    @classmethod
    def deserialise(cls, data):
        return [cls.model(**d) for d in data]


class PatientJSONSerialiser(PatientSerialiser):
    @classmethod
    def save(cls, instances, path):
        with open(path, 'w') as jsonfile:
            json.dump(cls.serialise(instances), jsonfile)

    @classmethod
    def load(cls, path):
        with open(path) as jsonfile:
            data = json.load(jsonfile)

        return cls.deserialise(data)
