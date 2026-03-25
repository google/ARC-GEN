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


def generate(width=None, height=None, row=None, col=None, thicks=None,
             colors=None, extra=0):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    row: The row of the box.
    col: The column of the box.
    thicks: The thicknesses of the boxes.
    colors: The colors of the boxes.
    extra: Extra padding for the one ambiguous case.
  """

  if width is None:
    thicks = [common.randint(1, 3) for _ in range(2)]
    bigthick = 2 * thicks[0] + 3 * thicks[1]
    width = bigthick + common.randint(2, 5)
    height = bigthick + common.randint(2, 5)
    row = common.randint(0, height - bigthick)
    col = common.randint(0, width - bigthick)
    row += thicks[1]
    col += thicks[1]
    colors = common.random_colors(2)

  grid, output = common.grids(width, height)
  common.rect(grid,
              2 * thicks[0] + thicks[1],
              2 * thicks[0] + thicks[1] + extra,
              row,
              col,
              colors[0])
  common.rect(grid,
              thicks[1],
              thicks[1] + extra,
              row + thicks[0],
              col + thicks[0],
              colors[1])

  common.rect(output,
              2 * thicks[0] + 3 * thicks[1] - 2 * extra,
              2 * thicks[0] + 3 * thicks[1] - extra,
              row - thicks[1] + extra,
              col - thicks[1] + extra,
              colors[1])
  common.rect(output,
              2 * thicks[0] + thicks[1],
              2 * thicks[0] + thicks[1] + extra,
              row,
              col,
              colors[0])
  common.rect(output,
              thicks[1],
              thicks[1] + extra,
              row + thicks[0],
              col + thicks[0],
              colors[1])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=17, height=16, row=3, col=3, thicks=[2, 3], colors=[5, 2]),
      generate(width=14, height=13, row=3, col=3, thicks=[2, 1], colors=[3, 1]),
      generate(width=14, height=15, row=3, col=3, thicks=[1, 2], colors=[6, 4]),
      generate(width=11, height=12, row=3, col=3, thicks=[1, 1], colors=[1, 2]),
      generate(width=19, height=13, row=2, col=2, thicks=[2, 3], colors=[4, 5], extra=1),
  ]
  test = [
      generate(width=21, height=21, row=6, col=5, thicks=[1, 4], colors=[3, 8]),
  ]
  return {"train": train, "test": test}
