from abc import ABC
import json

from inflammation import models


class Serialiser(ABC):
    @classmethod
    def serialise(cls, instances):
        raise NotImplementedError

    @classmethod
    def save(cls, instances):
        raise NotImplementedError
    
    @classmethod
    def deserialise(cls, instances):
        raise NotImplementedError
    
    @classmethod
    def load(cls, instances):
        raise NotImplementedError


class ObservationSerialiser(Serialiser):
    model = models.Observation

    @classmethod
    def serialise(cls, instances):
        return [{
            'day': instance.day,
            'value': instance.value,
        } for instance in instances]

    @classmethod
    def deserialise(cls, data):
        return [cls.model(**d) for d in data]


class PatientSerialiser:
    model = models.Patient

    @classmethod
    def serialise(cls, instances):
        return [{
            'name': instance.name,
            'observations': ObservationSerialiser.serialise(instance.observations),
        } for instance in instances]

    @classmethod
    def deserialise(cls, data):
        instances = []

        for item in data:
            item['observations'] = ObservationSerialiser.deserialise(item.pop('observations'))
            instances.append(cls.model(**item))

        return instances


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
