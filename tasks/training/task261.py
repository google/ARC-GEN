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


def generate(size=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if size is None:
    size = common.randint(3, 7)
    width = common.randint(size // 2, (size + 1) // 2)
    height = common.randint(size // 2, (size + 1) // 2)
    row = common.randint(0, size - height - 1)
    col = common.randint(0, size - width)
    while True:
      pixels = common.random_pixels(width, height, 0.5)
      if not pixels: continue
      rows, cols = zip(*pixels)
      rows, cols = [r + row for r in rows], [c + col for c in cols]
      break

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    grid[r][c] = common.cyan()
    output[r + 1][c] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, rows=[0, 0, 1, 1], cols=[0, 1, 0, 1]),
      generate(size=3, rows=[0], cols=[1]),
      generate(size=5, rows=[1, 1, 1], cols=[1, 2, 3]),
  ]
  test = [
      generate(size=5, rows=[0, 1, 1, 2], cols=[2, 1, 2, 2]),
  ]
  return {"train": train, "test": test}
