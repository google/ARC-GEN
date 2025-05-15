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


def generate(basicrows=None, basiccols=None, weirdrows=None, weirdcols=None,
             colors=None, weird=None, xpose=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    basicrows: a list of vertical coordinates for the basic shape
    basiccols: a list of horizontal coordinates for the basic shape
    weirdrows: a list of vertical coordinates for the weird shape
    weirdcols: a list of horizontal coordinates for the weird shape
    colors: a list of digits representing the colors of the shapes
    weird: a digit representing which color is weird
    xpose: a boolean indicating whether the shapes are transposed
    size: the width and height of the (square) grid
  """
  if basicrows is None:
    colors = common.random_colors(common.randint(3, 5))
    while True:
      basicrows, basiccols = common.conway_sprite()
      weirdrows, weirdcols = common.conway_sprite()
      # Convert to sets to make sure they are unique.
      basicpixels = set(list(zip(basicrows, basiccols)))
      weirdpixels = set(list(zip(weirdrows, weirdcols)))
      if len(basicpixels) != len(weirdpixels): break
    weird = common.randint(0, len(colors) - 1)
    xpose = common.randint(0, 1)

  grid = common.grid(size, size * len(colors))
  output = common.grid(size, size)
  for idx, color in enumerate(colors):
    rows = weirdrows if idx == weird else basicrows
    cols = weirdcols if idx == weird else basiccols
    for r, c in zip(rows, cols):
      grid[size * idx + r][c] = color
  for r, c in zip(weirdrows, weirdcols):
    output[r][c] = colors[weird]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(basicrows=[0, 0, 1, 1, 2, 2], basiccols=[0, 2, 1, 2, 0, 2],
               weirdrows=[0, 0, 0, 1, 1, 2, 2, 2],
               weirdcols=[0, 1, 2, 0, 2, 0, 1, 2], colors=[6, 4, 8], weird=2,
               xpose=0),
      generate(basicrows=[0, 0, 1, 2], basiccols=[0, 1, 2, 2],
               weirdrows=[0, 0, 1, 2, 2], weirdcols=[0, 2, 1, 0, 2],
               colors=[2, 3, 7, 1], weird=2, xpose=1),
      generate(basicrows=[0, 1, 1, 2], basiccols=[0, 1, 2, 1],
               weirdrows=[0, 0, 0, 1, 2, 2, 2], weirdcols=[0, 1, 2, 1, 0, 1, 2],
               colors=[3, 4, 2, 8, 1], weird=1, xpose=1),
      generate(basicrows=[0, 1, 1, 2], basiccols=[0, 1, 2, 0],
               weirdrows=[0, 0, 1, 1, 2, 2], weirdcols=[1, 2, 0, 1, 0, 2],
               colors=[7, 3, 2, 8], weird=0, xpose=0),
  ]
  test = [
      generate(basicrows=[0, 1, 1, 2], basiccols=[1, 0, 2, 1],
               weirdrows=[0, 0, 1, 1, 2, 2], weirdcols=[0, 2, 0, 1, 0, 2],
               colors=[5, 3, 6, 4, 8], weird=2, xpose=0),
  ]
  return {"train": train, "test": test}
