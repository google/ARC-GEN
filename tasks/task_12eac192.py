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
    if len(set(colors)) < 4: return None, None
    grid, output = common.grids(width, height)
    def get_shape_size(row, col):
      queue = [(row, col)]
      shape = [(row, col)]
      visited = [(row, col)]
      while queue:
        r, c = queue.pop()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
          rr, cc = r + dr, c + dc
          if 0 <= rr < height and 0 <= cc < width:
            if grid[rr][cc] == grid[r][c] and (rr, cc) not in visited:
              queue.append((rr, cc))
              shape.append((rr, cc))
              visited.append((rr, cc))
      return len(shape)
    for i, color in enumerate(colors):
      output[i // width][i % width] = grid[i // width][i % width] = color
    for r in range(height):
      for c in range(width):
        if not grid[r][c]: continue
        if get_shape_size(r, c) < 3: output[r][c] = 3
    flattened = common.flatten(output)
    if 3 not in flattened or len(set(flattened)) < 3: return None, None
    return grid, output

  if width is None:
    width, height = common.randint(3, 9), common.randint(3, 9)
    while True:
      colors = [common.randint(0, 1) for _ in range(width * height)]
      colors = [common.choice([1, 5, 7, 8]) if color else 0 for color in colors]
      # To encourage large shapes, randomly spread the colors.
      for _ in range(width * height):
        r, c = common.randint(0, height - 1), common.randint(0, width - 1)
        color = colors[r * width + c]
        if not color: continue
        if common.randint(0, 1):
          r += common.choice([-1, 1])
        else:
          c += common.choice([-1, 1])
        if 0 <= r < height and 0 <= c < width:
          colors[r * width + c] = color
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=5,
               colors=[1, 7, 7, 1, 0, 8, 0, 5,
                       1, 7, 7, 1, 1, 0, 1, 0,
                       8, 8, 0, 0, 7, 7, 7, 7,
                       0, 1, 0, 0, 0, 0, 1, 1,
                       5, 0, 8, 0, 1, 0, 1, 1]),
      generate(width=8, height=9,
               colors=[0, 0, 1, 8, 1, 1, 1, 0,
                       1, 5, 1, 7, 1, 1, 0, 0,
                       0, 8, 0, 7, 7, 7, 8, 8,
                       0, 8, 8, 0, 0, 0, 8, 0,
                       0, 7, 0, 0, 8, 5, 5, 0,
                       1, 0, 0, 0, 0, 0, 0, 1,
                       1, 0, 8, 7, 7, 8, 0, 0,
                       0, 0, 8, 7, 7, 0, 8, 8,
                       0, 8, 8, 0, 8, 0, 8, 8]),
      generate(width=3, height=3,
               colors=[1, 0, 5,
                       1, 0, 0,
                       7, 7, 7]),
      generate(width=8, height=7,
               colors=[0, 0, 1, 0, 7, 7, 7, 0,
                       8, 8, 0, 0, 5, 5, 0, 0,
                       0, 8, 8, 0, 0, 5, 5, 0,
                       0, 1, 1, 0, 8, 0, 0, 1,
                       0, 7, 0, 1, 8, 0, 0, 0,
                       8, 0, 0, 0, 1, 0, 7, 0,
                       0, 8, 8, 8, 1, 0, 0, 0]),
  ]
  test = [
      generate(width=8, height=8,
               colors=[0, 5, 0, 1, 5, 5, 0, 5,
                       1, 1, 0, 0, 0, 1, 1, 0,
                       0, 7, 7, 0, 0, 0, 0, 5,
                       1, 1, 0, 5, 0, 1, 0, 0,
                       0, 1, 0, 5, 5, 5, 0, 1,
                       0, 7, 0, 0, 7, 0, 0, 7,
                       1, 0, 1, 0, 0, 0, 1, 7,
                       0, 0, 1, 1, 0, 1, 0, 7]),
  ]
  return {"train": train, "test": test}
