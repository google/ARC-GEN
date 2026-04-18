<p align="center">
<img src="misc/images/arc-gen-logo.jpg">
</p>

This repository contains the source code for *ARC-GEN*, a mimetic procedural benchmark generator for the Abstraction and Reasoning Corpus.

For a more in-depth description of this work, see the [corresponding paper on arxiv](https://arxiv.org/abs/2511.00162).

## News

 * `2026-04-04`: ARC-GEN to be used as the official benchmark generator in the [2026 NeuroGolf Championship](https://www.kaggle.com/competitions/neurogolf-2026) featured at [IJCAI-ECAI 2026](https://2026.ijcai.org/).
 * `2026-03-25`: ARC-GEN now supports 500 additional tasks from [ARC-AGI-2](https://arcprize.org/arc-agi/2).
 * `2025-10-31`: An ARC-GEN overview is now available on [arxiv](https://arxiv.org/abs/2511.00162).
 * `2025-07-31`: ARC-GEN to be used as the official benchmark generator in the [2025 Google Code Golf Championship](https://www.kaggle.com/competitions/google-code-golf-2025) featured at [NeurIPS 2025](https://neurips.cc/Conferences/2025).
 * `2025-05-15`: The initial ARC-GEN repository committed to GitHub.

## Installation

```
$ git clone --recurse-submodules https://github.com/google/ARC-GEN.git && cd ARC-GEN
```

## Usage

For **benchmark generation**, use the `generate` command with two arguments: the task ID, and the desired number of example pairs.

```
$ python3 arc_gen.py generate 1e0a9b12 1000
[{'input': [[4, 0, 0, 0], [0, 0, 0, 0], [4, 0, 8, 0], [0, 3, 8, 0]], 'output': ...
```

For **validation** (i.e., to ensure that the ARC-GEN generators can collectively reproduce the original [ARC-AGI-1](https://github.com/fchollet/ARC-AGI) benchmark suite), use the `validate` command:

```
$ python3 arc_gen.py validate
A total of 400 generators passed.
A total of 0 generators failed.
```

For an example of customized **variations**, refer to [arc_gen_variations.py](https://github.com/google/ARC-GEN/blob/main/arc_gen_variations.py), which produces two variations on [Task #125](https://arcprize.org/play?task=543a7ed5):

```
  generator, _ = task_list.task_list().get("543a7ed5")
  examples = []
  # Two examples of a "large" variation on Task #125.
  examples.extend([generator(boxes=8, size=28) for _ in range(2)])
  # Two examples of a "large + inverted" variation on Task #125.
  common.set_colors([0, 1, 2, 6, 8, 5, 3, 7, 4, 9])
  examples.extend([generator(boxes=8, size=28) for _ in range(2)])
```

## The ARC-GEN-100K Dataset

For those seeking a pre-generated dataset of sample pairs, the link below provides a static benchmark suite containing 100,000 examples produced by ARC-GEN (covering all four-hundred tasks):

<p align="center">
https://www.kaggle.com/datasets/arcgen100k/the-arc-gen-100k-dataset
<br><br>
<img src="misc/images/arc-gen-gallery-faded.png">
</p>

## How to Cite?

```
@misc{Moffitt2025,
  title={{ARC-GEN: A Mimetic Procedural Benchmark Generator for the Abstraction and Reasoning Corpus}}, 
  author={Michael D. Moffitt},
  year={2025},
  eprint={2511.00162},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2511.00162}, 
}
```

## Other Resouces

 * [RE-ARC: Reverse-Engineering the Abstraction and Reasoning Corpus](https://github.com/michaelhodel/re-arc) by Michael Hodel
 * [Bootstrapping ARC: Synthetic Problem Generation for ARC Visual Reasoning Tasks](https://github.com/xu3kev/BARC) by Wen-Ding Li and others
