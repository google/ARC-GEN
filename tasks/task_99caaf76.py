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


def generate(width=None, height=None, brows=None, cdirs=None, xpose=None,
             colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: Width of the grid.
    height: Height of the grid.
    brows: Rows of the flowers.
    cdirs: Directions of the flowers.
    xpose: Whether to transpose the grid.
    colors: Colors of the flowers.
  """

  if width is None:
    width, height = common.randint(7, 20), common.randint(5, 20)
    brow, brows, colors = common.randint(1, 2), [], []
    while brow + 1 < height:
      brows.append(brow)
      colors.extend(common.sample([0, 2, 3, 5, 6, 7, 9], 4))
      brow += common.randint(4, 5)
    cdirs = [common.randint(0, 1) for _ in brows]
    xpose = common.randint(0, 1)

  grid, output = common.grids(width, height, 8)
  for i, (brow, cdir) in enumerate(zip(brows, cdirs)):
    # Draw the blue stuff.
    for r, c, color in [(-1, 0, 1), (0, 1, 1), (0, 2, 1), (1, 0, 1), (0, 4, 4)]:
      grid[brow + r][c if not cdir else (width - 1 - c)] = color
      output[brow + r][(width - 6 + c) if not cdir else (5 - c)] = color
    # Draw the colorful stuff.
    for j, (r, c) in enumerate([(-1, 4), (0, 3), (0, 5), (1, 4)]):
      color = colors[4 * i + j]
      grid[brow + r][c if not cdir else (width - 1 - c)] = color
      output[brow - r][(width - 1 - (c - 3)) if not cdir else (c - 3)] = color

  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=8, brows=[2, 6], cdirs=[0, 1], xpose=False,
               colors=[6, 9, 3, 2, 7, 6, 5, 0]),
      generate(width=8, height=5, brows=[1], cdirs=[1], xpose=True,
               colors=[6, 3, 7, 5]),
      generate(width=9, height=13, brows=[1, 5, 10], cdirs=[1, 0, 0],
               xpose=True, colors=[7, 6, 5, 0, 7, 9, 5, 3, 0, 2, 6, 3]),
  ]
  test = [
      generate(width=17, height=18, brows=[1, 5, 10, 14],
               cdirs=[0, 1, 0, 0], xpose=False,
               colors=[0, 3, 7, 5, 7, 9, 5, 6, 9, 0, 5, 6, 5, 7, 3, 0]),
  ]
  return {"train": train, "test": test}
