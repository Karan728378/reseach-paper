import csv, statistics

with open('results/pilot-summary-clean.csv') as f:
    rows = list(csv.DictReader(f))

for v in ['v0-baseline','v1-jsonld','v2-aria','v3-data-attrs','v4-evidence-meta']:
    times = [float(r['total_time_seconds']) for r in rows if r['variant']==v]
    steps = [int(r['total_steps']) for r in rows if r['variant']==v]
    mn = statistics.mean(times)
    sd = statistics.stdev(times)
    mx = max(times)
    med_s = statistics.median(steps)
    mn_s = statistics.mean(steps)
    print(v, 'n=%d' % len(times), 'mean_time=%.1f' % mn, 'sd=%.1f' % sd, 'max=%.1f' % mx, 'med_steps=%.1f' % med_s, 'mean_steps=%.2f' % mn_s)

print()
print('Runs with time > 200s:')
for r in rows:
    t = float(r['total_time_seconds'])
    if t > 200:
        print(' ', r['run_id'], r['variant'], r['task_id'], r['repetition_index'], 'time=%.1f' % t, 'steps='+r['total_steps'])

print()
print('Failures:')
for r in rows:
    if r['success'] == 'False':
        print(' ', r['run_id'], r['variant'], r['task_id'], r['repetition_index'], 'score='+r['partial_score'], 'time='+r['total_time_seconds'][:8])
