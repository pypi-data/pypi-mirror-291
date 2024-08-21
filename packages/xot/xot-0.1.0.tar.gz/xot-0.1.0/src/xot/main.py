import typer
from xot.language_models import OpenAIModel
from xot.strategies.cot import ChainOfThought
from xot.strategies.pot import ProgramOfThought
from xot.strategies.tir import ToolIntegratedReasoning
from xot.tools.calculator import Calculator
from xot.tools.web_search import WebSearch
from typing import List, Optional

app = typer.Typer()

@app.command()
def generate_synthetic_data(
    dataset_name: str = typer.Option(..., help="Name of the HuggingFace dataset to use"),
    output_dataset: str = typer.Option(..., help="Name of the output dataset on HuggingFace"),
    model_name: str = typer.Option("gpt-3.5-turbo", help="Name of the model to use"),
    api_key: str = typer.Option(..., help="API key for the model"),
    synthetic_type: str = typer.Option("cot", help="Type of synthetic data to generate (cot, pot, tir)"),
    temperature: float = typer.Option(0.7, help="Sampling temperature"),
    num_samples: int = typer.Option(100, help="Number of samples to generate"),
    use_tools: bool = typer.Option(False, help="Whether to use tools in generation"),
    dry_run: bool = typer.Option(False, help="Perform a dry run and show preliminary generations"),
):
    # Load dataset
    dataset = DatasetLoader.load_dataset(dataset_name)
    
    # Initialize model
    model = OpenAIModel(api_key, model_name)
    
    # Initialize tools
    tools = [Calculator(), WebSearch()] if use_tools else []
    
    # Initialize synthetic data type
    if synthetic_type == "cot":
        synthetic_generator = ChainOfThought(model, tools)
    elif synthetic_type == "pot":
        synthetic_generator = ProgramOfThought(model, tools)
    elif synthetic_type == "tir":
        synthetic_generator = TaskInstructionResponse(model, tools)
    else:
        raise ValueError(f"Unknown synthetic type: {synthetic_type}")
    
    # Generate synthetic data
    synthetic_data = []
    for i, sample in enumerate(dataset[:num_samples]):
        question = sample["question"]
        solution = sample["solution"]
        generated = synthetic_generator.generate(question, solution, temperature)
        
        if dry_run:
            print(f"Sample {i + 1}:")
            print(f"Question: {question}")
            print(f"Generated: {generated}")
            print(f"Solution: {solution}")
            print("---")
        else:
            synthetic_data.append({
                "question": question,
                "generated": generated,
                "solution": solution
            })
    
    if not dry_run:
        # Save generated dataset
        DatasetSaver.save_dataset(synthetic_data, output_dataset)
        print(f"Generated {len(synthetic_data)} samples and saved to {output_dataset}")

if __name__ == "__main__":
    app()