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


def generate(width=None, height=None, rows=None, cols=None, idxs=None,
             brows=None, bcols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices of the sprites
    brows: a list of vertical coordinates where sprites should be placed
    bcols: a list of horizontal coordinates where sprites should be placed
  """
  if width is None:
    width, height = common.randint(8, 16), common.randint(8, 16)
    num_sprites = common.randint((width + height) // 10, (width + height) // 5)
    while True:
      lengths = [common.randint(3, 4) for _ in range(num_sprites)]
      brows = [common.randint(0, height - length) for length in lengths]
      bcols = [common.randint(0, width - length) for length in lengths]
      if not common.overlaps(brows, bcols, lengths, lengths, 1): break
    rows, cols, idxs = [], [], []
    for i in range(num_sprites):
      size = common.randint(4, 6) if lengths[i] == 3 else common.randint(6, 8)
      pixels = common.continuous_creature(size, lengths[i], lengths[i])
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([i] * len(pixels))

  grid, output = common.grid(width, height), common.grid(len(brows), len(bcols))
  for r, c, i in zip(rows, cols, idxs):
    grid[brows[i] + r][bcols[i] + c] = common.cyan()
  for i in range(len(brows)):
    output[i][i] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=16,
               rows=[0, 0, 1, 1, 2, 2, 2, 3, 0, 0, 1, 1, 1, 2, 0, 0, 1, 1, 1, 2,
                     0, 0, 1, 1],
               cols=[1, 2, 1, 2, 0, 1, 2, 1, 1, 2, 0, 1, 2, 2, 2, 3, 0, 1, 2, 2,
                     0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     3, 3, 3, 3],
               brows=[1, 6, 10, 12], bcols=[1, 4, 1, 7]),
      generate(width=12, height=12,
               rows=[0, 1, 1, 1, 2, 2, 0, 1, 1, 1, 1, 2, 2, 0, 0, 1, 1],
               cols=[2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 3, 0, 2, 0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               brows=[1, 3, 8], bcols=[1, 5, 3]),
      generate(width=12, height=8,
               rows=[0, 0, 1, 1, 1, 2, 2, 0, 1, 1, 2],
               cols=[0, 1, 0, 1, 2, 1, 2, 0, 0, 1, 0],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
               brows=[2, 3],
               bcols=[2, 8]),
  ]
  test = [
      generate(width=12, height=15,
               rows=[0, 1, 1, 2, 2, 0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 1,
                     1, 0, 0],
               cols=[1, 0, 1, 0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 1, 2, 2, 0, 1, 0, 1,
                     2, 0, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3,
                     3, 4, 4],
               brows=[1, 2, 9, 9, 13], bcols=[8, 3, 1, 8, 6]),
  ]
  return {"train": train, "test": test}
