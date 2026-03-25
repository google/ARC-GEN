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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    width, height = common.randint(3, 4), common.randint(3, 4)
    colors, color_list = [0] * (width * height), common.random_colors(9)
    while True:
      left, right, top, bottom, idx = 0, width, 0, height, 0
      while left < right and top < bottom:
        for r in range(top, bottom):
          for c in range(left, right):
            colors[r * width + c] = color_list[idx]
        didx = 0
        if common.randint(0, 1): left, didx = left + 1, 1
        if common.randint(0, 1): right, didx = right - 1, 1
        if common.randint(0, 1): top, didx = top + 1, 1
        if common.randint(0, 1): bottom, didx = bottom - 1, 1
        idx += didx
      counts_to_colors = {colors.count(x): x for x in colors}
      if len(counts_to_colors) == idx: break

  counts_to_colors = {colors.count(x): x for x in colors}
  counts = sorted(counts_to_colors.keys(), reverse=True)
  grid, output = common.grid(width, height), common.grid(len(counts), counts[0])
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
  for idx, count in enumerate(counts):
    for r in range(count):
      output[r][idx] = counts_to_colors[count]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, colors=[2, 2, 1, 2, 3, 1, 1, 1, 1]),
      generate(width=4, height=3, colors=[3, 1, 1, 4, 2, 2, 2, 4, 4, 4, 4, 4]),
      generate(width=3, height=4, colors=[8, 8, 2, 3, 8, 8, 3, 3, 4, 3, 3, 4]),
      generate(width=3, height=4, colors=[1, 1, 1, 2, 2, 1, 2, 8, 1, 2, 8, 1]),
  ]
  test = [
      generate(width=4, height=4,
               colors=[8, 8, 2, 2, 1, 8, 8, 2, 1, 3, 3, 4, 1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
