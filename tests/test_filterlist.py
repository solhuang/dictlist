from filterlist.filterlist import FilterList
from filterlist.filterlist import NotFound, InvalidList

import pytest
from copy import copy, deepcopy

people = [
    {
        'name': 'john',
        'age': 32,
        'occupation': 'fireman',
        'facts': {
            'quote': 'you miss 100% of the shots you don\'t take',
            'movie': 'Star Wars'
        },
        'pets': 'dog',
    },
    {
        'name': 'mary',
        'age': 32,
        'occupation': 'ceo',
        'facts': {
            'quote': 'Every strike brings me closer to the next home run',
            'movie': 'Fight Club'
        },
        'pets': '',
    },
    {
        'name': 'bob',
        'age': 32,
        'occupation': 'plumber',
        'facts': {
            'quote': 'We become what we think about',
            'movie': 'The Godfather'
        },
        'pets': 'cat',
    },
]
ppl = FilterList(people)


def test_init_no_initial_list():
    new_filterlist = FilterList()
    assert isinstance(new_filterlist, FilterList)
    assert isinstance(new_filterlist, list)
    assert list(new_filterlist) == []


def test_list_is_a_list_of_dictionaries():
    test_list = [1, 2, 3]
    with pytest.raises(InvalidList):
        FilterList(test_list)


def test_init_wrong_type():
    test_list = 'abcd'
    with pytest.raises(InvalidList):
        FilterList(test_list)


def test_get_returns_dict():
    assert isinstance(ppl.get(name='john'), dict)


def test_get_original_list_is_not_modified():
    tmp = deepcopy(ppl)
    ppl.get(name='john')
    assert tmp == people


def test_get_for_non_existent_item_raises_not_found_error():
    with pytest.raises(NotFound):
        ppl.get(name='barney')


def test_get_search_for_appended_item_returns_correct_results():
    new_person = {
        'name': 'jordan',
        'age': 56,
        'occupation': 'basketball player',
    }
    ppl.append(new_person)
    assert new_person == ppl.get(name='jordan')


def test_get_with_positional_args_raises_exception():

    with pytest.raises(TypeError):
        ppl.get('name')


def test_get_with_no_args_raises_exception():

    with pytest.raises(TypeError):
        ppl.get()


def test_filter_original_list_is_not_modified():
    tmp = copy(ppl)
    ppl.filter(name='john')
    assert tmp == ppl


def test_filter_match_empty_string():
    result = ppl.filter(pets='')
    assert len(result) == 1
    assert result[0]['name'] == 'mary'


def test_filter_returns_a_dict_list():
    result = ppl.filter(name='john')
    assert isinstance(result, FilterList)


def test_filter_chaining():
    result = ppl.filter(age=32).filter(name='bob')
    assert len(result) == 1
    assert isinstance(result, FilterList)


def test_filter__regex():
    items = FilterList([{'name': 'ge-0/0/0'}, {'name': 'ge-0/0/1'}, {'name': 'bvi10'}])
    expected_result = FilterList([{'name': 'ge-0/0/0'}, {'name': 'ge-0/0/1'}])
    result = items.filter(name__regex='\d/\d/\d')
    assert expected_result == result


def test_filter__iregex():
    items = FilterList([{'name': 'ge-0/0/0'}, {'name': 'ge-0/0/1'}, {'name': 'bvi10'}])
    expected_result = FilterList([{'name': 'ge-0/0/0'}, {'name': 'ge-0/0/1'}])
    result = items.filter(name__iregex='GE-\d/\d/\d')
    assert expected_result == result


def test_filter_nonexistent_key_returns_empty_list():
    assert [] == ppl.filter(abcdefg='john')


def test_filter_nonexistent_key_filtering_for_None():
    assert [] == ppl.filter(abcdefg=None)


def test_filter__contains():
    result = ppl.filter(name__contains='mar')
    assert len(result) == 1
    assert result[0]['name'] == 'mary'


def test_filter__icontains():
    result = ppl.filter(name__icontains='MAR')
    assert len(result) == 1
    assert result[0]['name'] == 'mary'


def test_filter__in():
    result = ppl.filter(name__in=['mary', 'bob'])
    assert len(result) == 2
    assert result[0]['name'] == 'mary'
    assert result[1]['name'] == 'bob'


def test_filter_with_positional_args_returns_error():

    with pytest.raises(TypeError):
        ppl.filter('name')


def test_filter_with_no_args_returns_itself():
    filtered_ppl = ppl.filter()
    assert filtered_ppl == ppl


def test_filter_matching_none_works():
    new_person = {
        'name': 'mary',
        'age': None,
        'occupation': 'ceo',
    }
    ppl.append(new_person)
    filtered_ppl = ppl.filter(age=None)
    assert filtered_ppl[0] == new_person


def test_filter__iexact():
    filtered_ppl = ppl.filter(name__iexact='JOHN')
    assert filtered_ppl == [ppl[0]]


def test_filter_nested_dicts():
    filtered_ppl = ppl.filter(facts__movie='Star Wars')
    assert filtered_ppl == [ppl[0]]


def test_get_value():
    nested = {
        'animal': {
            'dog': {
                'noises': 'woof'
            }
        }
    }
    keys = ['animal', 'dog', 'noises']
    value = ppl._get_value(keys, nested)
    assert value == 'woof'

    with pytest.raises(NotFound):
        keys = ['animal', 'cat']
        value = ppl._get_value(keys, nested)

    keys = ['animal', 'dog']
    value = ppl._get_value(keys, nested)
    assert value == {'noises': 'woof'}

    with pytest.raises(NotFound):
        keys = ['animal', 'dog', 'noises', 'woof']
        value = ppl._get_value(keys, nested)


def test_append_non_dict():
    with pytest.raises(TypeError):
        ppl.append('non_dictionary')


def test_set_non_dict():
    with pytest.raises(TypeError):
        ppl[0]('non_dictionary')


def test_get_keys():
    key_string = 'animal__contains'
    assert ppl._get_keys(key_string) == ['animal']

    key_string = 'animal__dog__mammal'
    assert ppl._get_keys(key_string) == ['animal', 'dog', 'mammal']

    key_string = 'animal__dog__mammal__iexactly'
    assert ppl._get_keys(key_string) == ['animal', 'dog', 'mammal', 'iexactly']


def test_get_operation():
    key_string = 'animal__contains'
    assert ppl._get_operation(key_string) == 'contains'

    key_string = 'animal__dog__mammal'
    assert ppl._get_operation(key_string) == 'exact'

    key_string = 'animal'
    assert ppl._get_operation(key_string) == 'exact'