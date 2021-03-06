import json
import re
import helpers

file_reputasi = 'reputasi.jl'

file_source = 'cekinfo.jl'
file_output = 'cekinfo.json'

def remove_unicode(text):
    return re.sub(r'[^\x00-\x7F\x80-\xFF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]', u'', text) 

def clean_data(data):
    data['url'] = re.sub('&amp;', '&', data['url'])

    data['address'] = bytes(data['address'], 'utf-8').decode('utf-8', 'ignore')
    data['address'] = re.sub(';', ', ', data['address'])
    data['address'] = re.sub('"', '', data['address'])
    data['address'] = re.sub('\'', '', data['address'])
    data['address'] = re.sub('\n', ' ', data['address'])
    if len(data['address']) < 10:
        data['address'] = ''

    if '/' in data['phone']:
        data['phone'] = data['phone'].split('/')[0].strip()
    if '&' in data['phone']:
        data['phone'] = data['phone'].split('&')[0].strip()
    if ',' in data['phone']:
        data['phone'] = data['phone'].split(',')[0].strip()
    if ';' in data['phone']:
        data['phone'] = data['phone'].split(';')[0].strip()
    if '  ' in data['phone']:
        data['phone'] = data['phone'].split('  ')[-1].strip()
    if ' – ' in data['phone']:
        data['phone'] = data['phone'].split(' – ')
        if len(data['phone']) >= 3:
            data['phone'] = ''.join(data['phone']).strip()
        else:
            data['phone'] = data['phone'][0].strip()
    if ' - ' in data['phone']:
        data['phone'] = data['phone'].split(' - ')
        if len(data['phone']) >= 3:
            data['phone'] = ''.join(data['phone']).strip()
        elif len(data['phone'][-1]) >= 7:
            data['phone'] = data['phone'][-1].strip()
        else:
            data['phone'] = ''.join(data['phone']).strip()
    data['phone'] = re.sub('[^0-9a-zA-Z]', '', data['phone']).strip().lower()
    if 'fax' in data['phone']:
        data['phone'] = data['phone'].split('fax')[0].strip()
    if 'ext' in data['phone']:
        data['phone'] = data['phone'].split('ext')[0].strip()
    if 'to' in data['phone']:
        data['phone'] = data['phone'].split('to')[0].strip()
    if 'hunting' in data['phone']:
        data['phone'] = data['phone'].split('hunting')[0].strip()
    if 'phone' in data['phone']:
        data['phone'] = data['phone'].split('phone')[-1].strip()
    if 'telp' in data['phone']:
        data['phone'] = data['phone'].split('telp')[-1].strip()
    data['phone'] = re.sub('[^0-9]', '', data['phone']).strip()
    if data['phone'][:2] == '62':
        if data['phone'][:3] == '620':
            data['phone'] = data['phone'][3:]
        else:
            data['phone'] = data['phone'][2:]
        data['phone'] = '0' + data['phone']

    if ':' in data['email']:
        data['email'] = data['email'].split(':')[-1].strip()
    if '/' in data['email']:
        data['email'] = data['email'].split('/')[0].strip()
    if ';' in data['email']:
        data['email'] = data['email'].split(';')[0].strip()
    if ',' in data['email']:
        data['email'] = data['email'].split(',')[0].strip()
    if ' ' in data['email']:
        data['email'] = data['email'].split(' ')[0].strip()
    data['email'] = re.sub('-', '', data['email']).strip()

    data['website'] = re.sub('&amp;', '&', data['website'])
    data['website'] = re.sub('-', '', data['website']).strip()

    data['description'] = bytes(data['description'], 'utf-8').decode('utf-8', 'ignore')
    data['description'] = re.sub(';', ', ', data['description'])
    data['description'] = re.sub('"', '', data['description'])
    data['description'] = re.sub('\'', '', data['description'])
    data['description'] = re.sub('\n', '. ', data['description'])
    data['description'] = data['description'].strip()
    if len(data['description']) < 50:
        data['description'] = ''
    # if len(data['description']) == 0:
    #     data['description'] = '{} adalah perusahaan yang bergerak di bidang {}'.format(
    #         data['name'],
    #         data['category']
    #     )

    for k, v in data.items():
        v = remove_unicode(v)
        v = v.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
        data[k] = v

    return data

print('Load done data...')
done = {}
with open(file_reputasi, 'r', encoding='utf8') as f:
    for row in f.read().strip().split('\n'):
        row = json.loads(row)
        # print(helpers.fix_title(row['name']))
        # done[helpers.get_slug(helpers.fix_title(row['name']), '', True)] = row['url']
        done[helpers.get_slug(helpers.fix_title(row['slug']), '', True)] = row['url']
print('{} done data loaded'.format(len(done)))

print('Load perusahaan data...')
perusahaan = []
skipped_counter = {
    'done': 0,
    'empty_name': 0,
    'empty_address': 0,
    'empty_phone': 0,
    'empty_email': 0,
    'invalid_phone': 0,
    'invalid_email': 0,
}
with open(file_source, 'r') as f:
    result = [json.loads(row) for row in f.read().strip().split('\n')]

    for row in result:
        row['name'] = helpers.fix_title(row['name'])
        row['slug'] = helpers.get_slug(row['name'])
        row = clean_data(row)
        print(row['name'])
        print('-- %s' % row['slug'])
        print('-- %s' % row['url'])
        if (row['slug'] in done or
            len(row['name']) == 0 or
            len(row['address']) == 0 or
            len(row['phone']) < 7 or
            len(row['email']) < 8 or
                '@' not in row['email'] or '.' not in row['email']):
            if row['slug'] in done:
                print('-- SKIPPED : DONE')
                skipped_counter['done'] += 1
                continue
            if len(row['name']) == 0:
                print('-- SKIPPED : EMPTY NAME')
                skipped_counter['empty_name'] += 1
            if len(row['address']) == 0:
                print('-- SKIPPED : EMPTY ADDRESS')
                skipped_counter['empty_address'] += 1
            if len(row['phone']) == 0:
                print('-- SKIPPED : EMPTY PHONE')
                skipped_counter['empty_phone'] += 1
            elif len(row['phone']) < 7:
                print('-- SKIPPED : INVALID PHONE (<6)')
                skipped_counter['invalid_phone'] += 1
            if len(row['email']) == 0:
                print('-- SKIPPED : EMPTY EMAIL')
                skipped_counter['empty_email'] += 1
            elif len(row['email']) < 8:
                print('-- SKIPPED : INVALID EMAIL (<8)')
                skipped_counter['invalid_email'] += 1
            elif '@' not in row['email'] or '.' not in row['email']:
                print('-- SKIPPED : INVALID EMAIL (bad format)')
                skipped_counter['invalid_email'] += 1
            # continue
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
