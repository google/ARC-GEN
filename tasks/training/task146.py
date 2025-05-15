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


def generate(idx=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    idx: which of the grids is the asymmetric one
    colors: the colors with which to fill the grid
  """
  if idx is None:
    idx = common.randint(0, 2)
    while True:
      colors, color_list = [], common.random_colors(6)
      for i in range(3):
        grid = [color_list[2 * i + common.randint(0, 1)] for _ in range(9)]
        colors.extend(grid)
      asymmetric = False
      for i in range(3):
        for r in range(3):
          for c in range(r):
            if i != idx:
              colors[i * 9 + r * 3 + c] = colors[i * 9 + c * 3 + r]
            elif colors[i * 9 + r * 3 + c] != colors[i * 9 + c * 3 + r]:
              asymmetric = True
      if len(set(colors)) < 6: continue  # We want each color used at least once
      if asymmetric: break

  grid, output = common.grid(3, 9), common.grid(3, 3)
  for r in range(9):
    for c in range(3):
      grid[r][c] = colors[r * 3 + c]
  for r in range(3):
    for c in range(3):
      output[r][c] = grid[r + idx * 3][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(idx=2,
               colors=[8, 9, 8, 9, 8, 8, 8, 8, 8, 2, 2, 1, 2, 2, 1, 1, 1, 2, 4,
                       4, 4, 4, 4, 3, 3, 3, 3]),
      generate(idx=1,
               colors=[1, 5, 5, 5, 1, 1, 5, 1, 1, 3, 3, 3, 3, 6, 3, 3, 6, 6, 7,
                       7, 7, 7, 2, 2, 7, 2, 2]),
      generate(idx=2,
               colors=[2, 2, 2, 2, 2, 3, 2, 3, 3, 5, 7, 7, 7, 5, 5, 7, 5, 5, 8,
                       8, 1, 1, 8, 1, 1, 8, 1]),
      generate(idx=0,
               colors=[8, 8, 4, 4, 4, 4, 4, 4, 8, 1, 1, 3, 1, 3, 3, 3, 3, 1, 6,
                       2, 2, 2, 2, 2, 2, 2, 6]),
  ]
  test = [
      generate(idx=0,
               colors=[5, 4, 4, 4, 5, 4, 4, 5, 4, 3, 3, 2, 3, 3, 2, 2, 2, 3, 1,
                       1, 1, 1, 8, 8, 1, 8, 8]),
  ]
  return {"train": train, "test": test}
