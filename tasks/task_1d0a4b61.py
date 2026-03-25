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


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the pattern.
    height: The height of the pattern.
    wides: The widths of the rectangles.
    talls: The heights of the rectangles.
    brows: The row offsets of the rectangles.
    bcols: The column offsets of the rectangles.
    pattern: The pattern to use.
  """

  if width is None:
    width = common.randint(3, 10)
    height = common.randint(3, 10)
    subset = [1, 5, 2] + [common.choice([3, 4, 6, 7, 8, 9])]
    grid = common.grid(width, height, 1)
    for row in range(1, height - 1):
      for col in range(1, width - 1):
        color = common.choice(subset)
        grid[row][col] = color
        grid[height - 1 - row][col] = color
        grid[row][width - 1 - col] = color
        grid[height - 1 - row][width - 1 - col] = color
    pattern = "".join(str(x) for x in common.flatten(grid))
    wides = [common.randint(2, 6) for _ in range(5)]
    talls = [common.randint(2, 6) for _ in range(5)]
    brows = [common.randint(1, 23 - tall) for tall in talls]
    bcols = [common.randint(1, 23 - wide) for wide in wides]

  grid, output = common.grids(25, 25)
  for row in range(25):
    for col in range(25):
      r, c = row % (height - 1), col % (width - 1)
      color = int(pattern[r * width + c])
      output[row][col] = grid[row][col] = color
  for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
    common.rect(grid, wide, tall, brow, bcol, 0)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=8, wides=[4, 3, 2, 4, 4], talls=[6, 4, 2, 5, 5],
               brows=[1, 12, 14, 16, 19], bcols=[11, 4, 14, 3, 9],
               pattern="1111111112355321152332511352253113522531152332511235532111111111"),
      generate(width=7, height=7, wides=[2, 5, 4, 5, 3], talls=[4, 5, 3, 6, 2],
               brows=[11, 12, 13, 17, 20], bcols=[17, 8, 3, 12, 3],
               pattern="1111111125452115515511414141155155112545211111111"),
      generate(width=3, height=5, wides=[4, 4, 3, 2, 3], talls=[5, 4, 5, 2, 3],
               brows=[1, 3, 4, 14, 20], bcols=[19, 18, 16, 4, 1],
               pattern="111121151121111"),
  ]
  test = [
      generate(width=10, height=10, wides=[4, 2, 5, 2, 4],
               talls=[5, 2, 3, 6, 5], brows=[8, 12, 13, 13, 16],
               bcols=[6, 10, 5, 22, 11],
               pattern="1111111111128155182115218812511111111111185122158118512215811111111111152188125112815518211111111111"),
  ]
  return {"train": train, "test": test}
