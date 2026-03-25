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


def generate(size=None, scale=None, bcol=None, brows=None, prows=None,
             flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    scale: The scale of the boxes.
    bcol: The leftmost column of the boxes.
    brows: The row of the maroon box, and the orange box.
    prows: A list of rows of the black lines.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  def draw():
    grid, output = common.grids(size, size, 6)
    common.rect(grid, scale, scale, brows[0], bcol, 9)
    common.rect(grid, scale, scale, brows[1], bcol, 7)
    common.rect(output, scale, scale, brows[0], bcol, 7)
    good = False
    for prow in prows:
      for col in [bcol - 2, bcol - 1, bcol + scale, bcol + scale + 1]:
        output[prow][col] = grid[prow][col] = 0
      if prow < brows[0] + scale: continue
      good = True
      for col in range(bcol, bcol + scale):
        output[prow][col] = 2
    if flip: grid, output = common.flip(grid), common.flip(output)
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    if not good: return None, None
    return grid, output

  if size is None:
    while True:
      scale = common.randint(1, 4)
      size = (scale + 1) * 4 + common.randint(0, 6)
      bcol = common.randint(3, size - scale - 3)
      brows = [common.randint(0, size // 2), size - scale - common.randint(0, 2)]
      prows = [common.randint(1, 3)]
      while True:
        prow = prows[-1] + common.randint(2, 4)
        if prow + 1 >= brows[1]: break
        prows.append(prow)
      flip, xpose = common.randint(0, 1), common.randint(0, 1)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, scale=2, bcol=6, brows=[1, 10], prows=[3, 5, 8], flip=0,
               xpose=0),
      generate(size=8, scale=1, bcol=4, brows=[0, 6], prows=[2, 4], flip=1,
               xpose=1),
      generate(size=16, scale=2, bcol=7, brows=[4, 12], prows=[1, 3, 5, 7, 10],
               flip=0, xpose=1),
  ]
  test = [
      generate(size=26, scale=4, bcol=10, brows=[13, 22],
               prows=[2, 6, 8, 10, 12, 14, 17, 19], flip=1, xpose=0),
  ]
  return {"train": train, "test": test}
