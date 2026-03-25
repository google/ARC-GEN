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


def generate(size=None, rows=None, cols=None, colors=None, magnifier=None,
             linecolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    magnifier: the zoom ratio in the input grid
    linecolor: the color of the gridlines
  """
  if rows is None:
    size, magnifier = common.randint(3, 4), common.randint(2, 5)
    linecolor, num_colors = common.random_color(), common.randint(1, 3)
    color_list = common.random_colors(num_colors, exclude=[linecolor])
    pixels = common.random_pixels(size, size)
    rows, cols = zip(*pixels)
    colors = [common.choice(color_list) for _ in pixels]

  output = common.grid(size, size)
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = color
  grid = common.create_linegrid(output, magnifier, linecolor)
  grid = common.flip_horiz(grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, rows=[0, 1, 2, 3, 3, 3], cols=[3, 2, 1, 1, 2, 3],
               colors=[3, 3, 3, 3, 3, 3], magnifier=4, linecolor=2),
      generate(size=4, rows=[0, 1, 1, 2, 3], cols=[2, 2, 3, 1, 0],
               colors=[2, 1, 2, 1, 3], magnifier=4, linecolor=8),
      generate(size=3, rows=[0, 1, 1, 2], cols=[1, 1, 2, 0],
               colors=[8, 8, 8, 4], magnifier=3, linecolor=2),
  ]
  test = [
      generate(size=4, rows=[0, 0, 0, 0, 1, 2, 2, 2, 3],
               cols=[0, 1, 2, 3, 2, 0, 2, 3, 2],
               colors=[1, 1, 3, 1, 3, 2, 3, 2, 3], magnifier=5, linecolor=8),
  ]
  return {"train": train, "test": test}
