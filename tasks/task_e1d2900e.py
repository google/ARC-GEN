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


def generate(width=None, height=None, brows=None, bcols=None, rrows=None,
             rcols=None, extra_idxs=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    brows: The rows of the blue pixels.
    bcols: The columns of the blue pixels.
    rrows: The rows of the red blocks.
    rcols: The columns of the red blocks.
    extra_idxs: Extra indices to fix a broken / ambiguous case.
  """

  def draw():
    grid, output = common.grids(width, height)
    # Draw the red blocks.
    for rrow, rcol in zip(rrows, rcols):
      common.rect(grid, 2, 2, rrow, rcol, 2)
      common.rect(output, 2, 2, rrow, rcol, 2)
    # Draw the blue pixels.
    for i, (brow, bcol) in enumerate(zip(brows, bcols)):
      if grid[brow][bcol] != 0: return None, None  # overwrites
      grid[brow][bcol] = 1
      best_dist, rows, cols = 60, [], []
      for rrow, rcol in zip(rrows, rcols):
        if extra_idxs is not None and i in extra_idxs: continue
        row, col = None, None
        if brow in [rrow, rrow + 1] and bcol < rcol: row, col = brow, rcol - 1
        if brow in [rrow, rrow + 1] and bcol > rcol: row, col = brow, rcol + 2
        if bcol in [rcol, rcol + 1] and brow < rrow: row, col = rrow - 1, bcol
        if bcol in [rcol, rcol + 1] and brow > rrow: row, col = rrow + 2, bcol
        if row is None or col is None: continue
        dist = abs(row - brow) + abs(col - bcol)
        if best_dist < dist: continue
        if best_dist > dist: best_dist, rows, cols = dist, [], []
        rows.append(row)
        cols.append(col)
      if not rows:
        if output[brow][bcol] != 0: return None, None  # overwrites
        output[brow][bcol] = 1
      elif len(rows) == 1:
        if output[rows[0]][cols[0]] != 0: return None, None  # overwrites
        if brow == rows[0] and bcol == cols[0]: return None, None  # didn't move
        output[rows[0]][cols[0]] = 1
      else:
        return None, None
    return grid, output

  if width is None:
    if common.randint(0, 1):
      width, height = 30, 30
    else:
      width, height = common.randint(10, 20), common.randint(10, 20)
    num_boxes = 2 + common.randint(0, (width + height) // 30)
    while True:
      rrows = [common.randint(1, height - 3) for _ in range(num_boxes)]
      rcols = [common.randint(1, width - 3) for _ in range(num_boxes)]
      if not common.overlaps(rrows, rcols, [4] * num_boxes, [4] * num_boxes):
        break
    while True:
      brows, bcols = [], []
      for rrow, rcol in zip(rrows, rcols):
        for row in [rrow, rrow + 1]:
          if common.randint(0, 1):
            brows.append(row)
            bcols.append(common.randint(0, rcol - 1))
          if common.randint(0, 1):
            brows.append(row)
            bcols.append(common.randint(rcol + 2, width - 1))
        for col in [rcol, rcol + 1]:
          if common.randint(0, 1):
            brows.append(common.randint(0, rrow - 1))
            bcols.append(col)
          if common.randint(0, 1):
            brows.append(common.randint(rrow + 2, height - 1))
            bcols.append(col)
      for _ in range(common.randint(1, 4)):
        brows.append(common.randint(0, height - 1))
        bcols.append(common.randint(0, width - 1))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=30, height=30,
               brows=[2, 3, 7, 7, 8, 10, 15, 18, 21, 23, 27],
               bcols=[26, 6, 1, 16, 17, 7, 11, 23, 16, 3, 24],
               rrows=[7, 17], rcols=[6, 16]),
      generate(width=30, height=30,
               brows=[0, 4, 4, 4, 4, 7, 9, 10, 10, 15, 16, 16, 23, 28],
               bcols=[18, 2, 11, 14, 24, 5, 18, 10, 26, 18, 6, 20, 13, 21],
               rrows=[3, 4, 15, 22], rcols=[5, 18, 10, 20], extra_idxs=[12]),
      generate(width=13, height=10, brows=[3, 4, 8], bcols=[5, 7, 4],
               rrows=[3, 3], rcols=[1, 10]),
  ]
  test = [
      generate(width=30, height=30,
               brows=[1, 2, 3, 6, 9, 10, 11, 13, 16, 17, 17, 17, 20, 26, 27],
               bcols=[14, 25, 5, 10, 27, 5, 18, 9, 14, 2, 13, 22, 28, 14, 1],
               rrows=[5, 16, 16, 25], rcols=[5, 9, 17, 22]),
  ]
  return {"train": train, "test": test}
