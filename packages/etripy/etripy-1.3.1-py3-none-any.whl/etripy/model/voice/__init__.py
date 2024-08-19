"""MIT License

Copyright (c) 2023 Kim Suyun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class RecognitionResult:
    recognized: Optional[str] = field(repr=True, compare=True, default=None)
    """음성 언어 코드에 따른 음성인식 결과"""


@dataclass(frozen=True)
class PronunciationResult:
    recognized: Optional[str] = field(repr=True, compare=True, default=None)
    """음성 언어 코드에 따른 발음평가 결과"""

    score: Optional[str] = field(repr=True, compare=True, default=None)
    """발음 평가 점수로 1~5점까지 제공"""
