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


def generate(size=None, wide=None, tall=None, brow=None, bcol=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    wide: The width of the box.
    tall: The height of the box.
    brow: The row of the box.
    bcol: The column of the box.
    colors: The colors of the background.
  """

  if size is None:
    size = common.randint(12, 24)
    color = common.random_color(exclude=[5, 8])
    wide, tall = common.randint(2, 4), common.randint(2, 4)
    brow = common.randint(3, size - tall - 3)
    bcol = common.randint(3, size - wide - 3)
    colors = [color if common.randint(0, 5) else 0 for _ in range(size * size)]
    if common.randint(0, 3) == 0:  # Sometimes sprinkle with grey pixels
      colors = [c if common.randint(0, 9) else 5 for c in colors]
    # Now, add extra pixels on all sides just to be safe.
    row, col = common.randint(brow, brow + tall - 1), bcol - 2
    colors[row * size + col] = color
    row, col = common.randint(brow, brow + tall - 1), bcol + wide + 1
    colors[row * size + col] = color
    row, col = brow - 2, common.randint(bcol, bcol + wide - 1)
    colors[row * size + col] = color
    row, col = brow + tall + 1, common.randint(bcol, bcol + wide - 1)
    colors[row * size + col] = color

  grid, output = common.grids(size, size)
  for i, color in enumerate(colors):
    output[i // size][i % size] = grid[i // size][i % size] = color
  common.rect(grid, wide + 2, tall + 2, brow - 1, bcol - 1, 0)
  common.rect(output, wide + 2, tall + 2, brow - 1, bcol - 1, 0)
  common.rect(output, wide, tall, brow, bcol, 8)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, wide=2, tall=2, brow=4, bcol=6,
               colors=[0, 0, 2, 2, 2, 0, 2, 2, 0, 0, 0, 0, 2, 2, 2,
                       2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 0, 2, 2,
                       2, 2, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 2, 0,
                       2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2,
                       2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2,
                       0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0,
                       2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 2, 2,
                       0, 0, 2, 2, 0, 0, 0, 2, 2, 2, 0, 2, 0, 2, 2,
                       2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 0, 2, 2,
                       0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2,
                       2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 0, 0, 2, 0,
                       2, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0,
                       2, 0, 2, 2, 2, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2,
                       0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0,
                       0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0]),
      generate(size=19, wide=3, tall=4, brow=5, bcol=5,
               colors=[4, 0, 0, 4, 0, 0, 0, 4, 0, 0, 5, 0, 0, 0, 0, 4, 4, 4, 4,
                       0, 4, 4, 4, 4, 5, 4, 4, 0, 0, 0, 4, 4, 4, 0, 4, 0, 4, 0,
                       0, 0, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 0, 4,
                       0, 4, 0, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 5, 0, 5, 4, 4,
                       4, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 4, 0, 4, 0, 4, 0, 4,
                       4, 4, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 4, 4, 0, 4,
                       4, 4, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 5, 4, 4, 0, 5, 4,
                       4, 4, 4, 0, 0, 0, 0, 0, 0, 4, 5, 4, 4, 4, 0, 4, 0, 0, 5,
                       0, 4, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 4, 4, 5, 4, 0, 0, 4,
                       4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 0, 4, 0, 4, 0, 4, 4, 5,
                       4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 5, 5, 4, 0, 4, 0, 4, 4, 5,
                       4, 4, 4, 4, 4, 5, 0, 4, 0, 4, 0, 4, 4, 0, 4, 0, 5, 4, 4,
                       5, 4, 4, 0, 4, 4, 0, 0, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4,
                       4, 0, 4, 0, 4, 0, 4, 4, 4, 4, 4, 4, 0, 4, 0, 4, 0, 4, 4,
                       5, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 0, 0, 4, 4, 4, 0,
                       0, 0, 4, 4, 0, 4, 4, 4, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4, 4,
                       4, 0, 0, 4, 4, 5, 4, 5, 4, 5, 4, 0, 4, 4, 0, 4, 4, 5, 0,
                       4, 0, 0, 4, 4, 0, 0, 0, 5, 4, 4, 0, 0, 4, 4, 5, 4, 4, 0]),
      generate(size=16, wide=4, tall=2, brow=11, bcol=8,
               colors=[0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0, 3, 3, 3, 0,
                       0, 0, 3, 0, 0, 3, 0, 3, 0, 0, 0, 3, 3, 0, 3, 3,
                       0, 3, 0, 3, 0, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 0,
                       3, 3, 3, 3, 3, 0, 3, 0, 3, 3, 3, 3, 0, 3, 3, 3,
                       3, 3, 0, 3, 0, 0, 3, 0, 0, 3, 3, 3, 0, 0, 3, 3,
                       0, 0, 3, 3, 0, 0, 3, 3, 3, 3, 3, 0, 0, 3, 3, 0,
                       3, 0, 3, 3, 3, 0, 0, 0, 0, 3, 0, 3, 3, 3, 3, 3,
                       0, 0, 0, 0, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0,
                       3, 3, 3, 0, 3, 3, 0, 3, 0, 3, 0, 3, 3, 3, 3, 0,
                       3, 0, 0, 3, 0, 0, 0, 0, 3, 3, 3, 3, 0, 3, 3, 3,
                       0, 0, 0, 3, 0, 3, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                       0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3,
                       3, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3,
                       0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                       3, 3, 3, 3, 3, 3, 0, 0, 0, 3, 3, 3, 3, 0, 3, 0,
                       0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 3, 3, 0, 0, 3, 3]),
  ]
  test = [
      generate(size=21, wide=4, tall=3, brow=13, bcol=11,
               colors=[7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 0, 7, 0, 0, 7, 7, 0, 7, 0, 7, 7,
                       7, 0, 7, 7, 7, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 0, 0, 7, 7, 0, 0,
                       7, 7, 7, 7, 7, 0, 7, 0, 0, 7, 7, 7, 7, 7, 0, 0, 7, 7, 7, 7, 0,
                       7, 0, 0, 7, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 7, 0, 0, 7, 7, 0,
                       7, 7, 7, 7, 0, 7, 7, 0, 7, 0, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7,
                       7, 7, 0, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7,
                       0, 7, 7, 7, 0, 0, 7, 7, 7, 7, 0, 0, 7, 0, 0, 7, 7, 7, 7, 7, 7,
                       7, 0, 0, 7, 0, 0, 7, 7, 7, 7, 0, 7, 0, 7, 7, 7, 7, 0, 7, 7, 7,
                       7, 7, 7, 0, 7, 0, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7,
                       7, 7, 7, 0, 7, 7, 7, 7, 0, 7, 0, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7,
                       0, 7, 7, 0, 7, 0, 7, 0, 0, 7, 7, 7, 7, 7, 0, 7, 0, 0, 0, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 7, 0, 7, 7, 7, 7, 7, 7, 0, 0, 0,
                       7, 7, 0, 0, 0, 7, 7, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 7,
                       0, 7, 7, 0, 0, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 7,
                       7, 7, 7, 0, 7, 7, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0,
                       7, 0, 7, 7, 0, 7, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0,
                       7, 7, 7, 7, 7, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 0, 7, 7,
                       0, 0, 7, 7, 0, 7, 0, 0, 7, 7, 0, 0, 0, 7, 7, 0, 0, 7, 0, 0, 7,
                       7, 0, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 0, 7, 0, 0, 0, 0, 0, 0,
                       0, 7, 7, 0, 0, 7, 7, 0, 7, 0, 0, 0, 0, 7, 0, 7, 7, 7, 7, 7, 7,
                       0, 7, 7, 0, 7, 7, 7, 0, 0, 7, 7, 0, 0, 7, 7, 0, 7, 7, 0, 7, 7]),
  ]
  return {"train": train, "test": test}
