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


def generate(size=None, brows=None, bcols=None, grows=None, gcols=None, dists=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  def draw():
    grid, output = common.grids(size, size, 7)
    def put(g, r, c, color):
      if g[r][c] != 7: return False
      g[r][c] = color
      return True
    for brow, bcol, grow, gcol, dist in zip(brows, bcols, grows, gcols, dists):
      # Draw the green center.
      output[brow][bcol] = grid[brow][bcol] = 3
      # Draw the black sides.
      row, col, angle = brow, bcol, -1
      if brow in [0, size - 1]:
        if common.get_pixel(grid, brow, bcol - 2) not in [-1, 7]: return None, None
        if common.get_pixel(grid, brow, bcol + 2) not in [-1, 7]: return None, None
        if not put(grid, brow, bcol - 1, 0): return None, None
        if not put(grid, brow, bcol + 1, 0): return None, None
        if not put(output, brow, bcol - 1, 0): return None, None
        if not put(output, brow, bcol + 1, 0): return None, None
        row += -1 if brow else 1
        angle = 1 if gcol > bcol else 3
      if bcol in [0, size - 1]:
        if common.get_pixel(grid, brow - 2, bcol) not in [-1, 7]: return None, None
        if common.get_pixel(grid, brow + 2, bcol) not in [-1, 7]: return None, None
        if not put(grid, brow - 1, bcol, 0): return None, None
        if not put(grid, brow + 1, bcol, 0): return None, None
        if not put(output, brow - 1, bcol, 0): return None, None
        if not put(output, brow + 1, bcol, 0): return None, None
        col += -1 if bcol else 1
        angle = 2 if grow > brow else 0
      # Place the greys.
      if not put(grid, grow, gcol, 5): return None, None
      if not put(output, grow if dist else row, gcol if dist else col, 5): return None, None
      # If needed, shift the greens.
      while bcol in [0, size - 1] and abs(gcol - col) > 1:
        if not put(grid, row, col, 3): return None, None
        if dist:
          if not put(output, row, col, 3): return None, None
        col += -1 if bcol else 1
      while brow in [0, size - 1] and abs(grow - row) > 1:
        if not put(grid, row, col, 3): return None, None
        if dist:
          if not put(output, row, col, 3): return None, None
        row += -1 if brow else 1
      # Place the remaining greens -- draw using blue if meant to vanish.
      while True:
        if brow in [0, size - 1]:
          color = 3 if abs(gcol - col) >= dist else 1
          if not put(grid, row, col, color): return None, None
          if dist:
            if not put(output, row, col, color): return None, None
        if bcol in [0, size - 1]:
          color = 3 if abs(grow - row) >= dist else 1
          if not put(grid, row, col, color): return None, None
          if dist:
            if not put(output, row, col, color): return None, None
        if row == grow or col == gcol: break
        if angle == 0: row -= 1
        if angle == 1: col += 1
        if angle == 2: row += 1
        if angle == 3: col -= 1
    # Convert the blues back to oranges.
    grid = [[color if color != 1 else 7 for color in row] for row in grid]
    output = [[color if color != 1 else 7 for color in row] for row in output]
    return grid, output

  if size is None:
    size = common.randint(8, 16)
    markers = min(4, max(1, size - 9))
    while True:
      bad = False
      seen = set()
      brows, bcols, grows, gcols, dists = [], [], [], [], []
      for _ in range(markers):
        brow, bcol, grow, gcol, dist = -1, -1, -1, -1, 0
        side = common.randint(0, 3)
        if side == 0: brow, bcol, grow, gcol = 0, common.randint(1, size - 2), common.choice([0, 2, 3]), common.choice([0, size - 1])
        if side == 1: brow, bcol, grow, gcol = common.randint(1, size - 2), 0, common.choice([0, size - 1]), common.choice([0, 2, 3])
        if side == 2: brow, bcol, grow, gcol = size - 1, common.randint(1, size - 2), common.choice([size - 1, size - 3, size - 4]), common.choice([0, size - 1])
        if side == 3: brow, bcol, grow, gcol = common.randint(1, size - 2), size - 1, common.choice([0, size - 1]), common.choice([size - 1, size - 3, size - 4])
        if common.randint(0, 1): dist = common.randint(1, abs(gcol - bcol) if side in [0, 2] else abs(grow - brow))
        entry = (side, gcol if side in [0, 2] else grow)
        if entry in seen: bad = True
        seen.add(entry)
        brows.append(brow)
        bcols.append(bcol)
        grows.append(grow)
        gcols.append(gcol)
        dists.append(dist)
      if bad: continue  # There are two markers going in the same direction.
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=12, brows=[0, 6, 8], bcols=[1, 0, 11], grows=[2, 11, 11], gcols=[11, 2, 9], dists=[0, 1, 0]),
      generate(size=9, brows=[2], bcols=[0], grows=[8], gcols=[3], dists=[0]),
      generate(size=13, brows=[0, 5, 11, 12], bcols=[4, 0, 0, 6], grows=[2, 0, 12, 10], gcols=[12, 0, 2, 12], dists=[4, 0, 0, 2]),
  ]
  test = [
      generate(size=14, brows=[0, 6, 11, 13], bcols=[11, 0, 0, 10], grows=[2, 0, 13, 13], gcols=[13, 2, 2, 13], dists=[0, 0, 1, 2]),
  ]
  return {"train": train, "test": test}
