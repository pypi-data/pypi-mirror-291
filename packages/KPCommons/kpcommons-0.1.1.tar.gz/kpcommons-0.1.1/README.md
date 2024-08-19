# Readme

KPCommons is a collection of methods which are regularly needed.

## Installation

```
pip install kpcommons
```

This installs the library without [pySBD](https://github.com/nipunsadvilkar/pySBD). To use the `SentenceChunker`,
install with the following command:

```
pip install kpcommons[chunk]
```

## Chunker
`SentenceChunker` can be used to split a text into chunks which are roughly sentences or multiple sentences. 
`BaseChunker` can be used to implement other variants.

## Util
`Util.py` contains the following methods:

- `calculate_overlap` is a method to calculate the overlap between two ranges.
  ~~~
  overlap = Util.calculate_overlap(0, 10, 5, 10)
  ~~~
  The first two arguments are the start and end position of the first range, and the last
  two arguments are the positions of the second range. The result is an `Overlap` object with the `start`, `end`, 
  `length` of the overlap, and the two ratios between the overlap and the ranges.

  **Note**: In case of no overlap, `overlap.length` is the distance between the two ranges as a negative value.
- `get_namespace` gets the namespace from a root tag of a xml file.
- `create_dated_folder` creates a subfolder with a date as the name. By default, `NowDateProvider` is used.

## Footnote
`Footnote.py` contains a collection of methods for working with footnotes.

- `get_footnotes_ranges` takes a text and returns two list of tuples of start and end character positions of footnote
  ranges, that is, text surrounded by '[[[' and ']]]'. The first list is without an offset, that is, the actual
  positions, and the second list is with an offset, that is, as if the footnotes were removed.
- `get_footnote_ranges_without_offset` and `get_footnote_ranges_with_offset` are variants of `get_footnotes_ranges`
  which only return one of the lists.
- `is_position_in_ranges` checks if a position is in one of the ranges.
- `is_range_in_ranges` checks if a range given by a start and end position overlaps with one of the given ranges.
- `remove_footnotes` removes footnotes from a text. Footnotes are marked by '[[[' and ']]]'.
- `map_to_real_pos` maps start and end character positions of a text with footnotes removed to real positions, that is,
  positions before footnotes where removed.

## XML
`get_text_from_element` extracts the text from an (annotated) xml root element. If the xml file contains annotations for
quotations or references, these will be tagged in the resulting text in the following way.

### Footnotes
Footnotes are enclosed with triple brackets, for example:

```
Some running text [[[This is a footnote]]] and more running text...
```

### Direct Quotations
A direct quotation can fall into one of two groups. A quotation from the primary literary work or a quotation from some
other source.
Direct quotations from the primary literary work are enclosed with `@@`. An optional id to a corresponding reference is
part of the starting tag, for example:

```
Some text with @id@a quote@@
```

Direct quotations from other sources are enclosed with `€`.

### References
References, for example, a page reference for a quotations (`S. 14`) are enclosed with `§µ§` and an id in the starting
tag, for example:

```
Some text, @1@a quote@@ (§µ1§S.5§µ§)
```

### Indirect Quotations
TBD