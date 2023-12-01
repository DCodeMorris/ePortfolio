---
layout: default
---

Text can be **bold**, _italic_, or ~~strikethrough~~.

[Link to another page](./CS-499 Algorithms and Data Structures/Artifact Two Original/index.html).

There should be whitespace between paragraphs.

There should be whitespace between paragraphs. We recommend including a README, or a file with information about your project.

# Header 1

This is a normal paragraph following a header. GitHub is a code hosting platform for version control and collaboration. It lets you and others work together on projects from anywhere.

## Header 2

> This is a blockquote following a header.
>
> When something is important enough, you do it even if the odds are not in your favor.

### Header 3

```js
// Javascript code with syntax highlighting.
var fun = function lang(l) {
  dateformat.i18n = require('./lang/' + l)
  return true;
}
```

```ruby
# Ruby code with syntax highlighting
GitHubPages::Dependencies.gems.each do |gem, version|
  s.add_dependency(gem, "= #{version}")
end
```

#### Header 4

*   This is an unordered list following a header.
*   This is an unordered list following a header.
*   This is an unordered list following a header.

##### Header 5

1.  This is an ordered list following a header.
2.  This is an ordered list following a header.
3.  This is an ordered list following a header.

###### Header 6

| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |

### There's a horizontal rule below this.

* * *

### Here is an unordered list:

*   Item foo
*   Item bar
*   Item baz
*   Item zip

### And an ordered list:

1.  Item one
1.  Item two
1.  Item three
1.  Item four

### And a nested list:

- level 1 item
  - level 2 item
  - level 2 item
    - level 3 item
    - level 3 item
- level 1 item
  - level 2 item
  - level 2 item
  - level 2 item
- level 1 item
  - level 2 item
  - level 2 item
- level 1 item

### Small image

![Octocat](https://github.githubassets.com/images/icons/emoji/octocat.png)

### Large image

![Branching](https://guides.github.com/activities/hello-world/branching.png)


### Definition lists can be used with HTML syntax.

<dl>
<dt>Name</dt>
<dd>Godzilla</dd>
<dt>Born</dt>
<dd>1952</dd>
<dt>Birthplace</dt>
<dd>Japan</dd>
<dt>Color</dt>
<dd>Green</dd>
</dl>

<details><summary>Code Preview:(Click to extend complete code)
```

```python
class AnimalShelter(object):
```

</summary>  
```

```python
    # =============================================================================
    # Created By  : Dustin Morris
    # Created Date: Mon November 20 2023
    # =============================================================================
    # Interpreter: Python 3.12
    # File Name: AnimalClass.py
    # =============================================================================
    __course__ = 'CS499'
    __author__ = 'Dustin Morris'
    __version__ = '1.4'
    __maintainer__ = 'Dustin Morris'
    __username__ = 'MyUserAdmins2'
    __password__ = '123456'
    __email__ = 'Dustin.Morris1@snhu.edu'    __status__ = 'Production'
    __description__ = 'Manages the class used in the Application.py which is "AnimalShelter".'
    # =============================================================================
    print('# ' + '=' * 78)
    print('Author: ' + __author__)
    print('Version: ' + __version__)
    print('Maintainer: ' + __maintainer__)
    print('Email: ' + __email__)
    print('Status: ' + __status__)
    print('Course: ' + __course__)
    print('Username: ' + __username__)
    print('Password: ' + __password__)
    print('Description: ' + __description__)
    print('# ' + '=' * 78)

    from pymongo import MongoClient
    from bson.objectid import ObjectId
    import urllib.parse

    class AnimalShelter(object):
    _instance = None  # Class variable to store the instance

    def __new__(cls, _password, _username='aacUser'):
        if cls._instance is None:
            # Creating a new instance involves setting up a MongoDB client connection,
            # assuming MongoClient connection setup has a constant time complexity.
            cls._instance = super(AnimalShelter, cls).__new__(cls)
            username = urllib.parse.quote_plus(_username)
            password = urllib.parse.quote_plus(_password)
            # Overall time complexity of creating a new instance is O(1).
            cls._instance.client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/?authSource=AAC')
            cls._instance.dataBase = cls._instance.client['AAC']
        return cls._instance

    def __init__(self, _password, _username='myUserAdmins2'):
        # Property variables
        self.records_updated = 0  # Variable to store the number of records updated
        self.records_matched = 0  # Variable to store the number of records matched
        self.records_deleted = 0  # Variable to store the number of records deleted

    def createRecord(self, data):
        if data:
            _insert_valid = self.dataBase.animals.insert_one(data)
            return _insert_valid.acknowledged
        else:
            return False  # or raise an exception if needed

    def getRecordId(self, post_id):
        _data = self.dataBase.animals.find_one({'_id': ObjectId(post_id)})
        return _data

    def getRecordCriteria(self, criteria):
        if criteria:
            _data = list(self.dataBase.animals.find(criteria, {'_id': 0}))
        else:
            _data = list(self.dataBase.animals.find({}, {'_id': 0}))
        return _data

    def updateRecord(self, query, new_value):
        if not query:
            raise Exception("No search criteria is present.")
        elif not new_value:
            raise Exception("No update value is present.")
        else:
            _update_valid = self.dataBase.animals.update_many(query, {"$set": new_value})
            self.records_updated = _update_valid.modified_count
            self.records_matched = _update_valid.matched_count
            return _update_valid.modified_count > 0

    def deleteRecord(self, query):
        if not query:
            raise Exception("No search criteria is present.")
        else:
            _delete_valid = self.dataBase.animals.delete_many(query)
            self.records_deleted = _delete_valid.deleted_count
            return _delete_valid.deleted_count > 0

    def addAnimal(self, name, breed, age, sex):
        new_animal = {'name': name, 'breed': breed, 'age_upon_outcome_in_weeks': age, 'sex_upon_outcome': sex}
        return self.createRecord(new_animal)

```
```
</details>
