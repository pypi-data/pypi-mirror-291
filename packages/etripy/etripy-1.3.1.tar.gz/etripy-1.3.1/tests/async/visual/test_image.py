import pytest
from etripy.client import ImageClient


# 객체 검출 테스트
@pytest.mark.asyncio
async def test_object_detect(image: ImageClient):
    r = await image.object_detect(file_path="./assets/object_detect.jpg")
    assert r


# 사람 속성 검출 테스트
@pytest.mark.asyncio
async def test_human_parsing(image: ImageClient):
    r = await image.human_parsing(file_path="./assets/human_parsing.jpg")
    assert r


# 얼굴 비식별화 테스트
@pytest.mark.asyncio
async def test_face_deid(image: ImageClient):
    r = await image.face_deid(file_path="./assets/face_deid.jpg")
    assert r


# 사람 상태 이해 테스트
@pytest.mark.asyncio
async def test_human_status(image: ImageClient):
    r = await image.human_status(file_path="./assets/human_status.jpg")
    assert r
