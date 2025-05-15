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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if size is None:
    colors = common.sample([2, 3, 8], common.randint(1, 3))
    while True:
      size = common.randint(6, 16)
      rows = [common.randint(1, size - 2) for _ in colors]
      cols = [common.randint(1, size - 2) for _ in colors]
      lengths = [3] * len(colors)
      if not common.overlaps(rows, cols, lengths, lengths): break

  grid, output = common.grids(size, size)
  colormap = {3: 6, 8: 4, 2: 1}
  for r, c, color in zip(rows, cols, colors):
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        output[r + dr][c + dc] = colormap[color]
    output[r][c] = grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, rows=[4, 5, 6], cols=[5, 1, 8], colors=[8, 3, 2]),
      generate(size=6, rows=[1], cols=[3], colors=[3]),
      generate(size=16, rows=[3, 10], cols=[12, 3], colors=[3, 2]),
      generate(size=6, rows=[2], cols=[2], colors=[8]),
  ]
  test = [
      generate(size=16, rows=[1, 10, 14], cols=[1, 13, 2], colors=[3, 2, 8]),
  ]
  return {"train": train, "test": test}
