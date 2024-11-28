class UnitTestResult(BaseTest):
    """A test result that can be used to report the result of a unit test."""
    def __init__(self, question):
        self.question = question
        # will store, a list of indivudual test case, pass/fail boolean and failure reason here.
        # might need nested objects and lists here


    # Different metrics for computation like accuracy, etc should go in here.