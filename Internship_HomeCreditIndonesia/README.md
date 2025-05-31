# Business Understanding
## Problem Statement

HomeCreditIndonesia memiliki 9,01% default kreditur. Permasalahan tersebut dapat menyebabkan kerugian Rp2.171.363.980,50. Perusahaan ingin Tim Data Scientist berkolaborasi dengan Tim Credit Analyst untuk menyelsaikan masalah tersebut.
## Goals and Objective

Tim sepakat untuk membuat model credit risk untuk mengurangi jumlah default kreditur dan kerugian. Model ini juga bisa menghasilkan credit scoring untuk tambahan pertimbangan menentukan kredit limit, interest rate ataupun term pada loan applicant.

# Feature Engineering and Data Preprocessing

Feature engineering bertujuan untuk melengkapi fitur yang sudah ada di application test. Tim Data Science mendapatkan data historical applicant dari pemerintah, financial lending lain ataupun sumber internal. Data-data tersebut akan melengkapi fitur yang ada.

Banyak data yang tidak lengkap atau tidak terisi sehingga dianggap sebagai null values. Oleh karena itu untuk Handling Missing Value tim data scientist melakukan imputasi. Data yang memiliki outlier ekstrim akan didrop dengan metode IQR. Kemudian dilakukan transformasi dengan metode WeightofEvidence (WOE). Lalu, data yang memiliki korelasi kuat dengan banyak variabel akan didrop karena akan menyebabkan multicollineriaty.

# Modelling


Total dataset yang digunakan untuk modeling adalah 223.008 dengan 32 fitur. Fitur yang dipilih berdasarkan profile dan historical repayment capability applicant. Dataset akan dibagi sebagai 80% train dan 20% test. Model akan diuji juga dengan test dataset tanpa label untuk analisis kedepannya.
Pada pengujian kali ini menggunakan beberapa algoritma. Hasil dari pengujian tersebut logistic regression dipilih karena memiliki nilai AUC test dan precission yang paling tinggi. AUC test dapat memaksimalkan performa yang baik dalam credit scoring karena menunjukan sensitifitas model. Lalu, precision dipilih untuk mengurangi false-negative pada hasil pengujian. Dilakukan GridSearchCV untuk mengoptimasi parameter yang digunakan dan menguji model pada cross validation berbeda-beda untuk meningkatkan kemampuan robust model pada Logistic Regression. 
Fitur yang paling berpengaruh adalah PAY INSTALLMENT (jumlah pembayaran yang pernah ditunggak applicant), CREDIT_ACTIVE (jumlah kredit aktif yang dimiliki applicant ketika mengajukan kredit) dan HIGH_APPROVED_CREDIT (jumlah kredit terbesar yang pernah diterima oleh applicant). Tim Data Scientist memberikan rekomendasi pada Tim Credit Analyst untuk waspada dengan appkicant yang sering menunggak pembayaran kredit dan memiliki jumlah kredit aktif yang banyak karena memiliki kemungkinan default yang tinggi.
Dengan menggunakan model dapat mengurangi jumlah kredit yang default sebesar Rp 964.231.128,00 dan  mengurangi jumlah default creditor sebanyak 3,23%.
Credit scoring yang dibuat oleh tim data scientist menyarankan untuk applicant yang memiliki kategori DECILE 0 dan 1 untuk ditolak karena kemungkinan terjadinya default sangat tinggi.
Untuk dataset yang memiliki label dari total 48.744 applicant ditemukan 8.380 applicant yang memiliki resiko yang tinggi untuk mengalami default. Oleh karena itu applicant tersebut dapat ditolak untuk meminimalisir jumlah default kredit.
