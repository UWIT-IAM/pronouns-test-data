## Overview

With the upcoming release of pronoun support at identity.UW, UW IAM is providing
test data that potential consumers of pronouns can use to:

- Verify that data is flowing through the system properly
- Verify that consuming services are able to correctly read and display the data
- Find edge cases in presentation layers (for example, very long strings, strings 
  without spaces, etc.)
  
The data use cases are a mix of "real" responses (responses that you are likely to 
see when users set their pronoun preferences), presumed edge cases (mistakes actual 
users are likely to make), and absolute jargon 
(for testing value length, parsing, etc.). Each case has a `use_case/useCase` 
property that describes the data value.

Each test case has an associated `uwnetid` field. If your system is able to look up 
Identity Registry or Person Web Service data, you should be able to validate that 
the user's pronoun values in those system match the value provided in the test data 
set. 

We currently have a limited pool of UW NetIDs allocated to this test. If you think 
there are important use cases we're missing from this test data, please email 
[help@uw.edu](mailto:help@uw.edu?subject=UW-IT+IAM+Pronouns+Test+Data+Request) and 
explain your request. You can ask for this to be routed to UW-IT IAM.

**Note:** We may update these cases to reflect actual usage once we have real data 
from our users.

## Using this data

There are a few ways to consume this data depending on your needs. You can download 
it for use an Excel, if you have administrative use cases. You can easily consume the 
data via raw JSON, or if you work in a python library, you can add a dependency on 
this package to load the data (or generate your own test cases).

No matter your use case, you can consume the data as:

- `JSON`: https://identity.cdn.iamprod.s.uw.edu/pronouns/test-data/latest.json
- `CSV`: https://identity.cdn.iamprod.s.uw.edu/pronouns/test-data/latest.csv

The `latest` version will always reflect what is stored in the Identity Registry.
However, see [versioning][#versioning] for how to rely on specific data values.


**Data is available in both prod and eval environments.** It is loaded into Identity 
Registry prod and eval, 

Eval data is reset every day. 
Prod data will only change when a new version of the data is released and tagged. 

See [versioning](#versioning) for more information.

### Excel/Google Sheets

The data is published in `csv` format and can be downloaded at any time using the 
CSV link above.

From your browser, you can choose `File → Save As...` to download it to your 
computer, then open it in any program you like. 

### Programmatically, via JSON


```javascript
// jQuery example

$.getJSON(
    "https://identity-cdn.iamprod.s.uw.edu/pronouns/test-data/latest.json",
    function(data) {
       var student = data.testCases[0];  // user 'javerage' is a student profile.
       alert("User " + student.uwnetid + "'s pronoun is: " + student.pronoun); 
    } 
);
```

You could similarly perform a GET request on this URL from any language's HTTP 
framework to depend on this data in some end-to-end test. (Example: to ensure that 
the data you are receiving matches the data that is being published.)

### Programmatically, as a python library

```bash
pip install uw-iam-pronouns-test-data   # Installs the pronouns_test_data  module.
```

Once installed, you can make use of the library itself to generate your own test cases,
or load the published data from disk:


#### Loading versioned data using various formats

```python
# Load the published data from disk
from pronouns_test_data import load_published_data, DataFormat

# Using the models defined in models.py
fancy_model = load_published_data()
for profile in fancy_model.test_cases:
    print(f"User {profile.uwnetid}'s pronoun is: {profile.pronoun}")

# A list of dictionaries (with snake_case keys)
list_of_dicts = load_published_data(version='1.0.0', data_format=DataFormat.dict_list)
for profile in list_of_dicts:
    print(f"User {profile['uwnetid']}'s pronoun is {profile['pronoun']}")

# Raw JSON
import json
json_data = load_published_data(version='1.0.0', data_format=DataFormat.raw_json)
assert json.loads(json_data)['test_cases'] == list_of_dicts

# Raw CSV
import csv
raw_csv = load_published_data(data_format=DataFormat.raw_csv)
rows = raw_csv.split('\n')
for row in csv.reader(rows[1:], ):  # The first row is a header
    print(f"User {row[0]}'s pronoun is {row[1]}")
```

The above code snippet should "just work" if the library is installed in your 
python path.

#### Generating your own data (good for randomizing edge cases)

```python
from pronouns_test_data import generate_test_data, GeneratedTestData

# This will randomize the "jargon" test cases while preserving the more curated cases.
attempt_1: GeneratedTestData = generate_test_data()  
attempt_2: GeneratedTestData = generate_test_data()

# Our 'javerage' profile should not have changed
assert attempt_1.test_cases[0] == attempt_2.test_cases[0]

# But this one should have a different pronoun, but everything else should be the same.
assert attempt_1.test_cases[-1] != attempt_2.test_cases[-1]
assert attempt_1.test_cases[-1].uwnetid == attempt_2.test_cases[-1].uwnetid
assert attempt_1.test_cases[-1].pronoun != attempt_2.test_cases[-1].pronoun
```

### Versioning

This package uses [semantic versioning] (`X.Y.Z`).

- Changes to support scripts will only update the `Z` portion; you do not need to keep
up to date with that if you are only consuming the data. We will use the following 
general guidelines to version this package:
- Changes to data _values_ will update the `Y` portion; these changes may impact you
if you are relying on the data _values_ to stay the same.
- Changes to the data _structure_ will update the `X` portion of the version. These
changes will probably impact you in some way.

Anytime you see `latest` in a URL or version number, it will always be pulling the
most recently published version. That means this is a dynamic data set that may
change out from under you. If you want a frozen data set,
you can substitute `X.Y.Z` for `latest`. (e.g., `1.0.0.json`). Just note that frozen
data sets will not be guaranteed to match what is in identity registry. Depending on
your use case, this might be fine.

## Updating and Publishing this Data

For more information on updating and publishing the data, please refer to the 
[developer documentation] on the internal UW-IT IAM Wiki.


[developer documentation]: https://wiki.cac.washington.edu/display/SMW/UW+IAM+Pronouns+Test+Data
[semantic versioning]: https://www.semver.org
