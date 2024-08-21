# Newline Tools

File processing utilities. Useful for working with massive datasets.

## Installation

```
pip install newline-tools
```

## CLI Usage

The `newline` command provides several subcommands:

```
newline <command> [options]
```

### shuffle

Shuffle lines in a file:

```
newline shuffle <input_file> <output_file> [-b BUFFER_SIZE] [--progress] [--include_empty] [-r ROUNDS]
```

Options:
- `-b, --buffer_size`: Buffer size in bytes (default: 1GB)
- `--progress`: Show progress bars during shuffling
- `--include_empty`: Include empty lines during shuffling (default: ignore empty lines)
- `-r, --rounds`: Number of shuffling rounds (default: 1)

### dedupe

Remove duplicate lines:

```
newline dedupe <input_file> <output_file> [--progress] [--error_ratio ERROR_RATIO]
```

Options:
- `--progress`: Show progress bar during deduplication
- `--error_ratio`: Error ratio for the Bloom filter (default: 1e-5)

### split

Split a file into parts:

```
newline split <input_file> <output_prefix> (-n NUM_PARTS | -s SIZE) [--progress]
```

Options:
- `-n, --num_parts`: Number of parts to split into
- `-s, --size`: Size of each part (e.g., '100MB', '1GB')
- `--progress`: Show progress bar during splitting

### sample

Sample lines from a file:

```
newline sample <input_file> <output_file> (-n NUM_LINES | -p PERCENTAGE) [--progress]
```

Options:
- `-n, --num_lines`: Number of lines to sample
- `-p, --percentage`: Percentage of lines to sample
- `--progress`: Show progress bar during sampling

## Python Usage

```python
from newline_tools import Shuffle, Dedupe, Split, Sample

# Shuffle
shuffler = Shuffle('input.txt', buffer_size=2**24, progress=True, ignore_empty=True, rounds=2)
shuffler.shuffle('output.txt')

# Dedupe
deduper = Dedupe('input.txt', progress=True)
deduper.dedupe('output.txt', error_ratio=1e-5)

# Split
splitter = Split('input.txt', progress=True)
splitter.split_by_parts('output_prefix', 5)
# or
splitter.split_by_size('output_prefix', '100MB')

# Sample
sampler = Sample('input.txt', 'output.txt', sample_size=10000)
sampler.sample(method='reservoir')  # or 'index'
```

## License

Dedicated to the public domain (CC0). Use as you wish.