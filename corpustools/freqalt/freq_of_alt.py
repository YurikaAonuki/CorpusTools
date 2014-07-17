#fun times with morphological relatedness
import time
import os
from codecs import open

from corpustools.corpus.classes import CorpusFactory
import corpustools.symbolsim.phono_align_ex as phono_align_ex
import corpustools.symbolsim.string_similarity as string_similarity

class Freqor(object):
    """Initializes the frequency of alternation analyzer

    Parameters
    ----------
    object: list
        contains parameters needed for the analyzer such as which algorithm to use for relating and which corpus to use
    Returns
    -------
    None
    """
    def calc_freq_of_alt(self, s1, s2, relator_type, count_what, string_type='transcription', output_filename = None,
                        min_rel = None, max_rel = None, phono_align = None, min_pairs_okay = None, from_gui=False):
        """Returns a double that is a measure of the frequency of alternation of two sounds in a given corpus

        Parameters
        ----------
        s1: char
            A sound segment, e.g. 's', 'ÃƒÆ’Ã…Â Ãƒâ€ Ã¢â‚¬â„¢',
        s2: char
            A sound segment
        relator_type: string
            The type of relator to be used to measure relatedness, e.g. 'string_similarity'
        string_type: string
            The type of segments to be used ('spelling' = roman letters, 'transcription' = IPA symbols)
        count_what: string
            The type of frequency, either 'type' or 'token'
        max_rel: double
            Filters out all words that are higher than max_rel from a relatedness measure
        min_rel: double
            Filters out all words that are lower than min_rel from a relatedness measure
        phono_align: boolean (1 or 0), optional
            1 means 'only count alternations that are likely phonologically aligned,' defaults to not force phonological alignment
        min_pairs_okay: boolean (1 or 0), optional
            1 means allow minimal pairs (e.g. in English, 's' and 'ÃƒÆ’Ã…Â Ãƒâ€ Ã¢â‚¬â„¢' do not alternate in minimal pairs, i.e. diss/dish is not an alternation, so allowing minimal pairs may skew results)

        Returns
        -------
        double
            The frequency of alternation of two sounds in a given corpus
        """

        list_s1, list_s2 = self.get_lists(s1, s2, string_type)
        comparisons = list()

        for word_s1 in list_s1:
            for word_s2 in list_s2:
                    comparisons.append( (word_s1, word_s2) )

        related_list = string_similarity.string_similarity_pairs('', relator_type, string_type, count_what, comparisons, 'return_data', min_rel = min_rel, max_rel = max_rel, ready_made_corpus = self.corpus)
        
        
        #Remove minimal pairs if specified
        if min_pairs_okay == 0:
            new_related_list = list()
            for w1, w2, score in related_list:
                if len(w1) != len(w2):
                    new_related_list.append( (w1, w2, score) )
                else:
                    count_diff = 0
                    for i in range(len(w1)):
                        if w1[i] != w2[i]:
                            count_diff += 1
                    if count_diff > 1:
                        new_related_list.append( (w1, w2, score) )
        related_list = new_related_list
                
        words_with_alt = set()
        #Remove pairs that are not phonologically aligned if specified
        if phono_align == 1:
            new_related_list = list()
            al = phono_align_ex.Aligner(features=self.corpus.specifier.matrix)
            for w1, w2, score in related_list:
                alignment = al.align(w1, w2)
                if al.morpho_related(alignment, s1, s2):
                    words_with_alt.add(w1)
                    words_with_alt.add(w2)
                    new_related_list.append( (w1, w2, score) )
            related_list = new_related_list
        else:
            for w1, w2, score in related_list:
                words_with_alt.add(w1)
                words_with_alt.add(w2)
        
        #Calculate frequency of alternation using sets to ensure no duplicates (i.e. words with both s1 and s2)
        all_words = set()
        for word in list_s1:
            w = getattr(word, 'spelling')
            all_words.add(w)
        for word in list_s2:
            w = getattr(word, 'spelling')
            all_words.add(w)
            
        freq_of_alt = len(words_with_alt)/len(all_words)
        
        if from_gui and not output_filename:
            return len(all_words), len(words_with_alt), freq_of_alt

        elif from_gui and output_filename:
            with open(output_filename, mode='w', encoding='utf-8') as outf2:
                outf2.write('{}\t{}\t{}\r\n\r\n'.format('FirstWord', 'SecondWord', 'RelatednessScore'))
                for w1, w2, score in related_list:
                    outf2.write('{}\t{}\t{}\r\n'.format(w1, w2, score))
                outf2.write('\r\nStats\r\n------\r\n')
                outf2.write('words_with_{}\t{}\r\n'.format(s1, len(list_s1)))
                outf2.write('words_with_{}\t{}\r\n'.format(s2, len(list_s2)))
                outf2.write('total_words\t{}\r\n'.format(len(all_words)))
                outf2.write('total_words_alter\t{}\r\n'.format(len(words_with_alt)))
                outf2.write('freq_of_alter\t{}\r\n'.format(freq_of_alt))
                
            return len(all_words), len(words_with_alt), freq_of_alt

    def get_lists(self, s1, s2, string):
        """Given two sounds, returns list of Words from the current corpus that have such sounds

        Parameters
        ----------
        s1: char
            A sound segment, e.g. 's', 'ÃƒÆ’Ã…Â Ãƒâ€ Ã¢â‚¬â„¢',
        s2: char
            A sound segment
        string: string
            The type of segments to be used ('spelling' = roman letters, 'transcription' = IPA symbols)
        """
        s1_list = list()
        s2_list = list()
        for w in self.corpus:
            word = getattr(w, string)
            if not isinstance(word, str):
                word = ''.join(seg.symbol for seg in word)
            if s1 in word and s2 in word:
                s1_list.append(w)
                s2_list.append(w)
            elif s1 in word:
                s1_list.append(w)
            elif s2 in word:
                s2_list.append(w)
            else:
                pass
        return [s1_list, s2_list]

    def __init__(self,corpus_name, size = 'all', ready_made_corpus=None):
        """Initialize a frequency of alternation analyzer by building a corpus or utilizing an already make corpus

        Parameters
        ----------
        corpus_name: string
            The corpus name, e.g. 'Iphod'
        size: int
            The size of the corpus
        ready_made_corpus: Corpus
            A corpus that has been built, if none provided, __init__ will build one

        Returns
        -------
        None
        """
        if ready_made_corpus is not None:
            self.corpus = ready_made_corpus
        else:
            print('Building Corpus')
            start_time = time.time()
            self.factory = CorpusFactory()
            self.corpus = self.factory.make_corpus(corpus_name, features='hayes', size=size)
            end_time = time.time()
            print('Corpus Complete')
            print('Corpus creation time: ' + str(end_time-start_time))


if __name__ == '__main__':
    pass
##    relator = Relator('subtlex') #give name of a corpus here, 'iphod' also works
##    relator.relate('children', 'subtlex_children_token_count.txt', string_type='spelling', count_what='token')
