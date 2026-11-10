#!/usr/bin/env python
"""Train the self-learning hub (PPO) on junction J2.

First:  .venv/bin/pip install stable-baselines3 torch
Then:   .venv/bin/python train_hub.py --steps 100000
Watch:  .venv/bin/python train_hub.py --eval models/hub_J2.zip --gui
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
from saarathi.env import SaarathiHubEnv

MODELS = Path(__file__).resolve().parent / 'models'


def train(steps: int):
    from stable_baselines3 import PPO
    env = SaarathiHubEnv(hours=(8, 10))
    # Keep the starter runnable with the documented requirements. TensorBoard
    # can be enabled later, but it must not be a hidden training dependency.
    model = PPO('MlpPolicy', env, verbose=1, n_steps=512, batch_size=128,
                learning_rate=3e-4, gamma=0.99)
    model.learn(total_timesteps=steps)
    MODELS.mkdir(exist_ok=True)
    model.save(MODELS / 'hub_J2')
    env.close()
    print('saved ->', MODELS / 'hub_J2.zip')


def evaluate(path: str, gui: bool):
    from stable_baselines3 import PPO
    env = SaarathiHubEnv(hours=(8, 10), seed_base=100, gui=gui)  # unseen seeds
    model = PPO.load(path)
    obs, _ = env.reset()
    total, n = 0.0, 0
    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, r, term, trunc, _ = env.step(int(action))
        total += r
        n += 1
        if term:
            break
    print(f'episode return {total:.1f} over {n} decisions')
    env.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--steps', type=int, default=100_000)
    ap.add_argument('--eval', metavar='MODEL_ZIP')
    ap.add_argument('--gui', action='store_true')
    args = ap.parse_args()
    if args.eval:
        evaluate(args.eval, args.gui)
    else:
        train(args.steps)
