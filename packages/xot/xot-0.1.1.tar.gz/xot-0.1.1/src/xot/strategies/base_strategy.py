from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..models.model_interface import ModelInterface
from ..tools.base_tool import BaseTool

class BaseThoughtStrategy(ABC):
    """
    Abstract base class for synthetic data types.
    """

    def __init__(self, model: ModelInterface, tools: List[BaseTool] = None):
        self.model = model
        self.tools = tools or []

    @abstractmethod
    def generate(self, question: str, solution: str, temperature: float = 0.7) -> str:
        """
        Generate synthetic data for the given question and solution.

        Args:
            question (str): Input question or task.
            solution (str): Expected solution or answer.
            temperature (float): Sampling temperature. Defaults to 0.7.

        Returns:
            str: Generated synthetic data.
        """
        pass

    @abstractmethod
    def validate(self, generated: str, solution: str, judge_model: ModelInterface = None) -> bool:
        """
        Validate the generated synthetic data against the solution.

        Args:
            generated (str): Generated synthetic data.
            solution (str): Expected solution or answer.
            judge_model (ModelInterface): Model to use for judging. Defaults to None (exact match).

        Returns:
            bool: True if the generated data is valid, False otherwise.
        """
        pass