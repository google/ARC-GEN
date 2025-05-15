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


def generate(lengths=None, cols=None, mode=None, gravity=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: the lengths of the two rectangles
    cols: the columns where the rectangles are placed
    mode: one of three options (0=space at bottom, 1=space at top, 2=no space)
    gravity: determines where the "bottom" of the grid is placed
    size: the width and height of the (square) grid
  """
  if lengths is None:
    lengths = [common.randint(4, 8) for _ in range(2)]
    cols = [common.randint(0, size - length) for length in lengths]
    mode = common.randint(0, 2)
    gravity = common.randint(0, 3)

  grid, output = common.grids(size, size)
  heights = [3, 6 if mode == 2 else 5]
  row = 1 if mode == 0 else 0
  for length, col, height in zip(lengths, cols, heights):
    for r in range(row, row + height):
      for c in range(col, col + length):
        output[r][c] = grid[r][c] = common.gray()
    for r in range(row + 1, row + height - 1):
      for c in range(col + 1, col + length - 1):
        output[r][c] = common.red()
    row += height + 1
  grid = common.apply_gravity(grid, gravity)
  output = common.apply_gravity(output, gravity)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[4, 5], cols=[3, 2], mode=0, gravity=3),
      generate(lengths=[5, 6], cols=[4, 1], mode=1, gravity=2),
  ]
  test = [
      generate(lengths=[6, 7], cols=[0, 3], mode=2, gravity=0),
  ]
  return {"train": train, "test": test}
