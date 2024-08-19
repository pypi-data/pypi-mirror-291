from typing import Dict, List
from .loaders import Loader
from .evaluator import Evaluator
from .generators import generate_testset
import pandas as pd
from .utils import _generate_id
from .interfaces.data import DataPoint
from .target import complete
from croniter import croniter
import datetime
import json
from .llm.client import ChatMessage
from .testset import Testset
from .services.api_service import NeuralTrustApiService

class EvaluationSet:
    def __init__(self, id: str = None, name: str = None, description: str = None, scheduler: str = None, testset_id: str = None, create_testset: bool = False, num_questions: int = 10, knowledge_base: pd.DataFrame = None, testset_name: str = None):
        if id is None:
            if name is None or description is None:
                raise ValueError("Name and description are required when creating a new EvaluationSet")
            self.id = _generate_id(name)
            self.name = name
            self.description = description
            
            if not self._is_valid_cron(scheduler):
                raise ValueError("Invalid cron expression for scheduler")
            self.scheduler = scheduler

            self.create_testset = create_testset
            self.num_questions = num_questions
            if self.create_testset:
                if knowledge_base is None:
                    raise ValueError("Knowledge base is required when create_testset is True")
                self.knowledge_base = knowledge_base
                self.testset_id = _generate_id(testset_name or f"{name}_testset")
                self.testset_name = testset_name
            else:
                if testset_id is None:
                    raise ValueError("testset_id is required when create_testset is False")
                self.testset_id = testset_id

            self._create()
        else:
            self.id = id
            self.create_testset = create_testset
            self._load_existing_evaluation_set()
            if self.create_testset:
                if knowledge_base is None:
                    raise ValueError("Knowledge base is required when create_testset is True")
                self.knowledge_base = knowledge_base
                self.testset_id = _generate_id(testset_name or f"{name}_testset")
                self.testset_name = testset_name
                self.num_questions = num_questions
            else:
                if self.testset_id is None:
                    raise ValueError("testset_id is required when create_testset is False")
        self._update({'status': 'running'})
    def _create(self):
        """
        Creates a new evaluation set with the specified properties.
        Raises:
        - Exception: If the testset could not be created due to an error like invalid parameters, database errors, etc.
        """
        evalset_data = {
            "id": self.id,
            "name": self.name,
            "testsetId": self.testset_id,
            "status": "ready",
            "description": self.description,
            "scheduler": self.scheduler,
            "numQuestions": self.num_questions or 0,
        }

        try:
            NeuralTrustApiService.create_evaluation_set(evalset_data)
        except Exception as e:
            raise
    
    def _update(self, eval_set: Dict):
        """
        Updates an existing evaluation set with the specified properties.
        Raises:
        - Exception: If the testset could not be updated due to an error like invalid parameters, database errors, etc.
        """
        try:
            NeuralTrustApiService.update_evaluation_set(self.id, eval_set)
        except Exception as e:
            raise

    def _load_existing_evaluation_set(self):
        evalset_data = NeuralTrustApiService.load_evaluation_set(self.id)
        self.name = evalset_data.get("name")
        self.testset_id = evalset_data.get("testsetId", None)
        self.status = evalset_data.get("status")
        self.description = evalset_data.get("description")
        self.scheduler = evalset_data.get("scheduler")
        self.num_questions = evalset_data.get("numQuestions", 5)

    def _is_valid_cron(self, cron_expression: str) -> bool:
        try:
            croniter(cron_expression, datetime.datetime.now())
            return True
        except ValueError:
            return False

    def run(self, max_parallel_evals: int = 5) -> Dict:
        try:        
            if self.create_testset:
                self._generate_testset(
                    knowledge_base=self.knowledge_base, 
                    num_questions=self.num_questions, 
                    agent_description=self.description
                )
                dataset = Loader().load_json(f"/tmp/{self.testset_id}.json")
            else:
                remote_data = self._load_testset_from_neuraltrust(self.testset_id)
                if not remote_data:
                    raise ValueError(f"No data found for testset_id: {self.testset_id}")
                dataset = [DataPoint(**row) for row in remote_data]
            self._update({'testsetId': self.testset_id})
            evaluator = Evaluator(evaluation_set_id=self.id, testset_id=self.testset_id, neuraltrust_failure_threshold=0.7)
            data = [self._run_target(data) for data in dataset]

            results = evaluator.run_batch( 
                        data=data, 
                        max_parallel_evals=max_parallel_evals)
            
            self._update({'status': 'completed'})
            return results
        except Exception as e:
            self._update({'status': 'failed'})
            raise

    def _generate_testset(self, knowledge_base: pd.DataFrame, num_questions: int, agent_description: str) -> str:
        if self.knowledge_base is None:
            raise ValueError("Knowledge base is not set.")
        
        if self.testset_id is None:
            self.testset_id = _generate_id(self.testset_name or f"{self.name}_testset")
        
        testset = generate_testset(
            knowledge_base, 
            num_questions=num_questions,
            agent_description=agent_description,
        )
        
        testset.save(path=f"/tmp/{self.testset_id}.json")
        self._load_testset_to_neuraltrust(self.id, self.testset_id, testset.samples)
    
    def _run_target(self, data: DataPoint) -> DataPoint:
        context = data['context'] + "\n"+ data['query']
        conversation_history = []
        if data['conversation_history'] is not None and data['conversation_history'] != "{}":
            conversation_history = [ChatMessage(**json.loads(msg)) if isinstance(msg, str) else ChatMessage(role=msg.get('role', ''), content=msg.get('content', '')) for msg in data['conversation_history']]
        response = complete({"system_prompt": ""}, context, conversation_history)

        if response.content is None:
            raise ValueError("No content in response")
        data['response'] = response.content
        return data

    def _load_testset_from_neuraltrust(self, testset_id: str):
        try:
            return Testset.fetch_testset_rows(
                testset_id=testset_id,
                number_of_rows=20
            )
        except Exception as e:
            raise ValueError(f"Failed to load testset to NeuralTrust: {e}")

    def _load_testset_to_neuraltrust(self, id: str, testset_id: str, data: List[DataPoint]):
        try:
            Testset.create(
                id=id,
                testset_id=testset_id,
                rows=data
            )
        except Exception as e:
            raise ValueError(f"Failed to load testset to NeuralTrust: {e}")
