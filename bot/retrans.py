from googletrans import Translator, LANGUAGES
from random import randint

class Retrans(Translator):

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.lang_list = ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', 'fil', 'he']
        self.level = 1
    
    def set_level(self, retrans_level):
        self.level = retrans_level
    
    def get_trans_list(self):
        trans_list = []
        lang_num = len(self.lang_list) - 1

        for i in range(self.level):
            trans_list.append(self.lang_list[randint(0, lang_num)])
        return trans_list

    def detect_lang(self):
        detected_lang = self.detect(self.text).lang
        return detected_lang

    def retrans(self):
        result = {}
        result["text"] = self.text
        result["level"] = self.level
        trans_rec = []
        for lang in self.get_trans_list():
            self.text = self.translate(self.text, dest=lang).text
            trans_rec.append({LANGUAGES[lang] : self.text})

        result["trans_rec"] = trans_rec
        result["retrans"] = self.translate(self.text, dest='ja').text
        return result
