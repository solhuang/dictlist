from filterlist.filterlist import FilterList
from filterlist.filterlist import NotFound, InvalidList

import pytest
from copy import copy, deepcopy

people = [
    {
        'name': 'john',
        'age': 32,
        'occupation': 'fireman',
    },
    {
        'name': 'mary',
        'age': 32,
        'occupation': 'ceo',
    },
    {
        'name': 'bob',
        'age': 32,
        'occupation': 'plumber',
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


def test_filter_original_list_is_not_modified():
    tmp = copy(ppl)
    ppl.filter(name='john')
    assert tmp == ppl


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


def test_append_non_dict():
    with pytest.raises(TypeError):
        ppl.append('non_dictionary')


def test_set_non_dict():
    with pytest.raises(TypeError):
        ppl[0]('non_dictionary')