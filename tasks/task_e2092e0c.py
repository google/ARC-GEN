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


def generate(colors=None, size=15, grey=5):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
    size: The size of the grid.
    grey: The color of the grey pixels.
  """

  def find_matches():
    matches = []
    for r in range(size - 2):
      for c in range(size - 2):
        match = True
        for dr in range(3):
          for dc in range(3):
            if colors[(r + dr) * size + c + dc] != colors[dr * size + dc]:
              match = False
        if match: matches.append((r, c))
    matches.pop(0)  # The first match is the target image.
    return matches

  if colors is None:
    while True:
      randoms = [common.randint(0, 9) for _ in range(size * size)]
      colors = [common.random_color() if rand < 4 else 0 for rand in randoms]
      for i in range(4):
        colors[size * i + 3] = colors[size * 3 + i] = grey
      upper_left = []
      upper_left += colors[0:3]
      upper_left += colors[size:(size + 3)]
      upper_left += colors[(2 * size):(2 * size + 3)]
      if grey in upper_left: continue  # No grey's allowed.
      if upper_left.count(0) < 4 or upper_left.count(0) > 5: continue
      brow, bcol = common.randint(1, size - 4), common.randint(1, size - 4)
      if brow < 5 and bcol <= 5: continue  # Would overlap with the target.
      if brow <= 5 and bcol < 5: continue  # Would overlap with the target.
      for i, color in enumerate(upper_left):
        colors[(brow + i // 3) * size + bcol + i % 3] = color
      if len(find_matches()) == 1: break

  grid, output = common.grids(size, size)
  for i, color in enumerate(colors):
    output[i // size][i % size] = grid[i // size][i % size] = color
  row, col = find_matches()[0]
  common.hollow_rect(output, 5, 5, row - 1, col - 1, grey)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[3, 4, 0, 5, 0, 0, 3, 0, 5, 8, 0, 7, 0, 0, 0,
                       0, 0, 4, 5, 8, 8, 0, 0, 0, 0, 7, 3, 3, 0, 0,
                       0, 8, 3, 5, 0, 0, 5, 0, 0, 1, 0, 2, 0, 0, 9,
                       5, 5, 5, 5, 6, 1, 0, 9, 0, 0, 3, 3, 0, 6, 0,
                       3, 7, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0, 0,
                       0, 4, 0, 0, 5, 5, 6, 0, 0, 0, 0, 0, 1, 5, 0,
                       0, 2, 1, 0, 0, 0, 0, 0, 4, 9, 0, 9, 0, 0, 0,
                       0, 0, 0, 0, 8, 0, 0, 0, 7, 2, 2, 0, 0, 9, 8,
                       1, 0, 0, 0, 1, 0, 3, 7, 0, 0, 0, 7, 0, 0, 3,
                       0, 0, 1, 2, 0, 9, 3, 4, 0, 0, 1, 0, 0, 2, 9,
                       0, 9, 0, 0, 8, 0, 0, 0, 4, 0, 0, 6, 0, 8, 4,
                       7, 7, 6, 0, 0, 0, 0, 8, 3, 0, 0, 0, 8, 2, 7,
                       0, 9, 0, 0, 2, 0, 4, 0, 0, 0, 0, 0, 0, 1, 6,
                       0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 4, 0, 9, 8, 0,
                       4, 0, 0, 0, 9, 0, 1, 1, 7, 9, 0, 0, 0, 8, 0]),
      generate(colors=[0, 7, 6, 5, 0, 0, 0, 0, 1, 4, 5, 6, 0, 0, 8,
                       7, 0, 0, 5, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 6,
                       0, 9, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 2,
                       5, 5, 5, 5, 4, 0, 0, 0, 4, 0, 9, 0, 9, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0,
                       2, 3, 6, 0, 0, 0, 7, 6, 0, 0, 9, 4, 0, 0, 4,
                       0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 3, 0, 0, 0,
                       0, 9, 0, 0, 0, 0, 9, 0, 8, 7, 0, 0, 0, 0, 0,
                       0, 6, 1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0,
                       1, 0, 5, 4, 0, 0, 8, 0, 0, 0, 0, 2, 2, 0, 6,
                       3, 0, 6, 0, 2, 0, 0, 0, 0, 4, 0, 0, 0, 6, 0,
                       4, 1, 0, 0, 0, 0, 1, 0, 7, 0, 0, 0, 0, 4, 0,
                       0, 2, 0, 0, 7, 0, 0, 9, 7, 6, 0, 0, 5, 3, 0,
                       4, 0, 4, 1, 0, 0, 8, 1, 8, 0, 0, 9, 4, 7, 7,
                       0, 8, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 5, 1, 6]),
      generate(colors=[4, 0, 2, 5, 0, 0, 0, 2, 6, 9, 0, 0, 5, 0, 0,
                       0, 7, 0, 5, 0, 8, 5, 8, 0, 7, 0, 0, 0, 8, 8,
                       0, 6, 6, 5, 7, 0, 3, 5, 0, 0, 0, 4, 7, 0, 0,
                       5, 5, 5, 5, 8, 0, 1, 9, 0, 0, 0, 0, 5, 0, 0,
                       8, 0, 0, 0, 0, 0, 1, 0, 3, 9, 8, 0, 0, 0, 0,
                       0, 2, 0, 0, 0, 6, 6, 4, 0, 9, 0, 0, 1, 7, 0,
                       8, 0, 6, 0, 0, 0, 8, 3, 0, 0, 0, 0, 0, 0, 9,
                       3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 0, 4, 0, 2, 0, 3, 2, 0, 0,
                       0, 0, 1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 5, 0, 8,
                       0, 9, 4, 4, 0, 0, 4, 0, 6, 6, 0, 7, 0, 0, 0,
                       7, 0, 0, 0, 9, 0, 0, 8, 0, 0, 0, 5, 0, 0, 0,
                       0, 6, 0, 0, 1, 0, 0, 7, 7, 0, 0, 0, 4, 0, 0,
                       0, 0, 0, 4, 0, 5, 0, 0, 0, 0, 7, 0, 5, 0, 0,
                       8, 0, 9, 8, 5, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0]),
  ]
  test = [
      generate(colors=[0, 7, 3, 5, 0, 0, 0, 0, 0, 0, 0, 3, 5, 4, 0,
                       1, 0, 3, 5, 2, 0, 1, 0, 0, 0, 0, 8, 0, 0, 0,
                       1, 0, 0, 5, 6, 0, 0, 9, 9, 0, 5, 0, 0, 0, 9,
                       5, 5, 5, 5, 0, 0, 2, 1, 0, 0, 3, 0, 0, 0, 0,
                       3, 0, 0, 3, 1, 8, 5, 0, 5, 2, 0, 0, 5, 0, 0,
                       4, 0, 9, 2, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 0, 0, 9, 5, 4, 0, 8, 0, 0, 5, 5,
                       0, 7, 0, 0, 0, 5, 5, 7, 0, 0, 1, 0, 0, 0, 1,
                       0, 0, 0, 3, 0, 7, 3, 7, 0, 0, 0, 0, 7, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 3, 0, 0, 0, 3, 4, 0, 7, 3, 0, 2,
                       0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0,
                       0, 0, 5, 2, 2, 2, 0, 0, 0, 0, 1, 0, 0, 2, 0,
                       0, 0, 3, 0, 0, 5, 4, 7, 0, 0, 0, 0, 0, 3, 5,
                       8, 0, 0, 1, 7, 1, 0, 8, 0, 8, 2, 0, 0, 0, 4]),
  ]
  return {"train": train, "test": test}
