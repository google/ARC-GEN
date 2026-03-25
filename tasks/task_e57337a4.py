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


def generate(rows=None, cols=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the black pixels.
    cols: The columns of the black pixels.
    color: The color of the grid.
  """

  if rows is None:
    rows, cols = [], []
    while True:
      for r in range(3):
        for c in range(3):
          if common.randint(0, 3): continue
          rows.append(5 * r + common.randint(0, 4))
          cols.append(5 * c + common.randint(0, 4))
      if len(rows) in [1, 2, 3]: break
    color = common.random_color()

  grid, output = common.grid(15, 15, color), common.grid(3, 3, color)
  for row, col in zip(rows, cols):
    output[row // 5][col // 5] = grid[row][col] = 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[2, 7], cols=[1, 7], color=8),
      generate(rows=[2], cols=[12], color=9),
      generate(rows=[2, 2, 9], cols=[3, 11, 2], color=7),
  ]
  test = [
      generate(rows=[1, 12], cols=[5, 13], color=6),
  ]
  return {"train": train, "test": test}
