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


def generate(letters=None, colors=None, depth=None):
  """Returns input and output grids according to the given parameters.

  Args:
    letters: The letters of the sprites.
    colors: The colors of the sprites.
    depth: The depth of the sprites.
  """

  if letters is None:
    num_letters, depth = common.randint(3, 4), common.randint(1, 3)
    colors = common.sample([1, 2, 3, 5], num_letters)
    while True:
      letter_keys = sorted(list(common.letter_map().keys()))
      letters = common.sample(letter_keys, num_letters)
      good = True
      for letter in letters:
        coords = common.letter_map()[letter]
        rows, cols = zip(*coords)
        if 0 not in rows or 0 not in cols or 2 not in rows or 2 not in cols:
          good = False
      if good: break
    letters = "".join(letters)

  grid = common.grid(4 * len(letters) - 1, 4 * depth + 1)
  output = common.grid(4 * len(letters) - 1, 3)
  for layer in range(depth):
    for i in range(len(letters)):
      letter = letters[(i + layer) % len(letters)]
      for dr, dc in common.letter_map()[letter]:
        r, c = 4 * layer + 1 + dr, 4 * i + dc
        grid[r][c] = colors[i]
  for i in range(len(letters)):
    letter = letters[(i + depth) % len(letters)]
    for dr, dc in common.letter_map()[letter]:
      r, c = dr, 4 * i + dc
      output[r][c] = colors[i]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(letters="7L:|", colors=[2, 3, 1, 5], depth=1),
      generate(letters="X4T", colors=[2, 3, 1], depth=2),
      generate(letters="4XV+", colors=[2, 3, 1, 5], depth=2),
      generate(letters="U+=", colors=[2, 1, 3], depth=3),
  ]
  test = [
      generate(letters="1>|+", colors=[2, 3, 1, 5], depth=2),
  ]
  return {"train": train, "test": test}
