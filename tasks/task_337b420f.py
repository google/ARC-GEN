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


def generate(colors=None, extra_color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    extra_color: The color of the extra color for the broken / ambiguous case.
  """

  def draw():
    grid, output = common.grid(17, 5), common.grid(5, 5, 8)
    for i, color in enumerate(colors):
      grid[i // 17][i % 17] = color
    ids = common.grid(17, 5, -1)
    idx = 0
    # Determine the IDs of the connected components.
    for row in range(5):
      for col in range(17):
        if grid[row][col] in [0, 8] or ids[row][col] != -1: continue
        ids[row][col] = idx
        queue = [(row, col)]
        while queue:
          r, c = queue.pop(0)
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if common.get_pixel(grid, nr, nc) != grid[row][col]: continue
            if ids[nr][nc] != -1: continue
            ids[nr][nc] = idx
            queue.append((nr, nc))
        idx += 1
    if idx != 6: return None, None  # There should be 6 connected components.
    for left in [0, 6, 12]:
      cells = []
      for row in range(5):
        for col in range(5):
          if ids[row][left + col] != -1: cells.append(ids[row][left + col])
      idxs = list(set(cells))
      if -1 in idxs: idxs.remove(-1)
      counts = sorted([(cells.count(idx), idx) for idx in idxs], reverse=True)
      if len(counts) != 2: return None, None
      if counts[0][0] == counts[1][0]: return None, None
      for row in range(5):
        for col in range(5):
          if ids[row][left + col] != counts[0][1]: continue
          offset = -1 if extra_color == grid[row][left + col] else 0
          output[row][col + offset] = grid[row][left + col]
    return grid, output

  if colors is None:
    subset = common.random_colors(3, exclude=[8])
    while True:
      union = common.grid(5, 5, -1)
      for _ in range(10):
        idx = common.randint(0, 2)
        length = common.randint(1, 5)
        pos = common.randint(0, 5 - length)
        val = common.randint(0, 4)
        angle = common.randint(0, 1)
        for i in range(length):
          if angle == 0:
            union[val][pos + i] = idx
          else:
            union[pos + i][val] = idx
      grid = common.grid(17, 5)
      common.rect(grid, 5, 5, 0, 0, 8)
      common.rect(grid, 5, 5, 0, 6, 8)
      common.rect(grid, 5, 5, 0, 12, 8)
      for row in range(5):
        for col in range(5):
          if union[row][col] == -1: continue
          left = 6 * union[row][col]
          grid[row][left + col] = subset[union[row][col]]
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 4, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 6,
                       8, 4, 4, 8, 8, 0, 5, 8, 8, 8, 5, 0, 8, 8, 8, 8, 8,
                       8, 8, 4, 4, 8, 0, 5, 5, 8, 8, 8, 0, 8, 8, 8, 8, 8,
                       4, 8, 8, 4, 4, 0, 8, 8, 8, 8, 8, 0, 8, 8, 6, 6, 8,
                       4, 4, 8, 8, 4, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 6, 6],
               extra_color=6),
      generate(colors=[8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 1, 1, 1, 8, 1,
                       2, 2, 2, 8, 2, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 0, 6, 6, 6, 8, 6, 0, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 0, 6, 6, 6, 8, 6, 0, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8]),
      generate(colors=[8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 7, 0, 8, 8, 8, 4, 4,
                       8, 8, 8, 8, 8, 0, 8, 7, 7, 7, 8, 0, 8, 8, 8, 8, 4,
                       6, 8, 8, 8, 6, 0, 8, 7, 8, 7, 8, 0, 8, 8, 4, 8, 8,
                       6, 8, 8, 8, 8, 0, 8, 7, 7, 7, 8, 0, 8, 8, 8, 8, 8,
                       6, 6, 6, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8]),
      generate(colors=[8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 9, 8, 8, 8, 8,
                       8, 1, 8, 8, 8, 0, 8, 8, 5, 5, 8, 0, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 9, 9, 8, 8,
                       8, 8, 8, 8, 1, 0, 8, 8, 8, 5, 8, 0, 8, 9, 8, 8, 8,
                       8, 8, 1, 1, 1, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8]),
  ]
  test = [
      generate(colors=[6, 6, 6, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 4, 4,
                       8, 6, 8, 8, 8, 0, 1, 8, 1, 8, 8, 0, 8, 8, 8, 4, 4,
                       8, 8, 8, 8, 8, 0, 1, 1, 1, 8, 8, 0, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 4, 4, 4, 4, 4,
                       8, 8, 8, 6, 6, 0, 8, 1, 8, 8, 8, 0, 8, 8, 8, 8, 8]),
      generate(colors=[8, 8, 8, 5, 5, 0, 8, 8, 2, 2, 8, 0, 3, 3, 8, 8, 8,
                       8, 8, 8, 8, 8, 0, 8, 8, 8, 2, 2, 0, 3, 3, 3, 8, 8,
                       8, 8, 8, 8, 8, 0, 2, 8, 8, 8, 8, 0, 8, 3, 8, 8, 8,
                       5, 5, 5, 8, 8, 0, 2, 8, 8, 8, 8, 0, 8, 8, 8, 3, 3,
                       5, 5, 5, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 3, 3]),
  ]
  return {"train": train, "test": test}
