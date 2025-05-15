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


def generate(height=None, rows=None, cols=None, megarows=None, megacols=None,
             width=10, colors=(1, 2, 4)):
  """Returns input and output grids according to the given parameters.

  Args:
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    megarows: a list of vertical coordinates where clusters should be placed
    megacols: a list of horizontal coordinates where clusters should be placed
    width: the width of the input grid
    colors: digits representing the colors to be used
    
  """
  if height is None:
    height = 5 * common.randint(1, 2)
    miniwidth, miniheight = common.randint(2, 3), common.randint(2, 3)
    num = common.randint(miniwidth * miniheight // 2, miniwidth * miniheight)
    while True:
      pixels = common.sample(common.all_pixels(miniwidth, miniheight), num)
      if common.diagonally_connected(pixels): break
    rows, cols = zip(*pixels)
    megarows = [common.randint(0, height - miniheight - 1) for _ in colors]
    megacols = [0, miniwidth, 2 * miniwidth]
    for i in range(common.randint(0, 3), len(colors)):
      megacols[i] += 1  # Shift some subset toward the right
    megacols = common.shuffle(megacols)

  grid, output = common.grids(width, height)
  for mr, mc, color in zip(megarows, megacols, colors):
    for r, c in zip(rows, cols):
      output[megarows[0] + r][mc + c] = grid[mr + r][mc + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(height=5, rows=[0, 0, 1, 1], cols=[0, 1, 0, 1],
               megarows=[1, 0, 2], megacols=[7, 1, 4]),
      generate(height=10, rows=[0, 0, 0, 1, 1, 1], cols=[0, 1, 2, 0, 1, 2],
               megarows=[5, 2, 0], megacols=[4, 1, 7]),
      generate(height=5, rows=[0, 1], cols=[0, 0], megarows=[2, 1, 3],
               megacols=[1, 3, 6]),
  ]
  test = [
      generate(height=10, rows=[0, 0, 1, 1, 2], cols=[1, 2, 1, 2, 0],
               megarows=[2, 0, 5], megacols=[0, 7, 3]),
  ]
  return {"train": train, "test": test}
