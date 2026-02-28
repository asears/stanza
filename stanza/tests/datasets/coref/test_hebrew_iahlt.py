import pytest

from stanza import Pipeline
from stanza.tests import TEST_MODELS_DIR
from stanza.utils.datasets.coref.convert_hebrew_iahlt import extract_doc

pytestmark = [pytest.mark.travis, pytest.mark.pipeline]


@pytest.fixture(scope="module")
def tokenizer():
    pipe = Pipeline(lang="he", processors="tokenize", dir=TEST_MODELS_DIR, download_method=None)
    return pipe


TEXT = """



מבולבלים\u200b? גם אנחנו\u200b: ל\u200bמסעדנים ו\u200bה\u200bמלצרים יש עוד סימני שאלה על ה\u200bטיפים\u200b

ה\u200bפער בין פסיקת בית ה\u200bדין ל\u200bעבודה לבין פסיקה קודמת של בג"ץ\u200b, משאיר את ה\u200bענף ב\u200bחוסר וודאות\u200b, ו\u200bה -\u200b1 ב\u200bינואר כבר מעבר ל\u200bפינה . "\u200bמ\u200bבחינת\u200bי , הייתי מוסיף ל\u200bתפריט תוספת שירות של 17\u200b% "\u200b, אמר בעלים של מסעדה ב\u200bשדרות\u200b

ב\u200bרשות ה\u200bמיסים מסתפקים ב\u200bמסר עמום באשר ל\u200bכוונותי\u200bהם לאור פסק דין ה\u200bטיפים ש\u200bצפוי להיכנס ל\u200bתוקפ\u200bו ב\u200b-\u200b1 ב\u200bינואר . על פי פרשנות\u200bם ה\u200bמקצועית , הבהירו\u200b, יש מקום לחייב את כספי ה\u200bטיפים ב\u200bמע"מ , "\u200bעם זאת\u200b, ה\u200bרשות עדין בוחנת את ה\u200bסוגיה ו\u200bטרם התקבלה החלטה אופרטיבית ב\u200bעניין "\u200b. ו\u200bאיך אמורים ה\u200bמסעדנים להיערך בינתיים ל\u200bיישום ה\u200bפסיקה ו\u200bל\u200bמחזור ה\u200bשנה ה\u200bבאה ? ב\u200bיום חמישי יפגשו אנשי ארגון '\u200bמסעדנים חזקים ביחד\u200b' עם מנהל רשות ה\u200bמיסים ערן יעקב\u200b, ו\u200bידרשו תשובות ברורות\u200b.\u200b

"\u200bאני עדיין לא מדבר עם ה\u200bעובדים של\u200bי , ו\u200bאני גם לא יודע איך להיערך החל מ\u200bעוד שבועיים\u200b"\u200b, אמר ל\u200b'\u200bדבר ראשון\u200b' ניר שוחט\u200b, ה\u200bבעלים של מסעדת סושי מוטו ב\u200bשדרות ו\u200bמוסיף כי יהיה קשה להתאים את ה\u200bפסיקה ל\u200bמציאות ב\u200bשטח . "\u200bאף אחד לא יודע\u200b. יש המון סתירות – עורך ה\u200bדין אומר דבר אחד ו\u200bרואה ה\u200bחשבון דבר אחר\u200b. עדיין לא הצליחו להבין את ה\u200bחוק ל\u200bאשור\u200bו "\u200b.\u200b

"\u200bמ\u200bבחינת\u200bי , הייתי מוסיף ל\u200bתפריט תוספת שירות של 17\u200b% . זה יגלם גם את ה\u200bמע"מ ו\u200bה\u200bטיפים ו\u200bמ\u200bזה אני אשלם ל\u200bמלצרים . די כבר עם ה\u200bטיפים ה\u200bאלה , מספיק\u200b.\u200b"\u200b
"""

CLUSTER = {'metadata': {'name': 'המסעדנים', 'entity': 'person'}, 'mentions': [[28, 35, {}], [572, 581, {}]]}


def test_extract_doc(tokenizer):
    doc = {'text': TEXT,
           'clusters': [CLUSTER],
           'metadata': {
               'doc_id': 'test',
           },
           }
    extracted = extract_doc(tokenizer, [doc])
    assert len(extracted) == 1
    assert len(extracted[0].coref_spans) == 2
    assert extracted[0].coref_spans[1] == [(0, 4, 4)]
    assert extracted[0].coref_spans[6] == [(0, 3, 4)]
