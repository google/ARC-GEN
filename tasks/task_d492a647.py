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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, prow=None, pcol=None, pcolor=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if width is None:
    width, height = common.randint(12, 18), common.randint(12, 18)
    colors = [5 * common.randint(0, 1) for _ in range(width * height)]
    wide = common.randint(6, width - 4)
    tall = common.randint(6, height - 4)
    brow = common.randint(1, height - tall - 1)
    bcol = common.randint(1, width - wide - 1)
    prow = brow + common.randint(1, tall - 2)
    pcol = bcol + common.randint(1, wide - 2)
    pcolor = common.random_color(exclude=[5])

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    r, c = i // width, i % width
    output[r][c] = grid[r][c] = color
  common.rect(grid, wide, tall, brow, bcol, 0)
  common.rect(output, wide, tall, brow, bcol, 0)
  grid[prow][pcol] = pcolor
  for r in range(height):
    for c in range(width):
      if not output[r][c] and r % 2 == prow % 2 and c % 2 == pcol % 2:
        output[r][c] = pcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=13, wide=8, tall=8, brow=2, bcol=3, prow=4,
               pcol=5, pcolor=1,
               colors=[0, 0, 5, 0, 5, 5, 5, 0, 5, 0, 5, 5, 5,
                       5, 5, 0, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5,
                       5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5,
                       5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                       5, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5, 0, 5]),
      generate(width=16, height=13, wide=8, tall=7, brow=2, bcol=3, prow=5,
               pcol=7, pcolor=3,
               colors=[5, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 0, 5, 5,
                       0, 5, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 0, 0, 5, 5,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0,
                       5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5, 0,
                       5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 5, 0,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5,
                       0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 0, 0,
                       5, 5, 5, 5, 0, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0, 0,
                       0, 5, 5, 0, 0, 5, 0, 5, 0, 0, 0, 0, 5, 5, 0, 5,
                       5, 5, 0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5]),
  ]
  test = [
      generate(width=17, height=15, wide=12, tall=11, brow=1, bcol=3, prow=9,
               pcol=8, pcolor=2,
               colors=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 5, 0,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 0,
                       0, 5, 5, 0, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0, 5, 5, 5,
                       0, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5]),
  ]
  return {"train": train, "test": test}
