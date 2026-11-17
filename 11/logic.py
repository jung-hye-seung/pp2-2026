
# BMI 건강관리 프로그램 - 모듈 2
# AI 사용: OpenAI ChatGPT (GPT-6)
# 사용 목적: 모듈 2의 건강정보 관리 기능 구현 지원
# 사용 날짜: 2026-11-17
# AI 사용 프롬프트: BMI 건강정보 추가, 조회, 검색, 수정,
# 삭제 및 통계 기능을 구현하는 코드 작성

import statistics
from datetime import datetime


class HealthManager:
    """건강정보를 관리하는 클래스"""

    def __init__(self, records=None):
        self.records = records if records is not None else []

    # BMI 계산
    def calculate_bmi(self, height, weight):
        height = float(height)
        weight = float(weight)

        if height <= 0 or weight <= 0:
            raise ValueError("키와 몸무게는 0보다 커야 합니다.")

        bmi = weight / ((height / 100) ** 2)
        return round(bmi, 2)

    # 비만도 판정
    def calculate_status(self, bmi):
        if bmi < 18.5:
            return "저체중"
        elif bmi < 23:
            return "정상"
        elif bmi < 25:
            return "과체중"
        else:
            return "비만"

    # 식별번호 자동 생성
    def generate_id(self):
        prefix = "P" + str(datetime.now().year) + "-"
        numbers = []

        for record in self.records:
            record_id = str(record.get("id", ""))

            if record_id.startswith(prefix):
                try:
                    numbers.append(int(record_id.split("-")[1]))
                except (ValueError, IndexError):
                    pass

        number = max(numbers, default=0) + 1
        return prefix + str(number).zfill(4)

    # 1. 건강정보 추가
    def add_record(self, name, birth_year, gender, height, weight):
        name = str(name).strip()
        gender = str(gender).strip()

        if not name or not gender:
            raise ValueError("이름과 성별을 입력하세요.")

        birth_year = int(birth_year)
        height = float(height)
        weight = float(weight)

        if birth_year <= 0 or birth_year > datetime.now().year:
            raise ValueError("생년을 확인하세요.")

        bmi = self.calculate_bmi(height, weight)

        # 중복 검사
        for record in self.records:
            if (record.get("name") == name
                and record.get("birth_year") == birth_year
                and record.get("gender") == gender):
                raise ValueError("이미 등록된 사용자입니다.")

        new_record = {
            "id": self.generate_id(),
            "name": name,
            "birth_year": birth_year,
            "gender": gender,
            "height": height,
            "weight": weight,
            "bmi": bmi,
            "status": self.calculate_status(bmi)
        }

        self.records.append(new_record)
        return new_record.copy()

    # 2. 전체 목록 조회
    def get_all_records(self):
        return [record.copy() for record in self.records]

    # 3. 이름 및 식별번호 검색
    def search_records(self, keyword):
        keyword = str(keyword).strip().lower()

        return [
            record.copy()
            for record in self.records
            if keyword in str(record.get("name", "")).lower()
            or keyword in str(record.get("id", "")).lower()
        ]

    # 4. 건강정보 수정
    def update_record(self, identifier, **changes):
        record = next(
            (r for r in self.records if r.get("id") == identifier),
            None
        )

        if record is None:
            return False

        allowed = ["name", "birth_year", "gender", "height", "weight"]

        # 변경할 데이터를 먼저 검사
        updated = record.copy()

        for key, value in changes.items():
            if key not in allowed:
                raise ValueError("수정할 수 없는 항목입니다.")

            if key == "name":
                value = str(value).strip()
                if not value:
                    raise ValueError("이름을 입력하세요.")

            elif key == "gender":
                value = str(value).strip()
                if not value:
                    raise ValueError("성별을 입력하세요.")

            elif key == "birth_year":
                value = int(value)
                if value <= 0 or value > datetime.now().year:
                    raise ValueError("생년을 확인하세요.")

            elif key in ("height", "weight"):
                value = float(value)
                if value <= 0:
                    raise ValueError("키와 몸무게는 양수여야 합니다.")

            updated[key] = value

        # BMI와 비만도 다시 계산
        updated["bmi"] = self.calculate_bmi(
            updated["height"], updated["weight"]
        )
        updated["status"] = self.calculate_status(updated["bmi"])

        record.update(updated)
        return record.copy()

    # 5. 건강정보 삭제
    def delete_record(self, identifier):
        for i, record in enumerate(self.records):
            if record.get("id") == identifier:
                del self.records[i]
                return True

        return False

    # 6. 건강정보 통계
    def get_statistics(self):
        if not self.records:
            return {
                "인원수": 0,
                "평균 키": 0,
                "평균 몸무게": 0,
                "평균 BMI": 0,
                "키 표준편차": 0,
                "몸무게 표준편차": 0,
                "BMI 표준편차": 0
            }

        heights = [r["height"] for r in self.records]
        weights = [r["weight"] for r in self.records]
        bmis = [r["bmi"] for r in self.records]

        return {
            "인원수": len(self.records),
            "평균 키": round(statistics.mean(heights), 2),
            "평균 몸무게": round(statistics.mean(weights), 2),
            "평균 BMI": round(statistics.mean(bmis), 2),
            "키 표준편차": round(statistics.pstdev(heights), 2),
            "몸무게 표준편차": round(statistics.pstdev(weights), 2),
            "BMI 표준편차": round(statistics.pstdev(bmis), 2)
        }
