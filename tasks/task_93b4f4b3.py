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


def generate(width=None, height=None, bgcolor=None, orders=None, pattern=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the shapes.
    height: The height of the shapes.
    bgcolor: The background color.
    orders: The order of the shapes in the output.
    pattern: The pattern of the shapes.
  """

  if width is None:
    width, height = common.randint(3, 4), common.randint(2, 3)
    num_shapes, shapes = common.randint(3, 4), []
    while len(shapes) < num_shapes:
      shape = []
      for r in range(height):
        for c in range(width):
          if common.randint(0, 1): shape.append((r, c))
      if not common.connected(shape) or shape in shapes: continue
      if len(set([r for r, _ in shape])) != height: continue
      shapes.append(shape)
    bgcolor = common.random_color()
    colors = common.random_colors(num_shapes, exclude=[bgcolor])
    pattern = []
    for i, shape in enumerate(shapes):
      for r in range(height):
        for c in range(width):
          pattern.append(0 if (r, c) not in shape else colors[i])
    orders = common.shuffle(list(range(num_shapes)))

  grid = common.grid(2 * width + 4, (height + 1) * len(orders) + 1)
  output = common.grid(width + 2, (height + 1) * len(orders) + 1, bgcolor)
  common.rect(grid, width + 2, (height + 1) * len(orders) + 1, 0, 0, bgcolor)
  common.rect(output, width + 2, (height + 1) * len(orders), 0, 0, bgcolor)
  for i, order in enumerate(orders):
    for r in range(height):
      for c in range(width):
        in_color = pattern[i * height * width + r * width + c]
        grid[i * (height + 1) + r + 1][width + 3 + c] = in_color
        out_color = pattern[order * height * width + r * width + c]
        if out_color:
          grid[i * (height + 1) + r + 1][c + 1] = 0
          output[i * (height + 1) + r + 1][c + 1] = out_color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=4, height=3, bgcolor=5, orders=[2, 1, 0],
               pattern=[3, 0, 0, 3, 3, 0, 0, 3, 3, 3, 3, 3,
                        2, 2, 2, 0, 2, 2, 0, 0, 2, 0, 0, 0,
                        0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]),
      generate(width=4, height=2, bgcolor=1, orders=[1, 2, 0],
               pattern=[0, 2, 2, 0, 0, 2, 2, 0,
                        0, 3, 3, 0, 3, 3, 3, 3,
                        6, 6, 6, 6, 0, 6, 6, 0]),
  ]
  test = [
      generate(width=3, height=3, bgcolor=8, orders=[2, 0, 1, 3],
               pattern=[2, 2, 2, 0, 0, 2, 0, 0, 2,
                        4, 0, 4, 4, 0, 4, 4, 4, 4,
                        3, 3, 3, 0, 3, 0, 3, 3, 3,
                        0, 7, 7, 7, 7, 7, 7, 7, 0]),
  ]
  return {"train": train, "test": test}
