import sys
import csv
import re
import helpers

COL_CATEGORY = 'Kategori'
COL_NAME = 'Nama Perusahaan'
COL_ADDRESS = 'Alamat'
COL_CITY = 'Kota'
COL_PHONE = 'No. HP'
COL_EMAIL = 'Email'
COL_WEBSITE = 'Website'
COL_DESCRIPTION = 'Deskripsi'

c_valid = ['Animal Feed Store','Aquarium Shop','Peternak Hewan Peliharaan','Pelatih Hewan','Menunggang Kuda','Toko Hewan Peliharaan','Kebun Binatang','Bird Store','Pet Groomer','Dokter Hewan','Aromatheraphy & Supplier','Barbershop & Supplier','Salon Kecantikan & Supplier','Kosmetik','Fitness & Nutrisi Service','Foot Care','Rambut & Supplier','Health & Spa','Make Up Artist','Pelatih Kesehatan','Tattoo Maker & Store','Yoga Studio & Instruktur','Herbalist','Nail Salon','Skin Care','Vitamin & Suplemen','Weight Loss Service','Therapis Kecantikan','Accounting Software','Advertising','Auditor','Perusahaan Outsourcing','Perusahaan Networking','Business to Business','Business to Customer','Customer Service','Kantor Dagang','Simpan Pinjam','Grosir Pakaian','Jasa Pengangkutan','Penyimpanan Data','Cleaning Service Company','Real Estate Agency','Real Estate & Perumahan','Toko Komputer & Service','Konsultant','Coworking Space','Jasa Pengetikan dan Input','Percetakan','Konsultan Pendidikan','Distributor Elektronika','Pencari Kerja','Export Import','Pengiriman & Logistik','HRD','Industry Berat','Internet Marketing','Web Design Studio','Marketing Agency','Media Consultant','Alat Kantor & Distributor','Bank & Perkreditan','Plastik','Stationery Store','Riset dan Pengembangan Produk','Talent Agency','SEO Service','Sound System & Lighting','Bisnis Center','Pabrik Kimia','Furniture','Printing Shop','Organizer','Jasa Keamanan','Telemarketing Service','Penterjemah','Pemasok Suku Cadang','Batere & Kabel','Aksesories Ponsel','Handphone & Service','Televisi & Komputer','Home Theater & Audio','Internet Provider','Telepon & Provider','Software & Aplikasi','Mesin Cuci, Kulkas & Service','Hosting Provider','Toko Kamera','Kelistrikan','Pusat Hiburan','Pusat Seni','Hiburan Dewasa','Game Service','Event Organizer','Theatre','Perpustakaan','Toko Mainan','Toko Hadiah','Pub & Diskotik','Sewa Peralatan Pesta','Produsen Mainan','Jasa Wedding','Karaoke','Photo Studio','Klinik & Ahli Akupunktur','Pusat Rehabilitasi','Pengobatan ALternatif','Laboratorium Kesehatan','Kesehatan Jantung','Pengobatan Kanker','Kaca Mata','Dentist','Rumah Sakit','Apotik','Pusat Perawatan Mata','Klinik Kesuburan','Operasi Plastic','Dokter Umum','Dokter Spesialis','Telinga Hidung Tenggorokan','Pelayanan Kesehatan di Rumah','Perlengkapan Rumah Sakit','Rumah Sakit Ibu & Anak','Klinik','Produsen Obat','Dokter Kandungan','Ahli Gizi','Patah Tulang','Fisiotherapi','Psikolog','Seksolog','Rumah Sakit Khusus','Pusat Bedah','Farmasi Hewan Peliharaan','Seni & Barang Antik','Gallery Seni','Peralatan Seni & Sulap','Berkemah','Kerajinan Tangan & Souvenir','Perancang Busana','Kaca Hias','Berburu & Memancing','Toko Barang Kulit','Pabrikan Alat Musik','Sanggar Lukis & Toko','Piano','Cenayang','Toko Piala','Toko Benang','Pengacara','Notaris & PPAT','Kantor Imigrasi','Mediator','Kantor Administrasi Kota','Perpajakan','Perdata','Pengadilan','Firma Hukum','Laundry','Tukang AC','Kontraktor Lantai','Pemeliharaan Kebun','Tukang Ledeng','Petugas Keamananan','Pindah Rumah','Pembersihan Kolam Renang','Pembantu Rumah Tangga','AC dan Supplier','Kaca dan Alumunium','Arsitek','Bioteknologi','Kontraktor Bangunan','Toko Bangunan','Perusahaan Konstruksi','Garment & Konveksi','Electrical Engineering','Plumbing Store & Supplier','Pertanian','Dealer Mesin','Pengeboran','Hidrolik & Supplier','Interior','Labrotaroium','Peralatan Survey','Landscape','Penata Taman','Toko Mesin','Pabrik Kelautan','Pemasok Batu Alam','Pabrik Cat','Pemasok Peralatan Bermain','Pemasok System Air','Distributor Logam','Distributor & Pabrik Keramik','Pemasok Kayu','Jendela dan Pintu','Supplier Alat Pabrik','Diesel','Distributor Produk Pertanian','Pabrik Alkohol & Toko','Bakery','Peralatan Memasak','Bir, Wine & Alkohol','Toko & Dekorasi Kue','Catering','Permen & Coklat','Rokok & Cerutu','Kopi & Susu','Pabrikan Makanan','Buah & Sayuran','Organic','Es & Es Krim','Daging & Pemasok','Teh','Cafe','Makanan Sehat','Oleh-oleh','Street Food / Kuliner','Fotografer','Studio Animasi','Audio Visual','Penerbit Buku','Toko Buku','Toko Buku Kristen','Produser Film & Peralatan','Perusahaan Media','Layanan Berita & Koran','Stasiun Radio','Stasiun Televisi','Editor Video dan Produksi','Kantor Akuntan','Perusahaan Asuransi','Money Changer','Bank & Perkreditan','Asuransi Mobil','Perusahaan Pembiayaan','Cryptocurrency','Debt Collector','Konsultan Bisnis','Pegadaian','Audit Keuangan','Broker Saham','Toko & Dealer Emas','Agen Asuransi','Perusahaan Investasi','Investor','Accounting School','Architecture School','Beauty School','Instruktur Mandarin','Persekutuan Kampus','Cooking Class','Penitipan Anak','Sekolah Mengemudi','Sekolah Dasar','Sekolah Menengah Pertama','Sekolah Menengah Atas','Photography School','Nursing School','Sanggar Bela Diri','Home Schooling','Technical School','Pusat Konseling','Business School','Pelatihan Karir','Kursus Komputer','Cullinary School','Institusi Pendidikan','Sekolah Penerbangan','Bimbingan Belajar','PAUD & TK','Balai Latihan Kerja','Universitas / Sekolah Tinggi','Gereja Kristen','Buddhism','Pura & Hindu','Agen Tenaga Kerja','Rumah Duka','Kepolisian & Tentara','Serikat Buruh','Asosiasi Usaha','Organisasi Keagamaan','Organisasi Sosial','Western Food','Chinesse Food','Restoran India','Restoran Keluarga','Drive Thru','Fast Food','Donuts & Pizza','Restoran Seafood','Restoran Jepang','Restoran Korea','Masakan Timur Tengah','Model Ulang Kamar Mandi','Mebel Jepara','Tirai & Gordyn','Perabot Kamar Tidur','Butik','Toko Karpet','Dekorasi Rumah dan Interior','Penjual Bunga','Toko Pecah Belah','Otomatisasi Rumah','Desain Ulang Dapur','Peralatan Rumput','Toko Lampu','Toko Outdoor Rumah','Toko Sofa','Pembuatan Kolam Renang','Wallpaper','Toko Pakaian','Toko Perlengkapan Tentara','Toko Perlengkapan Bayi','Toko Tas & Koper','Toko Pakaian Anak','Toko Perhiasan','Penjahit Pakaian','Toko Serba Ada','Sewa Baju Pesta & Adat','Pengrajin Perhiasan','Baju Renang & Pakaian Dalam','Pabrik & Toko Sepatu','Industri Sepatu Rumahan','Toko Olahraga','Toko Seragam Sekolah','Toko Jam','Toko Busana Muslim','Toko Baju Pria','Mall','Kaos & Konveksi','Olahraga Petualangan','Panahan','Basket','Sepeda','Tinju & Club','Panjat Tebing','Sekolah Dance','Menyelam','Berkuda','Fitness & Gym','Golf & Kursus','Klub Senam','Olahraga Beladiri','Jujitsu','Kick Boxing','Muay Thai Boxing','Olahraga Motor','Paintball','Skateboard & Sepatu Roda','Sepak Bola & Futsal','Selancar','Tenis','Angkat Beban','Olahraga Air','Bulu Tangkis','Perusahaan Penerbangan','Agen Tiket Pesawat','Bandar Udara','Hotel Bandara','Antar Jemput Bandara','Beach Resort','Agency Kapal Pesiar','Hotel','Agen Bus Tour','Cottage','Agen Travel dan Perjalanan','Resor Golf','Homestay','Taman Hiburan','Hotel Mewah','Taksi Bandara','Dealer Mobil','Aksesories Mobil','Bengkel Mobil','Pabrikan Suku Cadang','Sewa Sepeda','Perahu & Service','Penyewaan Mobil','Perusahaan Bus','Bengkel Motor','Toko Ban','Agen Tiket Kereta Api','Dealer Truk','Dealer Mobil Mewah','Dealer Mobil Bekas','Dealer Motor Bekas','Parkir Valet','Exportir Kendaraan','Sewa Yacht','Dealer Motor'];
c_invalid = []
f_desc = {
    'advertising': '{} adalah perusahaan yang bergerak di bidang Advertising.',
    'agen asuransi': '{} merupakan agen asuransi, orang yang bertindak untuk menawarkan dan memasarkan produk asuransi untuk dan atas nama penanggung.',
    'agen travel dan perjalanan': '{} merupakan Agen Travel dan Perjalanan yang melayani berbagai Tour dan Travel perjalanan.',
    'alat kantor & distributor': '{} merupakan distributor alat kantor yang menyediakan berbagai macam alat kantor.',
    'audit keuangan': '{} adalah lembaga audit keuangan,  Audit laporan keuangan merupakan penilaian atas suatu perusahaan atau badan hukum lainnya (termasuk pemerintah) sehingga dapat dihasilkan pendapat yang independen tentang laporan keuangan yang relevan, akurat, lengkap, dan disajikan secara wajar.',
    'bakery': '{} merupakan Bakery atau Toko Roti yang menyediakan berbagai jenis roti dengan berbagai varian.',
    'bank & perkreditan': '{} merupakan perusahaan dalam bidang Bank dan Perkreditan.',
    'beach resort': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'bimbingan belajar': '{} merupakan bimbingan belajar bagi para pelajar dengan berbagai mata pelajaran.',
    'bisnis center': '{} merupakan bisnis center',
    'buah & sayuran': '{} merupakan penyedia Buah dan Sayuran sehat.',
    'catering': '{} merupakan perusahaan catering yang menyediakan segala jenis makanan untuk berbagai acara.',
    'customer service': '{} merupakan perusahaan Customer service yang melayani kendala untuk pelanggan.',
    'dealer mesin': '{} Merupakan perusahaan dealer mesin yang menyediakan mesin - mesin.',
    'dealer mobil': '{} merupakan Dealer Mobil dan Motor yang menyediakan berbagai type Mobil dan Motor.',
    'distributor elektronika': '{} merupakan distributor elektronika yang menyediakan berbagai produk elektronik.',
    'distributor logam': '{} merupakan Distributor Logam yang menyediakan Logam Logam dengan kualitas tinggi.',
    'dokter umum': '{} merupakan dokter umum yang melayani berbagai keluhan penyakit.',
    'export import': '{} adalah perusahaan yang bergerak dalam bidang {}.',
    'furniture': '{} adalah perusahaan yang bergerak dalam bidang {}.',
    'gereja kristen': '{} merupakan gereja kristen yang juga bergerak dalam bidang organisasi sosial',
    'hidrolik & supplier': '{} merupakan Supplier yang menyediakan hidrolik.',
    'institusi pendidikan': '{} merupakan institusi pendidikan yang bergerak di bidang pendidikan.',
    'jasa pelayanan': '{} adalah perusahaan yang bergerak dalam bidang {}.',
    'jasa pengangkutan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'jasa wedding': '{} adalah perusahaan yang bergerak dalam bidang {}.',
    'kaca mata': '{} merupakan Toko {} yang menyediakan berbagai jenis {}.',
    'kantor akuntan': '{} merupakan badan usaha yang telah mendapatkan izin dari Menteri Keuangan sebagai wadah bagi akuntan publik dalam memberikan jasanya.',
    'kantor dagang': '{} merupakan Perusahaan dagang , perusahaan yang bisnis utamanya membeli barang dari pemasok dan menjual lagi ke konsumen tanpa mengubah wujud barang tersebut.',
    'kaos & konveksi': '{} merupakan perusahaan yang bergerak dalam pembuatan {}.',
    'kelistrikan': '{} adalah perusahaan yang bergerak dalam bidang {}.',
    'kerajinan tangan & souvenir': '{} adalah perusahaan yang bergerak dalam bidang {}.',
    'konsultan bisnis': '{} merupakan perusahaan yang bergerak dalam bidang konsultan bisnis',
    'konsultant': '{} adalah seorang tenaga profesional yang menyediakan jasa kepenasihatan (consultancy service) dalam bidang keahlian tertentu, misalnya akuntansi, pajak, lingkungan, biologi, hukum, koperasi dan lain-lain.',
    'laundry': '{} merupakan perusahaan laundry yang memberikan jasa laundry pakaian dan berbagai macam lainnya',
    'lembaga keuangan': '{} merupakan badan usaha atau institusi di bidang jasa keuangan yang bergerak dengan cara menghimpun dana dari masyarakat dan menyalurkannya untuk pendanaan serta dengan mendapatkan keuntungan dalam bentuk bunga atau persentase.',
    'mall': '{} merupakan pusat perbelanjaan segala jenis barang.',
    'marketing agency': '{} merupakan perusahaan yang bergerak dalam bidang marketing agency.',
    'organisasi sosial': '{} merupakan Organisasi sosial yang bergerak dalam hal sosial.',
    'pabrik & toko sepatu': '{} merupakan perusahaan yang bergerak dalam pembuatan {}.',
    'pabrik kelautan': '{} merupakan Perusahaan yang bergerak dalam bidang perkapalan',
    'pabrik kimia': '{} merupakan Industri kimia merujuk pada suatu industri yang terlibat dalam produksi zat kimia.',
    'pabrikan makanan': '{} merupakan industry yang mengolah bahan mentah menjadi makanan.',
    'pemasok system air': '{} merupakan perusahaan {}.',
    'penerbit buku': '{} merupakan perusahaan {}.',
    'pengacara': '{} adalah orang yang berprofesi memberi jasa hukum, baik di dalam maupun di luar pengadilan yang wilayah kerjanya di seluruh wilayah Republik Indonesia.',
    'pengiriman & logistik': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'perbaikan & pembersihan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'percetakan': '{} merupakan perusahaan {}.',
    'pertanian': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'perusahaan asuransi': '{} merupakan perusahaan asuransi, perusahaan yang memberikan jasa dalam penanggulangan risiko atas kerugian, kehilangan manfaat, dan tanggung jawab hukum kepada pihak ketiga, yang timbul dari peristiwa yang tidak pasti.',
    'perusahaan investasi': '{} merupakan Perusahaan Investasi, perantara keuangan yang menghimpun dana dari para investor perorangan dan menanamkan dana tersebut pada beragam sekuritas atau aset lainnya.',
    'perusahaan konstruksi': '{} merupakan Perusahaan Konstruksi yang bergerak dalam bidang konstruksi',
    'perusahaan outsourcing': '{} merupakan Perusahaan outsourcing, perusahaan yang menyediakan jasa dan menyalurkan tenaga kerja dengan keahlian tertentu ke perusahaan yang membutuhkan',
    'perusahaan penerbangan': '{} merupakan perusahaan {}.',
    'peternak hewan peliharaan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'produsen': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'produsen obat': '{} merupakan perusahaan yang memproduksi obat - obatan',
    'produsen & perakitan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'pub & diskotik': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'real estate & perumahan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'restoran keluarga': '{} merupakan Restoran keluarga yang menyediakan berbagai jenis makanan.',
    'riset dan pengembangan produk': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'seni & barang antik': '{} merupakan perusahaan yang bergerak dalam pembuatan {}.',
    'supplier alat pabrik': '{} merupakan perusahaan yang menyediakan alat alat pabrik',
    'toko bangunan': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko buku': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko hewan peliharaan': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko mainan': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko olahraga': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko pakaian': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko pecah belah': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko perlengkapan bayi': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'toko serba ada': '{} merupakan {} yang menyediakan berbagai jenis {}.',
    'universitas / sekolah tinggi': '{} merupakan {}, lembaga untuk para siswa pengajaran siswa/murid di bawah pengawasan guru.',
}
# categories = ['agen asuransi', 'agrikultur', 'audit keuangan', 'bumn', 'export import', 'konsultan bisnis', 'marketing agency', 'pabrik kelautan', 'perusahaan asuransi', 'perusahaan konstruksi', 'produsen obat', 'universitas / sekolah tinggi']

def remove_unicode(text):
    return re.sub(r'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', text) 

def clean_data(data):
    # data['url'] = re.sub('&amp;', '&', data['url'])

    data[COL_ADDRESS] = bytes(data[COL_ADDRESS], 'utf-8').decode('utf-8', 'ignore')
    data[COL_ADDRESS] = re.sub(';', ', ', data[COL_ADDRESS])
    data[COL_ADDRESS] = re.sub('"', '', data[COL_ADDRESS])
    data[COL_ADDRESS] = re.sub('\'', '', data[COL_ADDRESS])
    data[COL_ADDRESS] = re.sub('\n', ' ', data[COL_ADDRESS])
    if len(data[COL_ADDRESS]) < 10:
        data[COL_ADDRESS] = ''

    if '/' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('/')[0].strip()
    if '&' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('&')[0].strip()
    if ',' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split(',')[0].strip()
    if ';' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split(';')[0].strip()
    if '  ' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('  ')[-1].strip()
    if ' – ' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split(' – ')
        if len(data[COL_PHONE]) >= 3:
            data[COL_PHONE] = ''.join(data[COL_PHONE]).strip()
        else:
            data[COL_PHONE] = data[COL_PHONE][0].strip()
    if ' - ' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split(' - ')
        if len(data[COL_PHONE]) >= 3:
            data[COL_PHONE] = ''.join(data[COL_PHONE]).strip()
        elif len(data[COL_PHONE][-1]) >= 7:
            data[COL_PHONE] = data[COL_PHONE][-1].strip()
        else:
            data[COL_PHONE] = ''.join(data[COL_PHONE]).strip()
    data[COL_PHONE] = re.sub('[^0-9a-zA-Z]', '', data[COL_PHONE]).strip().lower()
    if 'fax' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('fax')[0].strip()
    if 'ext' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('ext')[0].strip()
    if 'to' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('to')[0].strip()
    if 'hunting' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('hunting')[0].strip()
    if COL_PHONE in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split(COL_PHONE)[-1].strip()
    if 'telp' in data[COL_PHONE]:
        data[COL_PHONE] = data[COL_PHONE].split('telp')[-1].strip()
    data[COL_PHONE] = re.sub('[^0-9]', '', data[COL_PHONE]).strip()
    # print('ZZZ {}'.format(data[COL_PHONE]))
    if data[COL_PHONE][:2] == '62':
        if data[COL_PHONE][:3] == '620':
            data[COL_PHONE] = data[COL_PHONE][3:]
        else:
            data[COL_PHONE] = data[COL_PHONE][2:]
        data[COL_PHONE] = '0' + data[COL_PHONE]
    elif data[COL_PHONE][0] != '0' and data[COL_CITY].lower() not in ['singapore', 'australia']:
        data[COL_PHONE] = '0' + data[COL_PHONE]

    if ':' in data[COL_EMAIL]:
        data[COL_EMAIL] = data[COL_EMAIL].split(':')[-1].strip()
    if '/' in data[COL_EMAIL]:
        data[COL_EMAIL] = data[COL_EMAIL].split('/')[0].strip()
    if ';' in data[COL_EMAIL]:
        data[COL_EMAIL] = data[COL_EMAIL].split(';')[0].strip()
    if ',' in data[COL_EMAIL]:
        data[COL_EMAIL] = data[COL_EMAIL].split(',')[0].strip()
    if ' ' in data[COL_EMAIL]:
        data[COL_EMAIL] = data[COL_EMAIL].split(' ')[0].strip()
    data[COL_EMAIL] = re.sub('-', '', data[COL_EMAIL]).strip()

    data[COL_WEBSITE] = re.sub('&amp;', '&', data[COL_WEBSITE])
    data[COL_WEBSITE] = re.sub('-', '', data[COL_WEBSITE]).strip()

    data[COL_DESCRIPTION] = bytes(data[COL_DESCRIPTION], 'utf-8').decode('utf-8', 'ignore')
    data[COL_DESCRIPTION] = re.sub(';', ', ', data[COL_DESCRIPTION])
    data[COL_DESCRIPTION] = re.sub('"', '', data[COL_DESCRIPTION])
    data[COL_DESCRIPTION] = re.sub('\'', '', data[COL_DESCRIPTION])
    data[COL_DESCRIPTION] = re.sub('[\r\n]', '. ', data[COL_DESCRIPTION])
    data[COL_DESCRIPTION] = re.sub('[\n]', '. ', data[COL_DESCRIPTION])
    data[COL_DESCRIPTION] = data[COL_DESCRIPTION].strip()
    if len(data[COL_DESCRIPTION]) <= 70:
        data[COL_DESCRIPTION] = ''
    old_default = 'adalah perusahaan yang bergerak di bidang'
    new_default1 = '{} adalah'.format(data[COL_NAME])
    new_default2 = '{} merupakan'.format(data[COL_NAME])
    if len(data[COL_DESCRIPTION]) == 0 or old_default in data[COL_DESCRIPTION] or new_default1 in data[COL_DESCRIPTION] or new_default2 in data[COL_DESCRIPTION]:
        c_low = data[COL_CATEGORY].lower()
        if c_low in f_desc and len(f_desc[c_low]) > 0:
            data[COL_DESCRIPTION] = f_desc[c_low].format(data[COL_NAME], data[COL_CATEGORY], data[COL_CATEGORY].replace('Toko', '').strip())
        else:
            if data[COL_CATEGORY] not in c_valid and data[COL_CATEGORY] not in c_invalid:
                c_invalid.append(data[COL_CATEGORY])
                # print("INFO: {} - {} NOT IN f_desc!!!".format(c_low, data[COL_NAME]))
            data[COL_DESCRIPTION] = '{} {} {}'.format(
                data[COL_NAME],
                old_default,
                data[COL_CATEGORY]
            )

    for k, v in data.items():
        if k is None or v is None:
            continue
        v = remove_unicode(v)
        v = v.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        data[k] = v

    return data

if len(sys.argv) < 2:
    sys.exit("ERROR: empty target file")
target_file = sys.argv[1] or ''
ext = target_file.split('.')[-1].lower()
if ext != 'csv':
    sys.exit("ERROR: unsupported type ({})".format(ext))
print("INFO: reading file {}".format(target_file))
with open(target_file, mode='r', encoding='utf8') as f:
    data = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]
# print(data[0])
# sys.exit('wtf')
print("INFO: done reading {} data".format(len(data)))
empty = {
    'name': 0,
    'address': 0,
    'email': 0,
    'phone': 0,
    'description': 0,
}
duplicate = {
    'slug': 0,
    'email': 0,
    'phone': 0,
    'website': 0,
}
done_slug = []
done_email = []
done_phone = []
done_website = []
clean = []
print("INFO: start cleaning...")
for row in data:
    # print(row[COL_NAME])
    row = clean_data(row)
    category = row[COL_CATEGORY]
    # sc = category.lower()
    # if sc not in categories:
    #     categories.append(sc)
    name = helpers.fix_title(row[COL_NAME])
    slug = helpers.get_slug(name)
    email = row[COL_EMAIL]
    phone = row[COL_PHONE]
    website = row[COL_WEBSITE]
    city = row[COL_CITY]
    if len(city) == 0:
        city = row[COL_ADDRESS].strip().split(' ')[-1].strip()#.lower()
        row[COL_CITY] = city
    if slug in done_slug:
        duplicate['slug'] += 1
        print('INFO: dp slug => {}'.format(slug))
        continue
    if email in done_email:
        duplicate['email'] += 1
        print('INFO: dp email => {}'.format(email))
        continue
    if phone in done_phone:
        duplicate['phone'] += 1
        print('INFO: dp phone => {}'.format(phone))
        continue
    if len(website) > 0 and website in done_website:
        duplicate['website'] += 1
        row['website'] = ''
        print('INFO: dp website => {}'.format(website))
        continue
    done_slug.append(slug)
    done_email.append(email)
    done_phone.append(phone)
    if len(website) > 0:
        done_website.append(website)
    clean.append(row)
print("INFO: done cleaning, got {} / {} data".format(len(clean), len(data)))
target_clean = target_file.split('.')
target_clean.pop(-1)
target_clean = '.'.join(target_clean)
target_clean = '{}_clean.csv'.format(target_clean)
print("INFO: saving clean data to {}".format(target_clean))
with open(target_clean, 'w', encoding='utf8', newline='') as f:
    # for row in clean:
    #     f.write('{}\n'.format(row))
    f.write('')
    output = csv.writer(f)
    output.writerow(clean[0].keys())
    for row in clean:
        output.writerow(row.values())
print("INFO: done saving...")
print("INFO: total {} / {} data".format(len(clean), len(data)))
total_duplicate = 0
for k, v in duplicate.items():
    print("duplicate {}\t\t{}".format(k, v))
    total_duplicate += v
print("total duplicate\t\t{}".format(total_duplicate))
print("INFO: exiting...")

print("INFO: {} invalid c".format(len(c_invalid)))
print(c_invalid)
# categories.sort()
# print('{')
# for c in categories:
#     print("\t'{}': '',".format(c))
# print('}')
# print(categories)
