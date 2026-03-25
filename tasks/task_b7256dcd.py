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
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    # First, spread the color to any purple neighbors, and erase the pixel.
    num_changed = 0
    for row in range(height):
      for col in range(width):
        if grid[row][col] in [6, 7]: continue
        output[row][col] = 7
        coords = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
          nr, nc = row + dr, col + dc
          if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == 6:
            coords.append((nr, nc))
        if not coords: continue
        if len(coords) > 1: return None, None, None
        r, c = coords[0]
        output[r][c] = grid[row][col]
        num_changed += 1
    # Second, continue to spread the color to other purple neighbors.
    changed = True
    while changed:
      changed = False
      for row in range(height):
        for col in range(width):
          color = output[row][col]
          if color in [6, 7]: continue
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
              if output[nr][nc] not in [6, 7, color]: return None, None, None
              if output[nr][nc] != 6: continue
              output[nr][nc] = color
              changed = True
    return grid, output, num_changed

  if width is None:
    width, height = common.randint(3, 7), common.randint(3, 7)
    num_shapes = 3 if width >= 6 and height >= 6 else 2
    while True:
      grid = common.grid(width, height, 7)
      wides = [common.randint(2, 3) for _ in range(num_shapes)]
      talls = [common.randint(1, 3) for _ in range(num_shapes)]
      brows = [common.randint(0, height - t) for t in talls]
      bcols = [common.randint(0, width - w) for w in wides]
      if common.overlaps(brows, bcols, wides, talls, 1): continue
      for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
        to_remove = common.randint(0, wide * tall // 2 - 1)
        pixels = common.connected_sprite(wide, tall, to_remove)
        for r, c in pixels:
          grid[brow + r][bcol + c] = 6
      subset = common.random_colors(num_shapes + 1, exclude=[6, 7])
      num_drawn = 0
      for color in subset:
        r, c = common.randint(0, height - 1), common.randint(0, width - 1)
        if grid[r][c] != 7: continue
        grid[r][c] = color
        num_drawn += 1
      if num_drawn < num_shapes: continue
      colors = common.flatten(grid)
      grid, _, num_changed = draw()
      if grid and num_changed + 1 >= num_shapes: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=5, colors=[7, 6, 6, 3, 7,
                                          7, 7, 7, 4, 7,
                                          7, 7, 7, 6, 7,
                                          7, 7, 6, 6, 6,
                                          7, 7, 7, 6, 7]),
      generate(width=4, height=6, colors=[7, 7, 7, 6,
                                          3, 7, 6, 6,
                                          7, 7, 6, 7,
                                          7, 7, 7, 7,
                                          1, 6, 6, 6,
                                          7, 7, 6, 7]),
  ]
  test = [
      generate(width=7, height=7, colors=[4, 7, 6, 7, 7, 7, 5,
                                          6, 6, 6, 7, 7, 7, 7,
                                          7, 7, 6, 7, 1, 7, 7,
                                          7, 7, 7, 7, 6, 6, 7,
                                          7, 7, 7, 7, 6, 6, 7,
                                          6, 6, 8, 7, 7, 7, 7,
                                          7, 6, 7, 7, 7, 7, 7]),
  ]
  return {"train": train, "test": test}
