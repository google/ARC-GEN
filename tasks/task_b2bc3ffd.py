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


def generate(heights=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    heights: The heights of the lines.
    colors: The colors of the lines.
  """

  if heights is None:
    heights, colors = [], []
    while len(heights) <= 8:
      wide = common.choice([1, 1, 1, 1, 1, 2, 3, 3, 3, 6])
      wide = min(wide, 8 - len(heights))
      tall = 1
      if wide <= 3: tall = common.randint(1, 2)
      if wide <= 1: tall = common.randint(1, 3)
      color = common.random_color(exclude=colors + [7, 8])
      talls = [tall] * wide
      if wide >= 2 and tall >= 2:  # Trim one or both corners.
        cols = common.sample([0, -1], common.randint(1, 2))
        for col in cols:
          talls[col] -= 1
      heights.extend(talls)
      colors.extend([color] * wide)
      #  Add some space between us and the next shape.
      for _ in range(common.randint(1, 2)):
        heights.append(0)
        colors.append(8)
    # Hack to trim values or extend them.
    while len(heights) < 8:
      heights.append(0)
      colors.append(8)
    while len(heights) > 8:
      heights.pop()
      colors.pop()

  grid, output = common.grids(8, 8, 7)
  for c in range(8):
    output[7][c] = grid[7][c] = 8
  color_to_count = {}
  for col, height in enumerate(heights):
    color = colors[col]
    for r in range(7 - height, 7):
      grid[r][col] = color
    if color not in color_to_count: color_to_count[color] = 0
    color_to_count[color] += height
  for col, height in enumerate(heights):
    color = colors[col]
    for r in range(7 - height, 7):
      output[r - color_to_count[color]][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(heights=[1, 2, 1, 0, 0, 1, 1, 1], colors=[9, 9, 9, 8, 8, 2, 2, 2]),
      generate(heights=[0, 2, 0, 3, 0, 1, 0, 2], colors=[8, 2, 8, 9, 8, 1, 8, 3]),
      generate(heights=[2, 2, 1, 0, 1, 2, 0, 3], colors=[1, 1, 1, 8, 3, 3, 8, 4]),
  ]
  test = [
      generate(heights=[1, 1, 1, 1, 1, 1, 0, 1], colors=[5, 5, 5, 5, 5, 5, 8, 6]),
  ]
  return {"train": train, "test": test}
