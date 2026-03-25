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


def generate(size=None, rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    color: The color of the pixels.
  """

  if size is None:
    size, color = common.randint(2, 5), common.random_color(exclude=[2])
    pixels = common.randint(1, 2)
    rows = [common.randint(1, size - 1) for _ in range(pixels)]
    cols = [common.randint(0, size - 1) for _ in range(pixels)]

  grid, output = common.grid(size, size), common.grid(3 * size, 3 * size)
  # First, draw the red shadows.
  for row, col in zip(rows, cols):
    i, j = row - 1, col - 1
    if j < 0: j = size - 1
    for r in range(3):
      for c in range(3):
        output[size * r + i][size * c + j] = 2
  # Then, draw the pixels.
  for row, col in zip(rows, cols):
    grid[row][col] = color
    for r in range(3):
      for c in range(3):
        output[size * r + row][size * c + col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, rows=[1, 3], cols=[2, 1], color=5),
      generate(size=3, rows=[1, 2], cols=[2, 0], color=6),
      generate(size=5, rows=[1, 2], cols=[1, 1], color=8),
      generate(size=4, rows=[3], cols=[0], color=1),
      generate(size=2, rows=[1], cols=[1], color=7),
  ]
  test = [
      generate(size=4, rows=[1, 3], cols=[2, 0], color=4),
  ]
  return {"train": train, "test": test}
