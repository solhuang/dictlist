# FilterList: Simple filtering for list of dictionaries
Python library to filter list of dictionaries using Django-like queryset syntax.

filterlist is an extension of the list type.  It adds two convenience methods .get() and .filter() in order to easily filter list of dictionaries.

Installation
----
Use pip to install filterlist:

	pip install filterlist

Usage
---
Import filterlist:

	from filterlist import filterlist

Create a new filterlist by passing in an existing list of dictionaries:

	people = [
	    {
	        'id': 1,
	        'name': 'Obi-Wan Kenobi',
	        'gender': 'male',
	        'birth_year': 57,
	        'homeworld': {
	            'name': 'Stewjon',
	        }
	    },
	    {
	        'id': 2,
	        'name': 'Darth Vader',
	        'gender': 'male',
	        'birth_year': 41,
	        'homeworld': {
	            'name': 'Tatooine',
	        }
	    },
	    {
	        'id': 3,
	        'name': 'C-3PO',
	        'gender': 'n/a',
	        'birth_year': 112,
	        'homeworld': {
	            'name': 'Tatooine',
	        }
	    },
	]
	people = filterlist(people)


### get()

The get method will return one dictionary from within the list of dictionaries where the key/value that was passed as the keyword arguments matches the key/value of the dictionary.  If none is found or if multiple dictionaries match the search criteria, an exception is raised.

	>>> people.get(id=1)
	{'gender': 'male', 'birth_year': 57, 'id': 1, 'homeworld': {'name': 'Stewjon'}, 'name': 'Obi-Wan Kenobi'}

You can also filter by multiple search criteria:

	>>> people.get(gender='male', birth_year=41)
	{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}

### filter()

The filter method returns a filterlist object that matches the search criteria in the keyword arguments.  If none is found an empty filterlist is returned.

	>>> people.filter(gender='male')
	[{'gender': 'male', 'birth_year': 57, 'id': 1, 'homeworld': {'name': 'Stewjon'}, 'name': 'Obi-Wan Kenobi'},
	{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}]

Field Lookups
----

By default, the arguments you pass into the get and filter methods will look for an exact match of the key/value pairs.  However, you can control how to match each field using the double underscore syntax.


### iexact

Case-insensitive exact match

	>>> people.filter(name__iexact='darth vader')
	[{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}]

### in

In a given iterable; often a list or tuple

	>>> people.filter(id__in=[1, 2])
	[{'gender': 'male', 'birth_year': 57, 'id': 1, 'homeworld': {'name': 'Stewjon'}, 'name': 'Obi-Wan Kenobi'},
	{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}]

### contains

Case-sensitive containment test.

	>>> people.filter(name__contains='Darth')
	[{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}]

### icontains

Case-insensitive containment test.

	>>> people.filter(name__icontains='darth')
	[{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}]

### regex

Case-sensitive regular expression match.

	>>> people.filter(name__regex='\w-\w')
	[{'gender': 'male', 'birth_year': 57, 'id': 1, 'homeworld': {'name': 'Stewjon'}, 'name': 'Obi-Wan Kenobi'},
	{'gender': 'n/a', 'birth_year': 112, 'id': 3, 'homeworld': {'name': 'Tatooine'}, 'name': 'C-3PO'}]

### iregex

Case-insensitive regular expression match.

	>>> people.filter(name__iregex='obi-\w')
	[{'gender': 'male', 'birth_year': 57, 'id': 1, 'homeworld': {'name': 'Stewjon'}, 'name': 'Obi-Wan Kenobi'}]

Nested Lookups
----

To search inside nested dictionaries, use the double underscore to filter inside the nested dictionary. You can go as many levels deep as needed:

	>>> people.filter(homeworld__name='Tatooine')
	[{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'},
	{'gender': 'n/a', 'birth_year': 112, 'id': 3, 'homeworld': {'name': 'Tatooine'}, 'name': 'C-3PO'}]

Also, all the field lookups still work for nested dictionaries:

	>>> people.filter(homeworld__name__icontains='stew')
	[{'gender': 'male', 'birth_year': 57, 'id': 1, 'homeworld': {'name': 'Stewjon'}, 'name': 'Obi-Wan Kenobi'}]



Filter Based on Any Key
----
To search for a value that match any of the keys in a dictionary, use the _any keyword.

For example, if you wan to search for all users that match the word 'Darth Vader' regardless of key:

	>>> people.filter(_any='Darth Vader')
	[{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}]


The _any keyword also works in nested dictionaries as well.  Say you want to match for 'Tatooine' in any of the fields in the 'homeworld' nested dictionary:

	>>> people.filter(homeworld___any='Tatooine')
	[{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'},
	{'gender': 'n/a', 'birth_year': 112, 'id': 3, 'homeworld': {'name': 'Tatooine'}, 'name': 'C-3PO'}]

Notice that there is the usual double underscore to search inside a nested dictionary followed by the special keyword \_any, which means there are actually three underscores in the homeworld___any key.  In this particular case it's not particularly useful to use the _any keyword since we know the key is 'name'.  However, this may be useful if all you care about is the existence of a value, and don't care which key the value appears in.

You can also use the \_any keyword with any of the field lookups operations.  For example, if you want to find all items where the value contains the word 'vader', then the search criteria will look something like this:

	>>> people.filter(_any__icontains='vader')
	[{'gender': 'male', 'birth_year': 41, 'id': 2, 'homeworld': {'name': 'Tatooine'}, 'name': 'Darth Vader'}]

