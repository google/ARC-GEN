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


def generate(widths=None, heights=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    widths: The widths of the boxes.
    heights: The heights of the boxes.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
  """

  if widths is None:
    num_rects = common.randint(2, 3)
    while True:
      widths = [2 * common.randint(3, 8) for _ in range(num_rects)]
      heights = [2 * common.randint(3, 8) for _ in range(num_rects)]
      rows = [common.randint(1, 22 - h) for h in heights]
      cols = [common.randint(1, 22 - w) for w in widths]
      if not common.overlaps(rows, cols, widths, heights, 1): break

  grid, output = common.grids(23, 23)
  for width, height, row, col in zip(widths, heights, rows, cols):
    common.rect(grid, width, height, row, col, 8)
    for r in range(height):
      for c in range(width):
        color = None
        if r < height // 2 and c < width // 2: color = 6
        if r < height // 2 and c >= width // 2: color = 1
        if r >= height // 2 and c < width // 2: color = 2
        if r >= height // 2 and c >= width // 2: color = 3
        output[row + r][col + c] = color
    common.rect(output, width - 4, height - 4, row + 2, col + 2, 4)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(widths=[12, 12], heights=[10, 8], rows=[1, 14], cols=[5, 1]),
      generate(widths=[8, 12], heights=[8, 10], rows=[1, 10], cols=[2, 7]),
  ]
  test = [
      generate(widths=[6, 10, 6], heights=[10, 14, 6], rows=[1, 4, 15],
               cols=[3, 12, 3]),
  ]
  return {"train": train, "test": test}
