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


def generate(brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the input grid.
  """

  def draw():
    if common.overlaps(brows, bcols, [4] * 4, [4] * 4): return None, None
    grid, output = common.grids(19, 19)
    for i, color in enumerate(colors):
      output[i // 19][i % 19] = grid[i // 19][i % 19] = color
    cells = []
    for i, (brow, bcol) in enumerate(zip(brows, bcols)):
      # First, draw the output box.
      actual_red = 0
      for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
          if grid[brow + dr][bcol + dc] == 2:
            actual_red += 1
            cells.append((i, brow + dr, bcol + dc))
            continue
          output[brow + dr][bcol + dc] = 7 if dr or dc else 4
      if actual_red < 1: return None, None
      if actual_red > 6: return None, None
      # Second, check that there's a unique position for the center.
      for dbr in [-2, -1, 0, 1, 2]:
        for dbc in [-2, -1, 0, 1, 2]:
          if dbr == 0 and dbc == 0: continue  # It's the actual center.
          rr, cc = brow + dbr, bcol + dbc
          if rr < 1 or rr >= 18 or cc < 1 or cc >= 18: continue  # Out of bounds
          if grid[rr][cc] == 2: continue  # Center can't be red
          good, num_red = True, 0
          for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
              if grid[rr + dr][cc + dc] == 2: num_red += 1
              if grid[rr + dr][cc + dc] == 0: good = False
          if good and num_red == actual_red: return None, None  # Can't be good!
    # Finally, let's make sure that red cells from different boxes are far away.
    for (i, r1, c1) in cells:
      for (j, r2, c2) in cells:
        if i != j and abs(r1 - r2) <= 3 and abs(c1 - c2) <= 3: return None, None
    return grid, output

  if brows is None:
    while True:
      brows = [common.randint(1, 17) for _ in range(4)]
      bcols = [common.randint(1, 17) for _ in range(4)]
      colors = common.grid(19, 19)
      for row in range(19):
        for col in range(19):
          if common.randint(0, 1): colors[row][col] = 5
      for brow, bcol in zip(brows, bcols):
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
              colors[brow + dr][bcol + dc] = 5
            else:
              colors[brow + dr][bcol + dc] = 5 if common.randint(0, 2) else 2
      colors = common.flatten(colors)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brows=[2, 4, 10, 15], bcols=[12, 3, 17, 5],
               colors=[5, 5, 0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 5,
                       0, 0, 0, 5, 5, 5, 0, 5, 5, 0, 5, 2, 2, 5, 5, 5, 0, 0, 0,
                       0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 5, 2, 5, 5, 0, 5, 0, 0, 0,
                       5, 0, 5, 2, 2, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5,
                       0, 5, 5, 5, 2, 5, 0, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5, 0, 5,
                       0, 0, 2, 2, 2, 5, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 0, 0, 5,
                       0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 0,
                       5, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 5, 0, 5,
                       0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0,
                       0, 5, 5, 0, 5, 0, 5, 5, 5, 0, 5, 0, 0, 0, 0, 0, 2, 2, 5,
                       0, 5, 0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5,
                       5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 2,
                       5, 0, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5,
                       0, 5, 0, 5, 0, 0, 0, 0, 5, 0, 5, 5, 0, 5, 0, 0, 5, 5, 5,
                       0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0,
                       0, 5, 5, 5, 2, 5, 2, 5, 5, 0, 0, 5, 0, 0, 0, 5, 5, 5, 0,
                       5, 5, 5, 0, 2, 2, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 5, 5, 0,
                       0, 5, 0, 0, 5, 0, 0, 5, 0, 5, 0, 5, 0, 5, 5, 5, 0, 5, 0,
                       5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5]),
      generate(brows=[6, 10, 12, 14], bcols=[5, 11, 3, 14],
               colors=[0, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 5, 5, 5, 0, 0,
                       0, 5, 0, 5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5,
                       5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 5, 5, 5, 5, 0,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 0, 0, 5, 5, 0, 0,
                       5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 5, 5,
                       0, 5, 0, 5, 2, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       5, 5, 5, 5, 5, 2, 5, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5,
                       0, 0, 5, 0, 5, 5, 0, 0, 5, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5,
                       0, 5, 5, 5, 5, 5, 5, 0, 5, 0, 2, 5, 5, 0, 0, 5, 0, 5, 5,
                       0, 5, 5, 0, 0, 0, 0, 5, 5, 0, 2, 5, 5, 0, 5, 5, 5, 5, 0,
                       5, 5, 2, 2, 2, 5, 0, 0, 0, 0, 5, 2, 2, 5, 5, 5, 0, 0, 5,
                       5, 0, 5, 5, 2, 5, 5, 5, 0, 0, 0, 5, 5, 0, 5, 5, 5, 0, 5,
                       0, 0, 2, 5, 2, 5, 0, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 5,
                       0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0,
                       5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 2, 5, 0, 5, 5,
                       5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 5,
                       5, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                       0, 5, 5, 5, 0, 5, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 0, 5, 0]),
      generate(brows=[1, 2, 11, 11], bcols=[3, 15, 3, 12],
               colors=[0, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                       5, 5, 2, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 0, 2, 2, 5, 5, 0,
                       5, 5, 5, 2, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 2, 5, 2, 5, 5,
                       0, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, 0, 5, 5, 2, 5, 0, 0,
                       0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5,
                       5, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 0, 5, 5, 5,
                       5, 5, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5, 0, 0, 0, 0,
                       0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5,
                       5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5,
                       5, 5, 5, 5, 0, 0, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5,
                       0, 5, 2, 2, 5, 5, 0, 0, 5, 0, 0, 5, 2, 5, 5, 5, 0, 5, 5,
                       5, 5, 5, 5, 5, 0, 0, 5, 0, 0, 0, 5, 5, 2, 5, 0, 0, 0, 5,
                       0, 5, 5, 5, 2, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5, 0,
                       5, 0, 0, 5, 5, 0, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 0, 0, 5, 5, 5, 0,
                       5, 5, 5, 5, 0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 5, 5, 0,
                       5, 0, 5, 0, 5, 5, 0, 5, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5, 5,
                       5, 0, 5, 0, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0, 5, 5, 5]),
  ]
  test = [
      generate(brows=[3, 7, 13, 14], bcols=[14, 1, 17, 5],
               colors=[5, 0, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0,
                       0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 0, 5,
                       0, 0, 5, 0, 0, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5,
                       0, 5, 5, 0, 5, 0, 0, 0, 5, 5, 5, 0, 5, 2, 5, 5, 5, 0, 5,
                       5, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 0, 2, 2, 5, 5, 0, 0,
                       5, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 0, 5, 0, 5, 0, 0, 5, 5,
                       5, 2, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5, 5, 0, 5, 0, 5, 5, 5,
                       5, 5, 2, 5, 5, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, 0, 5, 5,
                       5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 5, 0, 0,
                       5, 5, 0, 5, 5, 0, 5, 0, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 5,
                       5, 5, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5,
                       5, 5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 5,
                       5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 2, 5,
                       5, 5, 5, 5, 5, 2, 5, 5, 5, 5, 0, 5, 0, 0, 5, 0, 2, 5, 5,
                       5, 0, 5, 0, 5, 5, 2, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5,
                       5, 5, 5, 5, 5, 2, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5,
                       0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 0, 5, 5, 5, 0, 5,
                       5, 5, 0, 5, 0, 0, 0, 0, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 5,
                       5, 5, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 0, 5, 0, 0, 5, 5, 5]),
  ]
  return {"train": train, "test": test}
