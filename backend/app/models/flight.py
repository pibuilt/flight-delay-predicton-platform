from pydantic import BaseModel


class FlightRequest(BaseModel):

    AIRLINE: str
    ORIGIN_AIRPORT: str
    DESTINATION_AIRPORT: str
    DEPARTURE_TIME: int
    DISTANCE: int
    DAY_OF_WEEK: int