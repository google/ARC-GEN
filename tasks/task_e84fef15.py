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


def generate(rows=None, cols=None, colors=None, vanishes=None, brow=None,
             bcol=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
    vanishes: Whether the pixel is vanishing.
    brow: The row of the vanishing box.
    bcol: The column of the vanishing box.
  """

  if rows is None:
    while True:
      pixels = common.random_pixels(5, 5, 0.28)
      if len(pixels) >= 5 and len(pixels) <= 10: break
    rows, cols = zip(*pixels)
    colors = common.choices([0, 2, 4, 6], len(pixels))
    while True:
      vanishes = [common.randint(0, 1) for _ in range(len(pixels))]
      if len(set(vanishes)) == 2: break
    brow, bcol = common.randint(0, 4), common.randint(0, 4)

  grid, output = common.grid(29, 29, 8), common.grid(5, 5, 8)
  for r in range(5, 29, 6):
    for c in range(29):
      grid[r][c] = 3
  for r in range(29):
    for c in range(5, 29, 6):
      grid[r][c] = 3
  for row in range(5):
    for col in range(5):
      for r, c, color, vanish in zip(rows, cols, colors, vanishes):
        if row == brow and col == bcol and vanish: continue
        grid[row * 6 + r][col * 6 + c] = color
  for r, c, color, vanish in zip(rows, cols, colors, vanishes):
    output[r][c] = 1 if vanish else color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 2, 2, 2, 3, 4], cols=[2, 0, 2, 4, 0, 4],
               colors=[4, 0, 2, 2, 0, 4], vanishes=[0, 0, 1, 0, 1, 0], brow=2,
               bcol=4),
      generate(rows=[0, 0, 0, 2, 2, 4, 4], cols=[0, 2, 4, 0, 2, 2, 4],
               colors=[0, 2, 4, 4, 6, 0, 2], vanishes=[0, 1, 0, 0, 0, 1, 1],
               brow=2, bcol=1),
      generate(rows=[0, 0, 1, 2, 3, 4, 4], cols=[0, 2, 0, 1, 3, 0, 4],
               colors=[0, 4, 4, 2, 2, 0, 0], vanishes=[0, 1, 1, 1, 1, 0, 0],
               brow=4, bcol=2),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 3, 4, 4], cols=[0, 2, 1, 2, 4, 2, 0, 4],
               colors=[2, 2, 0, 0, 6, 4, 2, 4],
               vanishes=[0, 0, 1, 1, 1, 0, 0, 0], brow=1, bcol=3),
  ]
  return {"train": train, "test": test}
