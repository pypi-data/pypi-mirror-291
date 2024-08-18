import os, sys
import torch

# Directly run `python -m pytest` or
# Directly run `python -m pytest -v -s --disable-warnings` for Debugging

# To test single function:
# pytest tests/test_t2v.py::test_function_name

dummy_prompts = [
    "a teddy bear walking on the street, 2k, high quality",
    "a panda taking a selfie, 2k, high quality",
    "a polar bear playing drum kit in NYC Times Square, 4k, high resolution",
    "jungle river at sunset, ultra quality",
    "a shark swimming in clear Carribean ocean, 2k, high quality",
    "a Corgi walking in the park at sunrise, oil painting style",
]

import sys
sys.path.append("src")

def test_LaVie():
    from videogen_hub.infermodels import LaVie

    model = LaVie()
    assert model is not None
    out_video = model.infer_one_video(dummy_prompts[0])
    assert out_video is not None
    # check if out_video is a tensor or not
    assert isinstance(out_video, torch.Tensor)
    print(out_video.shape)


def test_VideoCrafter2():
    from videogen_hub.infermodels import VideoCrafter2

    model = VideoCrafter2()
    assert model is not None
    out_video = model.infer_one_video(dummy_prompts[0])
    assert out_video is not None
    # check if out_video is a tensor or not
    assert isinstance(out_video, torch.Tensor)
    print(out_video.shape)

def test_ModelScope():
    from videogen_hub.infermodels import ModelScope
    model = ModelScope()
    assert model is not None
    out_video = model.infer_one_video(dummy_prompts[0])
    print("video ouputted")
    assert out_video is not None
    # check if out_video is a tensor or not
    assert isinstance(out_video, torch.Tensor)
    print(out_video.shape)

def test_StreamingT2V():
    from videogen_hub.infermodels import StreamingT2V

    model = StreamingT2V()
    assert model is not None
    out_video = model.infer_one_video(dummy_prompts[0])
    print("video ouputted")
    assert out_video is not None
    # check if out_video is a tensor or not
    assert isinstance(out_video, torch.Tensor)
    print(out_video.shape)

def test_OpenSora():
    from videogen_hub.infermodels import OpenSora

    model = OpenSora()
    assert model is not None
    out_video = model.infer_one_video(dummy_prompts[0])
    assert out_video is not None
    # check if out_video is a tensor or not
    assert isinstance(out_video, torch.Tensor)
    print(out_video.shape)


def test_ShowOne():
    from videogen_hub.infermodels import ShowOne

    model = ShowOne()
    assert model is not None
    out_video = model.infer_one_video(dummy_prompts[0])
    assert out_video is not None
    # check if out_video is a tensor or not
    assert isinstance(out_video, torch.Tensor)
    print(out_video.shape)


if __name__ == "__main__":
    test_ShowOne()
    print("Everything passed")
    pass