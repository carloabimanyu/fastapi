# FastAPI

Nama: Carlo Abimanyu <br>
NPK: 67660 <br>

Ini adalah repository untuk assignment Product Operationalization & VCS. Pada tugas ini, saya mengambil data dari API Jikan (https://jikan.moe/) kemudian melakukan analisis sederhana sebagai API di https://fastapi-carlo.herokuapp.com/. Berikut adalah beberapa endpoints yang saya buat.
* `/topAnime` return top 10 anime
* `/topMember` return top 10 anime (based on members count)
* `/typeScore` return average score for each type
* `/yearScore` return average score for each year
* `/typeCount` return count of anime for each type
* `/typeMember` return count of member for each member
* `/bestSeasonalAnime/{year}/{season}` return top 3 anime for specific season in a year
* `/recommendation/{tipe}/{year}/{min_score}` return recommendation based on type, year, and minimum score
Untuk menampilkan 3 anime terbaik untuk season tertentu pada tahun tertentu, contohnya `/bestSeasonalAnime/2020/winter`. Adapun untuk menampilkan rekomendasi anime berdasarkan tipe (TV, Movie, Special, OVA, ONA, Music), tahun, dan rating minimum, contohnya `/recommendation/Movie/2017/8.5`.
