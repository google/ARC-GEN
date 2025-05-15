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


def generate(rows=None, cols=None, idx=None, color=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idx: the index into the pixel that should be the input grid location
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols = common.conway_sprite()
    idx = common.randint(0, len(rows) - 1)
    color = common.random_color()

  grid, output = common.grids(size * size, size * size)
  for row, col in zip(rows, cols):
    grid[rows[idx] * size + row][cols[idx] * size + col] = color
    for r, c in zip(rows, cols):
      output[row * size + r][col * size + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 2], cols=[0, 1, 2, 0], idx=0, color=8),
      generate(rows=[0, 1, 1, 2], cols=[2, 1, 2, 0], idx=1, color=7),
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 0, 2, 0, 1], idx=0, color=6),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2], cols=[0, 0, 1, 1, 2], idx=1, color=2),
  ]
  return {"train": train, "test": test}
