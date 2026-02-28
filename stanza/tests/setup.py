import logging
import os
import shutil
from pathlib import Path

import stanza
from stanza.resources import installation
from stanza.tests import TEST_HOME_VAR, TEST_WORKING_DIR

logger = logging.getLogger('stanza')

test_dir = os.getenv(TEST_HOME_VAR, None)
if not test_dir:
    test_dir = TEST_WORKING_DIR
    logger.info("STANZA_TEST_HOME not set.  Will assume %s", test_dir)
    logger.info("To use a different directory, export or set STANZA_TEST_HOME=...")
test_dir = Path(test_dir)

in_dir = test_dir / "in"
out_dir = test_dir / "out"
scripts_dir = test_dir / "scripts"
models_dir = test_dir / "models"
corenlp_dir = test_dir / "corenlp_dir"

test_dir.mkdir(parents=True, exist_ok=True)
in_dir.mkdir(parents=True, exist_ok=True)
out_dir.mkdir(parents=True, exist_ok=True)
scripts_dir.mkdir(parents=True, exist_ok=True)
models_dir.mkdir(parents=True, exist_ok=True)
corenlp_dir.mkdir(parents=True, exist_ok=True)

logger.info("COPYING FILES")

shutil.copy("stanza/tests/data/external_server.properties", scripts_dir)
shutil.copy("stanza/tests/data/example_french.json", out_dir)
shutil.copy("stanza/tests/data/aws_annotations.zip", in_dir)
for emb_file in Path("stanza/tests/data").glob("tiny_emb.*"):
    shutil.copy(emb_file, in_dir)

logger.info("DOWNLOADING MODELS")

stanza.download(lang='en', model_dir=str(models_dir), logging_level='info')
stanza.download(lang="en", model_dir=str(models_dir), package=None, processors={"ner": "ncbi_disease"})
stanza.download(lang='fr', model_dir=str(models_dir), logging_level='info')
# Latin ITTB has no case information for the lemmatizer
stanza.download(lang='he', model_dir=str(models_dir), processors='tokenize', logging_level='info')
stanza.download(lang='la', model_dir=str(models_dir), package='ittb', logging_level='info')
stanza.download(lang='zh', model_dir=str(models_dir), logging_level='info')
# useful not just for verifying RtL, but because the default Arabic has a unique style of xpos tags
stanza.download(lang='ar', model_dir=str(models_dir), logging_level='info')
stanza.download(lang='multilingual', model_dir=str(models_dir), logging_level='info')

logger.info("DOWNLOADING STANZA TOKENIZERS FOR MORPHSEG TESTS")

morphseg_langs = ['en', 'es', 'ru', 'fr', 'it', 'cs', 'hu', 'la']
for lang in morphseg_langs:
    stanza.download(lang=lang, model_dir=str(models_dir), processors='tokenize', logging_level='info')
    logger.info(f"Downloaded {lang} tokenizer for morphseg tests")

logger.info("DOWNLOADING CORENLP")

installation.install_corenlp(dir=str(corenlp_dir))
installation.download_corenlp_models(model="french", version="main", dir=str(corenlp_dir))
installation.download_corenlp_models(model="german", version="main", dir=str(corenlp_dir))
installation.download_corenlp_models(model="italian", version="main", dir=str(corenlp_dir))
installation.download_corenlp_models(model="spanish", version="main", dir=str(corenlp_dir))

logger.info("Test setup completed.")
