from mangum import Mangum

from npb.app import app

handler = Mangum(app, lifespan="off")
