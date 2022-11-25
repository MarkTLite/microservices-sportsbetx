from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DBResponse(_message.Message):
    __slots__ = ["data", "message", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: DataDict
    message: str
    status: bool
    def __init__(self, status: bool = ..., message: _Optional[str] = ..., data: _Optional[_Union[DataDict, _Mapping]] = ...) -> None: ...

class DataDict(_message.Message):
    __slots__ = ["away_team", "away_team_win_odds", "date_range", "draw_odds", "game_date", "home_team", "home_team_win_odds", "league", "odds_id", "user_id"]
    AWAY_TEAM_FIELD_NUMBER: _ClassVar[int]
    AWAY_TEAM_WIN_ODDS_FIELD_NUMBER: _ClassVar[int]
    DATE_RANGE_FIELD_NUMBER: _ClassVar[int]
    DRAW_ODDS_FIELD_NUMBER: _ClassVar[int]
    GAME_DATE_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_FIELD_NUMBER: _ClassVar[int]
    HOME_TEAM_WIN_ODDS_FIELD_NUMBER: _ClassVar[int]
    LEAGUE_FIELD_NUMBER: _ClassVar[int]
    ODDS_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    away_team: str
    away_team_win_odds: float
    date_range: str
    draw_odds: float
    game_date: str
    home_team: str
    home_team_win_odds: float
    league: str
    odds_id: str
    user_id: str
    def __init__(self, league: _Optional[str] = ..., home_team: _Optional[str] = ..., away_team: _Optional[str] = ..., home_team_win_odds: _Optional[float] = ..., away_team_win_odds: _Optional[float] = ..., draw_odds: _Optional[float] = ..., game_date: _Optional[str] = ..., odds_id: _Optional[str] = ..., date_range: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...
