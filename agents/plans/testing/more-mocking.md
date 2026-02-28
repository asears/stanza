stanza/tests/common/test_pretrain.py::test_text_pretrain 2026-02-28 15:08:27,091 - stanza - INFO - Reading pretrained vectors from \AppData\Local\StanfordNLP\stanza_test\Cache\1.11.0/in/tiny_emb.txt ...
FAILED                                                                                                                                           [ 15%]

=================================================================================================== FAILURES ===================================================================================================
______________________________________________________________________________________________ test_text_pretrain ______________________________________________________________________________________________
stanza\tests\common\test_pretrain.py:44: in test_text_pretrain
    check_pretrain(pt)
stanza\tests\common\test_pretrain.py:38: in check_pretrain
    check_vocab(pt.vocab)
                ^^^^^^^^
stanza\models\common\pretrain.py:49: in vocab
    self.load()
stanza\models\common\pretrain.py:89: in load
    vocab, emb = self.read_pretrain()
                 ^^^^^^^^^^^^^^^^^^^^
stanza\models\common\pretrain.py:133: in read_pretrain
    words, emb, failed = self.read_from_file(self._vec_filename, self._max_vocab)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
stanza\models\common\pretrain.py:190: in read_from_file
    with open_read_binary(filename) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^
\AppData\Roaming\uv\python\cpython-3.12.6-windows-x86_64-none\Lib\contextlib.py:137: in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
stanza\models\common\utils.py:134: in open_read_binary
    with open(filename, mode='rb') as fin:
         ^^^^^^^^^^^^^^^^^^^^^^^^^
E   FileNotFoundError: [Errno 2] No such file or directory: 'AppData\\Local\\StanfordNLP\\stanza_test\\Cache\\1.11.0/in/tiny_emb.txt'
--------------------------------------------------------------------------------------------- Captured stderr call ---------------------------------------------------------------------------------------------
2026-02-28 15:08:27 INFO: Reading pretrained vectors from \AppData\Local\StanfordNLP\stanza_test\Cache\1.11.0/in/tiny_emb.txt ...
---------------------------------------------------------------------------------------------- Captured log call -----------------------------------------------------------------------------------------------
INFO     stanza:pretrain.py:181 Reading pretrained vectors from \AppData\Local\StanfordNLP\stanza_test\Cache\1.11.0/in/tiny_emb.txt ...
=========================================================================================== short test summary info ============================================================================================
FAILED stanza/tests/common/test_pretrain.py::test_text_pretrain - FileNotFoundError: [Errno 2] No such file or directory: 'AppData\\Local\\StanfordNLP\\stanza_test\\Cache\\1.11.0/in/tiny_emb.txt'

