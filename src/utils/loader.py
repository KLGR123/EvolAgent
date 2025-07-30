import os
import shutil
import datasets
import json
from huggingface_hub import snapshot_download


def get_zip_files(file_path: str):
    """
    Unzip a zip file and return the list of file paths.
    """
    folder_path = file_path.replace(".zip", "")
    os.makedirs(folder_path, exist_ok=True)
    shutil.unpack_archive(file_path, folder_path)
    file_paths=[]
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


def load_gaia_dataset(use_raw_dataset: bool, split: str) -> datasets.Dataset:
    """
    Load the GAIA dataset from the Hugging Face Hub.
    """
    if not os.path.exists("data/gaia"):
        if use_raw_dataset:
            snapshot_download(
                repo_id="gaia-benchmark/GAIA",
                repo_type="dataset",
                local_dir="data/gaia",
                ignore_patterns=[".gitattributes", "README.md"],
            )
        else:
            snapshot_download(
                repo_id="smolagents/GAIA-annotated",
                repo_type="dataset",
                local_dir="data/gaia",
                ignore_patterns=[".gitattributes", "README.md"],
            )

    def preprocess_file_paths(row):
        if len(row["file_name"]) > 0:
            row["file_name"] = f"data/gaia/2023/{split}/" + row["file_name"]
        return row

    eval_ds = datasets.load_dataset(
        "data/gaia/GAIA.py",
        name="2023_all",
        split=split,
        trust_remote_code=True,
        data_files={"validation": "2023/validation/metadata.jsonl", "test": "2023/test/metadata.jsonl"},
    )

    eval_ds = eval_ds.rename_columns({"Question": "question", "Final answer": "true_answer", "Level": "level"})
    eval_ds = eval_ds.map(preprocess_file_paths)
    return eval_ds 


def get_task_from_gaia(task_id: str, split: str) -> dict:
    """
    Get a task from the GAIA dataset.
    """
    ds = load_gaia_dataset(use_raw_dataset=True, split=split)
    task = None

    for record in ds.to_list():
        if record['task_id'] == task_id:
            task = record
            break

    if not task:
        print(f"Task {task_id} not found in dataset")
        raise ValueError(f"Task {task_id} not found in dataset")

    question = task["question"]

    if task["file_name"]:
        if ".zip" in task["file_name"]:
            question += " Attached local file(s): " + str(get_zip_files(task['file_name']))
        else:
            question += " Attached local file(s): " + str(task['file_name'])

    task_info = {
        "task_id": task["task_id"],
        "question": question,
        "true_answer": task["true_answer"],
        "level": task["level"],
        "file_name": task.get("file_name"),
        "steps": task.get("Annotator Metadata", {}).get("Steps"),
        "tools": task.get("Annotator Metadata", {}).get("Tools")
    }

    return task_info


def get_all_task_ids_by_level(split: str = "validation") -> list:
    """
    Get all task IDs from GAIA dataset sorted by level.
    
    Args:
        split: Dataset split to use ("validation" or "test")
        
    Returns:
        List of task IDs sorted by level (1, 2, 3)
    """
    ds = load_gaia_dataset(use_raw_dataset=True, split=split)
    
    # Get all tasks with their levels
    tasks = []
    for record in ds.to_list():
        tasks.append({
            'task_id': record['task_id'],
            'level': record['level']
        })
    
    # Sort by level, then by task_id for consistent ordering within each level
    tasks.sort(key=lambda x: (x['level'], x['task_id']))
    
    # Return just the task IDs
    return [task['task_id'] for task in tasks]


def load_coldstart_dataset(split) -> list:
    """
    Get all coldstart task IDs from GAIA dataset sorted by level.
    
    Returns:
        List of coldstart task IDs sorted by level (1, 2, 3)
    """

    data_path = f"data/coldstart/{split}.jsonl"

    with open(data_path, "r") as f:
        lines = f.readlines()
        coldstart_tasks = []
        for line in lines:
            coldstart_tasks.append(json.loads(line))
        return coldstart_tasks

def get_task_from_coldstart(task_id: str, split: str=None) -> dict:
    """
    Get a task from the GAIA dataset.
    """
    ds = load_coldstart_dataset(split)
    task = None

    for record in ds:
        if record['task_id'] == task_id:
            task = record
            break

    if not task:
        print(f"Task {task_id} not found in dataset")
        raise ValueError(f"Task {task_id} not found in dataset")

    question = task["question"]
    task_info = {
        "task_id": task["task_id"],
        "question": question,
        "true_answer": task["true_answer"],
        # "level": task["level"],
        # "file_name": task.get("file_name"),
        # "steps": task.get("Annotator Metadata", {}).get("Steps"),
        # "tools": task.get("Annotator Metadata", {}).get("Tools")
    }

    return task_info