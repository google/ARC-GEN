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


def generate(top=None, bottom=None, width=4, height=5):
  """Returns input and output grids according to the given parameters.

  Args:
    top: Boolean values for the top grid.
    bottom: Boolean values for the top grid.
    width: Width of the output grid.
    height: Height of the output grid.
  """
  if top is None:
    top = [common.randint(0, 1) for _ in range(width * height)]
    bottom = [common.randint(0, 1) for _ in range(width * height)]

  grid = common.grid(2 * width + 1, height)
  output = common.grid(width, height)
  for i in range(len(top)):
    grid[i // width][i % width] = 8 if top[i] else 0
  for i in range(height):
    grid[i][width] = 4
  for i in range(len(bottom)):
    grid[i // width][width + 1 + i % width] = 5 if bottom[i] else 0
  for i in range(len(top)):
    output[i // width][i % width] = 2 if top[i] + bottom[i] == 1 else 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
               bottom=[0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1]),
      generate(top=[0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
               bottom=[1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0]),
      generate(top=[0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
               bottom=[0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1]),
      generate(top=[1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1],
               bottom=[0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1]),
  ]
  test = [
      generate(top=[0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
               bottom=[1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
