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

        self.valid_operations = ['in', 'regex', 'iregex', 'contains', 'icontains', 'iexact']

    def __setitem__(self, key, item, *args, **kwargs):
        if not isinstance(item, dict):
            raise TypeError('All elements must be a dictionary. You are trying to add the element {}, which is not a dictionary'.format(item))
        super(FilterList, self).__setitem__(key, item, *args, **kwargs)

    def append(self, value, *args, **kwargs):
        if not isinstance(value, dict):
            raise TypeError('All elements must be a dictionary. You are trying to add the element {}, which is not a dictionary.'.format(value))
        super(FilterList, self).append(value, *args, **kwargs)

    def get(self, *args, **kwargs):
        if args:
            msg = 'Get method only accepts keyword arguments. For example, item.get(id=1)'
            raise TypeError(msg)

        if not kwargs:
            msg = 'Get method requires at least one keyword argument. For example, item.get(id=1)'
            raise TypeError(msg)

        result_list = self.filter(**kwargs)

        if not result_list:
            raise NotFound('No items found with the following filter: {}'.format(kwargs))

        if len(result_list) != 1:
            raise FilterListException('Expected to find 1 item but found {}'.format(len(self)))
        return result_list[0]

    def filter(self, *args, **kwargs):
        """
        Accepts a list of keyword arguments to search for.
        The key can contain the following special operations __regex, __contains
        ie, you can pass in name__contains="bob", and this method will return all dictionaries in the list
        where name field contains the word "bob"
        return: new FilterList object that matches the given kwargs
        """

        if args:
            msg = 'Get method only accepts keyword arguments. For example, item.get(id=1)'
            raise TypeError(msg)

        filtered_result = copy(self)
        for key_string, value in kwargs.items():
            keys = self._get_keys(key_string)
            operation = self._get_operation(key_string)
            filtered_result = self._get_filtered_list(filtered_result, keys, value, operation)

        return self.__class__(filtered_result)

    def _get_keys(self, key_string):
        """
        parses the key string into a list of keys
        for example, if key_string is animal__dog__contains, it will return ['animal', 'dog']
        return: a list of keys
        """
        assert key_string  # should never be an empty string
        keys = key_string.split('__')
        if keys[-1] in self.valid_operations:
            keys = keys[:-1]
        return keys

    def _get_operation(self, key_string):
        """
        returns the operation
        """
        assert key_string  # should never be an empty string
        operation = 'exact'
        keys = key_string.split('__')
        if keys[-1] in self.valid_operations:
            operation = keys[-1]
        return operation

    def _get_filtered_list(self, original_list, keys, value, operation):
        """
        returns a list where the key matches the value based on the operation
        """
        result = []
        for item in original_list:
            try:
                found_value = self._get_value(keys, item)
            except NotFound:
                continue

            if operation == 'exact':
                if found_value == value:
                    result.append(item)

            elif operation == 'iexact':
                if found_value.lower() == value.lower():
                    result.append(item)

            elif operation == 'in':
                if found_value in value:
                    result.append(item)

            elif operation == 'regex':
                if re.search(value, found_value):
                    result.append(item)

            elif operation == 'iregex':
                if re.search(value, found_value, re.IGNORECASE):
                    result.append(item)

            elif operation == 'contains':
                if value in found_value:
                    result.append(item)

            elif operation == 'icontains':
                if value.lower() in found_value.lower():
                    result.append(item)

            else:
                raise FilterListException('{} is not a valid operation'.format(operation))

        return result

    def _get_value(self, keys, mydict):
        """
        :param keys - a list of keys
        :param mydict - a nested dictionary
        returns the value of mydict[keys[0]][keys[1]]...
                None if any of the keys is missing
        """
        tmp_dict = copy(mydict)
        for i, key in enumerate(keys):
            if key not in tmp_dict:
                raise NotFound
            value = tmp_dict.get(key)
            if i == len(keys) - 1:
                return value
            else:
                if not isinstance(value, dict):
                    raise NotFound
                tmp_dict = value
