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


def generate(prows=None, pcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(17, 17)
    for r in range(4):
      for c in range(4):
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if not dr and not dc: continue
            grid[r * 4 + 2 + dr][c * 4 + 2 + dc] = 8
            output[r * 4 + 2 + dr][c * 4 + 2 + dc] = 8
    for row, col, color in zip(prows, pcols, colors):
      grid[row][col] = color
    for color in set(colors):
      rows = [r for r, hue in zip(prows, colors) if hue == color]
      cols = [c for c, hue in zip(pcols, colors) if hue == color]
      min_row, max_row = min(rows), max(rows)
      min_col, max_col = min(cols), max(cols)
      if (min_row + 3) % 4 == 0: min_row -= 1
      if (max_row + 1) % 4 == 0: max_row += 1
      if (min_col + 3) % 4 == 0: min_col -= 1
      if (max_col + 1) % 4 == 0: max_col += 1
      for r in range(min_row, max_row + 1):
        if output[r][min_col] not in [0, color]: return None, None
        if output[r][max_col] not in [0, color]: return None, None
        output[r][min_col] = output[r][max_col] = color
      for c in range(min_col, max_col + 1):
        if output[min_row][c] not in [0, color]: return None, None
        if output[max_row][c] not in [0, color]: return None, None
        output[min_row][c] = output[max_row][c] = color
      for r in range(min_row + 2, max_row, 4):
        for c in range(min_col + 2, max_col, 4):
          output[r][c] = color
    return grid, output

  if prows is None:
    hues = common.random_colors(common.randint(1, 2), exclude=[8])
    while True:
      prows, pcols, colors = [], [], []
      for hue in hues:
        wide, tall = common.randint(1, 3), common.randint(1, 3)
        left, top = common.randint(0, 3 - wide), common.randint(0, 3 - tall)
        right, bottom = left + wide, top + tall
        northwest = [4 * top, 4 * left]
        southeast = [4 * bottom, 4 * right]
        bump = common.randint(0, 2)
        if bump == 1: northwest[0] += 1
        if bump == 2: northwest[1] += 1
        bump = common.randint(0, 2)
        if bump == 1: southeast[0] -= 1
        if bump == 2: southeast[1] -= 1
        if common.randint(0, 1):
          temp = northwest[0]
          northwest[0] = southeast[0]
          southeast[0] = temp
        prows.extend([northwest[0], southeast[0]])
        pcols.extend([northwest[1], southeast[1]])
        colors.extend([hue] * 2)
        if common.randint(0, 7) == 0:  # Sometimes we include the centers.
          for i in range(top, bottom):
            for j in range(left, right):
              prows.append(4 * i + 2)
              pcols.append(4 * j + 2)
              colors.append(hue)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(prows=[1, 4, 13, 16], pcols=[4, 16, 8, 0], colors=[6, 6, 1, 1]),
      generate(prows=[0, 8], pcols=[0, 12], colors=[2, 2]),
      generate(prows=[0, 3, 8, 12], pcols=[12, 16, 1, 11], colors=[7, 7, 3, 3]),
  ]
  test = [
      generate(prows=[1, 7, 13, 14, 14, 15], pcols=[4, 12, 12, 10, 6, 4],
               colors=[4, 4, 2, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
