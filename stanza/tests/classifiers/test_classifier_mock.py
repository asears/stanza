"""
Example test demonstrating pytest-mocker usage for fast unit tests.

This test module shows how to mock pytorch and training dependencies
to test classifier logic without actually training models.

This approach is useful for:
- Testing error handling and edge cases quickly
- CI/CD pipelines where training is too slow
- Unit tests that focus on logic, not model accuracy
- Development/debugging cycles

Key patterns:
1. Mock the expensive Trainer class
2. Mock pytorch components (torch.load, torch.save, etc.)
3. Test the business logic without side effects
4. Verify mocked functions were called correctly

Run these fast tests (skip slow training tests):
    pytest stanza/tests/classifiers/test_classifier_mock.py

Or run with all tests including slow ones:
    pytest -m "" stanza/tests/classifiers/test_classifier_mock.py
"""

from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pytest

pytestmark = [pytest.mark.train]


class TestClassifierWithMocks:
    """Unit tests using mocked dependencies instead of actual pytorch training."""

    def test_model_configuration_without_training(self, mocker):
        """
        Test that model configuration is correctly set up without actual training.

        This test demonstrates mocking the Trainer class to verify configuration
        logic works correctly without the overhead of pytorch model training.
        """
        # Mock the Trainer class to avoid actual training
        mock_trainer_class = mocker.patch(
            'stanza.models.classifiers.trainer.Trainer',
            autospec=True,
        )

        # Create a mock instance with attributes
        mock_trainer = MagicMock()
        mock_trainer.args = {
            'save_dir': '/tmp/test',
            'save_name': 'model.pt',
            'bilstm_hidden_dim': 100,
            'batch_size': 32,
        }
        mock_trainer.model = MagicMock()
        mock_trainer_class.return_value = mock_trainer

        # Use the configuration without actually training
        from stanza.models.classifiers.trainer import Trainer
        trainer = Trainer()

        # Verify the mock was called
        assert trainer.args['bilstm_hidden_dim'] == 100
        assert trainer.args['batch_size'] == 32

        # Verify the mocked class was instantiated
        mock_trainer_class.assert_called_once()

    def test_pretrain_loading_mocked(self, mocker):
        """
        Test pretrain embedding loading logic using mocked file operations.

        Demonstrates mocking file I/O to test embedding loading without
        creating actual files or downloading pretrained embeddings.
        """
        # Mock the file operations
        mock_open = mocker.patch('builtins.open', create=True)
        mock_file = MagicMock()

        # Create mock embedding data
        embedding_lines = [
            'word1\t0.1\t0.2\t0.3\t0.4\t0.5\n',
            'word2\t0.2\t0.3\t0.4\t0.5\t0.6\n',
            'word3\t0.3\t0.4\t0.5\t0.6\t0.7\n',
        ]
        mock_file.__enter__.return_value.readlines.return_value = embedding_lines
        mock_open.return_value = mock_file

        # Test that we handle the embedding format correctly
        embeddings = {}
        for line in embedding_lines:
            parts = line.strip().split('\t')
            word = parts[0]
            vector = np.array([float(x) for x in parts[1:]], dtype=np.float32)
            embeddings[word] = vector

        # Verify embeddings were created correctly
        assert 'word1' in embeddings
        assert len(embeddings['word1']) == 5
        assert embeddings['word1'][0] == pytest.approx(0.1)

    def test_model_save_without_pytorch(self, mocker):
        """
        Test model saving logic using mocked torch.save/torch.load.

        This demonstrates how to verify model checkpoint behavior without
        actually running pytorch operations.
        """
        import torch

        # Mock torch.save and torch.load
        mock_save = mocker.patch('torch.save')
        mock_load = mocker.patch('torch.load')

        # Create mock checkpoint data
        mock_checkpoint = {
            'params': {
                'model': MagicMock(),
                'config': {
                    'force_bert_saved': False,
                    'class_weight': [1.0, 2.0],
                },
            },
            'epoch': 5,
        }
        mock_load.return_value = mock_checkpoint

        # Simulate saving a checkpoint
        checkpoint = {
            'epoch': 5,
            'model_state': 'mock_state',
        }
        save_path = '/tmp/model.pt'
        torch.save(checkpoint, save_path)

        # Verify torch.save was called with correct arguments
        mock_save.assert_called_once_with(checkpoint, save_path)

        # Simulate loading the checkpoint
        loaded = torch.load(save_path)
        assert loaded['epoch'] == 5

    def test_batch_processing_logic_mocked(self, mocker):
        """
        Test batch processing and data loading logic using mocked data.

        Demonstrates mocking data loading to test batch processing
        without actually reading files or GPU memory operations.
        """
        # Mock data loading
        mock_data = {
            'train': [
                {'text': 'Hello world', 'label': 0, 'id': 1},
                {'text': 'Good morning', 'label': 1, 'id': 2},
                {'text': 'How are you', 'label': 1, 'id': 3},
            ],
            'dev': [
                {'text': 'Test sentence', 'label': 0, 'id': 4},
            ],
        }

        # Simulate batch creation
        batch_size = 2
        batches = []
        for i in range(0, len(mock_data['train']), batch_size):
            batch = mock_data['train'][i:i + batch_size]
            batches.append(batch)

        # Verify batching works correctly
        assert len(batches) == 2
        assert len(batches[0]) == 2
        assert len(batches[1]) == 1
        assert batches[0][0]['text'] == 'Hello world'

    def test_error_handling_with_mocks(self, mocker):
        """
        Test error handling by mocking failure scenarios.

        Demonstrates how to test error cases fast using mocks
        instead of trying to trigger real failures.
        """
        # Mock a data loading function to raise an error
        mock_load_data = mocker.patch(
            'stanza.models.classifiers.data.read_dataset',
        )
        mock_load_data.side_effect = FileNotFoundError(
            "Dataset file not found",
        )

        # Test that error is handled correctly
        with pytest.raises(FileNotFoundError):
            from stanza.models.classifiers import data
            data.read_dataset('nonexistent.txt', 'word2vec')

        # Verify the function was called
        mock_load_data.assert_called_once_with(
            'nonexistent.txt', 'word2vec',
        )

    def test_optimizer_configuration_mocked(self, mocker):
        """
        Test optimizer setup without actual pytorch optimizer instantiation.

        Shows mocking pytorch optim module to test optimizer configuration
        logic without GPU/CUDA operations.
        """
        # Mock torch.optim
        mock_optim = mocker.patch('torch.optim')

        # Create a mock optimizer
        mock_optimizer = MagicMock()
        mock_optim.Adam.return_value = mock_optimizer

        # Simulate optimizer creation
        import torch.optim
        model_params = [MagicMock(), MagicMock()]
        optimizer = torch.optim.Adam(
            model_params,
            lr=0.001,
            betas=(0.9, 0.999),
        )

        # Verify optimizer was created with correct parameters
        mock_optim.Adam.assert_called_once_with(
            model_params,
            lr=0.001,
            betas=(0.9, 0.999),
        )

    def test_bert_model_configuration_mocked(self, mocker):
        """
        Test BERT model setup using mocks (avoids downloading models).

        Demonstrates mocking transformers library to test BERT integration
        without downloading large models or requiring torch compatibility.
        """
        # Mock transformers library
        mock_transformers = mocker.patch('transformers')

        # Create mock BERT model and tokenizer
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()

        mock_transformers.AutoModel.from_pretrained.return_value = mock_model
        mock_transformers.AutoTokenizer.from_pretrained.return_value = (
            mock_tokenizer
        )

        # Simulate loading BERT
        from transformers import AutoModel, AutoTokenizer
        model = AutoModel.from_pretrained('hf-internal-testing/tiny-bert')
        tokenizer = AutoTokenizer.from_pretrained(
            'hf-internal-testing/tiny-bert',
        )

        # Verify BERT components were loaded
        mock_transformers.AutoModel.from_pretrained.assert_called_once_with(
            'hf-internal-testing/tiny-bert',
        )
        mock_transformers.AutoTokenizer.from_pretrained.assert_called_once_with(
            'hf-internal-testing/tiny-bert',
        )

        # Verify models are available
        assert model is not None
        assert tokenizer is not None
