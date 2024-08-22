import os

ASSET_PATH = os.path.join('./assets')
LOG_PATH = os.path.join('./logs')
TRANSLATION_TABLE = 'translation_table.clinical_diagnosis.final.json'

for path in [ASSET_PATH, LOG_PATH]:
    if not os.path.exists(path):
        os.makedirs(path)

