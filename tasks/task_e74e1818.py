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
    width: The width of the grid.
    height: The height of the grid.
    colors: A list of colors to use.
  """

  def draw():
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      grid[i // width][i % width] = color
    last, length, lengths = -1, 1, []
    for row in range(1, height - 1):
      subset = list(set(grid[row]))
      if 0 in subset: subset.remove(0)
      if subset[0] == last:
        length += 1
      else:
        if last != -1: lengths.append(length)
        last, length = subset[0], 1
    lengths.append(length)
    inrow = outrow = 1
    for length in lengths:
      outrow = outrow + length - 1
      for _ in range(length):
        output[outrow] = grid[inrow]
        inrow, outrow = inrow + 1, outrow - 1
      outrow = inrow
    return grid, output

  if width is None:
    width = height = 2 * common.randint(3, 7) + 1
    colors = common.random_colors(common.randint(3, height // 2))
    while True:
      lengths = [common.randint(1, len(colors)) for _ in colors]
      if sum(lengths) + 2 == height: break
    while True:
      offset = 1
      grid = common.grid(width, height)
      for i, color in enumerate(colors):
        spacing = common.randint(1, width // 2 - 3)
        while True:
          sprite = common.grid(width, lengths[i])
          for r in range(lengths[i]):
            for c in range(spacing, width - spacing):
              if common.randint(0, 3): continue
              sprite[r][c] = sprite[r][width - 1 - c] = color
          good, pixels = True, []
          for r in range(lengths[i]):
            covered = False
            for c in range(1, width - 1):
              if not sprite[r][c]: continue
              covered = True
              pixels.append((r, c))
            if not covered: good = False
          if good and pixels: break
        for r in range(lengths[i]):
          for c in range(1, width - 1):
            grid[offset + r][c] = sprite[r][c]
        offset += lengths[i]
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=11,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                       0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0,
                       0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0,
                       0, 0, 0, 5, 0, 5, 0, 5, 0, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=13, height=13,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 4, 4, 0, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=7, height=7,
               colors=[0, 0, 0, 0, 0, 0, 0,
                       0, 0, 9, 9, 9, 0, 0,
                       0, 9, 0, 9, 0, 9, 0,
                       0, 0, 4, 4, 4, 0, 0,
                       0, 3, 3, 3, 3, 3, 0,
                       0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(width=15, height=15,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0,
                       0, 0, 0, 2, 2, 2, 0, 2, 0, 2, 2, 2, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 0, 0, 0,
                       0, 0, 0, 0, 4, 0, 4, 0, 4, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 4, 4, 4, 0, 4, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 8, 8, 0, 8, 8, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
