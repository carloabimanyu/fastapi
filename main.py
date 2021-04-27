import json
import pandas as pd
from urllib.request import urlopen
from fastapi import FastAPI

app = FastAPI()

# Proses pengambilan data dari API Jikan
data = []
pages = 2
for i in range(pages):
    url = 'https://api.jikan.moe/v3/top/anime/{}/'.format(str(i+1))
    response = urlopen(url)
    data.extend(json.load(response)['top'])
df = pd.json_normalize(data)
df['release_year'] = df['start_date'].apply(lambda x: x[-4:]).astype(int)


# Halaman awal API dan penjelasan endpoints
@app.get("/")
def read_root():
    return {"title":"MyAnimeList Unofficial API (Jikan)",
            "message":"please read endpoint instructions",
            "endpoints":{
                "/docs":"API documentation",
                "/topAnime":"return top 10 anime",
                "/topMemberCount":"return top 10 anime (based on members count)",
                "/typeScore":"return average score for each type",
                "/yearScore":"return average score for each year",
                "/typeCount":"return count of anime for each type",
                "/typeMember":"return count of member for each member",
                r"/bestSeasonalAnime/{year}/{season}":"return top 3 anime for specific season in a year",
                r"/recommendation/{tipe}/{year}/{min_score}":"return recommendation based on type, year, and minimum score",
                "/data":"return raw data"
            },
            "type options":"TV, Movie, Special, OVA, ONA, Music (case sensitive)",
            "season options":"winter, spring, summer, fall (case sensitive)"
        }


# Endpoint untuk menampilkan raw data
@app.get("/data")
def raw_data():
    return df.to_json(orient='records')


# Endpoint untuk menampilkan top 10 anime
@app.get("/topAnime")
def read_topAnime():
    col = ['rank', 'title', 'type', 'members', 'score']
    result = df[col].head(10)
    return result.to_dict(orient='records')


# Endpoint untuk menampilkan top 10 anime dengan member terbanyak
@app.get("/topMemberCount")
def read_topMemberCount():
    col = ['title', 'type', 'members', 'score']
    result = df[col].head(10)
    return result.to_dict(orient='records')


# Endpoint untuk menampilkan rata-rata score berdasarkan tipe
@app.get("/typeScore")
def read_typeScore():
    result = df.groupby('type')[['score']].mean()
    return result.to_dict(orient='dict')


# Endpoint untuk menampilkan rata-rata score berdasarkan tahun
@app.get("/yearScore")
def read_yearScore():
    result = df.groupby('release_year')[['score']].mean()
    return result.to_dict(orient='dict')


# Endpoint untuk menampilkan jumlah anime berdasarkan tipe
@app.get("/typeCount")
def read_typeCount():
    result = df.groupby('release_year')[['mal_id']].count()
    result.rename(columns={'mal_id':'count'}, inplace=True)
    return result.to_dict(orient='dict')


# Endpoint untuk menampilkan jumlah member berdasarkan tipe
@app.get("/typeMember")
def read_typeMember():
    result = df.groupby('type')[['members']].sum()
    return result.to_dict(orient='dict')


# Endpoint untuk menampilkan 3 anime terbaik pada season dan tahun tertentu
@app.get("/bestSeasonalAnime/{year}/{season}")
def read_bestSeasonalAnime(year: int, season: str):
    seasonal = []
    url_season = 'https://api.jikan.moe/v3/season/{}/{}'.format(year, season)
    response_season = urlopen(url_season)
    seasonal.extend(json.load(response_season)['anime'])
    df_seasonal = pd.DataFrame(seasonal)
    col = ['title', 'type', 'members', 'score', 'url']
    result = df_seasonal[col].sort_values(by='score', ascending=False).head(3)
    return result.to_dict(orient='records')


# Endpoint untuk mendapatkan rekomendasi anime berdasarkan tahun, tipe, dan score minimal
@app.get("/recommendation/{tipe}/{year}/{min_score}")
async def read_recommendation(tipe: str, year: int, min_score: float):
    col = ['rank', 'title', 'members', 'score', 'release_year', 'url']
    result = df[col][(df.type == tipe) & (df.release_year >= year) & (df.score >= min_score)].sort_values(by='score', ascending=False)
    return result.to_dict(orient='records')
