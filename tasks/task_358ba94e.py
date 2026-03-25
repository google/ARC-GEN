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


def generate(width=None, height=None, brows=None, bcols=None, colors=None,
             fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the pixels (1 = cut a hole here).
    fgcolor: The color of the foreground.
  """

  if width is None:
    width, height = common.randint(18, 19), common.randint(13, 17)
    num_boxes = common.randint(4, 5)
    while True:
      brows = [common.randint(0, height - 5) for _ in range(num_boxes)]
      bcols = [common.randint(0, width - 5) for _ in range(num_boxes)]
      lengths = [6] * num_boxes
      if not common.overlaps(brows, bcols, lengths, lengths): break
    numbers = common.sample([1, 2, 3, 4], 2)
    rare, mode = numbers[0], numbers[1]
    counts = [rare] + [mode] * (num_boxes - 1)
    colors = []
    for count in counts:
      while True:
        rows = [common.randint(0, 2) for _ in range(count)]
        cols = [common.randint(0, 2) for _ in range(count)]
        if not common.overlaps(rows, cols, [2] * count, [2] * count): break
      entries = [0] * 9
      for row, col in zip(rows, cols):
        entries[row * 3 + col] = 1
      colors.extend(entries)
    fgcolor = common.random_color()

  grid, output = common.grid(width, height), common.grid(5, 5, fgcolor)
  for brow, bcol in zip(brows, bcols):
    common.rect(grid, 5, 5, brow, bcol, fgcolor)
  for i, color in enumerate(colors):
    index, r, c = i // 9, (i % 9) // 3, i % 3
    if color: grid[brows[index] + r + 1][bcols[index] + c + 1] = 0
    if color and index == 0: output[r + 1][c + 1] = 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, height=16, brows=[1, 1, 7, 9, 11], bcols=[12, 1, 7, 1, 14],
               colors=[1, 0, 1, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 1, 0, 1, 0, 0, 0,
                       1, 0, 0, 0, 0, 0, 0, 0, 1,
                       0, 1, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 1], fgcolor=6),
      generate(width=19, height=15, brows=[9, 0, 1, 2, 8], bcols=[3, 14, 1, 8, 12],
               colors=[1, 0, 1, 0, 0, 0, 1, 0, 1,
                       1, 0, 0, 0, 0, 1, 1, 0, 0,
                       1, 0, 1, 0, 0, 0, 1, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 1,
                       0, 0, 1, 1, 0, 0, 0, 0, 1], fgcolor=8),
      generate(width=19, height=16, brows=[10, 0, 2, 4, 8], bcols=[9, 8, 1, 14, 2],
               colors=[0, 0, 0, 1, 0, 0, 0, 0, 0,
                       0, 0, 1, 1, 0, 0, 0, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 1, 0, 0, 0, 0, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 1], fgcolor=2),
      generate(width=18, height=14, brows=[8, 1, 2, 8], bcols=[12, 2, 9, 3],
               colors=[1, 0, 0, 0, 0, 1, 1, 0, 0,
                       0, 0, 1, 1, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 1,
                       0, 0, 1, 1, 0, 0, 0, 0, 0], fgcolor=7),
  ]
  test = [
      generate(width=19, height=17, brows=[7, 0, 1, 7, 9], bcols=[0, 1, 9, 14, 7],
               colors=[1, 0, 1, 0, 0, 0, 1, 0, 1,
                       0, 0, 1, 0, 0, 0, 1, 0, 0,
                       1, 0, 1, 0, 0, 0, 0, 0, 0,
                       1, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 1, 1, 0, 0, 0, 0, 0], fgcolor=1),
  ]
  return {"train": train, "test": test}
