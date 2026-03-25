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


def generate(colors=None, widths=None, heights=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    widths: A list of widths to use.
    heights: A list of heights to use.
  """

  if colors is None:
    num_colors = common.randint(4, 5)
    colors = common.random_colors(num_colors)
    widths = [2, 3, 2, 3] if num_colors == 4 else [2, 2, 2, 2, 2]
    heights = [2, 3, 2, 3] if num_colors == 4 else [2, 2, 2, 2, 2]
    for _ in range(10):
      idxs, dim = common.sample(range(num_colors), 2), common.randint(0, 1)
      min_val = 1 if idxs[0] + 1 < num_colors else 2
      if dim == 0 and widths[idxs[0]] > min_val:
        widths[idxs[0]] -= 1
        widths[idxs[1]] += 1
      elif dim == 1 and heights[idxs[0]] > min_val:
        heights[idxs[0]] -= 1
        heights[idxs[1]] += 1

  grid, output = common.grids(10, 10)
  row, col = 0, 0
  for color, width, height in zip(colors, widths, heights):
    common.rect(output, width, height, row, col, color)
    for _ in range(width):
      output[9][col] = grid[9][col] = color
      col += 1
    for _ in range(height):
      output[row][9] = grid[row][9] = color
      row += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 6, 7, 8, 9], widths=[1, 2, 3, 1, 3], heights=[1, 2, 3, 1, 3]),
      generate(colors=[9, 8, 7, 6, 5], widths=[2, 2, 2, 2, 2], heights=[2, 2, 2, 2, 2]),
      generate(colors=[8, 4, 5, 3], widths=[2, 3, 2, 3], heights=[3, 2, 2, 3]),
  ]
  test = [
      generate(colors=[3, 4, 6, 9, 7], widths=[2, 1, 3, 2, 2], heights=[3, 2, 2, 1, 2]),
  ]
  return {"train": train, "test": test}
