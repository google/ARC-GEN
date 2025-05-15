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


def generate(cols=None, lengths=None, idxs=None, colors=None, flip=None,
             width=4, height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: a list of horizontal coordinates where columns should be placed
    lengths: a list of column lengths
    idxs: a list of color indices
    colors: a list of colors
    flip: whether to flip the grid
    width: the width of the grid
    height: the height of the grid
  """
  if cols is None:
    cols = list(range(width))
    lengths = [common.randint(4, 5),
               common.randint(2, 5),
               common.randint(1, 2),
               common.randint(0, 2)]
    idxs = list(range(width))
    extra_cols = common.sample([2, 3], common.randint(0, 2))
    for extra_col in extra_cols:
      cols.append(extra_col)
      lengths.append(common.randint(1, 2))
      idxs.append(common.randint(1, width - 1))
    colors = common.random_colors(width)
    flip = common.randint(0, 1)

  grid, output = common.grids(width, 2 * height)
  heights = [0] * width
  for col, length, idx in zip(cols, lengths, idxs):
    for r in range(heights[col], heights[col] + length):
      grid[2 * height - 1 - r][col] = colors[idx]
      output[r][col] = output[2 * height - 1 - r][col] = colors[idx]
    heights[col] += length
  if flip:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[0, 1, 2, 3], lengths=[5, 4, 1, 2], idxs=[0, 1, 2, 3],
               colors=[9, 3, 4, 2], flip=1),
      generate(cols=[0, 1, 2, 3, 2], lengths=[5, 2, 2, 1, 1],
               idxs=[0, 1, 2, 2, 1], colors=[2, 8, 3, 4], flip=1),
  ]
  test = [
      generate(cols=[0, 1, 2, 3, 2, 3], lengths=[4, 5, 1, 1, 2, 1],
               idxs=[0, 1, 2, 2, 3, 3], colors=[7, 1, 4, 3], flip=0),
  ]
  return {"train": train, "test": test}
