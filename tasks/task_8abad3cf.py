# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generator."""

import common


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    colors: A list of colors to use.
  """

  if width is None:
    counts = common.sample([1, 2, 3, 4], common.randint(2, 3))
    subset = common.sample([0, 1, 2, 3, 4, 5, 6, 8, 9], len(counts))
    sum_of_squares = sum([count * count for count in counts])
    # Choose a big enough grid to hold the sprites.
    while True:
      width, height = common.randint(4, 10), common.randint(4, 10)
      if width * height < 2 * sum_of_squares - 1: continue
      if width * height > 3 * sum_of_squares + 1: continue
      break
    # Draw segments of the sprites.
    grid = common.grid(width, height, 7)
    for color, count in zip(subset, counts):
      while True:
        num_segments = common.randint(1, count * count)
        segments = [common.randint(1, count) for _ in range(num_segments)]
        if sum(segments) == count * count: break
      for segment in segments:
        while True:
          good = True
          if common.randint(0, 1):
            pos = common.randint(0, height - 1)
            val = common.randint(0, width - segment)
            for i in range(segment):  # Check that it's available.
              if grid[pos][val + i] != 7: good = False
            for i in range(segment):  # If it's available, draw it.
              if good: grid[pos][val + i] = color
          else:
            pos = common.randint(0, width - 1)
            val = common.randint(0, height - segment)
            for i in range(segment):  # Check that it's available.
              if grid[val + i][pos] != 7: good = False
            for i in range(segment):  # If it's available, draw it.
              if good: grid[val + i][pos] = color
          if good: break
    colors = common.flatten(grid)

  grid = common.grid(width, height)
  for i, color in enumerate(colors):
    grid[i // width][i % width] = color
  flattened = common.flatten(grid)
  subset = list(set(flattened))
  subset.remove(7)
  counts = [common.int_sqrt(flattened.count(color)) for color in subset]
  zipped = sorted(zip(counts, subset), key=lambda x: x[0])
  counts, subset = [list(x) for x in zip(*zipped)]
  output = common.grid(sum(counts) + len(counts) - 1, max(counts), 7)
  for i, count in enumerate(counts):
    row, col = max(counts) - count, sum(counts[:i]) + i
    common.rect(output, count, count, row, col, subset[i])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=7, colors=[4, 4, 4, 4, 4, 7, 7,
                                          4, 7, 7, 7, 4, 7, 5,
                                          4, 7, 1, 7, 4, 7, 5,
                                          4, 7, 7, 7, 4, 7, 7,
                                          4, 4, 4, 4, 4, 7, 5,
                                          7, 7, 7, 7, 7, 7, 5,
                                          5, 5, 5, 5, 5, 7, 7]),
      generate(width=4, height=7, colors=[9, 9, 9, 9,
                                          7, 7, 9, 7,
                                          9, 9, 9, 9,
                                          7, 7, 7, 7,
                                          7, 6, 7, 6,
                                          7, 6, 7, 6,
                                          7, 7, 7, 7]),
  ]
  test = [
      generate(width=10, height=5, colors=[7, 7, 7, 0, 0, 0, 7, 7, 7, 4,
                                           0, 0, 7, 0, 7, 0, 7, 9, 7, 4,
                                           0, 0, 7, 0, 0, 0, 7, 7, 7, 4,
                                           7, 7, 7, 7, 7, 7, 7, 0, 7, 4,
                                           7, 7, 7, 7, 7, 0, 0, 0, 7, 7]),
  ]
  return {"train": train, "test": test}
