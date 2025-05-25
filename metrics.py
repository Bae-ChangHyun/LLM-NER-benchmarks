import itertools
import json
import numpy as np
import pandas as pd
from deepdiff import DeepDiff
from loguru import logger


def format_framework_name(framework_name, model_host=None):
    """프레임워크 이름과 모델 이름을 포맷팅하는 함수.
    
    Args:
        framework_name (str): '프레임워크_모델이름' 형식의 문자열
        model_host (str, optional): 모델 패밀리 이름
        
    Returns:
        tuple: (프레임워크 이름, 모델 이름) 형식의 튜플
    """
    if '_' in framework_name:
        # 첫 번째 _ 를 기준으로 프레임워크 이름과 모델 이름 분리
        parts = framework_name.split('_', 1)
        framework = parts[0].replace("Framework", "")
        model = parts[1]
        return framework, model
    else:
        return framework_name.replace("Framework", ""), "unknown"


def reliability_metric(percent_successful: dict[str, list[float]], model_hosts=None):
    """신뢰성 지표를 계산하는 함수.
    
    Args:
        percent_successful (dict): 프레임워크별 실행 성공률
        model_hosts (dict, optional): 모델 호스트 정보
        
    Returns:
        pd.DataFrame: 신뢰성 지표가 포함된 데이터프레임
    """
    # 프레임워크와 모델 이름 분리
    frameworks = []
    models = []
    reliabilities = []
    
    if model_hosts is None:
        model_hosts = {}
    
    for key, values in percent_successful.items():
        framework, model = format_framework_name(key)
        
        # 모델 패밀리 정보가 있으면 추가
        model_host = model_hosts.get(key, {}).get("host", "")
        if model_host:
            model_display = f"{model}({model_host})"
        else:
            model_display = model
            
        frameworks.append(framework)
        models.append(model_display)
        # 빈 배열 체크 추가
        if len(values) > 0:
            reliabilities.append(values[0])
        else:
            reliabilities.append(0.0)  # 빈 배열인 경우 0으로 처리
    
    # 데이터프레임 생성 (프레임워크와 모델을 별도 컬럼으로)
    reliability_df = pd.DataFrame({
        "Framework": frameworks,
        "Model(host)": models,
        "reliability": reliabilities
    })
    
    reliability_df = reliability_df.round(3)
    reliability_df = reliability_df.sort_values(by="reliability", ascending=False)
    return reliability_df


def latency_metric(latencies: dict[str, list[float]],model_hosts=None):
    """지연 시간 지표를 계산하는 함수.
    
    Args:
        latencies (dict): 프레임워크별 지연 시간 목록
        model_hosts (dict, optional): 모델 호스트 정보
        
    Returns:
        pd.DataFrame: 지연 시간 지표가 포함된 데이터프레임
    """
    # Flatten the list of latencies
    latencies = {
        key: list(itertools.chain.from_iterable(value))
        for key, value in latencies.items()
    }

    # 프레임워크와 모델 이름 분리하고 백분위 계산
    frameworks = []
    models = []
    latency_values = []
    
    if model_hosts is None:
        model_hosts = {}
    
    for key, values in latencies.items():
        framework, model = format_framework_name(key)
        
        # 모델 패밀리 정보가 있으면 추가
        model_host = model_hosts.get(key, {}).get("host", "unknown")

        model_display = f"{model}({model_host})"
            
        frameworks.append(framework)
        models.append(model_display)
        # 빈 배열 체크 추가
        if len(values) > 0:
            latency_values.append(np.mean(values))  # 평균 지연 시간 계산
        else:
            latency_values.append(0.0)  # 빈 배열인 경우 0으로 처리
    
    # 데이터프레임 생성 (프레임워크와 모델을 별도 컬럼으로)
    latency_df = pd.DataFrame({
        "Framework": frameworks,
        "Model(host)": models,
        "Latency(s)": latency_values
    })
    
    latency_df = latency_df.round(3)
    latency_df = latency_df.sort_values(by="Latency(s)", ascending=True)
    return latency_df


def flatten_json_to_set(data, prefix=""):
    """JSON 구조를 평면화하여 비교 가능한 문자열 집합으로 변환합니다.
    완전히 동일한 값만 일치로 간주합니다.
    
    Args:
        data: JSON 형태의 데이터 (dict, list, 또는 primitive type)
        prefix: 현재 키의 접두사
        
    Returns:
        set: 평면화된 키-값 쌍들의 집합
    """
    result = set()
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if value is not None:  # None 값은 제외
                result.update(flatten_json_to_set(value, new_prefix))
    elif isinstance(data, list):
        # 리스트의 경우 인덱스를 포함하여 완전히 동일한 항목만 일치할 수 있게 함
        for i, item in enumerate(data):
            new_prefix = f"{prefix}[{i}]"
            if item is not None:  # None 값은 제외
                result.update(flatten_json_to_set(item, new_prefix))
    else:
        # primitive type (str, int, float, bool)
        if data is not None and data != "":  # None과 빈 문자열 제외
            # 완전한 문자열 일치를 위해 값을 문자열로 변환
            result.add(f"{prefix}={str(data)}")
    
    return result


def calculate_json_metrics(pred_json, truth_json):
    """두 JSON 구조를 비교하여 TP, FP, FN을 계산합니다.
    완전히 동일한 값만 일치로 간주합니다.
    
    Args:
        pred_json: 예측된 JSON 데이터
        truth_json: 실제 정답 JSON 데이터
        
    Returns:
        tuple: (true_positives, false_positives, false_negatives)
    """
    pred_set = flatten_json_to_set(pred_json)
    truth_set = flatten_json_to_set(truth_json)
    
    # True Positives: 예측과 실제가 일치하는 항목
    true_positives = len(pred_set.intersection(truth_set))
    
    # False Positives: 예측은 했지만 실제론 없는 항목
    false_positives = len(pred_set - truth_set)
    
    # False Negatives: 예측하지 못한 실제 항목
    false_negatives = len(truth_set - pred_set)
    
    return true_positives, false_positives, false_negatives


def ner_micro_metrics(results: dict[str, dict], ground_truths=None):
    """NER 작업에 대한 마이크로 평가 지표를 계산합니다.
    
    Args:
        results (dict): 프레임워크별 예측 결과가 포함된 딕셔너리
        ground_truths (list, optional): 정답 데이터. None인 경우 results에 저장된 metrics 사용
        
    Returns:
        pd.DataFrame: 마이크로 정밀도, 재현율, F1 점수가 포함된 데이터프레임
    """
    micro_metrics = {
            "Framework": [],
            "Model(host)": [],
            "distance": [],
            "precision": [],
            "recall": [],
            "f1": []
        }
    
    for framework, values in results.items():
        tp_total, fp_total, fn_total = 0, 0, 0
        predictions = values["predictions"]
        
        # predictions가 비어 있는지 확인
        if not predictions or not ground_truths:
            # 빈 예측 결과 처리
            framework_name, model_name = format_framework_name(framework)
            model_host = values.get("llm_provider", values.get("llm_model_host", "unknown"))
            model_display = f"{model_name}({model_host})"
            
            micro_metrics["Framework"].append(framework_name)
            micro_metrics["Model(host)"].append(model_display)
            micro_metrics["distance"].append(1.0)
            micro_metrics["precision"].append(0.0)
            micro_metrics["recall"].append(0.0)
            micro_metrics["f1"].append(0.0)
            continue
        # 각 예측마다 true positives, false positives, false negatives 계산
        for i, pred_runs in enumerate(predictions):
            # i가 ground_truths의 범위를 벗어나지 않는지 확인
            if i >= len(ground_truths):
                continue
                
            truth = ground_truths[i]

            with open(truth, 'r') as f:
                truth = json.load(f)
            
            # 각 실행마다 집계
            for pred in pred_runs:
                # JSON 구조를 직접 비교
                tp, fp, fn = calculate_json_metrics(pred, truth)
                tp_total += tp
                fp_total += fp
                fn_total += fn
                
                diff = DeepDiff(truth, pred, ignore_order=True, get_deep_distance=True)


        # 정밀도, 재현율, F1 계산
        precision = tp_total / (tp_total + fp_total) if (tp_total + fp_total) > 0 else 0
        recall = tp_total / (tp_total + fn_total) if (tp_total + fn_total) > 0 else 0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        # 프레임워크 이름과 모델 이름 분리
        framework_name, model_name = format_framework_name(framework)
        
        # 모델 패밀리 정보가 있으면 추가
        model_host = values.get("llm_provider",  values.get("llm_model_host", "unknown"))
        model_display = f"{model_name}({model_host})"
        
        micro_metrics["Framework"].append(framework_name)
        micro_metrics["Model(host)"].append(model_display)
        micro_metrics["distance"].append(diff['deep_distance'])
        micro_metrics["precision"].append(precision)
        micro_metrics["recall"].append(recall)
        micro_metrics["f1"].append(f1)

    return pd.DataFrame(micro_metrics)


def combined_metrics(results: dict[str, dict], ground_truths=None, sort_by: str = "distance"):
    """모든 평가 지표(정밀도, 재현율, F1, 신뢰성, 지연 시간)를 하나의 표로 통합합니다.
    
    Args:
        results (dict): 프레임워크별 예측 결과가 포함된 딕셔너리
        ground_truths (list, optional): 정답 데이터. None인 경우 results에 저장된 metrics 사용
        percentile (int, optional): 지연 시간 백분위 기준. 기본값은 95
        sort_by (str, optional): 정렬 기준 ('f1', 'recall', 'precision', 'reliability', 'latency' 중 하나). 기본값은 'f1'
        
    Returns:
        pd.DataFrame: 모든 지표가 포함된 데이터프레임
    """
    # 결과가 비어있는지 확인
    if not results:
        return pd.DataFrame(columns=["Framework", "Model(host)", "distance","precision", "recall", 
                                   "f1", "reliability", "Latency"])
    
    # ground_truths가 None인지 확인
    if ground_truths is None:
        # 여기서 ground_truths가 필요한 경우의 처리
        ground_truths = []
    
    # 데이터 준비
    percent_successful = {
        framework: value.get("percent_successful", [])
        for framework, value in results.items()
    }
    
    latencies = {
        framework: value.get("latencies", [])
        for framework, value in results.items()
    }
    
    # 모델 호스트 정보 추출
    model_hosts = {}
    for framework, value in results.items():
        model_hosts[framework] = {
            "model": value.get("llm_model", "unknown"),
            "host": value.get("llm_provider", value.get("llm_model_host", "unknown"))
        }
    
    try:
        # 각 지표 계산
        json_df = ner_micro_metrics(results, ground_truths)
        reliability_df = reliability_metric(percent_successful, model_hosts)
        latency_df = latency_metric(latencies, model_hosts)
        
        # 데이터프레임이 비어있는지 확인
        if json_df.empty or reliability_df.empty or latency_df.empty:
            logger.warning("하나 이상의 지표 데이터프레임이 비어 있습니다.")
        
        # 데이터프레임 병합
        combined_df = json_df.merge(
            reliability_df, on=["Framework", "Model(host)"], how="outer"
        ).merge(
            latency_df, on=["Framework", "Model(host)"], how="outer"
        )
        combined_df = combined_df.fillna(0)

        if sort_by in combined_df.columns:
            # 지연 시간은 낮을수록 좋으므로 오름차순 정렬, 나머지는 내림차순 정렬
            ascending = (sort_by in ["distance","Latency"])
            combined_df = combined_df.sort_values(by=sort_by, ascending=ascending)
            cols = list(combined_df.columns)
            remaining_cols = [col for col in cols if col not in ["Framework", "Model(host)", sort_by]]
            new_cols = ["Framework", "Model(host)", sort_by] + remaining_cols
            combined_df = combined_df[new_cols]
        else:
            logger.warning(f"정렬 컬럼 '{sort_by}'이 데이터프레임에 존재하지 않습니다.")
        
        # 인덱스 재설정 (인덱스를 순차적으로 새로 부여하고 인덱스 컬럼 제거)
        combined_df = combined_df.reset_index(drop=True)
        
        return combined_df
    
    except Exception as e:
        logger.error(f"combined_metrics 함수 실행 중 오류 발생: {e}")
        # 오류 발생시 빈 데이터프레임 반환
        return pd.DataFrame(columns=["Framework", "Model(host)", "precision", "recall", 
                                   "f1", "reliability", "Latency"])
