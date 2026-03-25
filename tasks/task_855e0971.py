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


def generate(width=None, colors=None, heights=None, strata=None, rows=None,
    cols=None, xpose=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    colors: a list of colors (one per strata)
    heights: a list of heights (one per strata)
    strata: a list of strata indices (one for each pixel)
    rows: a list of row indices (one for each pixel)
    cols: a list of column indices (one for each pixel)
    xpose: a boolean indicating whether to transpose the grid
  """
  if width is None:
    width = common.randint(10, 20)
    colors = common.random_colors(common.randint(2, 5))
    heights = [common.randint(2, 10) for _ in colors]
    while True:
      strata, rows = [], []
      for idx, height in enumerate(heights):
        num_pixels = common.randint(0, 2)
        strata.extend([idx] * num_pixels)
        rows.extend(common.sample(range(height), num_pixels))
      if strata: break
    cols = common.sample(range(width), len(strata))
    xpose = common.randint(0, 1)

  grid, output, floor = [], [], 0
  for idx, (color, height) in enumerate(zip(colors, heights)):
    for _ in range(height):
      grid.append([color for _ in range(width)])
      output.append([color for _ in range(width)])
    for stratum, col, row in zip(strata, cols, rows):
      if stratum != idx: continue
      grid[floor + row][col] = common.black()
      for r in range(height):
        output[floor + r][col] = common.black()
    floor += height
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=19, colors=[5, 4, 8], heights=[2, 7, 6], strata=[1, 2, 1],
               rows=[3, 3, 1], cols=[4, 9, 13], xpose=0),
      generate(width=14, colors=[2, 1], heights=[5, 8], strata=[0, 1],
               rows=[2, 3], cols=[3, 11], xpose=1),
      generate(width=15, colors=[8, 2, 3], heights=[5, 5, 3],
               strata=[0, 0, 1, 2], rows=[2, 3, 2, 1], cols=[3, 11, 5, 7],
               xpose=0),
      generate(width=14, colors=[2, 5, 4], heights=[4, 5, 6], strata=[1, 2, 2],
               rows=[2, 1, 3], cols=[6, 12, 2], xpose=1),
  ]
  test = [
      generate(width=15, colors=[8, 1, 4, 2], heights=[4, 4, 5, 4],
               strata=[0, 0, 1, 2, 3], rows=[0, 2, 2, 2, 2],
               cols=[4, 12, 6, 10, 1], xpose=0),
  ]
  return {"train": train, "test": test}
