'''
Defines the set of symbols used in eng_text_norm input to the model.

The default is a set of ASCII characters that works well for English or eng_text_norm that has been run
through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details.
'''
from eng_text_norm import cmudict

_pad        = '_'
_eos        = '~'
_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\'\"(),-.:;? '

# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in cmudict.valid_symbols]

# Export all symbols:
symbols = [_pad, _eos] + list(_characters) + _arpabet
