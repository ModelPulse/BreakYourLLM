import json
from sources.models.execute_tests import LLMExecutor
import time

def run_pipeline(file):
    from sources.models.unit_tests import UnitTests
    tests = UnitTests(file)

    import os
    # TODO: Use a central environment variable for results directory and use that variable everywhere instead of hardcoding.
    os.makedirs("results", exist_ok=True)
    start_time = time.time()

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

    tests.execute(LLMExecutor())
    print("Stage 3/5 completed - LLM queries executed and will be stored in results/stage3_execution_result.json")

    execution_result_json = tests.to_dict()

    with open("results/stage3_execution_result.json", 'w') as json_file:
        json.dump(execution_result_json, json_file, indent=4)

    #-----------------------------------------------------

    tests.evaluate_responses()
    print("Stage 4/5 completed - Paraphrases generated and will be stored in results/stage4_response_evaluation.json")

    response_evaluation_result_json = tests.to_dict()

    with open("results/stage4_response_evaluation.json", 'w') as json_file:
        json.dump(response_evaluation_result_json, json_file, indent=4)



    # file_path = "results/stage5_metric_evaluation.json"
    # with open(file_path, "r") as json_file:
    #     test_data = json.load(json_file)
    #     from sources.models.unit_tests import UnitTests
    #     tests = UnitTests.from_json(test_data)
    # print(tests[0].question)

    #----------------------------------------------------- Stage 5

    result_array = tests.get_evaluation_result_as_numpy()
    from sources.metrics.accuracy import Accuracy
    from sources.metrics.general_stats import GeneralStats
    from sources.metrics.hallucination_rate import HallucinationRate
    from sources.metrics.llm_drift_rate import LLMDriftRate

    metrics = [Accuracy(), GeneralStats(), HallucinationRate(), LLMDriftRate()]
    for metric in metrics:
        metric.get_metric_value(result_array)
        tests.metrics.append(metric)
    print("Stage 5/5 completed - Metric evaluation completed and will be stored in results/stage5_metric_evaluation.json")

    # #----------------------------------------------------- Metadata creation

    end_time = time.time()
    execution_time = end_time - start_time
    execution_time = time.strftime('%H:%M:%S', time.gmtime(execution_time))

    from datetime import date, datetime
    # Get today's date
    today = date.today()

    now = datetime.now()
    # Extract and format the time
    current_time = now.strftime("%H:%M:%S")  # Format: HH:MM:SS


    from sources.models.metadata import MetaData
    metadata = MetaData(
        None, "medLLM", "This dataset contains the test cases for evaluating the responses of a medical chatbot regarding the dosing of Eliquis for DVT/PE",
        str(today), "John Doe", str(current_time), str(execution_time)
    )

    tests.metadata = metadata

    #----------------------------------------------------- Stage 5 JSON saving

    print("Stage 5 - Saving with Metadata")

    # TODO: It will make sense to have a simple JSON or dict for this rather than a massive json object.
    metric_evaluation_result = tests.to_dict()

    with open("results/stage5_metric_evaluation.json", 'w') as json_file:
        json.dump(metric_evaluation_result, json_file, indent=4)


    return tests

    # Below is the the code to load the object from JSON. Adapt it according to the stage you want to load the object from.
    # file_path = "results/stage5_metric_evaluation.json"
    # with open(file_path, "r") as json_file:
    #     test_data = json.load(json_file)
    #     from sources.models.unit_tests import UnitTests
    #     tests = UnitTests.from_json(test_data)