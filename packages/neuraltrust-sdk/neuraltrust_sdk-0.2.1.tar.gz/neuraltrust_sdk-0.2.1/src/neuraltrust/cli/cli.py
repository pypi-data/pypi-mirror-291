#!/usr/bin/env python3

import argparse
from utils.config import ConfigHelper
from utils.run_helper import RunHelper
from utils.kwparser import KeyValueAction
from interfaces.model import Model
from loaders import LoadFormat
from typing import Optional


def main():
    parser = argparse.ArgumentParser(
        prog="neuraltrust",
        description="Evaluation framework for your LLM-powered applications",
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")

    # neuraltrust init
    parser_init = subparsers.add_parser("init", help="Configure settings")
    parser_init.set_defaults(func=init)

    # neuraltrust config
    parser_config = subparsers.add_parser("config", help="Configure settings")
    parser_config.set_defaults(func=config)

    # neuraltrust list
    parser_config = subparsers.add_parser("list", help="Lists all available evals")
    parser_config.set_defaults(func=list)

    # neuraltrust run [eval_name] [kwargs]
    parser_run = subparsers.add_parser("run", help="Run an eval suite")

    # Add the 'eval_name' positional argument
    parser_run.add_argument(
        "eval_name",
        type=str,
        help="The name of the eval or eval suite to run",
    )

    # Add the 'kwargs' argument for key=value pairs
    parser_run.add_argument(
        "kwargs",
        nargs="*",
        action=KeyValueAction,
        help="Additional named arguments as key=value pairs",
    )

    # Add the '--format' optional argument
    parser_run.add_argument(
        "--model",
        type=str,
        choices=[
            Model.GPT35_TURBO.value,
            Model.GPT4.value,
            Model.GPT4_1106_PREVIEW.value,
        ],
        help="LLM model for evaluation",
    )

    # Add the '--format' optional argument
    parser_run.add_argument(
        "--format",
        type=str,
        choices=[
            LoadFormat.JSON.value,
            LoadFormat.DICT.value,
            LoadFormat.NEURALTRUST.value,
        ],
        help="Output format type",
    )

    # Add the '--filename' optional argument
    parser_run.add_argument(
        "--filename",
        type=str,
        help="Path to the file",
    )

    # Set the default function to be called
    parser_run.set_defaults(func=run_delegator)

    # Parse the arguments
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def init(args):
    """Initializes NeuralTrust and sets the necessary configuration variables"""
    config_data = ConfigHelper.load_config()

    openai_api_key = input("Enter your OpenAI API key: ")
    config_data["openai_api_key"] = openai_api_key

    neuraltrust_api_key = input("Enter your NeuralTrust API key: ")
    config_data["neuraltrust_api_key"] = neuraltrust_api_key

    config_data["llm_judge_model"] = "gpt-4o"
    config_data["llm_target_model"] = "gpt-4o"
    config_data["llm_provider"] = "openai"

    # Add other configuration prompts as needed

    ConfigHelper.save_config(config_data)
    print("Configuration updated successfully. See neuraltrust_config.yml for details.")


def config(args):
    """Prints the current configuration"""
    config_data = ConfigHelper.load_config()
    print(config_data)


def list(args):
    """Lists all available evals"""
    evals = RunHelper.all_evals()
    evals_list = "- "
    evals_list += "\n- ".join(evals)
    print(evals_list)


def run_delegator(args):
    """Delegates the run command to the appropriate function"""

    if not ConfigHelper.is_set():
        print("Please run 'neuraltrust init' to configure your API keys")
        return

    # Load the eval model
    model = ConfigHelper.load_llm_judge_model()
    if args.model is not None:
        model = args.model

    filename = args.filename if args.filename else None

    # Check if format is 'neuraltrust'
    if args.format == "neuraltrust":
        run_batch(args.eval_name, model, format="neuraltrust")
        return

    # Check if both format and filename are set
    elif args.format is not None and filename is not None:
        run_batch(args.eval_name, model, format=args.format, filename=filename)
        return

    # If format and filename are both None, call run_datapoint with kwargs
    elif args.format is None and filename is None:
        run_datapoint(args.eval_name, model, **dict(args.kwargs))
        return

    elif args.format is not None and filename is None:
        raise Exception("Filename must be specified for batch process")
        return

    else:
        raise Exception("Invalid run args")


# Define the run_batch function
def run_batch(
    eval_name: str, model: str, format: str, filename: Optional[str] = None, **kwargs
):
    # Implementation for running batch process
    try:
        print(
            f"Running batch with format={format}, model={model}, filename={filename}, kwargs={kwargs}"
        )

        RunHelper.run_eval_on_batch(
            eval_name=eval_name,
            model=model,
            format=format,
            filename=filename,
            **kwargs
        )
    except Exception as e:
        print(f"{e}")
        return


def run_datapoint(eval_name: str, model: str, **kwargs):
    """Runs a single eval on a single datapoint"""
    try:
        print(f"Running single with {eval_name} and kwargs {kwargs}")
        RunHelper.run_eval(eval_name, model, kwargs)
    except Exception as e:
        print(f"{e}")
        return


if __name__ == "__main__":
    main()