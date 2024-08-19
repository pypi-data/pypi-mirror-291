from datetime import datetime
from typing import Literal, Optional, Sequence

from pydantic import BaseModel, field_serializer


class Person(BaseModel):
    personid: int
    plastname: str
    pfirstname: str
    psurname: str
    ppsex: int
    isuser: bool
    pilogin: str
    pipassword: str
    caid: str
    caidname: str
    rspostid: str
    rspostidname: str
    personemail: str
    pstatus: int
    pextcode: str

    def __str__(self) -> str:
        return f"{self.plastname} {self.pfirstname} {self.psurname}"


class Persons:
    def __init__(self, persons: Sequence[Person], count: int):
        self._persons = sorted(persons, key=lambda x: x.personid)
        self.count = count

    def __getitem__(self, key: int) -> Person:
        return self._persons[key]

    def __str__(self) -> str:
        return "\n".join([str(person) for person in self._persons])
    
    def model_dump(self):
        return [model.model_dump() for model in self._persons]


class Measure(BaseModel):
    meid: Optional[int] = None
    mename: str
    medescription: Optional[str] = None
    metype: Literal["0", "1", "2"] = "1"
    mecode: Optional[str] = None
    mestatus: Optional[int] = None
    mestartdate: Optional[datetime] = None
    meenddate: Optional[datetime] = None
    meeduform: Literal["0", "1", "2"] = "1"
    mecontenttype: Optional[int] = None
    testid: Optional[str] = None
    testidname: Optional[str] = None
    ugrid: Optional[int] = None
    ugridname: Optional[str] = None
    mepasses: Optional[int] = None

    def __str__(self):
        result = f"{self.mename}\n"
        if self.mestartdate:
            result += f"Начало: {
                self.mestartdate.strftime('%d.%m.%Y %H:%M')}\n"
        if self.meenddate:
            result += f"Окончание: {
                self.meenddate.strftime('%d.%m.%Y %H:%M')}\n"
        return result

    @field_serializer("mestartdate", "meenddate")
    def format_date(self, dt: Optional[datetime]):
        if dt:
            return dt.strftime("%Y-%m-%d %H:%M:%S.000")


class Measures:
    def __init__(self, measures: Sequence[Measure], count: int):
        self._measures = sorted(measures, key=lambda x: x.meid, reverse=True)
        self.count = count

    def __getitem__(self, key: int) -> Measure:
        return self._measures[key]

    def __str__(self):
        return "\n".join([str(measure) for measure in self._measures])
    
    def model_dump(self):
        return [model.model_dump() for model in self._measures]


class Member(BaseModel):
    isaccess: bool
    meid: int
    meidname: str
    mmfinishstatus: int
    mmid: int
    personid: int
    personidname: str

    def __str__(self):
        return self.personidname


class Members:
    def __init__(self, members: Sequence[Member], count: int):
        self._members = members
        self.count = count

    def __getitem__(self, key: int) -> Member:
        return self._members[key]

    def __str__(self):
        if self._members:
            return "\n".join([member.personidname for member in self._members])
        else:
            return "Нет участников"
    
    def model_dump(self):
        return [model.model_dump() for model in self._members]


class Tutor(BaseModel):
    isaccess: bool
    meid: int
    meidname: str
    mtid: int
    personid: int
    personidname: str

    def __str__(self):
        return self.personidname


class Tutors:
    def __init__(self, tutors: Sequence[Tutor], count: int):
        self._tutors = tutors
        self.count = count

    def __getitem__(self, key: int) -> Tutor:
        return self._tutors[key]

    def __str__(self):
        if self._tutors:
            return "\n".join([tutor.personidname for tutor in self._tutors])
        else:
            return "Нет преподавателей"
    
    def model_dump(self):
        return [model.model_dump() for model in self._tutors]


class MeasureResult(BaseModel):
    mmid: int
    mrstatusid: Optional[int] = None
    mrlastaccesstime: Optional[datetime] = None
    mrscoreinpercent: Optional[int] = None
    mrscore: Optional[float] = None
    mrprocent: Optional[int] = None
    mrduration: Optional[float] = None
    mrstarttime: Optional[datetime] = None
    mrendtime: Optional[datetime] = None
    mrattemptcount: Optional[int] = None


class MeasureResults:
    def __init__(self, measure_results: Sequence[MeasureResult], count: int):
        self._measure_results = measure_results
        self.count = count

    def __getitem__(self, key: int) -> MeasureResult:
        return self._measure_results[key]

    def model_dump(self):
        return [model.model_dump() for model in self._measure_results]


class WebinarRecord(BaseModel):
    id: str
    name: str
    period: Optional[str] = None
    duration: Optional[str] = None
    viewlink: str
    downloadlink: Optional[str] = None

    def __str__(self) -> str:
        return self.viewlink


class WebinarRecords:
    def __init__(self, webinar_records: Sequence[WebinarRecord], count: int):
        self._webinar_records = webinar_records
        self.count = count

    def __getitem__(self, key: int) -> WebinarRecord:
        return self._webinar_records[key]

    def model_dump(self):
        return [model.model_dump() for model in self._webinar_records]
