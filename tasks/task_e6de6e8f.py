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


def generate(commands=None):
  """Returns input and output grids according to the given parameters.

  Args:
    commands: A list of commands to use.
  """

  if commands is None:
    while True:
      commands = [common.randint(-1, 1) for _ in range(5)]
      if commands.count(0) == 2: break

  grid, output = common.grid(12, 2), common.grid(7, 8)
  # Draw the input grid.
  col = 0
  for command in commands:
    if command == -1:
      grid[0][col + 1] = grid[1][col] = grid[1][col + 1] = 2
      col += 3
    if command == 0:
      grid[0][col] = grid[1][col] = 2
      col += 2
    if command == 1:
      grid[0][col] = grid[1][col] = grid[1][col + 1] = 2
      col += 3
  # Draw the output grid.
  output[0][3] = 3
  row, col = 1, 3
  for command in commands:
    if command == -1:
      output[row][col] = output[row][col - 1] = 2
      row, col = row + 1, col - 1
    if command == 0:
      output[row][col] = output[row + 1][col] = 2
      row += 2
    if command == 1:
      output[row][col] = output[row][col + 1] = 2
      row, col = row + 1, col + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(commands=[-1, 1, 1, 0, 0]),
      generate(commands=[1, -1, 0, 1, 0]),
      generate(commands=[1, 1, 1, 0, 0]),
  ]
  test = [
      generate(commands=[0, 1, 1, -1, 0]),
  ]
  return {"train": train, "test": test}
