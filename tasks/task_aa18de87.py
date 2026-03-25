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


def generate(width=None, height=None, bottom=None, top=None, start=None,
             cdir=None, color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw():
    nonlocal start, cdir
    grid, output = common.grids(width, height)
    for c in range(width):
      common.draw(grid, start, c, color)
      common.draw(output, start, c, color)
      if start == bottom: cdir = 1
      if start + 1 == top: cdir = -1
      start += cdir
    good = False
    for row in range(height):
      for col in range(width):
        if grid[row][col]: continue
        if color not in [grid[row][c] for c in range(col)]: continue
        if color not in [grid[row][c] for c in range(col + 1, width)]: continue
        output[row][col] = 2
        good = True
    if not good: return None, None
    return grid, output

  if width is None:
    color = common.random_color(exclude=[2])
    while True:
      width, height = common.randint(8, 12), common.randint(3, 5)
      bottom = common.randint(-2, 0)
      top = height + common.randint(0, 2)
      start = common.randint(bottom, top)
      cdir = 2 * common.randint(0, 1) - 1
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=12, height=5, bottom=0, top=5, start=1, cdir=-1, color=8),
      generate(width=8, height=3, bottom=-2, top=3, start=-1, cdir=1, color=4),
      generate(width=8, height=5, bottom=0, top=5, start=0, cdir=1, color=1),
      generate(width=8, height=4, bottom=0, top=5, start=3, cdir=-1, color=3),
  ]
  test = [
      generate(width=9, height=4, bottom=0, top=4, start=2, cdir=-1, color=6),
  ]
  return {"train": train, "test": test}
