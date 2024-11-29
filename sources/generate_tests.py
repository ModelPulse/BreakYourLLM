import json

def generate_tests(test_type, file):
    if test_type=="unit_test":
        from sources.models.unit_tests import UnitTests
        tests = UnitTests(file)

    tests.generate_tests()
    tests.paraphrase()
    
    tests_json = tests.to_dict()

    with open("tests.json", 'w') as json_file:
        json.dump(tests_json, json_file, indent=4)

    return tests
    # file_path = "tests.json"
    # with open(file_path, "r") as json_file:
    #     test_data = json.load(json_file)
    #     # Need to fix: the JSON object must be str, bytes or bytearray, not dict
    #     tests = UnitTests.from_json(test_data)