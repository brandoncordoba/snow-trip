import re, json, statistics as st
out = {}
town = None
for line in open('booking_raw.txt'):
    line = line.strip()
    if line.startswith('## '):
        name, av = line[3:].split(' | available: ')
        town = name; out[town] = {'available': [int(x) for x in av.split(' / ')], 'props': []}
    elif line and not line.startswith('#'):
        for item in line.split('; '):
            n, v = item.rsplit(':', 1)
            a, b, c = [None if x == '-' else int(x) for x in v.split('/')]
            out[town]['props'].append({'name': n.strip(), 'xmas': a, 'peak': b, 'feb': c})
for t, d in out.items():
    P = d['props']
    ac = [p for p in P if p['xmas'] and p['feb']]
    bc = [p for p in P if p['peak'] and p['feb']]
    ab = [p for p in P if p['xmas'] and p['peak']]
    med = lambda xs: round(st.median(xs)) if xs else None
    d['matched_xmas_feb'] = {'n': len(ac), 'xmas': med([p['xmas'] for p in ac]), 'feb': med([p['feb'] for p in ac]),
                             'median_pct_diff': round(st.median([(p['xmas']/p['feb']-1)*100 for p in ac])) if ac else None,
                             'cheaper_in_feb': sum(p['feb'] < p['xmas'] for p in ac)}
    d['matched_peak_feb'] = {'n': len(bc), 'peak': med([p['peak'] for p in bc]), 'feb': med([p['feb'] for p in bc]),
                             'median_pct_diff': round(st.median([(p['peak']/p['feb']-1)*100 for p in bc])) if bc else None}
    d['matched_xmas_peak'] = {'n': len(ab), 'median_pct_diff': round(st.median([(p['peak']/p['xmas']-1)*100 for p in ab])) if ab else None}
    print(t, d['available'], d['matched_xmas_feb'], d['matched_peak_feb'], d['matched_xmas_peak'])
json.dump(out, open('booking.json', 'w'), indent=1)
