import unittest
import test_common
from nytimes_article import *
from nytimes_article_accessor import *
from pronoun_gender import *

class PronounGenderTest(unittest.TestCase):
  def setUp(self):
    self.pronoun_gender = PronounGender("data/pronouns/female-EN.csv", "data/pronouns/male-EN.csv", "data/pronouns/neutral-EN.csv")

  def testEstimateGender(self):
    article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    data_file = article.getDataFileObject("data/full", "test/fixtures/nytimes-data/", "txt")
    fulltext = data_file.read();
    self.assertEqual("M", self.pronoun_gender.estimate_gender(fulltext))
    self.assertEqual("M", self.pronoun_gender.estimate_gender("him Him he"))
    self.assertEqual("N", self.pronoun_gender.estimate_gender("Him her him herself"))
    self.assertEqual("F", self.pronoun_gender.estimate_gender("she her him herself"))

  def testCountPronounGender(self):
    article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    data_file = article.getDataFileObject("data/full", "test/fixtures/nytimes-data/", "txt")
    fulltext = data_file.read();
    pg = self.pronoun_gender.count_pronoun_gender(fulltext)
    self.assertEqual(4, pg["male"])
    self.assertEqual(4, pg["neutral"])
    self.assertEqual(0, pg["female"])
    
    pg = self.pronoun_gender.count_pronoun_gender("Him he he's she her she's they theirs")
    self.assertEqual(3, pg["male"])
    self.assertEqual(3, pg["female"])
    self.assertEqual(2, pg["neutral"])

test_common.ALL_TESTS.append(PronounGenderTest)

if __name__ == '__main__':
  unittest.main()
