PATTERNS = {
    'push_pattern': r'^push(?!a)',
    "pusha_pattern": r"^pusha",
    "popa_pattern": r"^popa",
    "pop_pattern": r'^pop(?!a)',
    'call_pattern': r'^call ',
    'label_pattern': r':$',
    'loop_pattern': r'^(?:loop|jmp) ',
    'comment_pattern': r'^;',
    'add_esp': r'^add esp',
    'sub_esp': r'^sub esp',
    'segment_text': r'.text$',
    'ret_pattern': r'^ret$',
    "mov_esp": r'^mov ebp',
    'condition_pattern': r'^j(?:e|ne|le|ge|z)\s+'
}
