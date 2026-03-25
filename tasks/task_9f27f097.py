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


def generate(wide=None, brows=None, bcols=None, bgcolor=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    wide: Width of the shape.
    brows: Rows of the shape.
    bcols: Columns of the shape.
    bgcolor: Background color of the grid.
    colors: Colors of the pixels in the shape.
  """

  if wide is None:
    wide, tall = common.randint(4, 6), common.randint(3, 5)
    while True:
      brows = [common.randint(0, 12 - tall) for _ in range(2)]
      bcols = [common.randint(0, 12 - wide) for _ in range(2)]
      if common.overlaps(brows, bcols, [wide] * 2, [tall] * 2, 1): continue
      if common.overlaps_1d(brows, [tall] * 2): continue
      if not common.overlaps_1d(bcols, [wide] * 2): continue
      break
    subset = common.sample([1, 2, 3, 4, 8], 3)
    bgcolor = subset.pop()
    while True:
      colors = common.choices(subset, wide * tall)
      if len(set(colors)) == 2: break

  grid, output = common.grids(12, 12, bgcolor)
  for i, (brow, bcol) in enumerate(zip(brows, bcols)):
    for j, color in enumerate(colors):
      col = (bcol + wide - 1 - j % wide) if i else (bcol + j % wide)
      grid[brow + j // wide][col] = 0 if i else color
      output[brow + j // wide][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=5, brows=[6, 0], bcols=[1, 5], bgcolor=2,
               colors=[4, 4, 4, 1, 4, 4, 4, 1, 4, 4, 4, 1, 4, 1, 1, 4, 4, 1, 4, 1, 4, 4, 4, 4, 4]),
      generate(wide=4, brows=[1, 7], bcols=[1, 4], bgcolor=2,
               colors=[1, 3, 3, 1, 1, 1, 3, 1, 1, 3, 3, 3, 1, 1, 1, 1]),
      generate(wide=6, brows=[2, 8], bcols=[1, 3], bgcolor=1,
               colors=[3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 2, 2, 3, 2, 3, 3, 3, 3, 2, 3, 3]),
  ]
  test = [
      generate(wide=4, brows=[1, 9], bcols=[1, 2], bgcolor=8,
               colors=[1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
