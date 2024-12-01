# "meta_data":{
#         "uuid": "1234-5678-9101-1121",
#         "name": "medllm testing",
#         "description": "This dataset contains the test cases for evaluating the responses of a medical chatbot regarding the dosing of Eliquis for DVT/PE.",
#         "run_date": "2022-01-01",
#         "run_by": "John Doe",
#         "run_time": "10:00:00",
#         "run_duration": "00:30:00"
#     }
from sources.models.common_interface import BaseTest
import uuid 

class MetaData(BaseTest):

    def __init__(self, uuid_val, name, description, run_date, run_by, run_time, run_duration):
        super().__init__()
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.run_date = run_date
        self.run_by = run_by
        self.run_time = run_time
        self.run_duration = run_duration