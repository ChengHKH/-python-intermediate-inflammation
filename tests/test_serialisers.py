from inflammation import models, serialisers

def test_patients_json_serialiser():
    patients = [
        models.Patient('Alice', [models.Observation(i, i + 1) for i in range(3)]),
        models.Patient('Bob', [models.Observation(i, 2 * i) for i in range(3)]),
    ]

    output_file = 'patients.json'
    serialisers.PatientJSONSerialiser.save(patients, output_file)
    patients_new = serialisers.PatientJSONSerialiser.load(output_file)

    for patient_new, patient in zip(patients_new, patients):
        assert patient_new.name == patient.name

        for obs_new, obs in zip(patient_new.observations, patient.observations):
            assert obs_new.day == obs.day
            assert obs_new.value == obs.value