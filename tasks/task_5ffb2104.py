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


def generate(width=None, height=None, colors=None, brows=None, bcols=None,
             prows=None, pcols=None, pidxs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    colors: The colors of the shapes.
    brows: The row indices of the top of the shapes.
    bcols: The column indices of the left of the shapes.
    prows: The row indices of the pixels in the shapes.
    pcols: The column indices of the pixels in the shapes.
    pidxs: The indices of the shapes that the pixels belong to.
  """

  if width is None:
    width, height = common.randint(6, 15), common.randint(6, 15)
    num_shapes = common.randint(5, (width + height) // 2)
    while True:
      wides = [common.randint(1, 2) for _ in range(num_shapes)]
      talls = [common.randint(1, 3) for _ in range(num_shapes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      # Our solver expects the shapes to be sorted by row.
      wides, talls, brows, bcols = zip(*sorted(zip(wides, talls, brows, bcols), key=lambda x: x[2]))
      if common.overlaps(brows, bcols, wides, talls): continue
      mrows = [common.randint(0, tall - 1) for tall in talls]
      mcols = [common.randint(0, wide - 1) for wide in wides]
      mdels = [common.randint(0, 1) for _ in range(num_shapes)]
      colors = [common.random_color() for _ in range(num_shapes)]
      grid, ids = common.grid(width, height), common.grid(width, height, -1)
      prows, pcols, pidxs = [], [], []
      for idx, (wide, tall, mrow, mcol, mdel, color) in enumerate(zip(wides, talls, mrows, mcols, mdels, colors)):
        for row in range(tall):
          for col in range(wide):
            if tall > 1 and wide > 1 and mdel and row == mrow and col == mcol:
              continue
            prows.append(row)
            pcols.append(col)
            pidxs.append(idx)
            grid[brows[idx] + row][bcols[idx] + col] = color
            ids[brows[idx] + row][bcols[idx] + col] = idx
      # Check that shapes of the same color are not touching.
      good = True
      for row in range(height):
        for col in range(width):
          if grid[row][col] == 0: continue
          for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if common.get_pixel(grid, nr, nc) != grid[row][col]: continue
            if common.get_pixel(ids, nr, nc) != ids[row][col]: good = False
      if good: break

  grid, output = common.grids(width, height)
  for idx, (brow, bcol, color) in enumerate(zip(brows, bcols, colors)):
    rows = [prow for prow, pidx in zip(prows, pidxs) if pidx == idx]
    cols = [pcol for pcol, pidx in zip(pcols, pidxs) if pidx == idx]
    for row, col in zip(rows, cols):
      grid[brow + row][bcol + col] = color
    r = brow
    while r:
      clear = True
      for row, col in zip(rows, cols):
        if output[r + row - 1][bcol + col]: clear = False
      if not clear: break
      r -= 1
    for row, col in zip(rows, cols):
      output[r + row][bcol + col] = color
  grid, output = common.transpose(grid), common.transpose(output)
  grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6, colors=[2, 2, 6, 3, 8], brows=[0, 2, 3, 4, 4],
               bcols=[3, 1, 5, 0, 3],
               prows=[0, 0, 1, 1, 0, 0, 0, 1, 2, 0, 0, 0],
               pcols=[0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
               pidxs=[0, 0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4]),
      generate(width=10, height=13, colors=[5, 8, 3, 2, 6],
               brows=[4, 6, 7, 9, 10], bcols=[2, 7, 4, 1, 7],
               prows=[0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
               pcols=[0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
               pidxs=[0, 0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 4, 4]),
      generate(width=6, height=6, colors=[3, 2, 8, 6, 8], brows=[1, 3, 3, 5, 5],
               bcols=[3, 0, 3, 1, 5],
               prows=[0, 0, 0, 0, 1, 0, 0, 0, 0],
               pcols=[0, 1, 0, 1, 0, 0, 0, 1, 0],
               pidxs=[0, 0, 1, 1, 1, 2, 3, 3, 4]),
  ]
  test = [
      generate(width=10, height=10, colors=[2, 4, 6, 8, 3, 5, 8, 8, 8, 2],
               brows=[3, 3, 3, 4, 5, 5, 6, 6, 8, 9],
               bcols=[0, 3, 6, 9, 2, 8, 0, 5, 7, 2],
               prows=[0, 1, 1, 0, 0, 1, 2, 2, 0, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 0, 0],
               pcols=[1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               pidxs=[0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 3, 4, 4, 4, 5, 5, 6, 7, 8, 9, 9]),
  ]
  return {"train": train, "test": test}
