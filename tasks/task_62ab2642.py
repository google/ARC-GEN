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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grids.
    height: The height of the grids.
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(width, height)
    ids = common.grid(width, height, -1)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    idx = 0
    while True:
      r, c = None, None
      for row in range(height):
        for col in range(width):
          if grid[row][col] == 0 and ids[row][col] == -1: r, c = row, col
      if r is None: break
      ids[r][c] = idx
      queue = [(r, c)]
      while queue:
        row, col = queue.pop()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
          nr, nc = row + dr, col + dc
          if nr < 0 or nr >= height or nc < 0 or nc >= width: continue
          if grid[nr][nc] == 0 and ids[nr][nc] == -1:
            ids[nr][nc] = idx
            queue.append((nr, nc))
      idx += 1
    flattened = common.flatten(ids)
    subset = list(set(flattened))
    subset.remove(-1)
    counts = [flattened.count(x) for x in subset]
    mins = [idx for idx, count in zip(subset, counts) if count == min(counts)]
    maxs = [idx for idx, count in zip(subset, counts) if count == max(counts)]
    if len(mins) != 1 or len(maxs) != 1: return None, None
    for row in range(height):
      for col in range(width):
        if ids[row][col] in mins: output[row][col] = 7
        if ids[row][col] in maxs: output[row][col] = 8
    return grid, output

  if width is None:
    width, height = common.randint(5, 15), common.randint(5, 15)
    while True:  # Keep going until we have clear "min" and "max" sections.
      grid = common.grid(width, height)
      r, c = common.randint(1, height // 2), common.randint(1, width // 2)
      for i in range(r + 1):
        grid[i][c] = 5
      for i in range(c + 1):
        grid[r][i] = 5
      while common.flatten(grid).count(5) * 3 < width * height:
        # Choose some grey cell somewhere in the grid.
        candidates = []
        for row in range(height):
          for col in range(width):
            if grid[row][col] == 5: candidates.append((row, col))
        # We're going to start drawing random lines until we hit something.
        # If we leave the boundary, we're good -- if we hit a grey, we're bad.
        r, c = common.choice(candidates)
        done, good = False, False
        while not done:
          if common.randint(0, 1):
            rdir, cdir = 0, 2 * common.randint(0, 1) - 1
          else:
            rdir, cdir = 2 * common.randint(0, 1) - 1, 0
          for _ in range(common.randint(3, 4)):
            r, c = r + rdir, c + cdir
            if r < 0 or r >= height or c < 0 or c >= width:
              good, done = True, True
              break
            if grid[r][c] in [-1, 5]:
              done = True
              break
            grid[r][c] = -1
        # We don't allow any "squares of grey" or "touching corners".
        for row in range(height - 1):
          for col in range(width - 1):
            a = grid[row][col]
            b = grid[row][col + 1]
            c = grid[row + 1][col]
            d = grid[row + 1][col + 1]
            if a in [-1, 5] and b in [-1, 5] and c in [-1, 5] and d in [-1, 5]:
              good = False
            if a in [-1, 5] and b in [0] and c in [0] and d in [-1, 5]:
              good = False
            if a in [0] and b in [-1, 5] and c in [-1, 5] and d in [0]:
              good = False
        for row in range(height):
          for col in range(width):
            if grid[row][col] == -1: grid[row][col] = 5 if good else 0
      if common.randint(0, 1): grid = common.flip(grid)
      if common.randint(0, 1): grid = common.flop(grid)
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=10, colors=[0, 0, 5, 0, 0, 5, 0, 0, 0,
                                           0, 0, 5, 5, 5, 5, 0, 0, 0,
                                           5, 5, 5, 0, 0, 0, 0, 0, 0,
                                           0, 5, 0, 0, 0, 0, 0, 0, 0,
                                           0, 5, 0, 0, 0, 5, 5, 5, 5,
                                           0, 5, 5, 5, 5, 5, 0, 0, 0,
                                           5, 5, 0, 0, 0, 5, 5, 5, 5,
                                           0, 0, 0, 0, 0, 5, 0, 0, 0,
                                           5, 5, 5, 5, 5, 5, 0, 0, 0,
                                           0, 0, 0, 0, 0, 5, 0, 0, 0]),
      generate(width=5, height=15, colors=[5, 0, 0, 5, 0,
                                           5, 0, 0, 5, 0,
                                           5, 0, 5, 5, 5,
                                           5, 5, 5, 0, 0,
                                           0, 0, 5, 0, 0,
                                           0, 0, 5, 5, 5,
                                           0, 0, 0, 5, 0,
                                           5, 5, 5, 5, 0,
                                           0, 5, 0, 0, 0,
                                           0, 5, 0, 0, 0,
                                           0, 5, 5, 5, 0,
                                           0, 0, 0, 5, 0,
                                           0, 5, 5, 5, 5,
                                           5, 5, 0, 0, 0,
                                           0, 5, 0, 0, 0]),
      generate(width=12, height=10, colors=[0, 5, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0,
                                            0, 5, 0, 0, 5, 5, 5, 0, 0, 5, 0, 0,
                                            0, 5, 5, 5, 5, 0, 5, 0, 0, 5, 0, 0,
                                            0, 0, 5, 0, 0, 0, 5, 5, 5, 5, 0, 0,
                                            5, 5, 5, 0, 0, 0, 5, 0, 0, 5, 5, 5,
                                            0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                                            0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0,
                                            5, 5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 0,
                                            0, 0, 0, 5, 0, 0, 5, 5, 5, 0, 0, 0,
                                            0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0]),
  ]
  test = [
      generate(width=12, height=5, colors=[0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0,
                                           0, 5, 0, 0, 0, 5, 5, 5, 0, 5, 5, 0,
                                           5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 0,
                                           0, 0, 5, 5, 5, 5, 0, 5, 0, 5, 5, 0,
                                           0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 5, 0]),
  ]
  return {"train": train, "test": test}
