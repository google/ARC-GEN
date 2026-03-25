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


def generate(row=None, col=None, thick=None, show=None, color=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    row: a vertical coordinate where the center mat starts
    col: a list of horizontal coordinates where the center mat starts
    thick: the thickness of the repeating mats
    show: how many mats to show
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
  """
  if row is None:
    if common.randint(0, 1):
      row, col = common.randint(0, size - 1), 0
    else:
      row, col = 0, common.randint(0, size - 1)
    thick, show = common.randint(1, 2), common.randint(2, 3)
    color = common.random_color(exclude=[common.gray()])

  grid, output = common.grid(size, size), common.grid(size, size, common.gray())
  for i in range(size):
    radius = (thick + 1) * i
    for r in range(row - radius + thick, row + radius):
      common.draw(output, r, col - radius + thick, color)
      common.draw(output, r, col + radius - 1, color)
      if i > show: continue
      common.draw(grid, r, col - radius + thick, color)
      common.draw(grid, r, col + radius - 1, color)
    for c in range(col - radius + thick, col + radius):
      common.draw(output, row - radius + thick, c, color)
      common.draw(output, row + radius - 1, c, color)
      if i > show: continue
      common.draw(grid, row - radius + thick, c, color)
      common.draw(grid, row + radius - 1, c, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(row=9, col=0, thick=1, show=3, color=8),
      generate(row=0, col=8, thick=2, show=2, color=1),
      generate(row=0, col=4, thick=1, show=2, color=2),
  ]
  test = [
      generate(row=4, col=0, thick=2, show=2, color=4),
  ]
  return {"train": train, "test": test}
