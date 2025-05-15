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


def generate(rows=None, cols=None, colors=None, size=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_colors = common.randint(3, 5)
    colors_list = common.random_colors(num_colors, exclude=[common.blue(),
                                                            common.gray()])
    idxs = [common.randint(0, num_colors - 1) for _ in range(size * size)]
    colors = [colors_list[idx] for idx in idxs]
    pixels = common.sample(common.all_pixels(size, size), common.randint(2, 7))
    rows, cols = zip(*pixels)

  grid, output = common.grids(4 * size + 1, 3 * size)
  for r in range(3 * size):
    output[r][size] = grid[r][size] = common.gray()
  for r, c in zip(rows, cols):
    grid[size * r + 1][size * (c + 1) + 2] = common.blue()
    for mr in range(size):
      for mc in range(size):
        output[mr][mc] = grid[mr][mc] = colors[mr * size + mc]
        output[size * r + mr][size * (c + 1) + mc + 1] = colors[mr * size + mc]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 2], cols=[0, 1, 1],
               colors=[4, 2, 2, 2, 6, 2, 6, 4, 4]),
      generate(rows=[0, 1, 1, 2, 2], cols=[1, 0, 2, 0, 1],
               colors=[2, 7, 3, 2, 3, 3, 3, 7, 7]),
      generate(rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 1, 2],
               colors=[3, 8, 6, 9, 8, 2, 9, 9, 9]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 2], cols=[1, 2, 0, 2, 0, 1],
               colors=[3, 3, 9, 8, 4, 4, 8, 9, 8]),
  ]
  return {"train": train, "test": test}
