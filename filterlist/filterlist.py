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

        valid_operations = ['in', 'regex', 'iregex', 'contains', 'icontains', 'iexact']
        if args:
            msg = 'Get method only accepts keyword arguments. For example, item.get(id=1)'
            raise TypeError(msg)

        filtered_result = copy(self)
        for key, value in kwargs.items():
            operation = None
            if '__' in key:
                keys = key.split('__')
                if keys[-1] in valid_operations:
                    operation = keys[-1]
                    keys = keys[:-1]
            else:
                keys = [key]

            if operation == 'iexact':
                filtered_result = [item for item in filtered_result if
                                   self._get_value(keys, item) is not None and
                                   self._get_value(keys, item).lower() in value.lower()]

            elif operation == 'in':
                filtered_result = [item for item in filtered_result if
                                   self._get_value(keys, item) is not None and
                                   self._get_value(keys, item) in value]

            elif operation == 'regex':
                filtered_result = [item for item in filtered_result if
                                   self._get_value(keys, item) is not None and
                                   re.search(value, self._get_value(keys, item))]

            elif operation == 'iregex':
                filtered_result = [item for item in filtered_result if
                                   self._get_value(keys, item) is not None and
                                   re.search(value, self._get_value(keys, item), re.IGNORECASE)]

            elif operation == 'contains':
                filtered_result = [item for item in filtered_result if
                                   self._get_value(keys, item) is not None and
                                   value in self._get_value(keys, item)]

            elif operation == 'icontains':
                filtered_result = [item for item in filtered_result if
                                   self._get_value(keys, item) is not None and
                                   value.lower() in self._get_value(keys, item).lower()]

            else:
                filtered_result = [item for item in filtered_result if
                                   self._get_value(keys, item) is not None and
                                   self._get_value(keys, item) == value]

        return self.__class__(filtered_result)

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
                return None
            value = tmp_dict.get(key)
            if i == len(keys) - 1:
                return value
            else:
                if not isinstance(value, dict):
                    return None
                tmp_dict = value
