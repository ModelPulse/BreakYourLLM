def generate_tests(test_type, file):
    if test_type=="unit_test":
        from sources.models.unit_tests import UnitTests
        tests = UnitTests(file)

    tests.generate_tests()
    # tests_json = tests.json()
        