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

	from filterlist import filterlist
	people = [
	    {
	        "id": 1,
	        "name": "Obi-Wan Kenobi",
	        "status": "RETIRED",
	        "affiliation": "REBEL_ALLIANCE",
	        "age": 57
	    },
	    {
	        "id": 2,
	        "name": "Darth Vader",
	        "status": "ACTIVE",
	        "affiliation": "EMPIRE",
	        "age": 42
	    },
	    {
	        "id": 3,
	        "name": "Yoda",
	        "status": "RETIRED",
	        "affiliation": "REBEL_ALLIANCE",
	        "age": 896
	    },
	]
	people = filterlist(people)


### get()

The get method will return one dictionary from within the list of dictionaries where the key/value that was passed as the keyword arguments matches the key/value of the dictionary.  If none is found or if multiple dictionaries match the search criteria, an exception is raised.

	>>> people.get(id=1)
	{'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 57, 'id': 1, 'name': 'Obi-Wan Kenobi'}

You can also filter by multiple search criteria:

	>>> people.get(status='RETIRED', age=57)
	{'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 57, 'id': 1, 'name': 'Obi-Wan Kenobi'}

### filter()

The filter method returns a filterlist object that matches the search criteria in the keyword arguments.  If none is found an empty filterlist is returned.

	>>> people.filter(affiliation='REBEL_ALLIANCE')
	[{'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 57, 'id': 1, 'name': 'Obi-Wan Kenobi'},
	 {'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 896, 'id': 3, 'name': 'Yoda'}]


Field Lookups
----

By default, the arguments you pass into the get and filter methods will look for an exact match of the key/value pairs.  However, you can control how to match each field using the double underscore syntax.

### in

In a given iterable; often a list or tuple

	>>> people.filter(id__in=[1, 2])
	[{'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 57, 'id': 1, 'name': 'Obi-Wan Kenobi'},
	 {'status': 'ACTIVE', 'affiliation': 'EMPIRE', 'age': 42, 'id': 2, 'name': 'Darth Vader'}]

### contains

Case-sensitive containment test.

	>>> people.filter(name__contains='Darth')
	[{'status': 'ACTIVE', 'affiliation': 'EMPIRE', 'age': 42, 'id': 2, 'name': 'Darth Vader'}]

### icontains

Case-insensitive containment test.

	>>> people.filter(affiliation__icontains='rebel')
	[{'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 57, 'id': 1, 'name': 'Obi-Wan Kenobi'},
	 {'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 896, 'id': 3, 'name': 'Yoda'}]

### regex

Case-sensitive regular expression match.

	>>> people.filter(name__regex='\w-\w')
	[{'status': 'RETIRED', 'affiliation': 'REBEL_ALLIANCE', 'age': 57, 'id': 1, 'name': 'Obi-Wan Kenobi'}]