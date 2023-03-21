# Tubes Big Data
Proyek ini akan mengambil metadata video dari youtube api terkait video-video politik. Hal ini dilakukan untuk mengklasifikasikan sebuah video berdasarkan deskripsinya menggunakan sebuah model machine learning. Struktur dari proyek ini adalah sebagai berikut.

config : menyimpan konfigurasi yang diperlukan, untuk melakukan training maupun inference hanya tinggal mengubah parameter yang ada di config.py
data : menyimpan data untuk keperluan I/O 
model : menyimpan model DL untuk analisis sentimen maupun vectorizer untuk tokenisasi teks
src : menyimpan semua source code yang dibutuhkan

untuk keperluan training dan inference data dari sebuah file csv dapat langsung melihat di test.py
Sementara jika ingin menggunakan hdfs sebagai I/O proses maka dapat melihat test_inference.py
