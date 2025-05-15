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


def generate(width=None, height=None, wide=None, tall=None, redrow=None,
             redcol=None, cyanrow=None, cyancol=None, rows=None, cols=None,
             flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wide: The width of the red magnet.
    tall: The height of the red magnet.
    redrow: The row of the red magnet.
    redcol: The column of the red magnet.
    cyanrow: The row of the cyan magnet.
    cyancol: The column of the cyan magnet.
    rows: The rows of the red magnet nibbles.
    cols: The columns of red magnet nibbles.
    flip: Whether to flip the grids vertically.
    xpose: Whether to transpose the grids.
  """
  if width is None:
    width, height = common.randint(8, 16), common.randint(8, 16)
    wide, tall = common.randint(4, 5), common.randint(2, 3)
    while True:
      redrow = common.randint(0, height - tall)
      cyanrow = common.randint(0, height - 3)
      if redrow + tall < cyanrow: break
    redcol = common.randint(0, width - wide)
    cyancol = common.randint(max(0, redcol - 1),
                             min(width - 2, redcol + wide - 1))
    while True:  # Check that the nibbles don't just form a smaller box.
      rows, cols = common.rectangle_nibbles(wide, tall, cyancol - redcol)
      if not rows or not cols: continue
      all_gone = False
      for row in range(tall):
        if len([r for r in rows if r == row]) == wide: all_gone = True
      for col in range(wide):
        if len([c for c in cols if c == col]) == tall: all_gone = True
      if not all_gone: break
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  delta = cyanrow - redrow - tall
  # Draw the red cells.
  for r in range(tall):
    for c in range(wide):
      grid[redrow + r][redcol + c] = common.red()
      output[redrow + r + delta][redcol + c] = common.red()
  # Draw the cyan cells.
  for r in range(2):
    for c in range(2):
      grid[cyanrow + r][cyancol + c] = common.cyan()
      output[cyanrow + r][cyancol + c] = common.cyan()
  # Darken out the nibbles.
  for r, c in zip(rows, cols):
    grid[redrow + r][redcol + c] = common.black()
    output[redrow + r + delta][redcol + c] = common.black()
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=14, wide=4, tall=2, redrow=2, redcol=0,
               cyanrow=10, cyancol=3, rows=[0, 1], cols=[0, 2], flip=0,
               xpose=0),
      generate(width=9, height=10, wide=4, tall=3, redrow=0, redcol=1,
               cyanrow=6, cyancol=4, rows=[0, 0, 0], cols=[0, 1, 3], flip=0,
               xpose=1),
      generate(width=10, height=11, wide=5, tall=3, redrow=2, redcol=1,
               cyanrow=8, cyancol=3, rows=[0, 0, 0, 2, 2], cols=[0, 3, 4, 0, 1],
               flip=1, xpose=0),
  ]
  test = [
      generate(width=11, height=10, wide=4, tall=2, redrow=3, redcol=4,
               cyanrow=7, cyancol=6, rows=[0, 1], cols=[0, 3],
               flip=1, xpose=1),
  ]
  return {"train": train, "test": test}
