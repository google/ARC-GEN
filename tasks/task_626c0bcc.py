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


def generate(colors=None, size=7):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
    size: The size of the grid.
  """

  solutions = []

  def solve(output, matches, level=0):
    if level == len(matches):
      if 8 not in common.flatten(output):
        solutions.append(common.deepcopy(output))
      return
    solve(output, matches, level + 1)
    color, r, c = matches[level]
    stamp = [output[r][c], output[r][c + 1], output[r + 1][c], output[r + 1][c + 1]]
    # Check that nothing has written over this shape
    if color == 1 and sum(stamp) != 32: return
    if color == 2 and stamp[1] + stamp[2] + stamp[3] != 24: return
    if color == 4 and stamp[0] + stamp[2] + stamp[3] != 24: return
    if color == 3 and stamp[0] + stamp[1] + stamp[3] != 24: return
    # Write over the shape
    if color != 2: output[r][c] = color
    if color != 4: output[r][c + 1] = color
    if color != 3: output[r + 1][c] = color
    output[r + 1][c + 1] = color
    # Recurse
    solve(output, matches, level + 1)
    # Reset the output
    if color != 2: output[r][c] = 8
    if color != 4: output[r][c + 1] = 8
    if color != 3: output[r + 1][c] = 8
    output[r + 1][c + 1] = 8

  def draw():
    nonlocal solutions
    grid, output = common.grids(size, size)
    for r in range(size):
      for c in range(size):
        color = int(colors[r * size + c])
        output[r][c] = grid[r][c] = color
    # Let's require that problems always be diagonally connected.
    pixels = []
    for r in range(size):
      for c in range(size):
        if grid[r][c] == 8: pixels.append((r, c))
    if not common.diagonally_connected(pixels): return None, None
    # Find all possible matches.
    matches = []
    for r in range(size - 1):
      for c in range(size - 1):
        stamp = [grid[r][c], grid[r][c + 1], grid[r + 1][c], grid[r + 1][c + 1]]
        if sum(stamp) == 32: matches.append((1, r, c))
        if stamp[1] + stamp[2] + stamp[3] == 24: matches.append((2, r, c))
        if stamp[0] + stamp[2] + stamp[3] == 24: matches.append((4, r, c))
        if stamp[0] + stamp[1] + stamp[3] == 24: matches.append((3, r, c))
    # Make sure it's a "hard" problem with lots of matches.
    if len(matches) <= common.flatten(output).count(8): return None, None
    solutions = []
    solve(output, matches)
    # Make sure there's a single exact solution.
    if len(solutions) != 1: return None, None
    return grid, solutions[0]

  if colors is None:
    num_shapes = common.randint(4, 5)
    while True:
      hues = [common.randint(1, 4) for _ in range(num_shapes)]
      if len(set(hues)) < 4: continue
      brows = [common.randint(0, size - 2) for _ in range(num_shapes)]
      bcols = [common.randint(0, size - 2) for _ in range(num_shapes)]
      grid = common.grid(size, size)
      good = True
      for hue, brow, bcol in zip(hues, brows, bcols):
        if hue != 2:
          if grid[brow][bcol]: good = False
          grid[brow][bcol] = 8
        if hue != 4:
          if grid[brow][bcol + 1]: good = False
          grid[brow][bcol + 1] = 8
        if hue != 3:
          if grid[brow + 1][bcol]: good = False
          grid[brow + 1][bcol] = 8
        if grid[brow + 1][bcol + 1]: good = False
        grid[brow + 1][bcol + 1] = 8
      if not good: continue
      colors = "".join(str(c) for c in common.flatten(grid))
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors="0800800880088008808800880880008800000080000000000"),
      generate(colors="0088000888880008808800888800000880000000000000000"),
      generate(colors="8880000888800088080000888000000000000000000000000"),
  ]
  test = [
      generate(colors="0880880888888008808000088800000000000000000000000"),
  ]
  return {"train": train, "test": test}
