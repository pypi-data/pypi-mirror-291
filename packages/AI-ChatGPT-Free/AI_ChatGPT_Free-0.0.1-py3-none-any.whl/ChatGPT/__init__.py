from urllib.parse import quote as __quote

from requests import get as __get
from requests.exceptions import ConnectionError as __ConnectionError

if __name__ == '__main__':
    while 1:
        a = input('输入问题（啥都行）：')
        if a == 'exit':
            break
        reponse = __get('https://api.sizhi.com/bot?appid=9ffcb5785ad9617bf4e64178ac64f7b1&spoken=%s'% __quote(a))
        json = reponse.json()
        print(str(json['data']['info']['text']).replace('*',''))
        reponse.close()
#]
else:
    __all__ = ['chat','WIFIWarning','NullQuestionWarning']
    class WIFIWarning(Warning):
        def __init__(self,message):
            self.message = message
        def __str__(self):
            return self.message
    class NullQuestionWarning(Warning):
        def __init__(self, question=None):
            self.question = question
        def __str__(self):
            return repr(self.question)
    def chat(text:str):
        try:
            reponse = __get('https://api.sizhi.com/bot?appid=9ffcb5785ad9617bf4e64178ac64f7b1&spoken=%s' % __quote(text))
        except __ConnectionError:
            raise WIFIWarning('Your WiFi seems to be disconnected or experiencing issues.')
        json = reponse.json()
        reponse.close()
        if json['status'] == -1:
            raise NullQuestionWarning(text)
        return str(json['data']['info']['text']).replace('*', '')