#!/usr/bin/env python3
import os
import shutil

TASK_ID_LIST = [
    "676e5e31-a554-4acc-9286-b60d90a92d26",
    "0383a3ee-47a7-41a4-b493-519bdefe0488",
    "7d4a7d1d-cac6-44a8-96e8-ea9584a70825",
    "e142056d-56ab-4352-b091-b56054bd1359",
    "d0633230-7067-47a9-9dbf-ee11e0a2cdd6",
    "023e9d44-96ae-4eed-b912-244ee8c3b994",
    "20194330-9976-4043-8632-f8485c6c71b2",
    "48eb8242-1099-4c26-95d4-ef22b002457a",
    "853c8244-429e-46ca-89f2-addf40dfb2bd",
    "1dcc160f-c187-48c2-b68e-319bd4354f3d",
    "e2d69698-bc99-4e85-9880-67eaccd66e6c",
    "8131e2c0-0083-4265-9ce7-78c2d568425d",
    "872bfbb1-9ccf-49f6-8c5f-aa22818ccd66",
    "8d46b8d6-b38a-47ff-ac74-cda14cf2d19b",
    "ad2b4d70-9314-4fe6-bfbe-894a45f6055f",
    "c3a79cfe-8206-451f-aca8-3fec8ebe51d3",
    "3da89939-209c-4086-8520-7eb734e6b4ef",
    "46719c30-f4c3-4cad-be07-d5cb21eee6bb",
    "4b6bb5f7-f634-410e-815d-e673ab7f8632",
    "72e110e7-464c-453c-a309-90a95aed6538",
    "7673d772-ef80-4f0f-a602-1bf4485c9b43",
    "9318445f-fe6a-4e1b-acbf-c68228c9906a",
    "cca530fc-4052-43b2-b130-b30968d8aa44",
    "d5141ca5-e7a0-469f-bf3e-e773507c86e2",
    "0b260a57-3f3a-4405-9f29-6d7a1012dbfb",
    "0e9e85b8-52b9-4de4-b402-5f635ab9631f",
    "16d825ff-1623-4176-a5b5-42e0f5c2b0ac",
    "42d4198c-5895-4f0a-b0c0-424a66465d83",
    "4d51c4bf-4b0e-4f3d-897b-3f6687a7d9f2",
    "624cbf11-6a41-4692-af9c-36b3e5ca3130",
    "6359a0b1-8f7b-499b-9336-840f9ab90688",
    "708b99c5-e4a7-49cb-a5cf-933c8d46470d",
    "7a4a336d-dcfa-45a0-b014-824c7619e8de",
    "8b3379c0-0981-4f5b-8407-6444610cb212",
    "8f80e01c-1296-4371-9486-bb3d68651a60",
    "a7feb290-76bb-4cb7-8800-7edaf7954f2f",
    "bfcd99e1-0690-4b53-a85c-0174a8629083",
    "c8b7e059-c60d-472e-ad64-3b04ae1166dc",
    "df6561b2-7ee5-4540-baab-5095f742716a",
    "ecbc4f94-95a3-4cc7-b255-6741a458a625",
    "00d579ea-0889-4fd9-a771-2c8d79835c8d",
    "384d0dd8-e8a4-4cfe-963c-d37f256e7662",
    "5f982798-16b9-4051-ab57-cfc7ebdb2a91",
    "72c06643-a2fa-4186-aa5c-9ec33ae9b445",
    "983bba7c-c092-455f-b6c9-7857003d48fc",
    "bec74516-02fc-48dc-b202-55e78d0e17cf",
    "c526d8d6-5987-4da9-b24c-83466fa172f3",
    "56137764-b4e0-45b8-9c52-1866420c3df5", # wrong
    "b415aba4-4b68-4fc6-9b89-2c812e55a3e1", # wrong
    "0bb3b44a-ede5-4db5-a520-4e844b0079c5", # wrong
    "9f41b083-683e-4dcf-9185-ccfeaa88fa45", # wrong
    "05407167-39ec-4d3a-a234-73a9120c325d", # wrong
    "7b5377b0-3f38-4103-8ad2-90fe89864c04", # wrong
    "ed58682d-bc52-4baa-9eb0-4eb81e1edacc", # wrong
    "cca70ce6-1952-45d2-acd4-80c903b0bc49", # wrong
    "2dfc4c37-fec1-4518-84a7-10095d30ad75", # wrong
    "b4cc024b-3f5e-480e-b96a-6656493255b5", # wrong
    "de9887f5-ead8-4727-876f-5a4078f8598c", # wrong
    "a56f1527-3abf-41d6-91f8-7296d6336c3f", # wrong
    "e8cb5b03-41e0-4086-99e5-f6806cd97211", # wrong
    "0512426f-4d28-49f0-be77-06d05daec096", # wrong
    "5b2a14e8-6e59-479c-80e3-4696e8980152", # wrong
    "9e1fc53b-46ff-49a1-9d05-9e6faac34cc5", # wrong
    "a0c07678-e491-4bbc-8f0b-07405144218f", # wrong
    "23dd907f-1261-4488-b21c-e9185af91d5e", # wrong
]

def cleanup_logs():
    logs_dir = "logs"
    
    if not os.path.exists(logs_dir):
        print(f"Log directory {logs_dir} does not exist")
        return
    
    deleted_count = 0
    for task_id in TASK_ID_LIST:
        log_dir_name = f"log_{task_id}"
        log_dir_path = os.path.join(logs_dir, log_dir_name)
        
        if os.path.exists(log_dir_path):
            try:
                shutil.rmtree(log_dir_path)
                print(f"Deleted: {log_dir_name}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {log_dir_name}: {e}")
        else:
            print(f"Not found: {log_dir_name}")
    
    print(f"\nCleanup completed, deleted {deleted_count} log directories")

if __name__ == "__main__":
    cleanup_logs() 