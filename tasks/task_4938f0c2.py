# Copyright 2025 Google LLC
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


def generate(width=None, height=None, rows=None, cols=None, brow=None,
             bcol=None, showall=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    brow: the row of the green box
    bcol: the column of the green box
    showall: whether to show all the copies
  """
  if width is None:
    width, height = common.randint(10, 30), common.randint(10, 30)
    length = common.randint(3, 4)
    while True:
      pixels = common.random_pixels(length, length)
      if (0, 0) not in pixels: pixels.append((0, 0))
      if len(pixels) > 4: break
    rows, cols = zip(*pixels)
    brow = common.randint(length, height - length - 2)
    bcol = common.randint(length, width - length - 2)
    showall = 0 if common.randint(0, 3) else 1

  grid, output = common.grids(width, height)
  for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    output[brow + dr][bcol + dc] = grid[brow + dr][bcol + dc] = common.green()
  for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
    rowoff = brow - 1 if dr < 0 else brow + 2
    coloff = bcol - 1 if dc < 0 else bcol + 2
    for r, c in zip(rows, cols):
      output[rowoff + dr * r][coloff + dc * c] = common.red()
      if not showall and (dr > 0 or dc > 0): continue
      grid[rowoff + dr * r][coloff + dc * c] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=30, height=20, rows=[0, 0, 0, 0, 1, 1, 2, 2, 3, 3],
               cols=[0, 1, 2, 3, 0, 3, 0, 3, 0, 3], brow=7, bcol=9, showall=0),
      generate(width=10, height=10, rows=[0, 0, 1, 1, 2, 2],
               cols=[0, 1, 0, 2, 1, 2], brow=3, bcol=4, showall=0),
      generate(width=14, height=12, rows=[0, 0, 0, 1, 2, 2],
               cols=[0, 1, 2, 2, 0, 2], brow=4, bcol=5, showall=1),
  ]
  test = [
      generate(width=14, height=18, rows=[0, 0, 1, 2, 3, 3, 3, 3],
               cols=[0, 1, 1, 2, 0, 1, 2, 3], brow=6, bcol=6, showall=0),
  ]
  return {"train": train, "test": test}
