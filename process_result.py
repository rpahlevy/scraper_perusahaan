import json
import re

file_reputasi = 'reputasi.jl'

file_source = 'daftarperusahaan.jl'
file_output = 'daftarperusahaan.json'

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
    data['url'] = re.sub('&amp;', '&', data['url'])

    data['address'] = bytes(data['address'], 'utf-8').decode('utf-8', 'ignore')
    data['address'] = re.sub(';', ', ', data['address'])
    data['address'] = re.sub('"', '', data['address'])
    data['address'] = re.sub('\'', '', data['address'])
    data['address'] = re.sub('\n', ' ', data['address'])

    if '/' in data['phone']:
        data['phone'] = data['phone'].split('/')[0].strip()
    if '&' in data['phone']:
        data['phone'] = data['phone'].split('&')[0].strip()
    if ',' in data['phone']:
        data['phone'] = data['phone'].split(',')[0].strip()
    if ';' in data['phone']:
        data['phone'] = data['phone'].split(';')[0].strip()
    if ' – ' in data['phone']:
        data['phone'] = data['phone'].split(' – ')
        if len(data['phone']) >= 3:
            data['phone'] = ''.join(data['phone']).strip()
        else:
            data['phone'] = data['phone'][0].strip()
    data['phone'] = re.sub('[^0-9a-zA-Z]', '', data['phone']).strip()
    if data['phone'][:2] == '62':
        if data['phone'][:3] == '620':
            data['phone'] = data['phone'][3:]
        else:
            data['phone'] = data['phone'][2:]
        data['phone'] = '0' + data['phone']

    if '/' in data['email']:
        data['email'] = data['email'].split(':')[0].strip()
    if ';' in data['email']:
        data['email'] = data['email'].split(';')[0].strip()
    data['email'] = re.sub('-', '', data['email']).strip()

    data['website'] = re.sub('&amp;', '&', data['website'])
    data['website'] = re.sub('-', '', data['website']).strip()

    if len(data['description']) == 0 or True:
        data['description'] = '{} adalah perusahaan yang bergerak di bidang {}'.format(
            data['name'],
            data['category']
        )
    data['description'] = bytes(data['description'], 'utf-8').decode('utf-8', 'ignore')
    data['description'] = re.sub(';', ', ', data['description'])
    data['description'] = re.sub('"', '', data['description'])
    data['description'] = re.sub('\'', '', data['description'])
    data['description'] = re.sub('\n', ' ', data['description'])
    data['description'] = data['description'].strip()

    return data

print('Load done data...')
done = {}
with open(file_reputasi, 'r', encoding='utf8') as f:
    for row in f.read().strip().split('\n'):
        row = json.loads(row)
        # done[get_slug(fix_title(row['name']))] = row['url']
        done[get_slug(fix_title(row['slug']))] = row['url']
print('{} done data loaded'.format(len(done)))

print('Load perusahaan data...')
perusahaan = []
skipped_counter = {
    'done': 0,
    'empty_name': 0,
    'empty_address': 0,
    'empty_phone': 0,
    'empty_email': 0,
}
with open(file_source, 'r') as f:
    result = [json.loads(row) for row in f.read().strip().split('\n')]

    for row in result:
        row['name'] = fix_title(row['name'])
        row['slug'] = get_slug(row['name'])
        row = clean_data(row)
        print(row['name'])
        print('-- %s' % row['slug'])
        print('-- %s' % row['url'])
        if (row['slug'] in done or
            len(row['name']) == 0 or
            len(row['address']) == 0 or
            len(row['phone']) == 0 or
            len(row['email']) == 0):
            if row['slug'] in done:
                print('-- SKIPPED : DONE')
                skipped_counter['done'] += 1
            if len(row['name']) == 0:
                print('-- SKIPPED : EMPTY NAME')
                skipped_counter['empty_name'] += 1
            if len(row['address']) == 0:
                print('-- SKIPPED : EMPTY ADDRESS')
                skipped_counter['empty_address'] += 1
            if len(row['phone']) == 0:
                print('-- SKIPPED : EMPTY PHONE')
                skipped_counter['empty_phone'] += 1
            if len(row['email']) == 0:
                print('-- SKIPPED : EMPTY EMAIL')
                skipped_counter['empty_email'] += 1
            continue
        perusahaan.append(row)
        done[row['slug']] = ''
print('VALID : {}'.format(len(perusahaan)))
total_skipped = 0
for k, v in skipped_counter.items():
    print('{} : {}'.format(k, v))
    total_skipped += v
print('SKIPED : {}'.format(total_skipped))

print('Saving RESULT to {}'.format(file_output))
with open(file_output, 'w') as f:
    json.dump(perusahaan, f)

print('Saving DONE to {}'.format(file_reputasi))
with open(file_reputasi, 'w') as f:
    for k, v in done.items():
        f.write('{"slug": "%s", "url": "%s"}\n' % (k, v))
print('DONE')
