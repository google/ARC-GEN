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


def generate(rows=None, cols=None, colors=None, bcolors=None, pcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The color indices of the boxes.
    bcolors: The three box colors.
    pcolors: The three pixel colors.
  """

  if rows is None:
    num_boxes = common.randint(8, 9)
    while True:
      rows = [common.randint(0, 10) for _ in range(num_boxes)]
      cols = [common.randint(0, 8) for _ in range(num_boxes)]
      if not common.overlaps(rows, cols, [3] * num_boxes, [3] * num_boxes):
        break
    colors = common.sample([0, 1, 2, 3, 4, 5, 6, 8, 9], 6)
    bcolors, pcolors = colors[0:3], colors[3:6]
    colors = [common.randint(0, 2) for _ in range(num_boxes)]

  grid, output = common.grid(11, 20, 7), common.grid(11, 13, 7)
  # Draw the header.
  for r in range(3):
    grid[4][4 * r + 1] = pcolors[r]
    for c in range(3):
      grid[r][c] = bcolors[0]
      grid[r][c + 4] = bcolors[1]
      grid[r][c + 8] = bcolors[2]
  for c in range(11):
    grid[6][c] = 6
  for row, col, color in zip(rows, cols, colors):
    grid[row + 8][col + 1] = pcolors[color]
    for r in range(3):
      for c in range(3):
        output[row + r][col + c] = bcolors[color]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 5, 5, 5, 9, 10], cols=[0, 4, 7, 0, 4, 8, 8, 2],
               colors=[1, 0, 2, 2, 1, 0, 2, 2], bcolors=[9, 2, 3],
               pcolors=[5, 0, 8]),
      generate(rows=[0, 1, 1, 4, 4, 5, 8, 8, 10],
               cols=[0, 3, 8, 0, 8, 4, 0, 6, 3],
               colors=[2, 1, 1, 0, 0, 2, 1, 1, 2], bcolors=[5, 4, 6],
               pcolors=[2, 8, 1]),
  ]
  test = [
      generate(rows=[0, 0, 1, 4, 4, 8, 8, 9], cols=[4, 8, 1, 1, 6, 1, 4, 8],
               colors=[1, 2, 2, 0, 0, 2, 0, 2], bcolors=[2, 1, 5],
               pcolors=[8, 6, 9]),
  ]
  return {"train": train, "test": test}
