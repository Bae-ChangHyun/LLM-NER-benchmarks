from pydantic import BaseModel, Field
from typing import List, Optional

class PersonalInfo(BaseModel):
    name: Optional[str] = Field(default="", description="지원자의 이름")
    email: Optional[str] = Field(default="", description="지원자의 이메일")
    phone: Optional[str] = Field(default="", description="지원자의 전화번호")
    address: Optional[str] = Field(default="", description="지원자의 주소")
    age: Optional[str] = Field(default="", description="지원자의 나이(년도로 되어있으면 현재 2025년기준으로 계산하여 작성할것)")

# 모델 정의
class Education(BaseModel):
    institution: Optional[str] = Field(default="", description="최종학력")
    degree: Optional[str] = Field(default="", description="학위")
    score: Optional[str] = Field(default="", description="학점 (예: 4.5/4.5)")
    major: Optional[str] = Field(default="", description="전공")
    period: Optional[str] = Field(default="", description="기간 (예: 2015-2019) 없으면 비워둘 것")

class Activity(BaseModel):
    title: Optional[str] = Field(default="", description="활동/경험/포트폴리오 제목")
    description: Optional[str] = Field(default="", description="활동/경험/포트폴리오/프로젝트경험 내용")
    period: Optional[str] = Field(default="", description="활동 기간")

class Certificate(BaseModel):
    name: Optional[str] = Field(default="", description="자격증 이름")
    score: Optional[str] = Field(default="Pass", description="자격증 점수(없으면 Pass로 표기)")
    issuer: Optional[str] = Field(default="", description="발급 기관")
    date: Optional[str] = Field(default="", description="취득일")

class ResumeInfo(BaseModel):
    personal_info: PersonalInfo = Field(description="지원자의 개인 정보")
    education: List[Education] = Field(description="지원자의 학력 정보", default=[])
    activities: List[Activity] = Field(description="지원자의 경험/활동/프로젝트/포트폴리오 내역", default=[])
    certificates: List[Certificate] = Field(description="지원자의 자격증 정보", default=[])
    
    
######################################################################################################################
from pydantic import BaseModel, Field
from typing import List, Optional

class MaritimeAccidentReport(BaseModel):
    document_title: Optional[str] = Field(
        description="사건의 전체 이름 (예: 어선 제2017국제호 화재사건)"
    )
    case_id: Optional[str] = Field(
        description="사건 번호 (예: 목포해심 제 2023-028호)"
    )
    ship_name: Optional[str] = Field(
        description="사고 선박의 이름"
    )
    ship_type: Optional[str] = Field(
        description="사고 선박의 종류 (예: 어선, 카페리여객선)"
    )
    accident_type: Optional[str] = Field(
        description="사고의 핵심 유형 (예: 화재, 충돌, 침몰)"
    )
    accident_date: Optional[str] = Field(
        description="사고 발생 일시 (예: 2020. 10. 6.)"
    )
    accident_location: Optional[str] = Field(
        description="사고가 발생한 구체적인 장소"
    )
    accident_cause_keywords: List[str] = Field(
        description="문서의 '원인판단 주제어'에 명시된 사고 원인 핵심 키워드 목록"
    )
    summary_judgement: Optional[str] = Field(
        description="문서의 '판시사항' 내용을 간결하게 요약한 문장"
    )
    damage_summary: Optional[str] = Field(
        description="사고로 인한 인명 및 선박 피해를 요약한 내용"
    )
    
######################################################################################################################

class Career(BaseModel):
    company_name: str = Field(description="회사명")
    start_year: Optional[int] = Field(description="입사년")
    start_month: Optional[int] = Field(description="입사월")
    start_day: Optional[int] = Field(description="입사일")
    end_year: Optional[int] = Field(description="퇴사년")
    end_month: Optional[int] = Field(description="퇴사월")
    end_day: Optional[int] = Field(description="퇴사일")
    is_currently_employed: Optional[bool] = Field(description="재직여부 (현재 재직 중인 경우 True, 퇴사한 경우 False)")
    main_tasks_achievements: Optional[str] = Field(description="주요업무 및 성과")
    reason_for_job_change: Optional[str] = Field(description="이직사유")
    annual_salary: Optional[int] = Field(description="연봉 (숫자로 기재, 예: 50000000)")
    reason_for_resignation: Optional[str] = Field(description="퇴사사유")
    job_title: Optional[str] = Field(description="직무명")
    department: Optional[str] = Field(description="부서")
    position: Optional[str] = Field(description="직급")
    role: Optional[str] = Field(description="직책")
    responsibilities: Optional[str] = Field(description="담당업무")
    company_name_disclosure: Optional[bool] = Field(description="회사명 비공개 여부 (비공개를 원하는 경우 True, 공개하는 경우 False)")
    employment_type: Optional[str] = Field(description="고용형태 (정규직, 계약직, 프리랜서, 파견직 중 하나)")