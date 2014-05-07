# Retrosheet Pitch Sequence Parser

In order to generate pitch sequence linear weights, one needs to decompose
the sequence of pitches into each count-state (e.g., "0-0" to "0-1").

For example, the outcome of an at bat with pitch sequence `BBFBX`
would be read as:

1. Ball (1-0)
2. Ball (2-0)
3. Foul (2-1)
4. Ball (3-1)
5. Batter puts ball into play

This script parses Chadwick-parsed Retrosheet event data
and emits a CSV-formatted row detailing each count visited
in an event.

## Installation

Install this app via `pip`. This will install a single app, `rs-pitch-seq`.

```bash
$ pip install retrosheet-pitch-sequences
```

## Usage

Basic usage entails supplying one to many Chadwick-parsed Retrosheet event logs.
Users may also run in interactive mode to confirm each sequence's interpretation.

```bash
$ rs-pitch-seq -f /path/to/event-log [-f ...] [-i] -o /path/to/output.csv
```

e.g.,

```bash
$ rs-pitch-seq -f data/2013-events.csv -f data/2012-events.csv -f data/2011-events.csv -o 2010-2013-pitches.csv
```

### Help

```bash
Usage: extract.py [OPTIONS]

  Converts a pitch sequences into a matrix of ball-strike counts.

Options:
  -f FILENAME  Chadwick-parsed event log  [required]
  -i           Enable interactive mode
  -o FILENAME  Path to output file  [required]
```

## Events

This list of batting events is taken from
[Retrosheet's event file description page](http://www.retrosheet.org/eventfile.htm).

```
B  ball
C  called strike
F  foul
H  hit batter
I  intentional ball
K  strike (unknown type)
L  foul bunt
M  missed bunt attempt
N  no pitch (on balks and interference calls)
O  foul tip on bunt
P  pitchout
Q  swinging on pitchout
R  foul ball on pitchout
S  swinging strike
T  foul tip
U  unknown or missed pitch
V  called ball because pitcher went to his mouth
X  ball put into play by batter
Y  ball put into play on pitchout
```
