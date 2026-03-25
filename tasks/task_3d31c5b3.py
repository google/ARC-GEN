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


def generate(top=None, upper=None, lower=None, bottom=None, width=6, height=3):
  """Returns input and output grids according to the given parameters.

  Args:
    top: Boolean values for the top grid.
    upper: Boolean values for the upper grid.
    lower: Boolean values for the lower grid.
    bottom: Boolean values for the top grid.
    width: Width of the output grid.
    height: Height of the output grid.
  """
  if top is None:
    top = [common.randint(0, 1) for _ in range(width * height)]
    upper = [common.randint(0, 1) for _ in range(width * height)]
    lower = [common.randint(0, 1) for _ in range(width * height)]
    bottom = [common.randint(0, 1) for _ in range(width * height)]

  grid = common.grid(width, 4 * height)
  output = common.grid(width, height)
  for i in range(len(lower)):
    if lower[i]:
      grid[2 * height + i // width][i % width] = 2
      output[i // width][i % width] = 2
  for i in range(len(bottom)):
    if bottom[i]:
      grid[3 * height + i // width][i % width] = 8
      output[i // width][i % width] = 8
  for i in range(len(upper)):
    if upper[i]:
      grid[height + i // width][i % width] = 4
      output[i // width][i % width] = 4
  for i in range(len(top)):
    if top[i]:
      grid[i // width][i % width] = 5
      output[i // width][i % width] = 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(top=[1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
               upper=[1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0],
               lower=[1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0],
               bottom=[0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]),
      generate(top=[1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
               upper=[0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
               lower=[1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
               bottom=[1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0]),
      generate(top=[1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
               upper=[0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
               lower=[0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1],
               bottom=[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0]),
      generate(top=[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
               upper=[1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0],
               lower=[1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
               bottom=[1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1]),
      generate(top=[0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
               upper=[0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
               lower=[1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
               bottom=[0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]),
      generate(top=[0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
               upper=[1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
               lower=[0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
               bottom=[1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0]),
  ]
  test = [
      generate(top=[1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
               upper=[0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
               lower=[1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               bottom=[0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0]),
  ]
  return {"train": train, "test": test}
