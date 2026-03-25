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


def generate(rows=None, cols=None, idxs=None, bluerows=None, bluecols=None,
             grayrows=None, graycols=None, width=15, height=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the sprite list
    bluerows: a list of vertical coordinates where blue boxes should be placed
    bluecols: a list of horizontal coordinates where blue boxes should be placed
    grayrows: a list of vertical coordinates where gray boxes should be placed
    graycols: a list of horizontal coordinates where gray boxes should be placed
    width: the width of the grid
    height: the height of the grid
  """

  if rows is None:
    num_shapes = max(3, common.randint(0, 4))
    while True:
      # Choose the dimensions and contents of the creatures.
      wides = [common.randint(1, 4) for _ in range(num_shapes)]
      talls = [common.randint(2, 4) for _ in range(num_shapes)]
      sizes = [common.randint(max(2, wide * tall // 2), wide * tall)
               for wide, tall in zip(wides, talls)]
      creatures = [common.continuous_creature(size, wide, tall)
                   for size, wide, tall in zip(sizes, wides, talls)]
      # Choose the blue locations of the creatures.
      bluerows = [common.randint(1, 2) for _ in range(num_shapes)]
      bluecols = [common.randint(0, width - wide) for wide in wides]
      # Extract the rows and columns, along with the creatures actual heights.
      rows, cols, idxs, max_rows = [], [], [], []
      for idx, creature in enumerate(creatures):
        rows.extend(p[0] for p in creature)
        cols.extend(p[1] for p in creature)
        idxs.extend([idx] * len(creature))
        max_rows.append(max(p[0] for p in creature))
      grayrows = [height - max_row - 1 for max_row in max_rows]
      graycols = [common.randint(0, width - wide) for wide in wides]
      # Make sure the creatures don't overlap.
      if common.overlaps(bluerows, bluecols, wides, talls, 1): continue
      if common.overlaps(grayrows, graycols, wides, talls, 1): continue
      # Draw the shapes, and make sure the red bar remains convex.
      illegal = False
      grid = common.grid(width, height)
      for r in range(3):
        for c in range(width):
          grid[r][c] = common.red()
      for r, c, idx in zip(rows, cols, idxs):
        grid[r + bluerows[idx]][c + bluecols[idx]] = common.black()
      for r in range(1, height):
        for c in range(width):
          if grid[r][c] == common.red() and grid[r - 1][c] == common.black():
            illegal = True
      # Make sure the footprints are unique (so we can match them exactly).
      footprints = []
      for creature in creatures:
        one_deep = [p for p in creature if p[0] < 1]
        two_deep = [p for p in creature if p[0] < 2]
        one_deep.sort()
        two_deep.sort()
        footprints.append([one_deep, two_deep])
      for i, creature in enumerate(creatures):
        footprint = [p for p in creature if p[0] < 3 - bluerows[i]]
        footprint.sort()
        for j in range(len(creatures)):
          if i != j and footprint in footprints[j]: illegal = True
      if not illegal: break

  grid, output = common.grids(width, height)
  for r in range(3):
    for c in range(width):
      output[r][c] = grid[r][c] = common.red()
  for r, c, idx in zip(rows, cols, idxs):
    grid[r + grayrows[idx]][c + graycols[idx]] = common.gray()
    grid[r + bluerows[idx]][c + bluecols[idx]] = common.black()
    output[r + bluerows[idx]][c + bluecols[idx]] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 1, 2, 2, 2, 0, 0, 0, 1, 1, 1, 0, 1, 2, 3],
               cols=[0, 0, 1, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 0, 0],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2],
               bluerows=[1, 2, 1],
               bluecols=[1, 6, 14],
               grayrows=[7, 8, 6],
               graycols=[6, 1, 13]),
      generate(rows=[0, 0, 1, 1, 1, 0, 1, 2, 0, 1, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2,
                     3, 3],
               cols=[1, 2, 0, 1, 2, 0, 0, 0, 1, 0, 1, 2, 1, 2, 1, 2, 0, 1, 2, 3,
                     1, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
                     3, 3],
               bluerows=[2, 1, 1, 1],
               bluecols=[0, 4, 7, 10],
               grayrows=[8, 7, 8, 6],
               graycols=[12, 10, 6, 0]),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2, 2, 2, 2, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 0,
                     1, 1, 2, 3, 3],
               cols=[0, 0, 1, 2, 0, 1, 2, 3, 0, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0,
                     0, 1, 0, 0, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                     2, 2, 2, 2, 2],
               bluerows=[1, 1, 1],
               bluecols=[11, 6, 1],
               grayrows=[7, 6, 6],
               graycols=[1, 11, 7]),
  ]
  return {"train": train, "test": test}
