import time
import inspect
import neuraltrust
from errors.exceptions import NoOpenAiApiKeyException
from interfaces.model import Model
from utils.config import ConfigHelper
from utils.loader_helper import LoaderHelper
from api_keys import OpenAiApiKey, NeuralTrustApiKey

class RunHelper:
    @staticmethod
    def all_evals():
        # List to store the names of classes
        exported_classes = []

        # Iterate through each attribute in the module
        for name in dir(neuraltrust):
            # Get the attribute
            attribute = getattr(neuraltrust, name)

            # Check if the attribute is a class and is listed in __all__
            if inspect.isclass(attribute) and name in neuraltrust.__all__:
                exported_classes.append(name)

        # Return the names of the exported classes
        return exported_classes

    @staticmethod
    def get_evaluator(eval_name, **kwargs):
        """Returns an evaluator class based on the eval name"""

        # Retrieve the evaluation class based on eval_name
        eval_class = getattr(neuraltrust, eval_name, None)

        # Check if the eval class exists and is a class
        if eval_class is None or not inspect.isclass(eval_class):
            raise ValueError(f"Invalid evaluation name: {eval_name}")

        return eval_class(**kwargs)

    @staticmethod
    def validate_eval_args(eval_name, model, kwargs):
        """Validates the arguments for an eval"""

        # Check if eval_name is a valid eval
        available_evals = RunHelper.all_evals()
        if eval_name not in available_evals:
            raise ValueError(
                f"{eval_name} is not a valid eval.\n\nUse `neuraltrust list` to see all available evals."
            )

        # Check if model is in supported models
        if not Model.is_supported(model):
            raise ValueError(
                f"{model} is not a valid model.\n\nUse `neuraltrust models` to see all available models."
            )

        # Retrieve the evaluation class based on eval_name
        evaluator = RunHelper.get_evaluator(eval_name, model=model)

        # Check if the eval class exists
        if evaluator is None:
            raise ValueError(f"Invalid evaluation name: {eval_name}")

        # Retrieve the required arguments from the eval class
        required_args = evaluator.required_args

        # Check if each required argument is in kwargs
        missing_args = [arg for arg in required_args if arg not in kwargs]
        if missing_args:
            raise ValueError(
                f"Missing required arguments for {eval_name}: {', '.join(missing_args)}"
            )

        # If all required arguments are present, return True or some confirmation
        return True

    @staticmethod
    def _set_keys():
        openai_api_key = ConfigHelper.load_openai_api_key()
        if (openai_api_key is None):
            raise NoOpenAiApiKeyException
        OpenAiApiKey.set_key(openai_api_key)

        neuraltrust_api_key = ConfigHelper.load_neuraltrust_api_key()
        NeuralTrustApiKey.set_key(neuraltrust_api_key)

    @staticmethod
    def run_eval(eval_name, model, **kwargs):
        """Runs an eval and returns the results"""

        print(f"Running eval {eval_name} on {model}...\n")
        # Set the keys globally
        RunHelper._set_keys()

        # Validate the arguments for the eval
        if not RunHelper.validate_eval_args(eval_name, model, kwargs):
            # Handle invalid arguments, either by raising an exception or returning an error
            raise ValueError("Invalid arguments for the evaluation.")

        # Run the evaluation
        dataset = [kwargs]
        return RunHelper.run_eval_on_dataset(eval_name, model, dataset)

    @staticmethod
    def run_eval_on_batch(eval_name, model, format, **kwargs):
        """Runs an eval on a batch dataset and outputs results in a user-friendly format"""

        print(f"Running eval {eval_name} on {model} with format {format}...")
        # Set the keys globally
        RunHelper._set_keys()

        # Load dataset
        loader = LoaderHelper.get_loader(eval_name)()
        dataset = loader.load(format, **kwargs)
        return RunHelper.run_eval_on_dataset(eval_name, model, dataset)

    @staticmethod
    def run_eval_on_dataset(eval_name, model, dataset, **kwargs):
        # Retrieve evaluator
        evaluator = RunHelper.get_evaluator(eval_name, model=model, failure_threshold=0.5)

        # Run batch evaluation and measure time
        start = time.perf_counter()
        result = evaluator.run_batch(data=dataset, max_parallel_evals=5)
        end = time.perf_counter()
        runtime = end - start

        # Output formatting
        print(f"\nEvaluation: {eval_name}")
        print(f"Model: {model}")
        print(f"Runtime: {runtime // 60} minutes and {runtime % 60:.2f} seconds\n")

        # Error handling and output
        print("\nResults:")
        for eval_result in result.eval_results:
            pass_fail_text = "❌ FAILED" if eval_result["failure"] else "✅ PASSED"
            
            # Printing data with structured formatting
            print(f"\n{'————' * 8}")
            print(f"\nData: {eval_result['data']}\n")
            print(f"{pass_fail_text}\n")
            print(f"Reason: {eval_result['reason']}\n")
            print(f"Metrics: {eval_result['metrics']}")

        return result