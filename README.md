# Pronouns test data

Any JSON parser should be able to correctly parse [pronouns-test-data.json]

You can copy the JSON, or even just [link to it directly](https://uwiam.page.link/test-pronouns-json) at `https://uwiam.page.link/test-pronouns-json` to consume it. 

The keys in this list are test UW NetIDs whose pronoun matches the "pronoun" value associated with their entry.

If the value your JSON parser extracts from the below JSON, and the text displayed on your website (or in your tests) match
when consuming the pronouns of the associated UW NetIDs, then you are correctly consuming the data.

NB: The only disallowed characters are  `|` and `\`. 

The `javerage` UW NetID is also a student who (should be) registered for classes.

## Discussion on test case values

* `javerage`: Uses all 5 grammatical representations of a personal pronoun: https://pronoun.is/they/.../themself
* `uwitpn01`: Uses 2 pronoun sets with default formatting
* `uwitpn02`: Uses a single pronoun set with default formatting
* `uwitpn03`: Uses 2 pronoun sets, neither with default formatting
* `uwitpn04`: Does not include a pronoun, but requests you use their name instead
* `uwitpn05`: Is in the process of exploring their identity, and would like to be asked
* `uwitpn06`: This user has only one pronoun set, but has accidentally submitted it three times without spaces!
* `uwitpn07`: This user has indicated 2 pronoun sets using a shorthand that means they accept both "she/.../hers" and "they/.../them" pronouns
* `uwitpn08`: Uses a neo-pronoun set, and represents it using only 2 (of the common 3) grammatical cases. (See https://pronoun.is/ze/hir)
* `uwitpn10`: This user has added some extra quotations, perhaps on accident. El has also opted for nonstandard formatting

The rest of the cases only include jargon in order to test parseability and length for presentation purposes:

* `uwitpn11`: 12 characters (uncommon)
* `uwitpn12`: 16 characters (likely)
* `uwitpn13`: 32 characters (unlikely)
* `uwitpn14`: 64 charagers (unlikely) 
* `uwitpn15`: 128 characters (very unlikely) 
* `uwitpn16`: 140 characters (maximum!) (extremely unlikely) 
* `uwitpn17`: 140 special characters only (maximum!) (will hopefully never happen)
* `uwitpn18`: 140 numbers, no spaces


[pronouns-test-data.json]: pronouns-test-data.json
