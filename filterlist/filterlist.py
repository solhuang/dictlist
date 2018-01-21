from copy import copy
import re


class FilterListException(Exception):
    pass


class NotFound(FilterListException):
    pass


class InvalidList(FilterListException):
    pass


class FilterList(list):

    def __init__(self, *args, **kwargs):
        super(FilterList, self).__init__(*args, **kwargs)
        if not all(isinstance(item, dict) for item in self):
            raise InvalidList('Every element in the list must be a dictionary')

    def __setitem__(self, key, item, *args, **kwargs):
        if not isinstance(item, dict):
            raise TypeError('All elements must be a dictionary. You are trying to add the element {}, which is not a dictionary'.format(item))
        super(FilterList, self).__setitem__(key, item, *args, **kwargs)

    def append(self, value, *args, **kwargs):
        if not isinstance(value, dict):
            raise TypeError('All elements must be a dictionary. You are trying to add the element {}, which is not a dictionary.'.format(value))
        super(FilterList, self).append(value, *args, **kwargs)

    def get(self, **kwargs):
        result_list = self.filter(**kwargs)

        if not result_list:
            raise NotFound('No items found with the following filter: {}'.format(kwargs))

        if len(result_list) != 1:
            raise FilterListException('Expected to find 1 item but found {}'.format(len(self)))
        return result_list[0]

    def filter(self, **kwargs):
        """
        Accepts a list of keyword arguments to search for.
        The key can contain the following special operations __regex, __contains
        ie, you can pass in name__contains="bob", and this method will return all dictionaries in the list
        where name field contains the word "bob"
        return: new FilterList object that matches the given kwargs
        """
        filtered_result = copy(self)
        for key, value in kwargs.items():
            operation = None
            if '__' in key:
                key, operation = key.split('__')

            if operation == 'in':
                filtered_result = [item for item in filtered_result if key in item and item[key] in value]

            elif operation == 'regex':
                filtered_result = [item for item in filtered_result if key in item and re.search(value, item[key])]

            elif operation == 'contains':
                filtered_result = [item for item in filtered_result if key in item and value in item[key]]

            elif operation == 'icontains':
                filtered_result = [item for item in filtered_result if key in item and value.lower() in item[key].lower()]

            else:
                filtered_result = [item for item in filtered_result if key in item and item[key] == value]

        return self.__class__(filtered_result)

