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


def generate(width=None, height=None, wides=None, talls=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The colors of the boxes.
  """

  if width is None:
    width = common.randint(12, 20)
    height = width + common.randint(0, 4) - 2
    num_boxes = common.randint(1, 4)
    colors = common.random_colors(num_boxes)
    while True:
      wides = [common.randint(5, 12) for _ in range(num_boxes)]
      talls = [common.randint(5, 12) for _ in range(num_boxes)]
      rows = [common.randint(0, height - t) for t in talls]
      cols = [common.randint(0, width - w) for w in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break

  grid, output = common.grids(width, height)
  for wide, tall, row, col, color in zip(wides, talls, rows, cols, colors):
    common.rect(grid, wide, tall, row, col, color)
    common.rect(output, wide, tall, row, col, color)
    for r in range(1, tall - 1):
      for c in range(1, wide - 1):
        if (r + c) % 2 == 0:
          output[row + r][col + c] = 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=13, wides=[5, 10], talls=[5, 6], rows=[0, 6], cols=[0, 4], colors=[1, 8]),
      generate(width=15, height=16, wides=[10], talls=[8], rows=[4], cols=[4], colors=[2]),
      generate(width=16, height=17, wides=[8, 8, 6], talls=[7, 7, 5], rows=[1, 9, 9], cols=[2, 0, 10], colors=[3, 4, 8]),
  ]
  test = [
      generate(width=19, height=19, wides=[8, 8, 11, 5], talls=[9, 7, 8, 6], rows=[1, 2, 11, 11], cols=[1, 10, 1, 13], colors=[8, 7, 6, 4]),
  ]
  return {"train": train, "test": test}
