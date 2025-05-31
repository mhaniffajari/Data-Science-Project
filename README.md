# Final_Project_Rakamin_23
## Problem
Trips&Travel.com memiliki 5 buah paket wisata yang sudah ditawarkan ke customernya, namun hanya 18% customer yang mengambil paket wisata tersebut. Hal ini menyebabkan membengkaknya cost marketing.

Kali ini, Trips&Travel.com ingin menambah 1 paket wisata baru, dan ingin memaksimalkan cost marketing ke customer potensial

## Goals

● Menurunkan biaya marketing dengan memprediksi pelanggan potensial yang akan
ditawarkan paket perjalanan baru berdasarkan data pelanggan yang tersedia pada
tahun lalu.

● Meningkatkan basis pelanggan

## Objective

● Membuat model yang bisa menurunkan biaya pemasaran sebanyak 50% dari biaya
pemasaran tahun lalu

● Membuat model untuk memprediksi customer yang potensial agar basis pelanggan naik
sebanyak 80%

## Business Metrics

● Buy Rate : Persentase banyaknya pelanggan yang akan membeli paket perjalanan.

● Marketing Cost : Dana yang dikeluarkan untuk pemasaran

## EDA
Target = ProdTaken

Kolom dibagi menjadi 3 bagian, yaitu

Numerical :
1. DurationOfPitch (Memiliki distribusi positive skewness dan berkorelasi
positif sebesar 0.078)

2. Age (Memiliki distribusi normal dimana customer dengan umur 30-40
paling banyak ditawarkan paket wisata, sedangkan rentang umur 18-21
merupakan umur yang paling tinggi %prodTaken dan berkorelasi negatif
sebesar -0.15 dengan target)

3. MonthlyIncome (Cenderung untuk positive skewness (Memiliki trend) dan
berkorelasi negatif sebesar -0.13. Nilai terkumpul pada range 20346.00 hingga
25571.00, memiliki nilai min 1000 dan max 98678 serta memiliki banyak
outliers)

Categoricals :
1. TypeOfContact berdistribusi negative dan memiliki korelasi positif terhadap
ProdTaken sebesar 0.078

2. Occupation berdistribusi positive dan Free lancer memiliki nilai tertinggi

3. Gender berdistribusi negative dimana Male memiliki nilai tertinggi

terhadap ProdTaken
4. ProductOfPitched

5. Marital Status berdistribusi negative

6. Designation berdistribusi normal dimana executive, manager, dan senior
manager banyak mengambil paket wisata

Numeric categorical :
1. ProdTaken

2. NumberOfPersonVisiting memiliki korelasi positif sebesar 0.0096

3. NumberOfFollowups memiliki korelasi positif sebesar 0.11

4. Passport memiliki korelasi positif sebesar 0.26

5. PitchSatisfactionScore memiliki korelasi positif sebesar 0.051

6. OwnCar memiliki korelasi positif sebesar -0.012

7. NumberOfChildrenVisiting memiliki korelasi positif sebesar 0.0074

8. CityTier memiliki korelasi positif sebesar 0.087


## Preparation

Setelah di cek ternyata data tidak memiliki data duplicate sedangkan jumlah baris yang memiliki missing value terdapat
760 atau sekitar 15%. Tindakan yang dilakukan untuk missing value tersebut, yaitu

• Imputasi numerikal dengan median

• Imputasi dengan designation (liat distribusi antara umur dan designation)

• Imputasi kategorikal bisa modus

• Imputasi kategorikal bisa korelasi dengan variabel lain

• NumberOfTrips nilai null disebabkan karena customer tidak pernah ikut trip

• NumberOfFollowups nilai null disebabkan karena customer belum dilakukan followup kembali setelah pitching

• NumberOfChildrenVisitting nilai null disebabkan customer tidak punya anak yang ikut

Lalu, Kolom DurationOfPitch memiliki outlier 2 data dengan boxplot karena jauh Q3 dan MonthlyIncome memiliki

banyak outlier, sehingga tindakan yang dilakukan yaitu menghilangkan outlier dengan Z-score dan IQR dimana data
yang digunakan saat ini sebesar 92.29%.

### Pemiihan Feature

Seluruh Features dalam dataset digunakan untuk membuat model


