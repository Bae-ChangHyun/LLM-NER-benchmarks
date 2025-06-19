import os
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Callable, Optional

import pandas as pd
import json
from loguru import logger
from pydantic import BaseModel
from tqdm import tqdm
import traceback

from utils import compatibility_checker, FrameworkCompatibilityError
from output_scheme import ResumeInfo, MaritimeAccidentReport

def response_parsing(response: Any) -> Any:
    if isinstance(response, list):
        response = {
            member.value if isinstance(member, Enum) else member for member in response
        }
    elif is_dataclass(response):
        response = asdict(response)
    elif isinstance(response, BaseModel):
        response = response.model_dump(exclude_none=True)
    return response

def experiment(
    retries: int = 10,
    expected_response: Any = None,
) -> Callable[..., tuple[list[Any], int, Optional[dict], list[list[float]]]]:
    """Decorator to run an LLM call function multiple times and return the responses

    Args:
        retries (int): Number of times to run the function
        expected_response (Any): The expected response. If provided, the decorator will calculate accurary too.

    Returns:
        Callable[..., Tuple[List[Any], int, Optional[dict], list[list[float]]]]: A function that returns a list of outputs from the function runs, percent of successful runs, metrics if expected_response is provided else None and list of latencies for each call.
    """

    def experiment_decorator(func):
        def wrapper(*args, **kwargs):
            # self 객체 (BaseFramework 인스턴스) 가져오기
            self = args[0]
            # config에서 api_delay_seconds 값을 가져오기 (없으면 0)
            api_delay_seconds = getattr(self, "api_delay_seconds", 0)

            responses, latencies = [], []
            actual_runs = 0
            success = False
            
            for i in tqdm(range(retries), leave=False):
                actual_runs = i + 1
                try:
                    start_time = time.time()
                    logger.debug(f"실험 실행 {i+1}/{retries} 시작")
                    response = func(*args, **kwargs)
                    end_time = time.time()
                    
                    logger.debug(f"Response: {str(response)[:200]}...")
                    response = response_parsing(response)

                    if "classes" in response:
                        response = response_parsing(response["classes"])

                    responses.append(response)
                    latencies.append(end_time - start_time)
                    logger.debug(f"실험 실행 {i+1}/{retries} Success (Time: {end_time - start_time:.2f}초)")
                    success = True
                    break  # 성공하면 즉시 중단
                except Exception as e:
                    logger.error(f"실험 실행 {i+1}/{retries} Failure: {str(e)}")
                    logger.error(traceback.format_exc())
                    if api_delay_seconds > 0:
                        time.sleep(api_delay_seconds)

            num_successful = len(responses)
            percent_successful = num_successful / actual_runs  # 실제 시도 횟수로 계산
            logger.info(f"총 {actual_runs}회 시도 중 {num_successful}회 성공 (성공률: {percent_successful:.2%})")
            
            return (
                responses,
                percent_successful,
                latencies,
            )

        return wrapper

    return experiment_decorator


class BaseFramework(ABC):
    prompt: str
    llm_model: str
    llm_provider: str
    base_url: str
    source_data_pickle_path: str
    sample_rows: int
    response_model: Any
    device: str
    api_delay_seconds: float  # API 요청 사이의 지연 시간(초)

    def __init__(self, *args, **kwargs) -> None:
        self.prompt = kwargs.get("prompt", "")
        self.llm_model = kwargs.get("llm_model", "gpt-3.5-turbo")
        self.llm_provider = kwargs.get("llm_provider", "openai")
        self.base_url = kwargs.get("base_url", os.environ.get("OLLAMA_HOST", ""))
        self.device = kwargs.get("device", "cpu")
        self.api_delay_seconds = kwargs.get("api_delay_seconds", 0)  # API 지연 시간 설정
        

        # Check framework compatibility with model host
        framework_name = self.__class__.__name__
        compatibility_checker.check_compatibility(framework_name, self.llm_provider)
        
        source_data_pickle_path = kwargs.get("source_data_pickle_path", "")

        # Load the data
        if source_data_pickle_path:
            self.source_data = pd.read_pickle(source_data_pickle_path)

            sample_rows = kwargs.get("sample_rows", 0)
            if sample_rows:
                self.source_data = self.source_data.sample(sample_rows)
                self.source_data = self.source_data.reset_index(drop=True)
            logger.info(f"Loaded source data from {source_data_pickle_path}")
        else:
            self.source_data = None
        
        #self.response_model = ResumeInfo
        self.response_model = MaritimeAccidentReport

    @abstractmethod
    def run(self, retries: int, expected_response: Any, *args, **kwargs): ...
