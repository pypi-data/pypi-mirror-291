from fastapi import FastAPI, UploadFile, File
from collections import Counter
import pandas as pd
import re
import liwc

class Social_LIWC:
    def __init__(self, dictionary_path):
        self.parse, self.category_names = liwc.load_token_parser(dictionary_path)
        self.last_file_counts = {}

    def tokenize(self, text):
        for match in re.finditer(r'\w+', text, re.UNICODE):
            yield match.group(0)

    def detect_text_column(self, df):
        text_column = None
        max_avg_length = 0
        for col in df.columns:
            if df[col].dtype == 'object':
                avg_length = df[col].apply(lambda x: len(str(x))).mean()
                if avg_length > max_avg_length:
                    max_avg_length = avg_length
                    text_column = col
        return text_column

    def analyze(self, df):
        file_counts = Counter()
        text_column = self.detect_text_column(df)
        
        if text_column is None:
            return {"error": "Nenhuma coluna de texto foi detectada no CSV"}

        for text in df[text_column]:
            text_tokens = self.tokenize(str(text))
            text_counts = Counter(category for token in text_tokens for category in self.parse(token))
            file_counts.update(text_counts)

        self.last_file_counts = dict(file_counts)
        return self.last_file_counts

app = FastAPI()
social_liwc = Social_LIWC('./Social_LIWC/dados/v2_LIWC2007_Portugues_win.dic')

@app.post("/analise-liwc")
async def analise_liwc(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        return {"error": "O arquivo enviado não é um CSV"}
    
    df = pd.read_csv(file.file)
    result = social_liwc.analyze(df)
    return result

@app.get("/categorias-liwc")
async def get_liwc_categories():
    if not social_liwc.last_file_counts:
        return {"error": "Nenhuma análise de arquivo foi feita ainda."}
    return social_liwc.last_file_counts