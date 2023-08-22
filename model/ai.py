# from nltk.corpus import stopwords
# from sklearn.metrics.pairwise import linear_kernel
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.tokenize import RegexpTokenizer
import re
import nltk
from html import unescape
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


class ai:
    nltk.download('punkt')
    nltk.download('stopwords')

    def preprocessing(data):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        stopword = StopWordRemoverFactory().create_stop_word_remover()

        def cleansing(row):
            text = re.sub(r'&[^\s;&]+;', '', unescape(row['text']))
            html_pattern = re.compile('<.*?>')
            text = html_pattern.sub(r' ', text)
            text = re.sub(
                r'((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', text)
            return text

        def caseFolding(row):
            text = row['text'].lower()
            return text

        def tokenizing(row):
            tokenized = word_tokenize(str(row['text']))
            return tokenized

        def stemming(row):
            stemmed = [stemmer.stem(token) for token in row['text']]
            stemmed = " ".join(stemmed)
            return stemmed

        def stopwording(row):
            stopworded = stopword.remove(row['text'])
            return stopworded

        data['text'] = data.apply(cleansing, axis=1)
        data['text'] = data.apply(caseFolding, axis=1)
        data['text'] = data.apply(tokenizing, axis=1)
        data['text'] = data.apply(stemming, axis=1)
        data['text'] = data.apply(stopwording, axis=1)

        return data

    def preprocessingEng(data):
        stemmer = PorterStemmer()

        def cleansing(row):
            text = re.sub(r'&[^\s;&]+;', '', unescape(row['text']))
            html_pattern = re.compile('<.*?>')
            text = html_pattern.sub(r' ', text)
            text = re.sub(
                r'((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', text)
            text = text.lower()
            return text

        def caseFolding(row):
            text = row['text'].lower()
            return text

        def tokenizing(row):
            tokenized = word_tokenize(str(row['text']))
            return tokenized

        def stemming(row):
            stemmed = [stemmer.stem(token) for token in row['text']]
            stemmed = " ".join(stemmed)
            return stemmed

        def stopwording(row):
            stopword = set(stopwords.words('english'))
            tokens = word_tokenize(str(row['text']))
            stopworded = [token for token in tokens if token not in stopword]
            stopworded = " ".join(stopworded)
            return stopworded

        data['text'] = data.apply(cleansing, axis=1)
        data['text'] = data.apply(caseFolding, axis=1)
        data['text'] = data.apply(tokenizing, axis=1)
        data['text'] = data.apply(stemming, axis=1)
        data['text'] = data.apply(stopwording, axis=1)

        return data

    def search(data, keyword):
        # cursor = mysql.connection.cursor()
        # cursor.execute("TRUNCATE `cbrs_words`")
        # mysql.connection.commit()

        # cursor.execute("TRUNCATE `cbrs_tfidf`")
        # mysql.connection.commit()

        # cursor.execute("TRUNCATE `cbrs_result`")
        # mysql.connection.commit()
        keyword = ai.preprocessing(keyword)

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(data['text'])
        new_tfidf_vector = vectorizer.transform(keyword["text"])

        print()
        print()
        # print(new_tfidf_vector)
        # for word_index, word in enumerate(words):
        #     query = "INSERT INTO `cbrs_words` (`word`) VALUES('" + \
        #         str(word) + "')"
        #     query2 = "INSERT INTO `cbrs_tfidf` (`word_id`, `tf`, `idf`) VALUES('" + str(word_index) + "', '" + str(
        #         document_frequencies[word_index]) + "', '" + str(idf_values[word_index]) + "')"
        #     cursor.execute(query)
        #     mysql.connection.commit()
        #     cursor.execute(query2)
        #     mysql.connection.commit()

        # for indexColumn, columnName in enumerate(dfCombine):
        #     for word_index, word in enumerate(words):
        #         tf = tfidf_matrix_count[indexColumn, word_index]
        #         tfidf = float(
        #             tfidf_matrix_count[indexColumn, word_index]) * float(idf_values[word_index])
        #         query = "INSERT INTO `cbrs_result` (`word_id`, `document_id`, `tf`, `tfidf`, `normalized_tfidf`) VALUES('" + str(
        #             word_index) + "', '" + str(indexColumn) + "', '" + str(tf) + "', '" + str(tfidf) + "', '" + str(tfidf_matrix.toarray()[indexColumn, word_index]) + "')"
        #         cursor.execute(query)
        #         mysql.connection.commit()
        # if indexColumn == 0:
        #     continue
        # elif indexColumn > len(dfCombine):
        #     if indexColumn == len(dfCombine):
        #         indexColumnTemp = 0

        #     for word_index, word in enumerate(words):
        #         printDataFrame.at[word_index,
        #                           columnName] = new_tfidf_vector_count[indexColumnTemp, word_index]
        # else:
        #     for word_index, word in enumerate(words):
        #         printDataFrame.at[word_index,
        #                           columnName] = tfidf_matrix_count[indexColumnTemp, word_index]

        # indexColumnTemp += indexColumnTemp
        print()
        print()
        similarity_scores = cosine_similarity(new_tfidf_vector, tfidf_matrix)
        return similarity_scores[0]

    # def search(data, keyword):

    #     print("")
    #     print("")

    #     data = [
    #         "Web Developer <p>Kami sedang mencari seorang Web Developer yang berpengalaman untuk bergabung dengan tim kami. Tanggung jawab Anda akan mencakup pengembangan front-end dan back-end, serta memastikan keberlanjutan dan performa tinggi dari situs web kami.</p> <h2>Kualifikasi:</h2> <ul> <li>Pengalaman dalam HTML, CSS, dan JavaScript</li> <li>Pemahaman yang baik tentang desain responsif</li> <li>Pengalaman dalam pengembangan situs web menggunakan CMS seperti WordPress</li> <li>Kemampuan untuk bekerja dalam tim</li> </ul>",
    #         "Data Scientist <p>Kami mencari seorang Data Scientist yang handal dan berpengalaman untuk bergabung dengan tim kami. Tugas Anda akan meliputi analisis data, pengembangan model prediktif, dan penemuan wawasan berharga dari set data yang kompleks.</p> <h2>Kualifikasi:</h2> <ul> <li>Pengalaman dalam analisis data menggunakan Python atau R</li> <li>Pemahaman yang kuat tentang statistik dan metode analisis data</li> <li>Pengalaman dalam penggunaan alat-alat seperti SQL dan Pandas</li> <li>Kemampuan komunikasi yang baik untuk menyampaikan hasil analisis dengan jelas</li> </ul>",
    #         "UI/UX Designer <p>Kami sedang mencari seorang UI/UX Designer yang kreatif dan berbakat untuk bergabung dengan tim kami. Tanggung jawab Anda akan meliputi merancang antarmuka pengguna yang menarik dan fungsional, serta melakukan pengujian pengguna dan iterasi desain.</p> <h2>Kualifikasi:</h2> <ul> <li>Pengalaman dalam merancang antarmuka pengguna yang menarik</li> <li>Pemahaman tentang prinsip-prinsip desain UI/UX</li> <li>Kemampuan menggunakan alat desain seperti Adobe XD atau Sketch</li> <li>Kemampuan untuk bekerja dalam tim dan berkolaborasi dengan pengembang</li> </ul>",
    #         "Front-end Developer <p>Kami mencari seorang Front-end Developer yang berpengalaman untuk bergabung dengan tim pengembangan kami. Anda akan bertanggung jawab dalam mengembangkan antarmuka pengguna interaktif menggunakan HTML, CSS, dan JavaScript serta memastikan kinerja optimal dan responsif dari situs web kami.</p> <h2>Kualifikasi:</h2> <ul> <li>Pengalaman dalam pengembangan antarmuka pengguna menggunakan HTML, CSS, dan JavaScript</li> <li>Pemahaman yang baik tentang desain responsif dan pengujian lintas browser</li> <li>Pengalaman dengan kerangka kerja (framework) seperti React atau Vue.js</li> <li>Kemampuan untuk bekerja dalam tim dan berkolaborasi dengan desainer UI/UX</li> </ul>",
    #         "Front-end Web Developer <ul> <li><strong>Deskripsi:</strong></li> <ul> <li>Mengembangkan antarmuka pengguna (UI) yang menarik dan responsif untuk website.</li> <li>Mengimplementasikan desain web menggunakan HTML, CSS, dan JavaScript.</li> <li>Memastikan kesesuaian lintas browser (cross-browser compatibility) pada antarmuka pengguna.</li> <li>Optimasi kinerja website agar responsif dan cepat diakses oleh pengguna.</li> <li>Kolaborasi dengan tim pengembang dan desainer untuk menghasilkan pengalaman pengguna terbaik.</li> <li>Menggunakan framework dan alat pengembangan front-end seperti React, Angular, atau Vue.js.</li> </ul> <li><strong>Kualifikasi:</strong></li> <ul> <li>Pemahaman yang kuat tentang HTML, CSS, dan JavaScript.</li> <li>Pengalaman dengan framework front-end seperti React, Angular, atau Vue.js merupakan nilai tambah.</li> <li>Kemampuan dalam desain responsif dan lintas browser compatibility.</li> <li>Kemampuan pemecahan masalah dan pemikiran kreatif dalam menghadapi tantangan pengembangan front-end.</li> <li>Kemampuan kerja dalam tim yang baik dan komunikasi yang efektif.</li> </ul> </ul>",
    #         "Back-end Web Developer <ul> <li><strong>Deskripsi:</strong></li> <ul> <li>Memiliki tanggung jawab dalam pengembangan logika aplikasi web sisi server.</li> <li>Integrasi antarmuka pengguna (UI) dengan elemen-elemen sisi depan.</li> <li>Mengembangkan API (Application Programming Interface) untuk komunikasi dengan aplikasi lain.</li> <li>Mengelola basis data dan memastikan keamanan serta efisiensi dalam pengaksesan data.</li> <li>Menerapkan praktik keamanan dalam pengembangan aplikasi web.</li> <li>Pemecahan masalah dan debugging pada sisi server.</li> </ul> <li><strong>Kualifikasi:</strong></li> <ul> <li>Pemahaman yang kuat tentang bahasa pemrograman sisi server seperti Java, Python, atau PHP.</li> <li>Pengalaman dengan pengembangan API (Application Programming Interface).</li> <li>Pengalaman dengan pengelolaan basis data dan SQL.</li> <li>Pemahaman tentang praktik keamanan dalam pengembangan aplikasi web.</li> <li>Kemampuan pemecahan masalah dan pemikiran analitis.</li> <li>Kemampuan kerja dalam tim dan komunikasi yang baik.</li> </ul> </ul>",
    #     ]

    #     # data = ['Ini adalah contoh dokumen pertama.', 'Ini adalah contoh dokumen kedua.', 'Ini adalah contoh dokumen ketiga.',
    #     #         'Ini adalah contoh dokumen keempat.', 'Saya suka makan nasi goreng', 'Nasi goreng adalah makanan favorit saya', 'Saya makan nasi goreng setiap hari', ]

    #     # df = pd.DataFrame(data, columns=["texttt"])
    #     # df = df.dropna()
    #     # # menghapus stop words (kata-kata umum yang sering muncul dan biasanya tidak memiliki makna penting dalam analisis teks)
    #     stopword = StopWordRemoverFactory().create_stop_word_remover()
    #     for i, text in enumerate(data):
    #         html_pattern = re.compile('<.*?>')
    #         data[i] = stopword.remove(html_pattern.sub(r'', text.lower()))

    #         # df.at[i, "texttt"] = stopword.remove(
    #         #     html_pattern.sub(r'', df.loc[i, 'texttt'].lower())
    #         # )

    #     # vectorizer = TfidfVectorizer()

    #     # vectorizer.fit(df['texttt'])
    #     # tfidf_matrix = vectorizer.fit_transform(df['texttt'])
    #     # new_tfidf_vector = vectorizer.transform(["contoh nasi"])
    #     # similarity_scores = cosine_similarity(new_tfidf_vector, tfidf_matrix)
    #     # # Mengurutkan indeks berdasarkan similarity score terbesar
    #     # sorted_indices = similarity_scores.argsort()[0][::-1]
    #     # # Dokumen dengan similarity score terbesar
    #     # most_similar_doc_index = sorted_indices[0]
    #     # most_similar_score = similarity_scores[0][most_similar_doc_index]
    #     # most_similar_doc = data[most_similar_doc_index]

    #     # # print(f"Dokumen baru {doc_index+1}: {tfidf_score}")
    #     # print(f"Dokumen yang paling mirip: {most_similar_doc}")
    #     # print(f"Skor similarity: {most_similar_score}")
    #     # print(similarity_scores)
    #     # print(sorted_indices)
    #     # vectorizer.fit(data)
    #     # tfidf_matrix = vectorizer.fit_transform(data)
    #     # new_tfidf_vector = vectorizer.transform(["nasi"])
    #     # Melakukan fitting dan transformasi pada data dokumen
    #     # tfidf_matrix = vectorizer.fit_transform(data)

    #     # Mendapatkan daftar fitur kata unik
    #     # feature_names = vectorizer.get_feature_names_out()

    #     # # Menampilkan hasil
    #     # for doc_index, doc in enumerate(data):
    #     #     print(f"Dokumen {doc_index+1}:")
    #     #     for feature_index in tfidf_matrix[doc_index].indices:
    #     #         print(
    #     #             f"{feature_names[feature_index]}: {tfidf_matrix[doc_index, feature_index]}")
    #     #     print()

    #     # # vectorizer.get_feature_names_out()
    #     # # print(tfidf_matrix)
    #     # print("")
    #     # print("")

    #     # keyword = "contoh"
    #     # new_tfidf_matrix = vectorizer.transform([keyword])
    #     # # keyword_index = feature_names.index(keyword)

    #     # # Menampilkan hasil
    #     # print(f"Kata kunci: {keyword}")
    #     # # Menampilkan hasil transformasi dokumen baru
    #     # for doc_index, doc in enumerate(new_documents):
    #     #     print(f"Dokumen baru {doc_index+1}:")
    #     #     for feature_index in new_tfidf_matrix[doc_index].indices:
    #     #         print(
    #     #             f"{feature_names[feature_index]}: {new_tfidf_matrix[doc_index, feature_index]}")
    #     #     print()

    #     print("")
    #     print("")
    #     return data
    # # new_tfidf_vector = vectorizer.transform([keyword])
    # similarity_scores = cosine_similarity(new_tfidf_vector, tfidf_matrix)

    # # return similarity_scores[0]
