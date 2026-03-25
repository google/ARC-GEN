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


def generate(size=None, rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
  """
  if size is None:
    size = common.randint(2, 6)
    num_pixels = common.randint(1, size)
    pixels = common.sample(common.all_pixels(size, size), num_pixels)
    rows, cols = zip(*pixels)
    color = common.random_color(exclude=[common.cyan()])

  grid, output = common.grid(size, size), common.grid(2 * size, 2 * size)
  for c in cols:
    for r in range(2 * size):
      output[r][c] = output[r][c + size] = common.cyan()
  for r, c in zip(rows, cols):
    grid[r][c] = color
    for dr, dc in [(0, 0), (0, size), (size, 0), (size, size)]:
      output[r + dr][c + dc] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=3, rows=[0, 2], cols=[0, 2], color=2),
      generate(size=6, rows=[0, 4, 4], cols=[1, 0, 5], color=5),
      generate(size=2, rows=[0], cols=[1], color=4),
  ]
  test = [
      generate(size=4, rows=[0, 2, 3], cols=[2, 3, 0], color=3),
  ]
  return {"train": train, "test": test}
