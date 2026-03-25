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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(5, 5)
    for i, color in enumerate(colors):
      output[i // 5][i % 5] = grid[i // 5][i % 5] = color
    # First, establish the maximum count for each color across all 2x2 subgrids.
    max_counts = [0] * 10
    for row in range(2):
      for col in range(2):
        counts = [0] * 10
        for r in range(2):
          for c in range(2):
            color = grid[3 * row + r][3 * col + c]
            if color != 7: counts[color] += 1
        for color in range(10):
          max_counts[color] = max(max_counts[color], counts[color])
    # Second, replace colors in each 2x2 subgrid to achieve the maximum count.
    for row in range(2):
      for col in range(2):
        counts = [0] * 10
        for r in range(2):
          for c in range(2):
            color = grid[3 * row + r][3 * col + c]
            if color != 7: counts[color] += 1
        the_colors = []
        for color in range(10):
          if counts[color] != max_counts[color]: the_colors.append(color)
        if len(the_colors) != 1: return None, None
        for r in range(2):
          for c in range(2):
            color = grid[3 * row + r][3 * col + c]
            if color == 7: output[3 * row + r][3 * col + c] = the_colors[0]
    return grid, output

  if colors is None:
    while True:
      grid = common.grid(5, 5, 7)
      subset = common.choices([0, 1, 2, 3, 4, 5, 6, 8, 9], 4)
      seen, good = [], True  # Let's make sure each quadrant is unique.
      for row in range(2):
        for col in range(2):
          subset = common.shuffle(subset)
          if subset in seen: good = False
          seen.append([color for color in subset])
          for r in range(2):
            for c in range(2):
              grid[3 * row + r][3 * col + c] = subset[r * 2 + c]
          r, c = common.randint(0, 1), common.randint(0, 1)
          grid[3 * row + r][3 * col + c] = 7
      colors = common.flatten(grid)
      grid, _ = draw()
      if good and grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[7, 1, 7, 8, 0,
                       0, 8, 7, 7, 1,
                       7, 7, 7, 7, 7,
                       8, 7, 7, 7, 1,
                       0, 1, 7, 8, 5]),
      generate(colors=[8, 9, 7, 9, 3,
                       3, 7, 7, 7, 8,
                       7, 7, 7, 7, 7,
                       8, 7, 7, 7, 8,
                       2, 9, 7, 9, 2]),
      generate(colors=[7, 4, 7, 4, 5,
                       4, 3, 7, 7, 3,
                       7, 7, 7, 7, 7,
                       5, 7, 7, 4, 3,
                       3, 4, 7, 5, 7]),
  ]
  test = [
      generate(colors=[8, 7, 7, 7, 8,
                       2, 4, 7, 4, 9,
                       7, 7, 7, 7, 7,
                       9, 7, 7, 7, 9,
                       4, 2, 7, 2, 8]),
  ]
  return {"train": train, "test": test}
