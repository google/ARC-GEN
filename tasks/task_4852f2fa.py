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


def generate(brow=None, bcol=None, prows=None, pcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brow: The row of the sprite.
    bcol: The column of the sprite.
    prows: The rows of the yellow pixels.
    pcols: The cols of the yellow pixels.
    colors: The contents of the sprites.
  """

  if prows is None:
    sprite = common.diagonally_connected_sprite()
    colors = []
    for r in range(3):
      for c in range(3):
        colors.append(1 if (r, c) in sprite else 0)
    brow, bcol = common.randint(0, 6), common.randint(0, 6)
    num_dots = common.randint(1, 4)
    while True:
      prows = [common.randint(0, 8) for _ in range(num_dots)]
      pcols = [common.randint(0, 8) for _ in range(num_dots)]
      rows, cols = [brow] + prows, [bcol] + pcols
      wides, talls = [3] + ([1] * len(prows)), [3] + ([1] * len(pcols))
      if not common.overlaps(rows, cols, wides, talls, 1): break

  grid, output = common.grid(9, 9), common.grid(3 * len(prows), 3)
  for i, color in enumerate(colors):
    grid[brow + i // 3][bcol + i % 3] = 8 * color
  for prow, pcol in zip(prows, pcols):
    grid[prow][pcol] = 4
  for col in range(0, len(prows)):
    for i, color in enumerate(colors):
      output[i // 3][3 * col + i % 3] = 8 * color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brow=5, bcol=1, prows=[2], pcols=[4],
               colors=[0, 1, 0, 1, 1, 0, 0, 1, 1]),
      generate(brow=1, bcol=0, prows=[0, 4, 6], pcols=[5, 5, 3],
               colors=[0, 0, 1, 1, 1, 0, 1, 1, 0]),
      generate(brow=0, bcol=0, prows=[1, 3, 5, 8], pcols=[4, 6, 1, 5],
               colors=[0, 1, 1, 1, 1, 0, 0, 1, 0]),
      generate(brow=2, bcol=1, prows=[1, 5, 7], pcols=[5, 6, 3],
               colors=[0, 0, 0, 1, 1, 1, 0, 1, 0]),  # Ambiguous / broken case!!
      generate(brow=1, bcol=1, prows=[2, 5], pcols=[6, 6],
               colors=[0, 1, 1, 1, 1, 1, 0, 1, 0]),
  ]
  test = [
      generate(brow=3, bcol=4, prows=[0, 1, 4, 8], pcols=[3, 0, 1, 4],
               colors=[0, 1, 0, 1, 1, 1, 0, 1, 0]),
      generate(brow=0, bcol=5, prows=[4, 7], pcols=[0, 3],
               colors=[1, 1, 0, 1, 0, 1, 1, 1, 0]),
  ]
  return {"train": train, "test": test}
