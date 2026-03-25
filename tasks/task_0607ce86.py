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


def generate(wide=None, tall=None, hoffset=None, voffset=None, hspacing=None,
             vspacing=None, colors=None, width=22):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  # Iteration -1 draws the expected pattern onto the output.
  # Iteration  0 extracts the pattern from the input.
  # Iteration  1 draws the extracted pattern onto the output.
  def draw(it_range=[0, 1], expected=[]):
    height = len(colors) // width
    grid, output = common.grids(width, height)
    for i, color in enumerate(colors):
      grid[i // width][i % width] = color
    hcopies = (width - 2) // (wide + hspacing)
    vcopies = (height - 2) // (tall + vspacing)
    pattern = []
    for it in it_range:
      for row in range(tall):
        for col in range(wide):
          seen = []
          for brow in range(vcopies):
            for bcol in range(hcopies):
              r = voffset + brow * (tall + vspacing) + row
              c = hoffset + bcol * (wide + hspacing) + col
              if it == -1: output[r][c] = expected[row * wide + col]
              if it == 0:
                if grid[r][c] == 0: return None, None  # Our math was off
                seen.append(grid[r][c])
              if it == 1: output[r][c] = pattern[row * wide + col]
          if it == 0:
            seen = sorted([(seen.count(c), c) for c in set(seen)], reverse=True)
            if len(seen) > 1 and seen[0][0] == seen[1][0]: return None, None
            if it == 0: pattern.append(seen[0][1])
    return grid, output

  if colors is None:
    height = common.randint(20, 25)
    colors = [0] * (width * height)
    wide, tall = common.randint(4, 6), common.randint(4, 6)
    hoffset, voffset = common.randint(1, 2), common.randint(1, 2)
    hspacing, vspacing = common.randint(1, 2), common.randint(1, 2)
    subset = common.sample([1, 2, 3, 6, 8], common.randint(3, 4))
    pattern = [0] * (wide * tall)
    # Keep adding lines to our pattern until it's completely filled.
    while 0 in pattern or len(set(pattern)) != len(subset):
      color = common.choice(subset)
      if common.randint(0, 1):
        row = common.randint(0, tall - 1)
        for col in range(wide): pattern[row * wide + col] = color
      else:
        col = common.randint(0, wide - 1)
        for row in range(tall): pattern[row * wide + col] = color
    # Keep trying to add noise to a clear image until we can infer the pattern.
    while True:
      _, output = draw([-1], pattern)
      for r in range(height):
        for c in range(width):
          if common.randint(0, 9) == 0: output[r][c] = common.choice(subset)
      colors = common.flatten(output)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wide=5, tall=5, hoffset=1, voffset=1, hspacing=1, vspacing=1,
               colors=[0, 3, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 1, 1, 1, 2, 3, 3, 0, 3, 0, 0,
                       0, 1, 1, 3, 3, 3, 0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 3, 0, 3, 0,
                       0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 1, 1, 1, 3, 3, 0, 0, 0, 3,
                       0, 1, 3, 3, 3, 1, 0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 0, 0, 0,
                       0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 1, 3, 3, 3, 0, 3, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 0, 3, 0,
                       0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 0, 0, 0,
                       0, 1, 1, 2, 3, 3, 0, 1, 3, 2, 1, 3, 0, 1, 1, 2, 3, 3, 0, 0, 0, 0,
                       1, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 3, 1, 3, 2, 3, 3, 0, 0, 0, 0,
                       0, 8, 1, 8, 8, 3, 0, 8, 8, 8, 8, 8, 0, 1, 8, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0,
                       0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 0, 3, 0,
                       0, 1, 1, 3, 3, 3, 0, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 3, 0, 0, 0, 0,
                       0, 1, 1, 2, 3, 3, 0, 1, 1, 1, 3, 3, 0, 1, 1, 2, 3, 1, 0, 0, 0, 0,
                       1, 1, 1, 2, 3, 3, 0, 1, 1, 2, 3, 1, 0, 1, 1, 2, 3, 3, 0, 0, 0, 0,
                       3, 8, 8, 8, 3, 3, 1, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 0, 1, 0,
                       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 0, 3, 0, 3, 0, 1, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                       0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(wide=6, tall=5, hoffset=2, voffset=1, hspacing=2, vspacing=2,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 6, 6, 6, 6, 3, 6, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 8, 3, 3, 3, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 3, 0, 0, 0,
                       0, 3, 8, 8, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 3, 0, 0, 0, 3, 0, 0,
                       0, 3, 8, 8, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 8, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 6, 6, 3, 6, 6, 6, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 3, 8, 3, 3, 8, 3, 0, 3, 0, 0, 0, 3,
                       0, 0, 8, 8, 3, 3, 3, 8, 0, 0, 3, 8, 3, 3, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 8, 3, 3, 3, 3, 8, 0, 0, 0, 0, 0, 0,
                       3, 3, 8, 8, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 6, 6, 3, 6, 6, 6, 0, 3, 6, 6, 6, 3, 6, 6, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 0, 0, 3, 0,
                       0, 0, 8, 3, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 8, 8, 3, 3, 8, 8, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(wide=4, tall=4, hoffset=1, voffset=1, hspacing=2, vspacing=2,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                       0, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 3,
                       0, 3, 2, 2, 3, 0, 0, 3, 2, 2, 3, 0, 3, 3, 2, 2, 3, 0, 0, 3, 0, 0,
                       0, 2, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 2, 3, 1, 3, 0, 0, 2, 2, 1, 2, 0, 0, 3, 1, 1, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                       0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                       0, 2, 2, 2, 2, 3, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0,
                       0, 3, 2, 2, 3, 0, 0, 3, 2, 2, 3, 0, 3, 3, 2, 2, 3, 2, 0, 0, 0, 0,
                       0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 3, 3, 1, 3, 0, 0, 3, 1, 1, 3, 0, 0, 3, 1, 1, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 2, 2, 0, 0, 3, 2, 3, 2, 0, 0, 2, 3, 2, 2, 0, 0, 0, 0, 0,
                       0, 3, 2, 2, 3, 0, 0, 3, 2, 3, 3, 0, 0, 3, 2, 3, 3, 0, 0, 0, 0, 0,
                       3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 2, 3, 3, 0, 0, 2, 0, 0,
                       0, 3, 1, 1, 3, 0, 3, 3, 1, 1, 3, 0, 0, 3, 1, 1, 3, 0, 0, 0, 0, 0,
                       0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0,
                       0, 0, 0, 3, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(wide=5, tall=5, hoffset=1, voffset=1, hspacing=1, vspacing=2,
               colors=[0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0,
                       0, 2, 2, 8, 3, 2, 0, 2, 2, 8, 2, 2, 0, 3, 2, 8, 2, 2, 0, 0, 0, 3,
                       0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 0, 0,
                       0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 0, 0, 0,
                       3, 8, 8, 3, 3, 8, 0, 8, 8, 8, 8, 8, 0, 8, 8, 3, 8, 8, 0, 0, 0, 0,
                       0, 8, 8, 8, 8, 3, 0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0,
                       0, 2, 3, 8, 2, 2, 0, 2, 2, 3, 2, 3, 0, 2, 2, 8, 2, 2, 0, 0, 0, 3,
                       0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 0, 0,
                       0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 0, 0, 0,
                       0, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 3, 0, 8, 8, 8, 3, 8, 0, 0, 0, 0,
                       0, 8, 8, 8, 3, 8, 0, 8, 3, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3,
                       0, 2, 2, 8, 2, 2, 0, 2, 2, 8, 2, 2, 0, 2, 2, 8, 2, 2, 0, 0, 0, 0,
                       0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 0, 3, 0,
                       0, 3, 3, 3, 3, 3, 0, 3, 3, 8, 3, 3, 0, 3, 3, 8, 3, 3, 0, 0, 0, 0,
                       0, 3, 8, 8, 8, 8, 0, 8, 8, 3, 3, 8, 0, 8, 8, 3, 8, 8, 0, 3, 0, 0,
                       0, 8, 8, 8, 8, 8, 0, 8, 8, 3, 8, 8, 0, 3, 8, 8, 8, 8, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0,
                       0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0,
                       3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
