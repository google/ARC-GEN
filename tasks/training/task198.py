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


def generate(size=None, minisize=None, color=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the number of large cells
    minisize: the number of pixels within a large cell
    color: a digit representing a color to be used
    rows: a list of vertical coordinates where black pixels should be placed
    cols: a list of horizontal coordinates where black pixels should be placed
  """
  if size is None:
    minisize = common.randint(3, 5)
    size = common.randint(8, 10) - minisize
    pixels = []
    for r in range(size * (minisize + 1) - 1):
      for c in range(size * (minisize + 1) - 1):
        if r % (minisize + 1) == minisize or c % (minisize + 1) == minisize:
          pixels.append((r, c))
    num_pixels = common.randint(size + minisize, size * minisize)
    pixels = common.sample(pixels, num_pixels)
    rows, cols = zip(*pixels)
    color = common.random_color(exclude=[common.yellow(), common.green()])

  # First, figure out which cells need to be flipped to yellow.
  grid = common.grid(size, size, common.black())
  output = common.grid(size, size, common.green())
  for r, c in zip(rows, cols):
    if r % (minisize + 1) != minisize:
      output[r // (minisize + 1)][c // (minisize + 1)] = common.yellow()
      output[r // (minisize + 1)][c // (minisize + 1) + 1] = common.yellow()
    if c % (minisize + 1) != minisize:
      output[r // (minisize + 1)][c // (minisize + 1)] = common.yellow()
      output[r // (minisize + 1) + 1][c // (minisize + 1)] = common.yellow()
  # Second, draw the black/yellow/green linegrids.
  grid = common.create_linegrid(grid, minisize, color)
  output = common.create_linegrid(output, minisize, color)
  # Third, sprinkle the permeable points into the linegrids.
  for r, c in zip(rows, cols):
    grid[r][c] = common.black()
    output[r][c] = common.yellow()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=5, minisize=4, color=8,
               rows=[4, 7, 8, 9, 9, 10, 12, 13, 14, 14, 17],
               cols=[17, 4, 19, 8, 13, 14, 4, 9, 20, 23, 9]),
      generate(size=5, minisize=5, color=1,
               rows=[6, 7, 8, 10, 11, 11, 13, 13, 14, 17, 17, 17, 23],
               cols=[11, 5, 5, 17, 8, 24, 5, 11, 17, 14, 20, 25, 0]),
      generate(size=4, minisize=4, color=9,
               rows=[2, 2, 3, 4, 6, 9, 14, 15, 17],
               cols=[4, 9, 4, 7, 4, 10, 18, 14, 4]),
  ]
  test = [
      generate(size=7, minisize=3, color=5,
               rows=[2, 3, 3, 3, 4, 5, 5, 7, 9, 11, 11, 11, 11, 12, 12, 12, 13,
                     15, 15, 18, 19, 20, 20, 21, 21, 22, 22, 23, 23, 24, 25, 26,
                     26],
               cols=[7, 6, 7, 26, 3, 11, 15, 13, 7, 5, 6, 10, 12, 3, 11, 19, 3,
                     2, 21, 11, 22, 15, 19, 15, 23, 11, 23, 5, 18, 11, 3, 7,
                     15]),
  ]
  return {"train": train, "test": test}
