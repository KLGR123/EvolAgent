import sys
import time

from src.utils.scorer import question_scorer, check_close_call
from src.utils.loader import get_task_from_gaia
from src.pipelines import EvolvePipeline


TASK_ID_LIST = [
    "0512426f-4d28-49f0-be77-06d05daec096",
    "05407167-39ec-4d3a-a234-73a9120c325d",
    "17b5a6a3-bc87-42e8-b0fb-6ab0781ef2cc",
    "23dd907f-1261-4488-b21c-e9185af91d5e",
    "2b3ef98c-cc05-450b-a719-711aee40ac65",
    "2dfc4c37-fec1-4518-84a7-10095d30ad75",
    "42576abe-0deb-4869-8c63-225c2d75a95a",
    "4fc2f1ae-8625-45b5-ab34-ad4433bc21f8",
    "56137764-b4e0-45b8-9c52-1866420c3df5",
    "5d0080cb-90d7-4712-bc33-848150e917d3",
    "65afbc8a-89ca-4ad5-8d62-355bb401f61d",
    "676e5e31-a554-4acc-9286-b60d90a92d26",
    "6b078778-0b90-464d-83f6-59511c811b01",
    "7619a514-5fa8-43ef-9143-83b66a43d7a4",
    "7b5377b0-3f38-4103-8ad2-90fe89864c04",
    "851e570a-e3de-4d84-bcfa-cc85578baa59",
    "9d191bce-651d-4746-be2d-7ef8ecadb9c2",
    "a0068077-79f4-461a-adfe-75c1a4148545",
    "a1e91b78-d3d8-4675-bb8d-62741b4b68a6",
    "a56f1527-3abf-41d6-91f8-7296d6336c3f",
    "b816bfce-3d80-4913-a07d-69b752ce6377",
    "c3a79cfe-8206-451f-aca8-3fec8ebe51d3",
    "cabe07ed-9eca-40ea-8ead-410ef5e83f91",
    "da52d699-e8d2-4dc5-9191-a2199e0b6a9b",
    "db4fd70a-2d37-40ea-873f-9433dc5e301f",
    "de9887f5-ead8-4727-876f-5a4078f8598c",
    "ded28325-3447-4c56-860f-e497d6fb3577",
    "ed58682d-bc52-4baa-9eb0-4eb81e1edacc",
    "edd4d4f2-1a58-45c4-b038-67337af4e029",
    "2a649bb1-795f-4a01-b3be-9a01868dae73",
    "3cef3a44-215e-4aed-8e3b-b1e3f08063b7",
    "5b2a14e8-6e59-479c-80e3-4696e8980152",
    "71345b0a-9c7d-4b50-b2bf-937ec5879845",
    "840bfca7-4f7b-481a-8794-c560c340185d",
    "c61d22de-5f6c-4958-a7f6-5e9707bd3466",
    "d1af70ea-a9a4-421a-b9cc-94b5e02f1788",
    "e1fc63a2-da7a-432f-be78-7c4a95598703",
    "e29834fd-413a-455c-a33e-c3915b07401c",
    "f3917a3d-1d17-4ee2-90c5-683b072218fe",
    "f46b4380-207e-4434-820b-f32ce04ae2a4",
    "08cae58d-4084-4616-b6dd-dd6534e4825b",
    "0bb3b44a-ede5-4db5-a520-4e844b0079c5",
    "114d5fd0-e2ae-4b6d-a65a-870da2d19c08",
    "1dcc160f-c187-48c2-b68e-319bd4354f3d",
    "3da89939-209c-4086-8520-7eb734e6b4ef",
    "46719c30-f4c3-4cad-be07-d5cb21eee6bb",
    "7d4a7d1d-cac6-44a8-96e8-ea9584a70825",
    "7dd30055-0198-452e-8c25-f73dbe27dcb8",
    "8131e2c0-0083-4265-9ce7-78c2d568425d",
    "872bfbb1-9ccf-49f6-8c5f-aa22818ccd66",
    "8d46b8d6-b38a-47ff-ac74-cda14cf2d19b",
    "935e2cff-ae78-4218-b3f5-115589b19dae",
    "a0c07678-e491-4bbc-8f0b-07405144218f",
    "c365c1c7-a3db-4d5e-a9a1-66f56eae7865",
    "dc22a632-937f-4e6a-b72f-ba0ff3f5ff97",
    "e142056d-56ab-4352-b091-b56054bd1359",
    "e8cb5b03-41e0-4086-99e5-f6806cd97211",
    "9318445f-fe6a-4e1b-acbf-c68228c9906a",
    "72e110e7-464c-453c-a309-90a95aed6538",
    "a7feb290-76bb-4cb7-8800-7edaf7954f2f"
]


def run(task_id, pipeline):
    """
    Run the pipeline for the whole gaia dataset.
    """
    
    task_info = get_task_from_gaia(task_id, "validation")
    print("Task: \n", task_info)
    print("\n")
    
    start_time = time.time()
    
    answer = pipeline(
        task=task_info["question"], 
        models=[
            "o4-mini", 
            "anthropic.claude-sonnet-4-20250514-v1:0", 
            "anthropic.claude-opus-4-20250514-v1:0"
        ]
    )
    
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: ", execution_time)
    
    is_correct = question_scorer(answer, task_info["true_answer"])
    is_close = check_close_call(answer, task_info["true_answer"], is_correct)
    if is_correct:
        pipeline.learn()
        
    result = {
        "answer": answer,
        "true_answer": task_info["true_answer"],
        "is_correct": is_correct,
        "is_close": is_close,
        "task_id": task_id,
        "execution_time": execution_time
    }
    print("Result: \n", result)
    print("\n")
    return result


if __name__ == "__main__":

    pipeline = EvolvePipeline()
    
    for task_id in TASK_ID_LIST:
        result = run(task_id, pipeline)

    pipeline.clear_episodic()