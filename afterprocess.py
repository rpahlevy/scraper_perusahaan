import sys
import csv
import re

COL_CATEGORY = 'Kategori'
COL_NAME = 'Nama Perusahaan'
COL_ADDRESS = 'Alamat'
COL_CITY = 'Kota'
COL_PHONE = 'No. HP'
COL_EMAIL = 'Email'
COL_WEBSITE = 'Website'
COL_DESCRIPTION = 'Deskripsi'

f_desc = {
    'advertising': 'Perusahan {} adalah perusahaan yang bergerak di bidang Advertising.',
    'agen asuransi': 'Perusahaan {} merupakan agen asuransi, orang yang bertindak untuk menawarkan dan memasarkan produk asuransi untuk dan atas nama penanggung.',
    'agen travel dan perjalanan': 'Perusahan {} merupakan Agen Travel dan Perjalanan yang melayani berbagai Tour dan Travel perjalanan.',
    'alat kantor & distributor': 'Perusahan {} merupakan distributor alat kantor yang menyediakan berbagai macam alat kantor.',
    'audit keuangan': 'Perusahaan {} adalah lembaga audit keuangan,  Audit laporan keuangan merupakan penilaian atas suatu perusahaan atau badan hukum lainnya (termasuk pemerintah) sehingga dapat dihasilkan pendapat yang independen tentang laporan keuangan yang relevan, akurat, lengkap, dan disajikan secara wajar.',
    'bakery': 'Perusahaan {} merupakan Bakery atau Toko Roti yang menyediakan berbagai jenis roti dengan berbagai varian.',
    'bank & perkreditan': 'Perusahaan {} merupakan perusahaan dalam bidang Bank dan Perkreditan.',
    'bimbingan belajar': 'Perusahan {} merupakan bimbingan belajar bagi para pelajar dengan berbagai mata pelajaran.',
    'bisnis center': 'Perusahaan {} merupakan bisnis center',
    'buah & sayuran': 'Perusahan {} merupakan penyedia Buah dan Sayuran sehat.',
    'bumn': 'Perusahaan {} merupakan perusahaan BUMN, perusahaan  yang dimiliki baik sepenuhnya, sebagian besar, maupun sebagian kecil oleh pemerintah dan pemerintah memberi kontrol terhadapnya.',
    'catering': 'Perusahan {} merupakan perusahaan catering yang menyediakan segala jenis makanan untuk berbagai acara.',
    'dealer mesin': '{} Merupakan perusahaan dealer mesin yang menyediakan mesin - mesin.',
    'dealer mobil': 'Perusahan {} merupakan Dealer Mobil dan Motor yang menyediakan berbagai type Mobil dan Motor.',
    'distributor': 'Perusahan {} merupakan Distributor berbagai barang dengan kualitas terjamin.',
    'distributor elektronika': 'Perusahaan {} merupakan distributor elektronika yang menyediakan berbagai produk elektronik.',
    'distributor logam': 'Perusahaan {} merupakan Distributor Logam yang menyediakan Logam Logam dengan kualitas tinggi.',
    'dokter umum': '{} merupakan dokter umum yang melayani berbagai keluhan penyakit.',
    'export import': 'Perusahaan {} adalah perusahaan yang bergerak dalam bidang {}.',
    'furniture': 'Perusahaan {} adalah perusahaan yang bergerak dalam bidang {}.',
    'gereja kristen': '{} merupakan gereja kristen yang juga bergerak dalam bidang organisasi sosial',
    'hidrolik & supplier': 'Perusahaan {} merupakan Supplier yang menyediakan hidrolik.',
    'jasa konstruksi': 'Perusahaan {} adalah perusahaan yang bergerak dalam bidang {}.',
    'jasa pelayanan': 'Perusahaan {} adalah perusahaan yang bergerak dalam bidang {}.',
    'jasa wedding': 'Perusahaan {} adalah perusahaan yang bergerak dalam bidang {}.',
    'kaca mata': '{} merupakan Toko {} yang menyediakan berbagai jenis {}.',
    'kantor akuntan': '{} merupakan badan usaha yang telah mendapatkan izin dari Menteri Keuangan sebagai wadah bagi akuntan publik dalam memberikan jasanya.',
    'kantor dagang': '{} merupakan Perusahaan dagang , perusahaan yang bisnis utamanya membeli barang dari pemasok dan menjual lagi ke konsumen tanpa mengubah wujud barang tersebut.',
    'kaos & konveksi': '{} merupakan perusahaan yang bergerak dalam pembuatan {}.',
    'kerajinan tangan & souvenir': 'Perusahaan {} adalah perusahaan yang bergerak dalam bidang {}.',
    'konsultan bisnis': 'Perusahaan {} merupakan perusahaan yang bergerak dalam bidang konsultan bisnis',
    'konsultant': '{} adalah seorang tenaga profesional yang menyediakan jasa kepenasihatan (consultancy service) dalam bidang keahlian tertentu, misalnya akuntansi, pajak, lingkungan, biologi, hukum, koperasi dan lain-lain.',
    'laundry': 'Perusahaan {} merupakan perusahaan laundry yang memberikan jasa laundry pakaian dan berbagai macam lainnya',
    'lembaga keuangan': '{} merupakan badan usaha atau institusi di bidang jasa keuangan yang bergerak dengan cara menghimpun dana dari masyarakat dan menyalurkannya untuk pendanaan serta dengan mendapatkan keuntungan dalam bentuk bunga atau persentase.',
    'mall': '{} merupakan pusat perbelanjaan segala jenis barang.',
    'marketing agency': 'Perusahan {} merupakan perusahaan yang bergerak dalam bidang marketing agency.',
    'organisasi sosial': '{} merupakan Organisasi sosial yang bergerak dalam hal sosial.',
    'pabrik & toko sepatu': '{} merupakan perusahaan yang bergerak dalam pembuatan {}.',
    'pabrik kelautan': 'Perusahaan {} merupakan Perusahaan yang bergerak dalam bidang perkapalan',
    'pabrik kimia': '{} merupakan Industri kimia merujuk pada suatu industri yang terlibat dalam produksi zat kimia.',
    'pabrikan makanan': '{} merupakan industry yang mengolah bahan mentah menjadi makanan.',
    'penerbitan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'pengacara': '{} adalah orang yang berprofesi memberi jasa hukum, baik di dalam maupun di luar pengadilan yang wilayah kerjanya di seluruh wilayah Republik Indonesia.',
    'perbaikan & pembersihan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'perbaikan & servis': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'percetakan & penerbitan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'percetakan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'pertanian': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'perusahaan asuransi': '{} merupakan perusahaan asuransi, perusahaan yang memberikan jasa dalam penanggulangan risiko atas kerugian, kehilangan manfaat, dan tanggung jawab hukum kepada pihak ketiga, yang timbul dari peristiwa yang tidak pasti.',
    'perusahaan investasi': '{} merupakan Perusahaan Investasi, perantara keuangan yang menghimpun dana dari para investor perorangan dan menanamkan dana tersebut pada beragam sekuritas atau aset lainnya.',
    'perusahaan konstruksi': 'Perusahaan {} merupakan Perusahaan Konstruksi yang bergerak dalam bidang konstruksi',
    'perusahaan outsourcing': '{} merupakan Perusahaan outsourcing, perusahaan yang menyediakan jasa dan menyalurkan tenaga kerja dengan keahlian tertentu ke perusahaan yang membutuhkan',
    'peternakan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'produsen': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'produsen obat': 'Perusahaan {} merupakan perusahaan yang memproduksi obat - obatan',
    'produsen & perakitan': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'pub & diskotik': '{} merupakan perusahaan yang bergerak dalam bidang {}.',
    'restoran keluarga': '{} merupakan Restoran keluarga yang menyediakan berbagai jenis makanan.',
    'sekolah': '{} merupakan {}, lembaga untuk para siswa pengajaran siswa/murid di bawah pengawasan guru.',
    'seni & barang antik': '{} merupakan perusahaan yang bergerak dalam pembuatan {}.',
    'supplier alat pabrik': 'Perusahaan {} merupakan perusahaan yang menyediakan alat alat pabrik',
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

def fix_title(title):
    # remove non utf
    title = bytes(title, 'utf-8').decode('utf-8', 'ignore')
    # remove non alpha and some characters
    title = re.sub('[^a-zA-Z0-9 \-,\.]', '', title)
    title = title.strip()
    title = title.strip(' ,.')
    slug = title.lower()
    # helper
    last2 = slug[-2:]
    # remove pt
    if last2 == 'pt':
        title = 'PT ' + title[:-2]
    # remove cv
    if last2 == 'cv':
        title = 'CV ' + title[:-2]
    # strip
    title = title.strip(' ,.')
    return title

def get_slug(title, replace_space=''):
    slug = title.lower().strip()
    slug = slug.strip(' ,.')
    # split by '-'
    if '-' in slug:
        slug = slug.split('-')
        if len(slug[-1].split(' ')) > 3:
            slug[-1] = slug[-1].strip()
            slug = ''.join(slug)
        else:
            slug = ''.join(slug[:-1])
        slug = slug.strip(' ,.')
    # split by '|'
    if '|' in slug:
        slug = slug.split('|')[0]
        slug = slug.strip(' ,.')
    # split by ':'
    if ':' in slug:
        slug = slug.split(':')[0]
        slug = slug.strip(' ,.')
    # remove ()
    slug = re.sub('[\(\)]', '', slug)
    slug = slug.strip(' ,.')
    # skip helper if len <= 4
    if len(slug) <= 4:
        if len(replace_space) > 0:
            slug = re.sub(' ', replace_space, slug).strip()
        return slug
    # helper
    first2 = slug[:2]
    first3 = slug[:3]
    last2 = slug[-2:]
    last3 = slug[-3:]
    last4 = slug[-4:]
    # cek pt & pt.
    if first2 == 'pt':
        slug = slug[2:]
    if last2 == 'pt':
        slug = slug[:-2]
    slug = slug.strip(' ,.')
    # cek cv & cv.
    if first2 == 'cv':
        slug = slug[2:]
    if last2 == 'cv':
        slug = slug[:-2]
    slug = slug.strip(' ,.')
    # cek tbk & tbk.
    if last3 == 'tbk':
        slug = slug[:-3]
    slug = slug.strip(' ,.')
    # cek ltd & ltd.
    if last3 == 'ltd':
        slug = slug[:-3]
    slug = slug.strip(' ,.')
    # cek co & co.
    if last2 == 'co':
        slug = slug[:-2]
    slug = slug.strip(' ,.')
    # replace_space
    if len(replace_space) > 0:
        slug = re.sub(' ', replace_space, slug).strip()
    return slug

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

    c_low = data[COL_CATEGORY].lower()
    if c_low in f_desc and len(f_desc[c_low]) > 0:
        data[COL_DESCRIPTION] = f_desc[c_low].format(data[COL_NAME], data[COL_CATEGORY], data[COL_CATEGORY].replace('Toko', '').strip())
    else:
        data[COL_DESCRIPTION] = bytes(data[COL_DESCRIPTION], 'utf-8').decode('utf-8', 'ignore')
        data[COL_DESCRIPTION] = re.sub(';', ', ', data[COL_DESCRIPTION])
        data[COL_DESCRIPTION] = re.sub('"', '', data[COL_DESCRIPTION])
        data[COL_DESCRIPTION] = re.sub('\'', '', data[COL_DESCRIPTION])
        data[COL_DESCRIPTION] = re.sub('[\r\n]', '. ', data[COL_DESCRIPTION])
        data[COL_DESCRIPTION] = re.sub('[\n]', '. ', data[COL_DESCRIPTION])
        data[COL_DESCRIPTION] = data[COL_DESCRIPTION].strip()
        if len(data[COL_DESCRIPTION]) < 50:
            data[COL_DESCRIPTION] = ''
        if len(data[COL_DESCRIPTION]) == 0:
            data[COL_DESCRIPTION] = '{} adalah perusahaan yang bergerak di bidang {}'.format(
                data[COL_NAME],
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
    name = row[COL_NAME] #fix_title(row[COL_NAME])
    slug = get_slug(name)
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

# categories.sort()
# print('{')
# for c in categories:
#     print("\t'{}': '',".format(c))
# print('}')
# print(categories)
