import re
def syl(text):
  try:
    result = re.sub(r'([က-အ][ါ-ှ]{0,}[က-အ][့]{0,}[်][ါ-ှ]*|[က-အ][္][က-အ][ါ-ှ]{0,}|[က-အ][ါ-ှ]{0,})', r'\1 ', text)
    return result
  except Exception as e:
    print(e)