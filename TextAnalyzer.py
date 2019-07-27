import requests, re
from bs4 import BeautifulSoup
from collections import Counter
import statistics as stats
import string

#create your class here
class TextAnalyzer:
    """ Python TextAnalyzer developed using Test Driven Development TDD"""
    def __init__(self, src, src_type=None):
        """
        The TextAnalyzer class accepts 3 types on input:
        Website url starting with http
        Text file ending with txt
        Plan Text
        """
        self._src = src
        self._src_type = src_type
        self._orig_content = None
        self._content = None

        self.discover()


    def discover(self):
        """Finds if the input is url, txt or plan text and open the input as per file type"""
        if self._src.startswith('http'):
            self._src_type = 'url'
            
            headers = {'user-agent': 'TextAnalyzer'}
            req = requests.get(self._src, headers=headers)
            self._content = self._orig_content = req.text
        
        elif self._src.endswith('txt'):
            self._src_type = 'path'
            with open(self._src, 'r') as f:
                self._content = f.read()
                
        else:
            self._src_type = 'text'
            self._content = self._src                                        
    
    def set_content_to_tag(self, tag, tag_id):
        """Parses the webwite using url and parser BeautifulSoup"""
        try:
            soup = BeautifulSoup(self._content, 'html.parser')
            self._content = soup.find(tag, {'id': tag_id}).get_text()
        except ValueError:
            print("Error reading webpage with BeautifulSoup tag {tag} and tag_id {tag_id}")

    def reset_content(self):
        """Set _content back to orginal as retrieved from source"""
        self._content = self._orig_content
        return self._content

    def _words(self, casesensitive=False):
        """A list of words"""
        if casesensitive is False:
            words = [word.strip(string.punctuation).upper() 
                     for word in self._content.split()] 
        else:
            words = [word.strip(string.punctuation) 
                     for word in self._content.split()]
        return words  

    def common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        """The list of words with count"""
        _word_list = []
        if casesensitive is False:
            _word_list = [w.upper() for w in self.words if (len(w) >= minlen) & (len(w) <= maxlen)]
        else:
            _word_list = [w for w in self.words if (len(w) >= minlen) & (len(w) <= maxlen)]
        cnt = Counter(_word_list)
        return cnt.most_common(count)
    
    def char_distribution(self, casesensitive=False, letters_only=False):
        """The letters used and the count"""
        chars = []
        # Remove any non aplha letters
        chars_alpha = re.compile('[^a-zA-Z]').sub('', self._content.rstrip('\n'))

        if casesensitive and letters_only:
            chars = [char.strip(string.punctuation) for char in chars_alpha]
        elif casesensitive and not letters_only:           
            chars = [char for char in self._content]
        elif not casesensitive and letters_only:
            chars = [char.strip(string.punctuation).upper() for char in chars_alpha]
        elif not casesensitive and not letters_only:
            chars = [char.upper() for char in self._content]
            
        cnt_chars = Counter(chars)
        char_dist = cnt_chars.most_common() 
        char_dist_sorted = sorted(char_dist, key=lambda x: x[1], reverse=False)
        return char_dist

    def plot_common_words(self, minlen=1, maxlen=100, count=10, casesensitive=False):
        """Setting for the words and frequency to be used in a plot"""
 
        df_cw = pd.DataFrame(self.common_words(minlen, maxlen, count, casesensitive))
    
        df_cw.columns = ['Word', 'Count']
        df_cw.index = df_cw['Word']

        plt_words = df_cw.plot(kind='bar',
                               title='Common Words',
                               figsize=(14,3),
                               width=.8,
                               fontsize=16)
        plt_words.set_ylabel('Word', fontsize=20)
        plt_words.set_xlabel('Count', fontsize=20)
        plt_words.grid(True)
        
    def plot_char_distribution(self, casesensitive=False, letters_only=False):
        """Setting for the characters and frequency to be used in a plot"""
 
        df_cd = pd.DataFrame(self.char_distribution(casesensitive, letters_only))
    
        df_cd.columns = ['Character', 'Count']
        df_cd.index = df_cd['Character']

        plt_chars = df_cd.plot(kind='bar',
                               title='Character Distribution',
                               figsize=(14, 4),
                               width=.8,
                               fontsize=16)
        plt_chars.set_ylabel('Character', fontsize=20)
        plt_chars.set_xlabel('Count', fontsize=20)
        plt_chars.grid(True)

    @property
    def words(self):
        """A list of words"""
        return self._words()
    
    @property
    def avg_word_length(self):
        """Average word length"""
        _avg_word_length = sum([len(w) for w in self.words]) / len(self._words())
        return round(_avg_word_length, 2)
    
    @property
    def word_count(self):
        """Word Count"""
        return len(self._words())
    
    @property
    def distinct_word_count(self):
        """Distinct Word Count"""
        return len(set(self._words()))
    
    @property
    def positivity(self):
        """Negative and Postive word list and determines the positivity of the input source"""
        with open('positive.txt', 'r') as _f:
            list_of_lines = _f.readlines() 
            positive_words = []
        for word in list_of_lines:
            positive_words = [word.strip(string.punctuation).rstrip('\n').upper() for word in list_of_lines]


        with open('negative.txt', 'r') as _f:
            list_of_lines = _f.readlines()
            negative_words = []
        for word in list_of_lines:
            negative_words = [word.strip(string.punctuation).rstrip('\n').upper() for word in list_of_lines]

        matches = []
        tally = 0
        positive = 0
        negative = 0
        # Comapring overall words in _content with positive and negative list
        for w in self.words:
            for p in positive_words:
                if w == p:
                    positive += 1
                    tally += 1
                    matches.append((w, p, tally))
            for n in negative_words:
                if w == n:
                    negative += 1
                    tally -= 1
                    matches.append((w, n, tally))


        _positivity = round(tally / self.word_count * 1000)

        return _positivity