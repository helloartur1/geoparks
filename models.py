from pydantic import BaseModel

class GeoobjectPathModel(BaseModel):
    id : str
    name : str
    description : str
    longitude : float
    latitude : float
    type : str
    idgeopark : str
    path_photo : str


class PathModel(BaseModel):
    path : str


class GeoobjectModel(BaseModel):
    id : str
    name : str
    description : str
    longitude : float
    latitude : float
    type : str
    idgeopark : str



class Data_geoobjects(BaseModel):
    id : str
    name : str
    description : str
    longitude : float
    latitude : float
    type : str
    idgeopark : str