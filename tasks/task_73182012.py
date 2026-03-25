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


def generate(brow=None, bcol=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brow: The row of the box.
    bcol: The column of the box.
    colors: The colors of the pixels.
  """

  if brow is None:
    brow, bcol = common.randint(0, 4), common.randint(0, 4)
    subset = common.random_colors(common.randint(3, 6))
    while True:
      rows, cols = common.conway_sprite(4, 4, 10)
      if common.diagonally_connected(list(zip(rows, cols))): break
    colors = [0] * 16
    for row, col in zip(rows, cols):
      colors[row * 4 + col] = colors[col * 4 + row] = common.choice(subset)

  grid, output = common.grid(12, 12), common.grid(4, 4)
  for i, color in enumerate(colors):
    output[i // 4][i % 4] = color
    grid[brow + i // 4][bcol + i % 4] = color
    grid[brow + i // 4][bcol + 7 - i % 4] = color
    grid[brow + 7 - i // 4][bcol + i % 4] = color
    grid[brow + 7 - i // 4][bcol + 7 - i % 4] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brow=2, bcol=2,
               colors=[0, 0, 0, 2, 0, 5, 5, 2, 0, 5, 3, 3, 2, 2, 3, 1]),
      generate(brow=0, bcol=0,
               colors=[0, 0, 0, 2, 0, 0, 2, 2, 0, 2, 3, 1, 2, 2, 1, 0]),
      generate(brow=4, bcol=4,
               colors=[0, 7, 7, 0, 7, 2, 2, 3, 7, 2, 8, 8, 0, 3, 8, 0]),
  ]
  test = [
      generate(brow=0, bcol=2,
               colors=[1, 0, 0, 5, 0, 5, 3, 8, 0, 3, 2, 8, 5, 8, 8, 6]),
  ]
  return {"train": train, "test": test}
