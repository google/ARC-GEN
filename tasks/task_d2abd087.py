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


def generate(rows=None, cols=None, idxs=None, brows=None, bcols=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    brows: a list of vertical coordinates where the sprites should be placed
    bcols: a list of horizontal coordinates where the sprites should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_sprites = common.randint(3, 6)
    # Choose dimensions for the sprites & find non-overlapping positions.
    while True:
      wides = [common.randint(2, 4) for _ in range(num_sprites)]
      talls = [6 - wide for wide in wides]
      brows = [common.randint(0, size - tall) for tall in talls]
      bcols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    # Finally, choose the sprite contents (leaning towards sixes).
    counts = [common.randint(4, 8) for _ in range(num_sprites)]
    counts = [count if common.randint(0, 2) else 6 for count in counts]
    rows, cols, idxs = [], [], []
    for idx in range(num_sprites):
      pixels = common.continuous_creature(counts[idx], wides[idx], talls[idx])
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))

  grid, output = common.grids(size, size)
  for row, col, idx in zip(rows, cols, idxs):
    grid[row + brows[idx]][col + bcols[idx]] = common.gray()
    sprite_size = len([i for i in idxs if i == idx])
    color = common.red() if sprite_size == 6 else common.blue()
    output[row + brows[idx]][col + bcols[idx]] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 2, 0, 0, 1, 1, 1],
               cols=[0, 1, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 1, 0, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
               brows=[2, 5, 7], bcols=[2, 5, 1]),
      generate(rows=[0, 1, 1, 1, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1,
                     1, 2, 2, 0, 0, 1, 1],
               cols=[2, 0, 1, 2, 2, 1, 2, 0, 1, 2, 3, 0, 1, 2, 3, 0, 0, 0, 1, 0,
                     1, 0, 1, 0, 1, 0, 1],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4,
                     4, 4, 4, 5, 5, 5, 5],
               brows=[0, 1, 4, 4, 6, 7],
               bcols=[6, 0, 2, 8, 5, 1]),
      generate(rows=[0, 0, 0, 1, 1, 2, 3, 0, 0, 0, 1, 2, 3, 0, 0, 1, 1, 0, 0, 1,
                     1, 2, 2, 0, 1, 2, 0, 0, 0, 1, 1, 1, 1, 2, 2],
               cols=[0, 1, 2, 1, 2, 2, 2, 0, 1, 2, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1,
                     2, 1, 2, 0, 0, 0, 0, 1, 1, 0, 1, 2, 3, 1, 2],
               idxs=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3,
                     3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6],
               brows=[0, 0, 1, 4, 4, 5, 7],
               bcols=[0, 7, 4, 4, 9, 1, 1]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1,
                     0, 1, 2, 3, 0, 0, 0, 0, 0],
               cols=[1, 2, 1, 2, 0, 1, 2, 3, 1, 2, 1, 2, 0, 1, 0, 1, 0, 1, 2, 3,
                     0, 0, 0, 0, 0, 1, 2, 3, 4],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     3, 3, 3, 3, 4, 4, 4, 4, 4],
               brows=[0, 0, 4, 4, 8],
               bcols=[0, 5, 1, 7, 1]),
  ]
  return {"train": train, "test": test}
