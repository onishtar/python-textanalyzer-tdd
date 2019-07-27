# python-textanalyzer-tdd
# Python TextAnalyzer developed using Test Driven Development TDD
## The TextAnalyzer class accepts 3 types on input:
- Website url starting with http
- Text file ending with txt
- Plan Text 

## Methods or functions:
- __init__()
A constructor
- discover() 
Finds if the input is url, txt or plan text and open the input as per file type
- set_context_to_tag()
Parses the webwite using url and parser BeautifulSoup
- reset_content()
Set _content back to orginal as retrieved from source
- _words()
The list of words in the document
- common_words()
Count of words
- char_distribution()
The letters used and the count
- plot_common_words()
Setting for the words and frequency to be used in a plot
- plot_char_distribution()
Setting for the characters and frequency to be used in a plot

## Properties (data from the source input)
- words
A list of words
- avg_word_length
Average word length
- word_count
Word Count
- distinct_word_count
Distinct Word Count
- positivity
-Uses Negative and Postive word list and determines the positivity of the input source
