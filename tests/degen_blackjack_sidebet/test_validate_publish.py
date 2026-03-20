import json
import sys
import tempfile
import unittest
from pathlib import Path

GAME_DIR = '/workspace/math-sdk/games/degen_blackjack_sidebet'
if GAME_DIR not in sys.path:
    sys.path.insert(0, GAME_DIR)

from validate_publish import ValidationError, validate_publish_folder


class TestValidatePublish(unittest.TestCase):
    def test_validate_publish_folder_accepts_documented_shapes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            publish_dir = temp_path / 'publish_files'
            books_dir = temp_path / 'books'
            publish_dir.mkdir()
            books_dir.mkdir()

            (publish_dir / 'index.json').write_text(
                json.dumps(
                    {
                        'modes': [
                            {
                                'name': 'base',
                                'cost': 1.0,
                                'events': 'books_base.jsonl.zst',
                                'weights': 'lookUpTable_base_0.csv',
                            }
                        ]
                    }
                ),
                encoding='utf-8',
            )
            (publish_dir / 'lookUpTable_base_0.csv').write_text('1,1,500\n', encoding='utf-8')
            (publish_dir / 'books_base.jsonl.zst').write_bytes(b'placeholder')
            (books_dir / 'books_base.jsonl').write_text(
                json.dumps({'id': 1, 'events': [{'type': 'dealCards'}], 'payoutMultiplier': 500}) + '\n',
                encoding='utf-8',
            )

            validate_publish_folder(publish_dir)

    def test_validate_publish_folder_rejects_missing_index(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValidationError):
                validate_publish_folder(Path(temp_dir))


if __name__ == '__main__':
    unittest.main()
