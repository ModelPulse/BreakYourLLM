import json

def run_pipeline(file):
    from sources.models.unit_tests import UnitTests
    tests = UnitTests(file)

    import os
    # TODO: Use a central environment variable for results directory and use that variable everywhere instead of hardcoding.
    os.makedirs("results", exist_ok=True)

    #-----------------------------------------------------

    tests.generate_tests()
    print("Stage 1/5 completed - Tests generated and will be stored in results/stage1_tests.json")

    tests_json = tests.to_dict()

    with open("results/stage1_tests.json", 'w') as json_file:
        json.dump(tests_json, json_file, indent=4)

    #-----------------------------------------------------

    tests.paraphrase()
    print("Stage 2/5 completed - Paraphrases generated and will be stored in results/stage2_paraphrased_tests.json")

    paraphrased_tests_json = tests.to_dict()

    with open("results/stage2_paraphrased_tests.json", 'w') as json_file:
        json.dump(paraphrased_tests_json, json_file, indent=4)

    #-----------------------------------------------------

    #tests.execute(llm_executor)
    print("Stage 3/5 completed - LLM queries executed and will be stored in results/stage3_execution_result.json")

    execution_result_json = tests.to_dict()

    with open("results/stage3_execution_result.json", 'w') as json_file:
        json.dump(execution_result_json, json_file, indent=4)

    #-----------------------------------------------------

    #tests.evaluate_responses()
    print("Stage 4/5 completed - Paraphrases generated and will be stored in results/stage4_response_evaluation.json")

    response_evaluation_result_json = tests.to_dict()

    with open("results/stage4_response_evaluation.json", 'w') as json_file:
        json.dump(response_evaluation_result_json, json_file, indent=4)

    #-----------------------------------------------------

    #tests.evaluate_responses()
    print("Stage 5/5 completed - Metric evaluation completed and will be stored in results/stage5_metric_evaluation.json")

    # TODO: It will make sense to have a simple JSON or dict for this rather than a massive json object.
    metric_evaluation_result = tests.to_dict()

    with open("results/stage5_metric_evaluation.json", 'w') as json_file:
        json.dump(metric_evaluation_result, json_file, indent=4)

    return tests

    # Below is the the code to load the object from JSON. Adapt it according to the stage you want to load the object from.
    # file_path = "results/tests.json"
    # with open(file_path, "r") as json_file:
    #     test_data = json.load(json_file)
    #     from sources.models.unit_tests import UnitTests
    #     tests = UnitTests.from_json(test_data)