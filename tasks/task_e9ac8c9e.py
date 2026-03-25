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


def generate(size=None, widths=None, rows=None, cols=None, tops=None,
             uppers=None, lowers=None, bottoms=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    widths: The widths of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    tops: The top colors of the boxes.
    uppers: The upper colors of the boxes.
    lowers: The lower colors of the boxes.
    bottoms: The bottom colors of the boxes.
  """

  if size is None:
    if common.randint(0, 1):
      size, widths = 10, [2 * common.randint(1, 3)]
    else:
      size, widths = 15, [6, 2, 4]
    while True:
      rows = [common.randint(1, size - w - 1) for w in widths]
      cols = [common.randint(1, size - w - 1) for w in widths]
      if not common.overlaps(rows, cols, widths, widths, 3): break
    colors = [common.random_colors(4, exclude=[5]) for _ in widths]
    tops = [colors[i][0] for i in range(len(widths))]
    uppers = [colors[i][1] for i in range(len(widths))]
    lowers = [colors[i][2] for i in range(len(widths))]
    bottoms = [colors[i][3] for i in range(len(widths))]

  grid, output = common.grids(size, size)
  for width, row, col, top, upper, lower, bottom in zip(widths, rows, cols,
                                                        tops, uppers, lowers,
                                                        bottoms):
    common.rect(grid, width, width, row, col, 5)
    grid[row - 1][col - 1] = top
    grid[row - 1][col + width] = upper
    grid[row + width][col - 1] = lower
    grid[row + width][col + width] = bottom
    common.rect(output, width // 2, width // 2, row, col, top)
    common.rect(output, width // 2, width // 2, row, col + width // 2, upper)
    common.rect(output, width // 2, width // 2, row + width // 2, col, lower)
    common.rect(output, width // 2, width // 2, row + width // 2, col + width // 2, bottom)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, widths=[4], rows=[3], cols=[3], tops=[3], uppers=[4],
               lowers=[8], bottoms=[6]),
      generate(size=10, widths=[2], rows=[3], cols=[2], tops=[4], uppers=[2],
               lowers=[7], bottoms=[1]),
      generate(size=10, widths=[6], rows=[1], cols=[1], tops=[8], uppers=[9],
               lowers=[7], bottoms=[6]),
  ]
  test = [
      generate(size=15, widths=[6, 2, 4], rows=[1, 4, 10], cols=[1, 11, 6],
               tops=[6, 9, 6], uppers=[9, 7, 2], lowers=[7, 2, 8], bottoms=[8, 6, 3]),
  ]
  return {"train": train, "test": test}
