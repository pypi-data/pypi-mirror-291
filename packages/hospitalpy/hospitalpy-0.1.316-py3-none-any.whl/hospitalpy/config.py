import os

base_dir = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(base_dir, 'assets')

LOG_PATH = os.path.join('./logs')
TRANSLATION_TABLE = 'translation_table.clinical_diagnosis.final.json'

for path in [ASSET_PATH, LOG_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)
