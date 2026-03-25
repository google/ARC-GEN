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


def generate(cdir=None, brow=None, bcol=None, lcolors=None, rcolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    cdir: The direction.
    brow: The row of the double block.
    bcol: The column of the double block.
    lcolors: The colors of the left sprite.
    rcolors: The colors of the right sprite.
  """

  if cdir is None:
    cdir = common.randint(0, 1)
    brow, bcol = common.randint(0, 3), common.randint(1, 11)
    rcolor = common.random_color(exclude=[1, 2, 5])
    lpixels = common.diagonally_connected_sprite()
    rpixels = common.diagonally_connected_sprite()
    rcolors, lcolors = [], []
    for r in range(3):
      for c in range(3):
        lcolors.append(1 if (r, c) in lpixels else 0)
        rcolors.append(rcolor if (r, c) in rpixels else 0)
    lcolors = "".join(str(c) for c in lcolors)
    rcolors = "".join(str(c) for c in rcolors)

  grid, output = common.grid(15, 15), common.grid(15, 9)
  for c in range(15):
    grid[5][c] = 5
  grid[1][7] = grid[2][7] = grid[3][7] = 2
  grid[3 - 2 * cdir][6] = grid[3 - 2 * cdir][8] = 2
  for r in range(3):
    for c in range(3):
      grid[r + 1][c + 2] = int(lcolors[3 * r + c])
      grid[r + 1][c + 10] = int(rcolors[3 * r + c])
      grid[6 + brow + 3 * (1 - cdir) + r][bcol + c] = int(lcolors[3 * r + c])
      output[brow + 3 * (1 - cdir) + r][bcol + c] = int(lcolors[3 * r + c])
      output[brow + 3 * cdir + r][bcol + c] = int(rcolors[3 * r + c])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cdir=1, brow=3, bcol=8, lcolors="110010011", rcolors="070707070"),
      generate(cdir=0, brow=0, bcol=5, lcolors="101010101", rcolors="444444040"),
      generate(cdir=1, brow=1, bcol=6, lcolors="010111010", rcolors="666606066"),
      generate(cdir=0, brow=2, bcol=5, lcolors="111101111", rcolors="030333030"),
  ]
  test = [
      generate(cdir=1, brow=3, bcol=1, lcolors="100110111", rcolors="333303333"),
      generate(cdir=0, brow=2, bcol=1, lcolors="110011110", rcolors="800880088"),
  ]
  return {"train": train, "test": test}
