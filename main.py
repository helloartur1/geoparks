from pydantic import UUID4
import uuid, db_conn
from fastapi import FastAPI
from geoparks.models import PathModel, GeoobjectPathModel, Data_geoobjects, GeoobjectModel

app = FastAPI()


@app.get("/geoobjects/{id_object}")
async def get_by_geoobject(id_object: UUID4):
    query = f"SELECT * FROM geoobject  WHERE id = '{id_object}'"

    result = db_conn.query(query, "one")

    res = Data_geoobjects(name=str(result[0]), description=str(result[1]), longitude=float(result[2]),
                          latitude=float(result[3]), id=str(result[4]),
                          type=str(result[5]), idgeopark=str(result[6]))

    return res


@app.get("/get_all_geoobject/")
async def get_all_geoobject():
    query1 = f"SELECT * FROM geoobject"

    result = db_conn.query(query1, "all")

    res = [GeoobjectModel(name=str(row[0]), description=str(row[1]), longitude=float(row[2]), latitude=float(row[3]),
                          id=str(row[4]),
                          type=str(row[5]), idgeopark=str(row[6])) for row in result]

    return res


@app.get("/get_all_geoobjects")
async def get_all_geoobjects(id_geopark: UUID4):
    query = f"SELECT geoobject.*, geopark.name FROM geoobject,geopark  WHERE geoobject.idgeopark = '{id_geopark}';"

    result = db_conn.query(query, "all")

    res = [GeoobjectModel(id=str(row[4]), name=str(row[0]), description=str(row[1]), longitude=float(row[2]),
                          latitude=float(row[3]), type=str(row[5]), idgeopark=str(row[6]), namegeopark=str(row[7])
                          ) for row in result]

    return res


@app.get("/get_photo_by_geoobject")
async def get_photo_by_geoobject(id_geoobject: UUID4):
    query1 = f"SELECT path FROM photo where geoobject_id = '{id_geoobject}';"

    result = db_conn.query(query1, "one")

    return {"path": str(result[0])}


@app.post("/create_photo_by_geoobject")
async def create_photo_by_geoobject(geoobject_id: UUID4, path_photo: str, preview_photo: bool):
    id = str(uuid.uuid4())

    path_photo = "/geopark_image/" + path_photo

    query = f"INSERT INTO photo(id,path,preview,geoobject_id) VALUES('{id}','{path_photo}','{preview_photo}','{geoobject_id}');"

    return db_conn.query(query, "")


@app.get("/aaa")  # хз как назвать его
async def photo_all(id_geoobject: UUID4):
    query1 = (
        f"SELECT geoobject.id, geoobject.name, geoobject.description, geoobject.longitude, geoobject.latitude, geoobject.type, geoobject.idgeopark, ARRAY_AGG(photo.path) as paths from geoobject"
        f" JOIN photo ON geoobject.id = photo.geoobject_id WHERE photo.geoobject_id = '{id_geoobject}'  AND photo.preview = '1' GROUP BY geoobject.id")

    result = db_conn.query(query1, "all")

    res = [GeoobjectPathModel(id=str(row[0]), name=str(row[1]), description=str(row[2]), longitude=float(row[3]),
                              latitude=float(row[4]), type=str(row[5]), idgeopark=str(row[6]),
                              path_photo=str(row[len(row) - 1][0])
                              ) for row in result]

    return res


@app.get("/get_photo")
async def get_photos(id_geoobject: UUID4):
    query = f"SELECT path FROM photo WHERE geoobject_id = '{id_geoobject}'"

    result = db_conn.query(query, "all")

    res = [PathModel(path=str(row[0])) for row in result]

    return res