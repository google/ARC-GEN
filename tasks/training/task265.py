# Copyright 2025 Google LLC
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


def generate(colors=None, size=18):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """

  def draw(grid, output, stripes=[0, 1]):
    legal = True
    for r in range(size):
      for c in range(size):
        output[r][c] = grid[r][c] = colors[r * size + c]
    def is_empty(r, c):
      if output[r][c] or output[r][c + 1]: return False
      if output[r + 1][c] or output[r + 1][c + 1]: return False
      return True
    def paint(paintlist):
      for (r, c) in paintlist:
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          output[r + dr][c + dc] = common.red()
    for stripe in stripes:
      topaint = []
      if stripe == 0:  # First, paint all downstripes
        for r in range(size - 1):
          for c in range(size - 1):
            if not is_empty(r, c): continue
            # Cells on one side can't both be empty
            if c > 0 and output[r][c - 1] + output[r + 1][c - 1] == 0:
              legal = False
              continue
            if c < size - 2 and output[r][c + 2] + output[r + 1][c + 2] == 0:
              legal = False
              continue
            topaint.append((r, c))
      if stripe == 1:  # Second, paint all sidestripes
        for r in range(size - 1):
          for c in range(size - 1):
            if not is_empty(r, c): continue
            # Cells on one side can't both be empty
            if r > 0 and output[r - 1][c] + output[r - 1][c + 1] == 0:
              legal = False
              continue
            if r < size - 2 and output[r + 2][c] + output[r + 2][c + 1] == 0:
              legal = False
              continue
            topaint.append((r, c))
      paint(topaint)
    return legal

  if colors is None:
    while True:
      # Create some static
      pixels = common.random_pixels(size, size, 0.8)
      grid = common.grid(size, size)
      for (r, c) in pixels:
        grid[r][c] = common.gray()
      # Add some holes
      for _ in range(common.randint(4, 6)):
        r, c = common.randint(0, size - 2), common.randint(0, size - 2)
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
          grid[r + dr][c + dc] = common.black()
      # Extract the colors
      colors = []
      for r in range(size):
        for c in range(size):
          colors.append(grid[r][c])
      grid, output1 = common.grids(size, size)
      if not draw(grid, output1, [0, 1]): continue
      grid, output2 = common.grids(size, size)
      if not draw(grid, output2, [1, 0]): continue
      if output1 == output2: break  # Avoid ambigous problems.

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5,
                       5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 0, 5, 0, 5, 0, 5, 0, 5,
                       5, 0, 5, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0,
                       5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5,
                       5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5,
                       0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 0,
                       0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 0, 5,
                       5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 5, 0, 0, 0,
                       5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 0, 0, 5, 5, 0, 0, 5, 5, 5,
                       5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 5, 5, 0, 0, 5, 0,
                       5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                       5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 5,
                       5, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 5, 5, 0, 0, 5, 5,
                       5, 0, 0, 0, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 0,
                       5, 5, 0, 0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0,
                       5, 0, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 5,
                       0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 0, 5, 5, 0, 5, 0, 5, 0, 5,
                       5]),
      generate(colors=[5, 5, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5, 0, 0, 5, 0, 5, 5, 5,
                       5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 0, 5, 5, 0, 5, 5,
                       5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 5,
                       5, 5, 5, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 5, 0,
                       5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 5, 0, 5, 0, 0, 0, 5,
                       0, 5, 5, 5, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 5, 5, 5,
                       0, 0, 0, 5, 5, 0, 0, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5,
                       5, 0, 5, 0, 0, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5, 5, 5,
                       0, 5, 5, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 5, 5, 5, 0, 5, 0,
                       5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 0, 5, 5, 5, 0, 5, 0, 5, 0,
                       0, 5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 5,
                       0, 5, 5, 5, 0, 0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 5, 0, 0, 5,
                       0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 0, 5, 5,
                       5, 0, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 0,
                       0, 0, 0, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5,
                       0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 5,
                       0, 0, 5, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5,
                       5]),
      generate(colors=[0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 0, 5,
                       0, 0, 0, 5, 5, 0, 0, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0,
                       5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 0, 5, 5, 5, 5, 5, 5,
                       0, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5,
                       5, 5, 5, 0, 5, 5, 5, 5, 0, 5, 0, 0, 0, 0, 5, 0, 0, 5, 5,
                       5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 0, 5, 5, 5, 5, 0, 5, 5,
                       5, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 0, 0, 5, 5, 0, 5, 5, 5,
                       5, 0, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5,
                       0, 5, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 0, 5, 5, 5,
                       5, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 5, 0, 5, 5, 0, 5, 5, 5,
                       0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 5,
                       5, 5, 5, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 0,
                       5, 0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 0, 0, 0, 5, 0, 5,
                       5, 0, 5, 0, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 0, 5, 0, 0, 0,
                       5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 5, 5,
                       0, 0, 5, 0, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 5, 5, 0, 5, 5,
                       5, 5, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 0, 0, 5,
                       0]),
  ]
  test = [
      generate(colors=[0, 0, 0, 5, 0, 5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 0, 0, 0,
                       0, 5, 5, 0, 5, 0, 5, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5, 0,
                       0, 0, 5, 5, 0, 5, 0, 0, 5, 0, 5, 0, 5, 5, 0, 5, 0, 5, 5,
                       5, 0, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 0, 5, 5, 5, 5, 5, 5,
                       5, 5, 5, 0, 0, 5, 5, 0, 0, 0, 0, 5, 5, 5, 0, 5, 5, 5, 5,
                       0, 5, 5, 5, 0, 5, 0, 0, 5, 5, 0, 5, 0, 5, 5, 0, 5, 5, 5,
                       5, 5, 5, 0, 0, 5, 0, 0, 5, 0, 5, 5, 5, 5, 5, 5, 0, 0, 5,
                       5, 0, 5, 5, 5, 5, 5, 0, 5, 5, 0, 5, 0, 5, 0, 0, 5, 5, 5,
                       0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5,
                       5, 5, 5, 0, 0, 5, 0, 5, 5, 5, 0, 5, 5, 0, 5, 5, 5, 0, 0,
                       5, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 5, 5, 0, 5, 0, 0, 5, 5,
                       0, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 0, 0, 5, 0, 0, 0, 5,
                       5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5,
                       5, 5, 0, 0, 5, 5, 5, 0, 5, 5, 5, 0, 5, 0, 5, 5, 5, 5, 0,
                       5, 0, 0, 5, 5, 0, 5, 5, 5, 5, 0, 5, 5, 0, 0, 0, 5, 5, 5,
                       5, 0, 5, 0, 5, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                       5, 5, 5, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 5, 5, 0, 5, 5, 0,
                       0]),
  ]
  return {"train": train, "test": test}
