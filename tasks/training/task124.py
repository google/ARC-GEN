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


def generate(height=None, rows=None, cols=None, offset=None, color=None,
             diag=None, width=10):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    offset: the vertical offset of the pattern
    color: a digit representing a color to be used
    diag: whether the pattern should repeat diagonally
    width: the width of the input grid
  """
  if height is None:
    height = common.randint(5, 8)
    wide, tall = common.randint(2, 3), common.randint(2, 3)
    if height < 8: tall = 2
    if height < 6: wide = 1
    while True:
      rows, cols = common.conway_sprite(wide, tall)
      if len(set(rows)) == tall and len(set(cols)) == wide: break
    offset, color = common.randint(0, 3), common.random_color()
    diag = 0 if tall > 2 else common.randint(0, 1)

  grid, output = common.grid(width, height), common.grid(width, width)
  wide, tall = max(cols) + 1, max(rows) + 1
  for dr in range(width):  # (actually max height)
    for row, col in zip(rows, cols):
      r = dr * tall + row
      c = dr * (wide - 1) * diag + col + offset
      common.draw(grid, r, c, color)
      common.draw(output, r, c, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=6, rows=[0, 0, 0, 1], cols=[0, 1, 2, 2], offset=0,
               color=1, diag=1),
      generate(height=5, rows=[0], cols=[0], offset=2, color=3, diag=0),
      generate(height=8, rows=[0, 1, 2, 2], cols=[1, 1, 0, 2], offset=0,
               color=2, diag=0),
  ]
  test = [
      generate(height=8, rows=[0, 1], cols=[1, 0], offset=3, color=6, diag=0),
      generate(height=5, rows=[0, 0, 0, 1, 1], cols=[0, 1, 2, 0, 2], offset=1,
               color=8, diag=0),
  ]
  return {"train": train, "test": test}
