#!/usr/bin/python

from __future__ import unicode_literals
import csv

import click

import prettytable


def interact(seq, desc, count, row, mtx):
    # status output
    keys = sorted(mtx)
    table = prettytable.PrettyTable(keys)
    table.add_row([
        '\033[92m\u2713\u2713\033[0m' if mtx[key] else '--'
        for key in keys
    ])

    print """
Sequence:    {seq}
    {desc}
Interpreted: {i_balls}-{i_strikes}
Final:       {balls}-{strikes}

{mtx}
""".format(seq=seq, desc=', '.join(desc),
           i_balls=count['balls'], i_strikes=count['strikes'],
           balls=row['BALLS_CT'], strikes=row['STRIKES_CT'],
           mtx=table)

    # keep going?
    if raw_input('Continue? [Y/n]: ').lower() == 'n':
        exit()


@click.command()
@click.option('files', '-f', type=click.File('r'), multiple=True,
                required=True, help='Chadwick-parsed event log')
@click.option('imode', '-i', is_flag=True, default=False,
              help='Enable interactive mode')
@click.option('output', '-o', type=click.File('w'), required=True,
              help='Path to output file')
def extract_sequences(files, imode, output):
    """Converts a pitch sequences into a matrix
    of ball-strike counts.
    """

    seq_obv = set()
    mtx = {
        '00': 1, '01': 0, '02': 0,
        '10': 0, '20': 0, '30': 0,
        '11': 0, '12': 0, '21': 0,
        '22': 0, '31': 0, '32': 0,
    }

    # write header row
    writer = csv.writer(output)
    headers = ['pitch_seq_tx']
    headers.extend(['c' + key for key in sorted(mtx)])
    writer.writerow(headers)

    for f in files:
        reader = csv.DictReader(f)

        for row in reader:
            seq = row['PITCH_SEQ_TX']

            if seq in seq_obv:
                continue

            count = {'balls': 0, 'strikes': 0}
            desc = []

            for pitch in seq:
                # handle walks
                if pitch in ('B', 'I', 'V'):
                    if count['balls'] < 3:
                        count['balls'] += 1
                        desc.append('Ball')
                    else:
                        # ball 4, take your base
                        break

                # handle fouls that do not terminate an at-bat
                elif pitch in ('F', 'R'):
                    # keep going forever
                    if count['strikes'] < 2:
                        count['strikes'] += 1
                    desc.append('Foul')

                # handle strikes that can terminate an at-bat
                elif pitch in ('C', 'K', 'L', 'O', 'Q', 'S', 'T'):
                    if count['strikes'] == 2:
                        # batter struck out
                        break
                    else:
                        count['strikes'] += 1
                        desc.append('Strike')
                else:
                    continue

                key = '%s%s' % (count['balls'], count['strikes'])
                if mtx[key] < 1:
                    mtx[key] += 1

            if imode is True:
                interact(seq, desc, count, row, mtx)

            # write output
            values = [seq]
            for key in sorted(mtx):
                values.append(mtx[key])
            writer.writerow(values)

            # mark sequence as observed
            seq_obv.add(seq)

            # reset matrix
            for key in mtx:
                mtx[key] = 0
            mtx['00'] = 1


if __name__ == '__main__':
    extract_sequences()
