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


def generate(widths=None, heights=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    widths: The widths of the boxes.
    heights: The heights of the boxes.
    colors: The colors of the boxes.
  """

  def draw():
    grid, output = common.grids(10, 10)
    grid_col, output_row, output_col = 0, 0, 0
    for width, height, color in zip(widths, heights, colors):
      for r in range(height):
        for c in range(width):
          if grid_col + c >= 10: return None, None
          if output_row + r >= 10: return None, None
          grid[9 - r][grid_col + c] = color
          output[output_row + r][output_col + c] = color
      grid_col += width + 1
      output_col += width - 1
      output_row += height - 1
    if grid_col not in [10, 11]: return None, None
    return grid, output

  if widths is None:
    while True:
      num_boxes = common.randint(3, 4)
      widths = [common.randint(1, 4) for _ in range(num_boxes)]
      heights = [common.randint(2, 5) for _ in range(num_boxes)]
      colors = common.random_colors(num_boxes)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(widths=[3, 2, 3], heights=[4, 2, 2], colors=[8, 7, 2]),
      generate(widths=[2, 2, 2, 1], heights=[3, 2, 2, 4], colors=[1, 2, 3, 4]),
      generate(widths=[4, 1, 3], heights=[2, 5, 3], colors=[4, 2, 3]),
  ]
  test = [
      generate(widths=[1, 2, 1, 2], heights=[4, 3, 3, 2], colors=[7, 8, 6, 3]),
  ]
  return {"train": train, "test": test}
