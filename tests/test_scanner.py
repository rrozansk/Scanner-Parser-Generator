"""
Testing for RegularGrammar objects located in spag/scanner.py
"""
from itertools import permutations
import pytest
from spag.scanner import RegularGrammar


class TestScanner:
    """
    A test suite for testing the RegularGrammar object.
    """

    @staticmethod
    def _compare_expressions(expected, actual):
        """
        Compare the expected and actual expressions.
        """
        assert len(expected) == len(actual), \
               'Incorrect expression size produced'

        assert set(expected.keys()) == set(actual.keys()), \
               'Incorrect token name/type set produced'

        for name in expected:
            expected_pattern = expected[name]
            actual_pattern = actual[name]

            assert len(expected_pattern) == len(actual_pattern), \
                  'Incorrect expression pattern size produced'

            for idx, expected_elem in enumerate(expected_pattern):
                assert expected_elem == actual_pattern[idx], \
                   'Incorrect token pattern produced'

    @staticmethod
    def _compare_dfa(expected, actual):
        """
        Check if DFA's are isomorphic by attempting to find a bijection
        between if they look 'similar' is size and shape.
        """
        V = actual.alphabet
        assert V == expected['V'], \
               'Incorrect alphabet produced'

        Q = actual.states
        assert len(Q) == len(expected['Q']), \
               'Incorrect number of states produced'

        F = actual.accepting
        assert len(F) == len(expected['F']), \
               'Incorrect number of finish states produced'

        G = actual.types
        assert len(G) == len(expected['G']), \
               'Incorrect number of types produced'

        state, symbol, T = actual.transitions
        assert len(T) == len(expected['T'])-1 or \
               (T and len(T[0]) == len(expected['T'][0])-1), \
               'Incorrect number of transitions produced'

        _state, _symbol, Tp = dict(), dict(), list()
        if T:
            _state = {s:idx for idx, s in enumerate(expected['T'].pop(0)[1:])}
            _symbol = {s:idx for idx, s in enumerate([row.pop(0) for row in expected['T']])}
            Tp = expected['T']

        S = actual.start
        Qp = expected['Q']

        perms = permutations(Qp, len(Qp))
        map_generator = ({q:perm[idx] for idx, q in enumerate(Q)} for perm in perms)
        for _map in map_generator:
            if _map[S] != expected['S']:
                continue
            if not all([_map[f] in expected['F'] for f in F]):
                continue
            if not all([{_map[s] for s in G[name]} == \
               expected['G'].get(name, set()) for name in G]):
                continue
            if not all([all([_map[T[symbol[v]][state[q]]] == \
               Tp[_symbol[v]][_state[_map[q]]] for q in Q]) for v in V]):
                continue
            return

        assert False, 'Non-isomorphic DFA produced'

    @staticmethod
    def _run(**kwargs):
        """
        The 'main' for testing which creates the required object and compares
        the results are what was expected, failing appropriately if they are
        not.
        """
        regular_grammar = RegularGrammar(kwargs['name'], kwargs['expressions'])

        assert regular_grammar.name == kwargs['name'], \
               'Incorrect DFA name returned'

        TestScanner._compare_expressions(kwargs['expressions'],
                                         regular_grammar.expressions)

        TestScanner._compare_dfa(kwargs['DFA'], regular_grammar)

    @staticmethod
    @pytest.mark.xfail(
        reason='Name is not of type string.',
        raises=TypeError,
    )
    def test_name_invalid():
        """
        Ensure a TypeError is raised when constructing a RegularGrammar object
        if the name is not of type string.
        """
        TestScanner._run(**{
            'name': ['Invalid Scanner Name'],
            'expressions': {
                'invalid': ['f', 'o', 'o']
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Name must be non empty.',
        raises=ValueError,
    )
    def test_name_empty():
        """
        Ensure a ValueError is raised when constructing a RegularGrammar object
        if the name is an empty string.
        """
        TestScanner._run(**{
            'name': '',
            'expressions': {
                'foo': ['b', 'a', 'r'],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Expression is not of type dict.',
        raises=TypeError,
    )
    def test_expressions_invalid():
        """
        Ensure a TypeError is raised when constructing a RegularGrammar object
        if the expressions is not of type dict.
        """
        TestScanner._run(**{
            'name': 'Invalid Scanner Expressions',
            'expressions': None,
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Empty expressions.',
        raises=ValueError,
    )
    def test_expressions_empty():
        """
        Ensure empty expressions produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Scanner Token',
            'expressions': {},
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid expressions.',
        raises=TypeError,
    )
    def test_expression_id_invalid():
        """
        Ensure invalid expressions produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Scanner Token Key',
            'expressions': {
                None: ['i', 'n', 'v', 'a', 'l', 'i', 'd']
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Exmpty expressions.',
        raises=ValueError,
    )
    def test_expression_id_empty():
        """
        Ensure invalid expressions produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Scanner Token Key',
            'expressions': {
                '': ['i', 'n', 'v', 'a', 'l', 'i', 'd']
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid expressions.',
        raises=TypeError,
    )
    def test_expression_pattern_invalid():
        """
        Ensure invalid expressions produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Scanner Token Value',
            'expressions': {
                'invalid': True
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Empty expression.',
        raises=ValueError,
    )
    def test_expression_pattern_empty():
        """
        Ensure empty expressions produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Empty Expression',
            'expressions': {
                'invalid': []
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid character.',
        raises=TypeError,
    )
    def test_character_invalid_type():
        """
        Ensure invalid character produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Character',
            'expressions': {
                'invalid': [True]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid character.',
        raises=ValueError,
    )
    def test_character_invalid():
        """
        Ensure invalid character produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Character',
            'expressions': {
                'invalid': ['fo']
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid operator arity.',
        raises=ValueError,
    )
    def test_invalid_airty_star():
        """
        Ensure invalid kleene star (*) operator airty produces the proper
        exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Expression * Arity',
            'expressions': {
                'invalid': [RegularGrammar.kleene_star()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid operator arity.',
        raises=ValueError,
    )
    def test_invalid_airty_plus():
        """
        Ensure invalid kleene plus (+) operator airty produces the proper
        exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Expression + Arity',
            'expressions': {
                'invalid': [RegularGrammar.kleene_plus()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid operator arity.',
        raises=ValueError,
    )
    def test_invalid_airty_alternate():
        """
        Ensure invalid alternate (|) operator airty produces the proper
        exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Expression | Arity',
            'expressions': {
                'invalid': ['a', RegularGrammar.alternative()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid operator arity.',
        raises=ValueError,
    )
    def test_invalid_airty_concat():
        """
        Ensure invalid concat (.) operator airty produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Expression . Arity',
            'expressions': {
                'invalid': ['a', RegularGrammar.concatenation()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid operator arity.',
        raises=ValueError,
    )
    def test_invalid_airty_maybe():
        """
        Ensure invalid maybe (?) operator airty produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Expression ? Arity',
            'expressions': {
                'invalid': [RegularGrammar.maybe()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid operator arity.',
        raises=ValueError,
    )
    def test_invalid_airty_group():
        """
        Ensure invalid group '()' operator airty produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Invalid Expression () Arity',
            'expressions': {
                'invalid': [RegularGrammar.left_group(), RegularGrammar.right_group()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Unbalanced parenthesis.',
        raises=ValueError,
    )
    def test_unbalanced_paren_left():
        """
        Ensure unbalanced parenthesis produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Unbalanced Right Paren',
            'expressions': {
                'invalid': [RegularGrammar.left_group()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Unbalanced parenthesis.',
        raises=ValueError,
    )
    def test_unbalanced_paren_right():
        """
        Ensure unbalanced parenthesis produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Unbalanced Left Paren',
            'expressions': {
                'invalid': [RegularGrammar.right_group()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid character range.',
        raises=ValueError,
    )
    def test_char_range_invalid_start():
        """
        Ensure an invalid character ranges produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Character Range/Class No Start',
            'expressions': {
                'class/range': [RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Invalid character range.',
        raises=ValueError,
    )
    def test_char_range_invalid_end():
        """
        Ensure an invalid character ranges produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Character Range/Class No End',
            'expressions': {
                'class/range': [RegularGrammar.left_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Empty character range.',
        raises=ValueError,
    )
    def test_char_range_empty():
        """
        Ensure empty character ranges produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Empty Character Range/Class',
            'expressions': {
                'class/range': [RegularGrammar.left_class(), RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Recursive character class/range not specified.',
        raises=ValueError,
    )
    def test_recursive_char_range_class():
        """
        Ensure recursive character ranges/classes produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Recursive Character Range/Class',
            'expressions': {
                'class/range': [RegularGrammar.left_class(), 'a', RegularGrammar.left_class(), 'b',
                                RegularGrammar.right_class(), RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Class range outside of brackets.',
        raises=ValueError,
    )
    def test_external_char_range():
        """
        Ensure character ranges outside brackets produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'External Character Range/Class',
            'expressions': {
                'range': ['a', RegularGrammar.character_range(), 'b']
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='No character range end.',
        raises=ValueError,
    )
    def test_char_range_no_end():
        """
        Ensure character ranges with no ending produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Character Range No End',
            'expressions': {
                'range': [RegularGrammar.left_class(), 'a', RegularGrammar.character_range(), RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='No character range start.',
        raises=ValueError,
    )
    def test_char_range_no_start():
        """
        Ensure character ranges with no beginning produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Character Range No Start',
            'expressions': {
                'range': [RegularGrammar.left_class(), RegularGrammar.character_range(), 'b', RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Double class range not defined.',
        raises=ValueError,
    )
    def test_double_char_range():
        """
        Ensure double character ranges produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Double Character Range',
            'expressions': {
                'range': [RegularGrammar.left_class(), 'a', RegularGrammar.character_range(),
                          RegularGrammar.character_range(), 'b', RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Character negation outside brackets.',
        raises=ValueError,
    )
    def test_external_char_negation():
        """
        Ensure character negation outside brackets produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'External Character Negation',
            'expressions': {
                'negation': [RegularGrammar.character_negation()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Character double negation not defined.',
        raises=ValueError,
    )
    def test_double_char_negation():
        """
        Ensure double character negation produces the proper exception.
        """
        TestScanner._run(**{
            'name': 'Double Character Negation',
            'expressions': {
                'negation': [RegularGrammar.left_class(), RegularGrammar.character_negation(),
                             RegularGrammar.character_negation(), 'a', RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        reason='Operator expansion not defined.',
        raises=ValueError,
    )
    def test_char_range_operator():
        """
        Ensure character range with operators produce the proper exception.
        """
        TestScanner._run(**{
            'name': 'Character Range Operator',
            'expressions': {
                'negation': [RegularGrammar.left_class(), 'a', RegularGrammar.character_range(),
                             RegularGrammar.kleene_star(), RegularGrammar.right_class()]
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Empty interval.'
    )
    def test_empty_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Empty Interval',
            'expressions': {
                'empty_curlies': ['a', RegularGrammar.left_interval(), RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Negative interval.'
    )
    def test_invalid_interval_count():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Negative Count',
            'expressions': {
                'invalid_count': ['a', RegularGrammar.left_interval(), -1, RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Backwards interval.'
    )
    def test_invalid_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Undefined Interval - Backwards Range',
            'expressions': {
                'invalid_interval': ['a', RegularGrammar.left_interval(), 2, 1, RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=TypeError,
        reason='Interval is defined over integers.'
    )
    def test_undefined_interval_1():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Undefined Interval - Character',
            'expressions': {
                'undefined_interval_1': ['a', RegularGrammar.left_interval(), 'a', RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Interval is only defined over 1-2 integers.'
    )
    def test_undefined_interval_2():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Undefined Interval - Multi Number',
            'expressions': {
                'undefined_interval_2': ['a', RegularGrammar.left_interval(), 2, 3, 4, RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=TypeError,
        reason='Intervals must be integers.'
    )
    def test_undefined_interval_3():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Undefined Interval - Float',
            'expressions': {
                'undefined_interval_3': ['a', RegularGrammar.left_interval(), 4.45, RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Intervals cannot be recursive.'
    )
    def test_recursive_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Recursive Interval',
            'expressions': {
                'recursive_interval': ['a', RegularGrammar.left_interval(), RegularGrammar.left_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Interval with no start.'
    )
    def test_no_start_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'No Start Interval',
            'expressions': {
                'no_start_interval': ['a', RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Interval with no end.'
    )
    def test_no_end_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'No End Interval',
            'expressions': {
                'no_end_interval': ['a', RegularGrammar.left_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=TypeError,
        reason='Integers only allows in interval expressions.'
    )
    def test_only_interval_ints_allowed():
        """
        Ensure integers are only permitted inside interval expressions.
        """
        TestScanner._run(**{
            'name': 'Non-interval integer',
            'expressions': {
                'non_interval_integer': ['a', 'b', 1],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='The group for the interval is incorrect.'
    )
    def test_interval_invalid_group():
        """
        Ensure interval expressions on invalid groups produces the expected
        error.
        """
        TestScanner._run(**{
            'name': 'Invalid Interval Group',
            'expressions': {
                'invalid_interval_group': ['b', RegularGrammar.right_group(), RegularGrammar.left_interval(), 1, RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    @pytest.mark.xfail(
        raises=ValueError,
        reason='Interval expressions are limited to character/groups.'
    )
    def test_smart_interval():
        """
        Ensure complex interval expression produces the expected result.
        """
        TestScanner._run(**{
            'name': 'Smart Interval',
            'expressions': {
                'smart_interval': ['b', RegularGrammar.maybe(), RegularGrammar.left_interval(), 3, RegularGrammar.right_interval()],
            },
            'DFA': {}
        })

    @staticmethod
    def test_single_alpha():
        """
        Ensure a one character expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Single Alpha',
            'expressions': {
                'alpha': ['a']
            },
            'DFA': {
                'Q': set(['S', 'A', 'Err']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S', 'A',   'Err'],
                    ['a', 'A', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['A']),
                'G': {
                    'alpha': set(['A']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_unicode_16bit_literal():
        """
        Ensure a one character 16bit unicode literal expression produces the
        expected output.
        """
        TestScanner._run(**{
            'name': 'Unicode 16 Bit Literal',
            'expressions': {
                'literal': [u'\u0394']
            },
            'DFA':{
                'Q': set(['S', 'Unicode', 'Err']),
                'V': set([u'\u0394']),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',       'S',       'Unicode', 'Err'],
                    [u'\u0394', 'Unicode', 'Err',     'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['Unicode']),
                'G': {
                    'literal': set(['Unicode']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_unicode_32bit_literal():
        """
        Ensure a one character 32bit unicode literal expression produces the
        expected output.
        """
        TestScanner._run(**{
            'name': 'Unicode 32 Bit Literal',
            'expressions': {
                'literal': [u'\U00000394']
            },
            'DFA':{
                'Q': set(['S', 'Unicode', 'Err']),
                'V': set([u'\U00000394']),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',           'S',       'Unicode', 'Err'],
                    [u'\U00000394', 'Unicode', 'Err',     'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['Unicode']),
                'G': {
                    'literal': set(['Unicode']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_unicode_name_literal():
        """
        Ensure a unicode name literal expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Unicode Name Literal',
            'expressions': {
                'literal': [u'\N{GREEK CAPITAL LETTER DELTA}']
            },
            'DFA':{
                'Q': set(['S', 'Unicode', 'Err']),
                'V': set([u'\N{GREEK CAPITAL LETTER DELTA}']),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',                               'S',       'Unicode', 'Err'],
                    [u'\N{GREEK CAPITAL LETTER DELTA}', 'Unicode', 'Err',     'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['Unicode']),
                'G': {
                    'literal': set(['Unicode']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_hex_literal():
        """
        Ensure a hex character literal expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Hex Literal',
            'expressions': {
                'literal': ['\x34']
            },
            'DFA': {
                'Q': set(['S', 'Hex', 'Err']),
                'V': set(['\x34']),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',    'S',   'Hex', 'Err'],
                    ['\x34', 'Hex', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['Hex']),
                'G': {
                    'literal': set(['Hex']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_unicode_range():
        """
        Ensure a unicode character range expression produces the expected
        output.
        """
        TestScanner._run(**{
            'name': 'Unicode Range',
            'expressions': {
                'range': [RegularGrammar.left_class(), u'\u2345', RegularGrammar.character_range(), u'\u2346', RegularGrammar.right_class()]
            },
            'DFA':{
                'Q': set(['S', 'Unicode', 'Err']),
                'V': set([u'\u2345', u'\u2346']),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',       'S',       'Unicode', 'Err'],
                    [u'\u2345', 'Unicode', 'Err',     'Err'],
                    [u'\u2346', 'Unicode', 'Err',     'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['Unicode']),
                'G': {
                    'range': set(['Unicode']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_hex_range():
        """
        Ensure a hex character range expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Hex Range',
            'expressions': {
                'range': [RegularGrammar.left_class(), '\x34', RegularGrammar.character_range(), '\x35', RegularGrammar.right_class()]
            },
            'DFA':{
                'Q': set(['S', 'Hex', 'Err']),
                'V': set(['\x34', '\x35']),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',    'S',   'Hex', 'Err'],
                    ['\x34', 'Hex', 'Err', 'Err'],
                    ['\x35', 'Hex', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['Hex']),
                'G': {
                    'range': set(['Hex']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_kleene_star():
        """
        Ensure Kleene on a single character produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Kleene Star',
            'expressions': {
                'star': ['a', RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['A']),
                'V': set('a'),
                'T': [
                    [' ', 'A'],
                    ['a', 'A']
                ],
                'S': 'A',
                'F': set(['A']),
                'G': {
                    'star': set(['A'])
                }
            }
        })

    @staticmethod
    def test_kleene_plus():
        """
        Ensure Kleene plus on a single character produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Kleene Plus',
            'expressions': {
                'plus': ['a', RegularGrammar.kleene_plus()]
            },
            'DFA': {
                'Q': set(['S', 'A']),
                'V': set('a'),
                'T': [
                    [' ', 'S', 'A'],
                    ['a', 'A', 'A']
                ],
                'S': 'S',
                'F': set(['A']),
                'G': {
                    'plus': set(['A'])
                }
            }
        })

    @staticmethod
    def test_alternation():
        """
        Ensure the alternative of two characters produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Alternation',
            'expressions': {
                'alt': ['a', RegularGrammar.alternative(), 'b']
            },
            'DFA': {
                'Q': set(['S', 'AB', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',  'AB',  'Err'],
                    ['a', 'AB', 'Err', 'Err'],
                    ['b', 'AB', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['AB']),
                'G': {
                    'alt': set(['AB']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_concatenation_explicit():
        """
        Ensure explicit concatenation of two characters produces the expected
        output.
        """
        TestScanner._run(**{
            'name': 'Explicit Concatenation',
            'expressions': {
                'concat': ['a', RegularGrammar.concatenation(), 'b']
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A',   'B',   'Err'],
                    ['a', 'A',   'Err', 'Err', 'Err'],
                    ['b', 'Err', 'B',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['B']),
                'G': {
                    'concat': set(['B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_concatenation_implicit():
        """
        Ensure implicit concatenation of two characters produces the expected
        output.
        """
        TestScanner._run(**{
            'name': 'Implicit Concatenation Characters',
            'expressions': {
                'concat': ['a', 'b']
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A',   'B',   'Err'],
                    ['a', 'A',   'Err', 'Err', 'Err'],
                    ['b', 'Err', 'B',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['B']),
                'G': {
                    'concat': set(['B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_concatenation_mixed():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Mixed Concatenation',
            'expressions': {
                'concat': ['a', RegularGrammar.concatenation(), 'b', 'c', RegularGrammar.concatenation(), 'd', 'e']
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'C', 'D', 'E', 'Err']),
                'V': set('abcde'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A',   'B',   'C',   'D',   'E',   'Err'],
                    ['a', 'A',   'Err', 'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['b', 'Err', 'B',   'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['c', 'Err', 'Err', 'C',   'Err', 'Err', 'Err', 'Err'],
                    ['d', 'Err', 'Err', 'Err', 'D',   'Err', 'Err', 'Err'],
                    ['e', 'Err', 'Err', 'Err', 'Err', 'E',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['E']),
                'G': {
                    'concat': set(['E']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_maybe():
        """
        Ensure maybe on a single character produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Choice',
            'expressions': {
                'maybe': ['a', RegularGrammar.maybe()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'Err']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S', 'A',   'Err'],
                    ['a', 'A', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S', 'A']),
                'G': {
                    'maybe': set(['S', 'A']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_grouping():
        """
        Ensure the group operator produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Grouping',
            'expressions': {
                'group': [RegularGrammar.left_group(), 'a', RegularGrammar.alternative(), 'b',
                          RegularGrammar.right_group(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['AB*']),
                'V': set('ab'),
                'T': [
                    [' ', 'AB*'],
                    ['a', 'AB*'],
                    ['b', 'AB*']
                ],
                'S': 'AB*',
                'F': set(['AB*']),
                'G': {
                    'group': set(['AB*'])
                }
            }
        })

    @staticmethod
    def test_character_range_forward():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Forward Character Range',
            'expressions': {
                'range': [RegularGrammar.left_class(), 'a', RegularGrammar.character_range(), 'c', RegularGrammar.right_class()]
            },
            'DFA': {
                'Q': set(['S', 'F', 'Err']),
                'V': set('abc'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'F',   'Err'],
                    ['a', 'F',   'Err', 'Err'],
                    ['b', 'F',   'Err', 'Err'],
                    ['c', 'F',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'range': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_character_range_backward():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Backward Character Range',
            'expressions': {
                'range': [RegularGrammar.left_class(), 'c', RegularGrammar.character_range(), 'a', RegularGrammar.right_class()]
            },
            'DFA': {
                'Q': set(['S', 'F', 'Err']),
                'V': set('abc'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'F',   'Err'],
                    ['a', 'F',   'Err', 'Err'],
                    ['b', 'F',   'Err', 'Err'],
                    ['c', 'F',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'range': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_character_range_negation():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Literal Negation Character Range',
            'expressions': {
                'range': [RegularGrammar.left_class(), 'a', RegularGrammar.character_range(), '^', RegularGrammar.right_class()]
            },
            'DFA': {
                'Q': set(['S', 'F', 'Err']),
                'V': set('^_`a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'F',   'Err'],
                    ['^', 'F',   'Err', 'Err'],
                    ['_', 'F',   'Err', 'Err'],
                    ['`', 'F',   'Err', 'Err'],
                    ['a', 'F',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'range': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_character_range_negated():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Negated Character Range',
            'expressions': {
                'range': [RegularGrammar.left_class(), RegularGrammar.character_negation(), '!',
                          RegularGrammar.character_range(), '~', RegularGrammar.right_class(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['S']),
                'V': set(' \t\n\r\f\v'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'S'],
                    [' ',  'S'],
                    ['\t', 'S'],
                    ['\n', 'S'],
                    ['\r', 'S'],
                    ['\f', 'S'],
                    ['\v', 'S']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S']),
                'G': {
                    'range': set(['S'])
                }
            }
        })

    @staticmethod
    def test_character_range_literal():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Character Class with Literal Right Bracket',
            'expressions': {
                'class': [RegularGrammar.left_class(), ']', RegularGrammar.right_class(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['S']),
                'V': set(']'),
                'T': [
                    [' ', 'S'],
                    [']', 'S']
                ],
                'S': 'S',
                'F': set(['S']),
                'G': {
                    'class': set(['S'])
                }
            }
        })

    @staticmethod
    def test_character_class():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Character Class',
            'expressions': {
                'class': [RegularGrammar.left_class(), 'a', 'b', 'c', RegularGrammar.right_class()]
            },
            'DFA': {
                'Q': set(['S', 'F', 'Err']),
                'V': set('abc'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'F',   'Err'],
                    ['a', 'F',   'Err', 'Err'],
                    ['b', 'F',   'Err', 'Err'],
                    ['c', 'F',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'class': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_character_class_duplicates():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Character Class with Copies',
            'expressions': {
                'class': [RegularGrammar.left_class(), 'a', 'a', 'a', RegularGrammar.right_class()]
            },
            'DFA': {
                'Q': set(['S', 'F', 'Err']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'F',   'Err'],
                    ['a', 'F',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'class': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_character_class_negated():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Negated Character Class',
            'expressions': {
                'class': [RegularGrammar.left_class(), RegularGrammar.character_negation(), '^', '!', '"', '#', '$', '%',
                          '&', '\'', '(', ')', '*', '+', ',', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8',
                          '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                          'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '\\', '[', ']',
                          '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                          'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '-',
                          RegularGrammar.right_class(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['S']),
                'V': set(' \t\n\r\f\v'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'S'],
                    [' ',  'S'],
                    ['\t', 'S'],
                    ['\n', 'S'],
                    ['\r', 'S'],
                    ['\f', 'S'],
                    ['\v', 'S']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S']),
                'G': {
                    'class': set(['S'])
                }
            }
        })

    @staticmethod
    def test_char_class_range_combo_1():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Character Class Range Combo',
            'expressions': {
                'class': [RegularGrammar.left_class(), 'a', 'b', 'c', RegularGrammar.character_range(), 'e',
                          RegularGrammar.right_class(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['S']),
                'V': set('abcde'),
                'T': [
                    [' ', 'S'],
                    ['a', 'S'],
                    ['b', 'S'],
                    ['c', 'S'],
                    ['d', 'S'],
                    ['e', 'S']
                ],
                'S': 'S',
                'F': set(['S']),
                'G': {
                    'class': set(['S'])
                }
            }
        })

    @staticmethod
    def test_char_class_range_combo_2():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Character Range Class Combo',
            'expressions': {
                'class': [RegularGrammar.left_class(), 'a', RegularGrammar.character_range(), 'c', 'd', 'e',
                          RegularGrammar.right_class(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['S']),
                'V': set('abcde'),
                'T': [
                    [' ', 'S'],
                    ['a', 'S'],
                    ['b', 'S'],
                    ['c', 'S'],
                    ['d', 'S'],
                    ['e', 'S']
                ],
                'S': 'S',
                'F': set(['S']),
                'G': {
                    'class': set(['S'])
                }
            }
        })

    @staticmethod
    def test_exact_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Exact Interval',
            'expressions': {
                'exact_count': ['a', RegularGrammar.left_interval(), 2, RegularGrammar.right_interval()],
            },
            'DFA': {
                'Q': set(['S', 'A1', 'F', 'Err']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',  'A1', 'F',   'Err'],
                    ['a', 'A1', 'F',  'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'exact_count': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_small_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Small Interval',
            'expressions': {
                'small_interval': ['a', RegularGrammar.left_interval(), 2, 3, RegularGrammar.right_interval()],
            },
            'DFA': {
                'Q': set(['S', 'A1', 'A2', 'F', 'Err']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',  'A1', 'A2', 'F',   'Err'],
                    ['a', 'A1', 'A2', 'F',  'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['A2', 'F']),
                'G': {
                    'small_interval': set(['A2', 'F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_minimum_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Minimum Interval',
            'expressions': {
                'minimum_interval': ['a', RegularGrammar.left_interval(), 2, 0, RegularGrammar.right_interval()],
            },
            'DFA': {
                'Q': set(['S', 'A1', 'F']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',  'A1', 'F'],
                    ['a', 'A1', 'F',  'F']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'minimum_interval': set(['F'])
                }
            }
        })

    @staticmethod
    def test_maximum_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Maximum Interval',
            'expressions': {
                'maximum_interval': ['a', RegularGrammar.left_interval(), 0, 2, RegularGrammar.right_interval()],
            },
            'DFA': {
                'Q': set(['S', 'A1', 'F', 'Err']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',  'A1', 'F',   'Err'],
                    ['a', 'A1', 'F',  'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S', 'A1', 'F']),
                'G': {
                    'maximum_interval': set(['S', 'F', 'A1']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_complex_interval():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Complex Interval',
            'expressions': {
                'complex_interval': [RegularGrammar.left_group(), 'a', RegularGrammar.kleene_star(), RegularGrammar.right_group(),
                                     RegularGrammar.left_interval(), 2, 0, RegularGrammar.right_interval()],
            },
            'DFA': {
                'Q': set(['S']),
                'V': set('a'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S'],
                    ['a', 'S']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S']),
                'G': {
                    'complex_interval': set(['S'])
                }
            }
        })

    @staticmethod
    def test_operator_literals():
        """
        Ensure operator literals produce the expected output.
        """
        TestScanner._run(**{
            'name': 'Operator Alpha Literals',
            'expressions': {
                'concat': ['.'],
                'alt': ['|'],
                'star': ['*'],
                'question': ['?'],
                'plus': ['+'],
                'slash': ['\\'],
                'lparen': ['('],
                'rparen': [')'],
                'lbracket': ['['],
                'rbracket': [']']
            },
            'DFA': {
                'Q': set(['S', 'F', 'Err']),
                'V': set('.|*?+\\()[]'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'S', 'F',   'Err'],
                    ['.',  'F', 'Err', 'Err'],
                    ['|',  'F', 'Err', 'Err'],
                    ['*',  'F', 'Err', 'Err'],
                    ['?',  'F', 'Err', 'Err'],
                    ['+',  'F', 'Err', 'Err'],
                    ['\\', 'F', 'Err', 'Err'],
                    ['(',  'F', 'Err', 'Err'],
                    [')',  'F', 'Err', 'Err'],
                    ['[',  'F', 'Err', 'Err'],
                    [']',  'F', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'concat': set(['F']),
                    'alt': set(['F']),
                    'star': set(['F']),
                    'question': set(['F']),
                    'plus': set(['F']),
                    'slash': set(['F']),
                    'lparen': set(['F']),
                    'rparen': set(['F']),
                    'lbracket': set(['F']),
                    'rbracket': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_precedence_star_plus():
        """
        Ensure association operator precedence produces the expected output.
        same precendence so nothing interesting here
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.kleene_star(), RegularGrammar.kleene_plus()]
            },
            'DFA': {
                'Q': set(['A']),
                'V': set('a'),
                'T': [
                    [' ', 'A'],
                    ['a', 'A']
                ],
                'S': 'A',
                'F': set(['A']),
                'G': {
                    'expression': set(['A']),
                }
            }
        })

    @staticmethod
    def test_precedence_star_maybe():
        """
        Ensure association operator precedence produces the expected output.
        same precendence so nothing interesting here
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.kleene_star(), RegularGrammar.maybe()]
            },
            'DFA': {
                'Q': set(['A']),
                'V': set('a'),
                'T': [
                    [' ', 'A'],
                    ['a', 'A']
                ],
                'S': 'A',
                'F': set(['A']),
                'G': {
                    'expression': set(['A']),
                }
            }
        })

    @staticmethod
    def test_precedence_star_concat():
        """
        Ensure association operator precedence produces the expected output.
        '*' is higher than '+' so a with any number of b instead of an number of
        ab pairs
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.concatenation(), 'b', RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'A',   'B',   'Err'],
                    ['a', 'B',   'Err', 'Err'],
                    ['b', 'Err', 'B',   'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'A',
                'F': set(['B']),
                'G': {
                    'expression': set(['B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_precedence_star_alternate():
        """
        Ensure association operator precedence produces the expected output.
        '*' is higher than '|' so a or any number of b's instead of an number
        of a or b's
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.alternative(), 'b', RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S', 'A',   'B',   'Err'],
                    ['a', 'A', 'Err', 'Err', 'Err'],
                    ['b', 'B', 'Err', 'B',   'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S', 'A', 'B']),
                'G': {
                    'expression': set(['S', 'A', 'B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_precedence_plus_maybe():
        """
        Ensure association operator precedence produces the expected output.
        same precendence so nothing interesting here
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.kleene_plus(), RegularGrammar.maybe()]
            },
            'DFA': {
                'Q': set(['A']),
                'V': set('a'),
                'T': [
                    [' ', 'A'],
                    ['a', 'A']
                ],
                'S': 'A',
                'F': set(['A']),
                'G': {
                    'expression': set(['A']),
                }
            }
        })

    @staticmethod
    def test_precedence_plus_concat():
        """
        Ensure association operator precedence produces the expected output.
        '+' is higher than '.' so a and 1 or more b's instead one or more ab+
        pairs.
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.concatenation(), 'b', RegularGrammar.kleene_plus()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A',   'B',   'Err'],
                    ['a', 'A',   'Err', 'Err', 'Err'],
                    ['b', 'Err', 'B',   'B',   'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['B']),
                'G': {
                    'expression': set(['B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_precedence_plus_alternate():
        """
        Ensure association operator precedence produces the expected output.
        '+' is higher than '|' so a or 1 or more b's instead one or more a or b
        pairs.
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.alternative(), 'b', RegularGrammar.kleene_plus()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S', 'A',   'B',   'Err'],
                    ['a', 'A', 'Err', 'Err', 'Err'],
                    ['b', 'B', 'Err', 'B',   'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['A', 'B']),
                'G': {
                    'expression': set(['A', 'B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_precedence_maybe_concat():
        """
        Ensure association operator precedence produces the expected output.
        '?' is higher than '.' so a and possibly 1 b instead of possible one ab
        pair.
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.concatenation(), 'b', RegularGrammar.maybe()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A',   'B',   'Err'],
                    ['a', 'A',   'Err', 'Err', 'Err'],
                    ['b', 'Err', 'B',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['A', 'B']),
                'G': {
                    'expression': set(['A', 'B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_precedence_maybe_alternate():
        """
        Ensure association operator precedence produces the expected output.
        '?' is higher than '|' so a or possibly 1 b instead of 1 possible a or
        b.
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.alternative(), 'b', RegularGrammar.maybe()]
            },
            'DFA': {
                'Q': set(['S', 'AB', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',  'AB',  'Err'],
                    ['a', 'AB', 'Err', 'Err'],
                    ['b', 'AB', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S', 'AB']),
                'G': {
                    'expression': set(['S', 'AB']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_precedence_concat_alt():
        """
        Ensure association operator precedence produces the expected output.
        '.' is higher than '|' so ab or possibly c instead a and b or c.
        """
        TestScanner._run(**{
            'name': 'Association',
            'expressions': {
                'expression': ['a', RegularGrammar.concatenation(), 'b', RegularGrammar.alternative(), 'c']
            },
            'DFA': {
                'Q': set(['S', 'A', 'BC', 'Err']),
                'V': set('abc'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A',   'BC',  'Err'],
                    ['a', 'A',   'Err', 'Err', 'Err'],
                    ['b', 'Err', 'BC',  'Err', 'Err'],
                    ['c', 'BC',  'Err', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['BC']),
                'G': {
                    'expression': set(['BC']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_concat_implicit_star():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Implicit Concatenation Star Operator',
            'expressions': {
                'permutation1': ['a', RegularGrammar.kleene_star(), 'b'],
                'permutation2': ['a', RegularGrammar.kleene_star(), RegularGrammar.left_group(), 'b', RegularGrammar.right_group()],
                'permutation3': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.kleene_star(), 'b'],
                'permutation4': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.kleene_star(),
                                 RegularGrammar.left_group(), 'b', RegularGrammar.right_group()]
            },
            'DFA': {
                'Q': set(['A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'A', 'B',   'Err'],
                    ['a', 'A', 'Err', 'Err'],
                    ['b', 'B', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'A',
                'F': set(['B']),
                'G': {
                    'permutation1': set(['B']),
                    'permutation2': set(['B']),
                    'permutation3': set(['B']),
                    'permutation4': set(['B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_concat_implicit_plus():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Implicit Concatenation Plus Operator',
            'expressions': {
                'permutation1': ['a', RegularGrammar.kleene_plus(), 'b'],
                'permutation2': ['a', RegularGrammar.kleene_plus(), RegularGrammar.left_group(), 'b', RegularGrammar.right_group()],
                'permutation3': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.kleene_plus(), 'b'],
                'permutation4': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.kleene_plus(),
                                 RegularGrammar.left_group(), 'b', RegularGrammar.right_group()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A', 'B',   'Err'],
                    ['a', 'A',   'A', 'Err', 'Err'],
                    ['b', 'Err', 'B', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['B']),
                'G': {
                    'permutation1': set(['B']),
                    'permutation2': set(['B']),
                    'permutation3': set(['B']),
                    'permutation4': set(['B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_concat_implicit_maybe():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Implicit Concatenation Question Operator',
            'expressions': {
                'permutation1': ['a', RegularGrammar.maybe(), 'b'],
                'permutation2': ['a', RegularGrammar.maybe(), RegularGrammar.left_group(), 'b', RegularGrammar.right_group()],
                'permutation3': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.maybe(), 'b'],
                'permutation4': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.maybe(),
                                 RegularGrammar.left_group(), 'b', RegularGrammar.right_group()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S', 'A',   'B',   'Err'],
                    ['a', 'A', 'Err', 'Err', 'Err'],
                    ['b', 'B', 'B',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['B']),
                'G': {
                    'permutation1': set(['B']),
                    'permutation2': set(['B']),
                    'permutation3': set(['B']),
                    'permutation4': set(['B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_concat_implicit_alternate():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Implicit Concatenation Question Operator',
            'expressions': {
                'permutation1': ['a', RegularGrammar.alternative(), 'b'],
                'permutation2': ['a', RegularGrammar.alternative(), RegularGrammar.left_group(), 'b', RegularGrammar.right_group()],
                'permutation3': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.alternative(), 'b'],
                'permutation4': [RegularGrammar.left_group(), 'a', RegularGrammar.right_group(), RegularGrammar.alternative(),
                                 RegularGrammar.left_group(), 'b', RegularGrammar.right_group()]
            },
            'DFA': {
                'Q': set(['S', 'AB', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',  'AB',  'Err'],
                    ['a', 'AB', 'Err', 'Err'],
                    ['b', 'AB', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['AB']),
                'G': {
                    'permutation1': set(['AB']),
                    'permutation2': set(['AB']),
                    'permutation3': set(['AB']),
                    'permutation4': set(['AB']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_miscellaneous_1():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Randomness 1',
            'expressions': {
                'random': ['a', RegularGrammar.kleene_star(), RegularGrammar.left_group(), 'b', RegularGrammar.alternative(),
                           'c', 'd', RegularGrammar.right_group(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['AC', 'B', 'DE', 'Err']),
                'V': set('abcd'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'AC',  'B',   'DE',  'Err'],
                    ['a', 'AC',  'Err', 'Err', 'Err'],
                    ['b', 'DE',  'Err', 'DE',  'Err'],
                    ['c', 'B',   'Err', 'B',   'Err'],
                    ['d', 'Err', 'DE',  'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'AC',
                'F': set(['AC', 'DE']),
                'G': {
                    'random': set(['AC', 'DE']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_miscellaneous_2():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Randomness 2',
            'expressions': {
                'random': ['a', RegularGrammar.maybe(), 'b', RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['A', 'B', 'Err']),
                'V': set('ab'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'A',  'B',   'Err'],
                    ['a', 'B',  'Err', 'Err'],
                    ['b', 'B',  'B',   'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'A',
                'F': set(['A', 'B']),
                'G': {
                    'random': set(['A', 'B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_miscellaneous_3():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Randomness 3',
            'expressions': {
                'random': [RegularGrammar.left_group(), 'a', RegularGrammar.kleene_star(), 'b',
                           RegularGrammar.right_group(), RegularGrammar.alternative(), RegularGrammar.left_group(),
                           'a', RegularGrammar.concatenation(), 'b', 'c', 'd', RegularGrammar.concatenation(), 'e',
                           RegularGrammar.right_group()]
            },
            'DFA': {
                'Q': set(['S', 'A', 'A*', 'B', 'C', 'D', 'F', 'Err']),
                'V': set('abcde'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'A',   'A*',  'B',   'C',   'D',   'F',   'Err'],
                    ['a', 'A',   'A*',  'A*',  'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['b', 'F',   'B',   'F',   'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['c', 'Err', 'Err', 'Err', 'C',   'Err', 'Err', 'Err', 'Err'],
                    ['d', 'Err', 'Err', 'Err', 'Err', 'D',   'Err', 'Err', 'Err'],
                    ['e', 'Err', 'Err', 'Err', 'Err', 'Err', 'F',   'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F', 'B']),
                'G': {
                    'random': set(['F', 'B']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_miscellaneous_4():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Randomness 4',
            'expressions': {
                'random': [RegularGrammar.left_group(), 'f', 'o', 'o', RegularGrammar.right_group(),
                           RegularGrammar.maybe(), RegularGrammar.left_group(), 'b', 'a', 'r',
                           RegularGrammar.right_group(), RegularGrammar.kleene_plus()]
            },
            'DFA': {
                'Q': set(['S', 'F', 'FO', 'FOO', 'B', 'BA', 'BAR', 'Err']),
                'V': set('fobar'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'F',   'FO',  'FOO', 'B',   'BA',  'BAR', 'Err'],
                    ['f', 'F',   'Err', 'Err', 'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['o', 'Err', 'FO',  'FOO', 'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['b', 'B',   'Err', 'Err', 'B',   'Err', 'Err', 'B',   'Err'],
                    ['a', 'Err', 'Err', 'Err', 'Err', 'BA',  'Err', 'Err', 'Err'],
                    ['r', 'Err', 'Err', 'Err', 'Err', 'Err', 'BAR', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['BAR']),
                'G': {
                    'random': set(['BAR']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_white_space():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'White Space',
            'expressions': {
                'white': [RegularGrammar.left_group(), ' ', RegularGrammar.alternative(), '\t', RegularGrammar.alternative(),
                          '\n', RegularGrammar.alternative(), '\r', RegularGrammar.alternative(), '\f',
                          RegularGrammar.alternative(), '\v', RegularGrammar.right_group(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['S']),
                'V': set(' \t\n\r\f\v'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'S'],
                    [' ',  'S'],
                    ['\t', 'S'],
                    ['\n', 'S'],
                    ['\r', 'S'],
                    ['\f', 'S'],
                    ['\v', 'S']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['S']),
                'G': {
                    'white': set(['S'])
                }
            }
        })

    @staticmethod
    def test_boolean():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Boolean',
            'expressions': {
                'bool': [RegularGrammar.left_group(), 't', 'r', 'u', 'e', RegularGrammar.right_group(),
                         RegularGrammar.alternative(), RegularGrammar.left_group(), 'f', 'a', 'l', 's', 'e',
                         RegularGrammar.right_group()]
            },
            'DFA': {
                'Q': set(['S', 'T', 'R', 'F', 'A', 'L', 'US', 'E', 'Err']),
                'V': set('truefals'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',   'T',   'R',   'F',   'A',   'L',   'US',  'E',   'Err'],
                    ['t', 'T',   'Err', 'Err', 'Err', 'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['r', 'Err', 'R',   'Err', 'Err', 'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['u', 'Err', 'Err', 'US',  'Err', 'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['e', 'Err', 'Err', 'Err', 'Err', 'Err', 'Err', 'E',   'Err', 'Err'],
                    ['f', 'F',   'Err', 'Err', 'Err', 'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['a', 'Err', 'Err', 'Err', 'A',   'Err', 'Err', 'Err', 'Err', 'Err'],
                    ['l', 'Err', 'Err', 'Err', 'Err', 'L',   'Err', 'Err', 'Err', 'Err'],
                    ['s', 'Err', 'Err', 'Err', 'Err', 'Err', 'US',  'Err', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['E']),
                'G': {
                    'bool': set(['E']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_character():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Character',
            'expressions': {
                'char': ['\'', RegularGrammar.left_class(), RegularGrammar.character_negation(), RegularGrammar.right_class(), '\'']
            },
            'DFA': {
                'Q': set(['S', '_1', '_2', 'F', 'Err']),
                'V': set('0123456789 \t\v\f\r\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'S',   '_1', '_2',  'F',   'Err'],
                    ['#',  'Err', '_2', 'Err', 'Err', 'Err'],
                    [';',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['\n', 'Err', '_2', 'Err', 'Err', 'Err'],
                    ['0',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['1',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['2',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['3',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['4',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['5',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['6',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['7',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['8',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['9',  'Err', '_2', 'Err', 'Err', 'Err'],
                    [' ',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['\t', 'Err', '_2', 'Err', 'Err', 'Err'],
                    ['\v', 'Err', '_2', 'Err', 'Err', 'Err'],
                    ['\f', 'Err', '_2', 'Err', 'Err', 'Err'],
                    ['\r', 'Err', '_2', 'Err', 'Err', 'Err'],
                    ['a',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['b',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['c',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['d',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['e',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['f',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['g',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['h',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['i',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['j',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['k',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['l',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['m',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['n',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['o',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['p',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['q',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['r',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['s',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['t',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['u',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['v',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['w',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['x',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['y',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['z',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['A',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['B',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['C',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['D',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['E',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['F',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['G',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['H',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['I',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['J',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['K',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['L',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['M',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['N',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['O',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['P',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['Q',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['R',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['S',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['T',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['U',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['V',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['W',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['X',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['Y',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['Z',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['!',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['"',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['$',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['%',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['&',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['\'', '_1',  '_2', 'F',   'Err', 'Err'],
                    ['(',  'Err', '_2', 'Err', 'Err', 'Err'],
                    [')',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['*',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['+',  'Err', '_2', 'Err', 'Err', 'Err'],
                    [',',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['-',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['.',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['/',  'Err', '_2', 'Err', 'Err', 'Err'],
                    [':',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['<',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['=',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['>',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['?',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['@',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['[',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['\\', 'Err', '_2', 'Err', 'Err', 'Err'],
                    [']',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['^',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['_',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['`',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['{',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['|',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['}',  'Err', '_2', 'Err', 'Err', 'Err'],
                    ['~',  'Err', '_2', 'Err', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'char': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_string():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'String',
            'expressions': {
                'str': ['"', RegularGrammar.left_class(), RegularGrammar.character_negation(), '"',
                        RegularGrammar.right_class(), RegularGrammar.kleene_star(), '"']
            },
            'DFA': {
                'Q': set(['S', '_', 'F', 'Err']),
                'V': set('0123456789 \t\v\f\r\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'S',   '_', 'F',   'Err'],
                    ['#',  'Err', '_', 'Err', 'Err'],
                    [';',  'Err', '_', 'Err', 'Err'],
                    ['\n', 'Err', '_', 'Err', 'Err'],
                    ['0',  'Err', '_', 'Err', 'Err'],
                    ['1',  'Err', '_', 'Err', 'Err'],
                    ['2',  'Err', '_', 'Err', 'Err'],
                    ['3',  'Err', '_', 'Err', 'Err'],
                    ['4',  'Err', '_', 'Err', 'Err'],
                    ['5',  'Err', '_', 'Err', 'Err'],
                    ['6',  'Err', '_', 'Err', 'Err'],
                    ['7',  'Err', '_', 'Err', 'Err'],
                    ['8',  'Err', '_', 'Err', 'Err'],
                    ['9',  'Err', '_', 'Err', 'Err'],
                    [' ',  'Err', '_', 'Err', 'Err'],
                    ['\t', 'Err', '_', 'Err', 'Err'],
                    ['\v', 'Err', '_', 'Err', 'Err'],
                    ['\f', 'Err', '_', 'Err', 'Err'],
                    ['\r', 'Err', '_', 'Err', 'Err'],
                    ['a',  'Err', '_', 'Err', 'Err'],
                    ['b',  'Err', '_', 'Err', 'Err'],
                    ['c',  'Err', '_', 'Err', 'Err'],
                    ['d',  'Err', '_', 'Err', 'Err'],
                    ['e',  'Err', '_', 'Err', 'Err'],
                    ['f',  'Err', '_', 'Err', 'Err'],
                    ['g',  'Err', '_', 'Err', 'Err'],
                    ['h',  'Err', '_', 'Err', 'Err'],
                    ['i',  'Err', '_', 'Err', 'Err'],
                    ['j',  'Err', '_', 'Err', 'Err'],
                    ['k',  'Err', '_', 'Err', 'Err'],
                    ['l',  'Err', '_', 'Err', 'Err'],
                    ['m',  'Err', '_', 'Err', 'Err'],
                    ['n',  'Err', '_', 'Err', 'Err'],
                    ['o',  'Err', '_', 'Err', 'Err'],
                    ['p',  'Err', '_', 'Err', 'Err'],
                    ['q',  'Err', '_', 'Err', 'Err'],
                    ['r',  'Err', '_', 'Err', 'Err'],
                    ['s',  'Err', '_', 'Err', 'Err'],
                    ['t',  'Err', '_', 'Err', 'Err'],
                    ['u',  'Err', '_', 'Err', 'Err'],
                    ['v',  'Err', '_', 'Err', 'Err'],
                    ['w',  'Err', '_', 'Err', 'Err'],
                    ['x',  'Err', '_', 'Err', 'Err'],
                    ['y',  'Err', '_', 'Err', 'Err'],
                    ['z',  'Err', '_', 'Err', 'Err'],
                    ['A',  'Err', '_', 'Err', 'Err'],
                    ['B',  'Err', '_', 'Err', 'Err'],
                    ['C',  'Err', '_', 'Err', 'Err'],
                    ['D',  'Err', '_', 'Err', 'Err'],
                    ['E',  'Err', '_', 'Err', 'Err'],
                    ['F',  'Err', '_', 'Err', 'Err'],
                    ['G',  'Err', '_', 'Err', 'Err'],
                    ['H',  'Err', '_', 'Err', 'Err'],
                    ['I',  'Err', '_', 'Err', 'Err'],
                    ['J',  'Err', '_', 'Err', 'Err'],
                    ['K',  'Err', '_', 'Err', 'Err'],
                    ['L',  'Err', '_', 'Err', 'Err'],
                    ['M',  'Err', '_', 'Err', 'Err'],
                    ['N',  'Err', '_', 'Err', 'Err'],
                    ['O',  'Err', '_', 'Err', 'Err'],
                    ['P',  'Err', '_', 'Err', 'Err'],
                    ['Q',  'Err', '_', 'Err', 'Err'],
                    ['R',  'Err', '_', 'Err', 'Err'],
                    ['S',  'Err', '_', 'Err', 'Err'],
                    ['T',  'Err', '_', 'Err', 'Err'],
                    ['U',  'Err', '_', 'Err', 'Err'],
                    ['V',  'Err', '_', 'Err', 'Err'],
                    ['W',  'Err', '_', 'Err', 'Err'],
                    ['X',  'Err', '_', 'Err', 'Err'],
                    ['Y',  'Err', '_', 'Err', 'Err'],
                    ['Z',  'Err', '_', 'Err', 'Err'],
                    ['!',  'Err', '_', 'Err', 'Err'],
                    ['"',  '_',   'F', 'Err', 'Err'],
                    ['$',  'Err', '_', 'Err', 'Err'],
                    ['%',  'Err', '_', 'Err', 'Err'],
                    ['&',  'Err', '_', 'Err', 'Err'],
                    ['\'', 'Err', '_', 'Err', 'Err'],
                    ['(',  'Err', '_', 'Err', 'Err'],
                    [')',  'Err', '_', 'Err', 'Err'],
                    ['*',  'Err', '_', 'Err', 'Err'],
                    ['+',  'Err', '_', 'Err', 'Err'],
                    [',',  'Err', '_', 'Err', 'Err'],
                    ['-',  'Err', '_', 'Err', 'Err'],
                    ['.',  'Err', '_', 'Err', 'Err'],
                    ['/',  'Err', '_', 'Err', 'Err'],
                    [':',  'Err', '_', 'Err', 'Err'],
                    ['<',  'Err', '_', 'Err', 'Err'],
                    ['=',  'Err', '_', 'Err', 'Err'],
                    ['>',  'Err', '_', 'Err', 'Err'],
                    ['?',  'Err', '_', 'Err', 'Err'],
                    ['@',  'Err', '_', 'Err', 'Err'],
                    ['[',  'Err', '_', 'Err', 'Err'],
                    ['\\', 'Err', '_', 'Err', 'Err'],
                    [']',  'Err', '_', 'Err', 'Err'],
                    ['^',  'Err', '_', 'Err', 'Err'],
                    ['_',  'Err', '_', 'Err', 'Err'],
                    ['`',  'Err', '_', 'Err', 'Err'],
                    ['{',  'Err', '_', 'Err', 'Err'],
                    ['|',  'Err', '_', 'Err', 'Err'],
                    ['}',  'Err', '_', 'Err', 'Err'],
                    ['~',  'Err', '_', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'str': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_identifier():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Identifiers',
            'expressions': {
                'id': [RegularGrammar.left_class(), '_', 'a', RegularGrammar.character_range(), 'z', 'A', RegularGrammar.character_range(),
                       'Z', RegularGrammar.right_class(), RegularGrammar.left_class(), '_', 'a', RegularGrammar.character_range(), 'z',
                       'A', RegularGrammar.character_range(), 'Z', '0', RegularGrammar.character_range(), '9',
                       RegularGrammar.right_class(), RegularGrammar.kleene_star()]
            },
            'DFA': {
                'Q': set(['Char', 'DigitOrChar', 'Err']),
                'V': set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'Char',        'DigitOrChar', 'Err'],
                    ['a',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['b',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['c',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['d',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['e',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['f',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['g',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['h',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['i',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['j',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['k',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['l',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['m',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['n',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['o',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['p',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['q',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['r',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['s',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['t',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['u',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['v',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['w',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['x',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['y',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['z',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['A',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['B',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['C',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['D',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['E',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['F',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['G',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['H',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['I',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['J',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['K',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['L',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['M',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['N',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['O',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['P',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['Q',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['R',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['S',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['T',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['U',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['V',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['W',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['X',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['Y',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['Z',  'DigitOrChar', 'DigitOrChar', 'Err'],
                    ['0',  'Err',         'DigitOrChar', 'Err'],
                    ['1',  'Err',         'DigitOrChar', 'Err'],
                    ['2',  'Err',         'DigitOrChar', 'Err'],
                    ['3',  'Err',         'DigitOrChar', 'Err'],
                    ['4',  'Err',         'DigitOrChar', 'Err'],
                    ['5',  'Err',         'DigitOrChar', 'Err'],
                    ['6',  'Err',         'DigitOrChar', 'Err'],
                    ['7',  'Err',         'DigitOrChar', 'Err'],
                    ['8',  'Err',         'DigitOrChar', 'Err'],
                    ['9',  'Err',         'DigitOrChar', 'Err'],
                    ['_',  'DigitOrChar', 'DigitOrChar', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'Char',
                'F': set(['DigitOrChar']),
                'G': {
                    'id': set(['DigitOrChar']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_integer():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Integer',
            'expressions': {
                'int': ['0', RegularGrammar.alternative(), RegularGrammar.left_group(), RegularGrammar.left_class(), '-', '+',
                        RegularGrammar.right_class(), RegularGrammar.maybe(), RegularGrammar.left_class(), '1',
                        RegularGrammar.character_range(), '9', RegularGrammar.right_class(), RegularGrammar.left_class(),
                        '0', RegularGrammar.character_range(), '9', RegularGrammar.right_class(), RegularGrammar.kleene_star(),
                        RegularGrammar.right_group()]
            },
            'DFA': {
                'Q': set(['S', 'Zero', 'Sign', 'Int', 'Err']),
                'V': set('+-0123456789'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',    'Zero', 'Sign', 'Int', 'Err'],
                    ['+', 'Sign', 'Err',  'Err',  'Err', 'Err'],
                    ['-', 'Sign', 'Err',  'Err',  'Err', 'Err'],
                    ['0', 'Zero', 'Err',  'Err',  'Int', 'Err'],
                    ['1', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['2', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['3', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['4', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['5', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['6', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['7', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['8', 'Int',  'Err',  'Int',  'Int', 'Err'],
                    ['9', 'Int',  'Err',  'Int',  'Int', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['Zero', 'Int']),
                'G': {
                    'int': set(['Zero', 'Int']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_float():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Float',
            'expressions': {
                'float': [RegularGrammar.left_class(), '-', '+', RegularGrammar.right_class(), RegularGrammar.maybe(),
                          RegularGrammar.left_class(), '0', RegularGrammar.character_range(), '9', RegularGrammar.right_class(),
                          RegularGrammar.kleene_star(), '.', RegularGrammar.maybe(), RegularGrammar.left_class(), '0',
                          RegularGrammar.character_range(), '9', RegularGrammar.right_class(), RegularGrammar.kleene_plus(),
                          RegularGrammar.left_group(), RegularGrammar.left_class(), 'e', 'E', RegularGrammar.right_class(),
                          RegularGrammar.left_class(), '-', '+', RegularGrammar.right_class(), RegularGrammar.maybe(),
                          RegularGrammar.left_class(), '0', RegularGrammar.character_range(), '9', RegularGrammar.right_class(),
                          RegularGrammar.kleene_plus(), RegularGrammar.right_group(), RegularGrammar.maybe()]
            },
            'DFA': {
                'Q': set(['S', 'WholePart', 'ExpPart', 'FractionPart', 'eSignum', 'Sigfrac', 'Sigexp', 'Signum', 'Err']),
                'V': set('+-.0123456789eE'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ', 'S',         'WholePart', 'ExpPart', 'FractionPart', 'eSignum', 'Sigfrac',      'Sigexp',  'Signum',    'Err'],
                    ['+', 'Signum',    'Err',       'Err',     'Err',          'Err',     'Err',          'eSignum', 'Err',       'Err'],
                    ['-', 'Signum',    'Err',       'Err',     'Err',          'Err',     'Err',          'eSignum', 'Err',       'Err'],
                    ['.', 'Sigfrac',   'Sigfrac',   'Err',     'Err',          'Err',     'Err',          'Err',     'Sigfrac',   'Err'],
                    ['0', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['1', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['2', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['3', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['4', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['5', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['6', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['7', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['8', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['9', 'WholePart', 'WholePart', 'ExpPart', 'FractionPart', 'ExpPart', 'FractionPart', 'ExpPart', 'WholePart', 'Err'],
                    ['E', 'Err',       'Sigexp',    'Err',     'Sigexp',       'Err',     'Err',          'Err',     'Err',       'Err'],
                    ['e', 'Err',       'Sigexp',    'Err',     'Sigexp',       'Err',     'Err',          'Err',     'Err',       'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['WholePart', 'ExpPart', 'FractionPart']),
                'G': {
                    'float': set(['WholePart', 'ExpPart', 'FractionPart']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_line_comment():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Line Comment',
            'expressions': {
                'comment': [RegularGrammar.left_group(), '#', RegularGrammar.alternative(), ';', RegularGrammar.right_group(),
                            RegularGrammar.left_class(), RegularGrammar.character_negation(), '\n', RegularGrammar.right_class(),
                            RegularGrammar.kleene_star(), '\n']
            },
            'DFA': {
                'Q': set(['S', '_', 'F', 'Err']),
                'V': set('0123456789 \t\v\f\r\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'S',   '_', 'F',   'Err'],
                    ['#',  '_',   '_', 'Err', 'Err'],
                    [';',  '_',   '_', 'Err', 'Err'],
                    ['\n', 'Err', 'F', 'Err', 'Err'],
                    ['0',  'Err', '_', 'Err', 'Err'],
                    ['1',  'Err', '_', 'Err', 'Err'],
                    ['2',  'Err', '_', 'Err', 'Err'],
                    ['3',  'Err', '_', 'Err', 'Err'],
                    ['4',  'Err', '_', 'Err', 'Err'],
                    ['5',  'Err', '_', 'Err', 'Err'],
                    ['6',  'Err', '_', 'Err', 'Err'],
                    ['7',  'Err', '_', 'Err', 'Err'],
                    ['8',  'Err', '_', 'Err', 'Err'],
                    ['9',  'Err', '_', 'Err', 'Err'],
                    [' ',  'Err', '_', 'Err', 'Err'],
                    ['\t', 'Err', '_', 'Err', 'Err'],
                    ['\v', 'Err', '_', 'Err', 'Err'],
                    ['\f', 'Err', '_', 'Err', 'Err'],
                    ['\r', 'Err', '_', 'Err', 'Err'],
                    ['a',  'Err', '_', 'Err', 'Err'],
                    ['b',  'Err', '_', 'Err', 'Err'],
                    ['c',  'Err', '_', 'Err', 'Err'],
                    ['d',  'Err', '_', 'Err', 'Err'],
                    ['e',  'Err', '_', 'Err', 'Err'],
                    ['f',  'Err', '_', 'Err', 'Err'],
                    ['g',  'Err', '_', 'Err', 'Err'],
                    ['h',  'Err', '_', 'Err', 'Err'],
                    ['i',  'Err', '_', 'Err', 'Err'],
                    ['j',  'Err', '_', 'Err', 'Err'],
                    ['k',  'Err', '_', 'Err', 'Err'],
                    ['l',  'Err', '_', 'Err', 'Err'],
                    ['m',  'Err', '_', 'Err', 'Err'],
                    ['n',  'Err', '_', 'Err', 'Err'],
                    ['o',  'Err', '_', 'Err', 'Err'],
                    ['p',  'Err', '_', 'Err', 'Err'],
                    ['q',  'Err', '_', 'Err', 'Err'],
                    ['r',  'Err', '_', 'Err', 'Err'],
                    ['s',  'Err', '_', 'Err', 'Err'],
                    ['t',  'Err', '_', 'Err', 'Err'],
                    ['u',  'Err', '_', 'Err', 'Err'],
                    ['v',  'Err', '_', 'Err', 'Err'],
                    ['w',  'Err', '_', 'Err', 'Err'],
                    ['x',  'Err', '_', 'Err', 'Err'],
                    ['y',  'Err', '_', 'Err', 'Err'],
                    ['z',  'Err', '_', 'Err', 'Err'],
                    ['A',  'Err', '_', 'Err', 'Err'],
                    ['B',  'Err', '_', 'Err', 'Err'],
                    ['C',  'Err', '_', 'Err', 'Err'],
                    ['D',  'Err', '_', 'Err', 'Err'],
                    ['E',  'Err', '_', 'Err', 'Err'],
                    ['F',  'Err', '_', 'Err', 'Err'],
                    ['G',  'Err', '_', 'Err', 'Err'],
                    ['H',  'Err', '_', 'Err', 'Err'],
                    ['I',  'Err', '_', 'Err', 'Err'],
                    ['J',  'Err', '_', 'Err', 'Err'],
                    ['K',  'Err', '_', 'Err', 'Err'],
                    ['L',  'Err', '_', 'Err', 'Err'],
                    ['M',  'Err', '_', 'Err', 'Err'],
                    ['N',  'Err', '_', 'Err', 'Err'],
                    ['O',  'Err', '_', 'Err', 'Err'],
                    ['P',  'Err', '_', 'Err', 'Err'],
                    ['Q',  'Err', '_', 'Err', 'Err'],
                    ['R',  'Err', '_', 'Err', 'Err'],
                    ['S',  'Err', '_', 'Err', 'Err'],
                    ['T',  'Err', '_', 'Err', 'Err'],
                    ['U',  'Err', '_', 'Err', 'Err'],
                    ['V',  'Err', '_', 'Err', 'Err'],
                    ['W',  'Err', '_', 'Err', 'Err'],
                    ['X',  'Err', '_', 'Err', 'Err'],
                    ['Y',  'Err', '_', 'Err', 'Err'],
                    ['Z',  'Err', '_', 'Err', 'Err'],
                    ['!',  'Err', '_', 'Err', 'Err'],
                    ['"',  'Err', '_', 'Err', 'Err'],
                    ['$',  'Err', '_', 'Err', 'Err'],
                    ['%',  'Err', '_', 'Err', 'Err'],
                    ['&',  'Err', '_', 'Err', 'Err'],
                    ['\'', 'Err', '_', 'Err', 'Err'],
                    ['(',  'Err', '_', 'Err', 'Err'],
                    [')',  'Err', '_', 'Err', 'Err'],
                    ['*',  'Err', '_', 'Err', 'Err'],
                    ['+',  'Err', '_', 'Err', 'Err'],
                    [',',  'Err', '_', 'Err', 'Err'],
                    ['-',  'Err', '_', 'Err', 'Err'],
                    ['.',  'Err', '_', 'Err', 'Err'],
                    ['/',  'Err', '_', 'Err', 'Err'],
                    [':',  'Err', '_', 'Err', 'Err'],
                    ['<',  'Err', '_', 'Err', 'Err'],
                    ['=',  'Err', '_', 'Err', 'Err'],
                    ['>',  'Err', '_', 'Err', 'Err'],
                    ['?',  'Err', '_', 'Err', 'Err'],
                    ['@',  'Err', '_', 'Err', 'Err'],
                    ['[',  'Err', '_', 'Err', 'Err'],
                    ['\\', 'Err', '_', 'Err', 'Err'],
                    [']',  'Err', '_', 'Err', 'Err'],
                    ['^',  'Err', '_', 'Err', 'Err'],
                    ['_',  'Err', '_', 'Err', 'Err'],
                    ['`',  'Err', '_', 'Err', 'Err'],
                    ['{',  'Err', '_', 'Err', 'Err'],
                    ['|',  'Err', '_', 'Err', 'Err'],
                    ['}',  'Err', '_', 'Err', 'Err'],
                    ['~',  'Err', '_', 'Err', 'Err']
                ],
                # pylint: enable=bad-whitespace
                'S': 'S',
                'F': set(['F']),
                'G': {
                    'comment': set(['F']),
                    '_sink': set(['Err'])
                }
            }
        })

    @staticmethod
    def test_block_comment():
        """
        Ensure the expression produces the expected output.
        """
        TestScanner._run(**{
            'name': 'Block Comment',
            'expressions': {
                'comment': ['/', RegularGrammar.left_class(), '*', RegularGrammar.right_class(),
                            RegularGrammar.left_class(), RegularGrammar.character_negation(), RegularGrammar.right_class(),
                            RegularGrammar.kleene_star(), RegularGrammar.left_class(), '*', RegularGrammar.right_class(), '/']
            },
            'DFA': {
                'Q': set(['BEGIN', 'SINK', 'FSLASH', 'SIGEND', 'END', 'ERR']),
                'V': set('0123456789 \t\v\f\r\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
                # pylint: disable=bad-whitespace
                'T': [
                    [' ',  'BEGIN',  'SINK',   'FSLASH', 'SIGEND', 'END',    'ERR'],
                    ['/',  'FSLASH', 'SINK',   'ERR',    'END',    'SINK',   'ERR'],
                    ['*',  'ERR',    'SIGEND', 'SINK',   'SIGEND', 'SIGEND', 'ERR'],
                    ['#',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    [';',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['\n', 'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['0',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['1',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['2',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['3',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['4',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['5',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['6',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['7',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['8',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['9',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    [' ',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['\t', 'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['\v', 'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['\f', 'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['\r', 'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['a',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['b',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['c',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['d',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['e',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['f',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['g',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['h',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['i',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['j',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['k',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['l',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['m',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['n',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['o',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['p',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['q',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['r',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['s',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['t',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['u',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['v',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['w',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['x',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['y',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['z',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['A',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['B',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['C',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['D',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['E',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['F',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['G',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['H',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['I',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['J',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['K',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['L',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['M',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['N',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['O',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['P',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['Q',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['R',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['S',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['T',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['U',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['V',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['W',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['X',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['Y',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['Z',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['!',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['"',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['$',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['%',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['&',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['\'', 'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['(',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    [')',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['+',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    [',',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['-',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['.',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    [':',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['<',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['=',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['>',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['?',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['@',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['[',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['\\', 'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    [']',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['^',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['_',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['`',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['{',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['|',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['}',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR'],
                    ['~',  'ERR',    'SINK',   'ERR',    'SINK',   'SINK',   'ERR']
                ],
                # pylint: enable=bad-whitespace
                'S': 'BEGIN',
                'F': set(['END']),
                'G': {
                    'comment': set(['END']),
                    '_sink': set(['ERR'])
                }
            }
        })
