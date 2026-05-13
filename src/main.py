from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
import db

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI(title="F1 System")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def standings(request: Request, session: Session = Depends(db.get_db)):
    drivers = session.query(models.Driver).order_by(models.Driver.points.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "drivers": drivers})

@app.post("/add-points/{driver_id}")
def add_points(driver_id: int, points: int = Form(...), session: Session = Depends(db.get_db)):
    driver = session.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver:
        driver.points += points
        session.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/create-driver")
def create_driver(
    first_name: str = Form(...),
    last_name: str = Form(...),
    number: int = Form(...),
    code: str = Form(...),
    team_id: int = Form(...),
    session: Session = Depends(db.get_db)
):
    new_driver = models.Driver(
        first_name=first_name,
        last_name=last_name,
        number=number,
        code=code,
        team_id=team_id
    )
    session.add(new_driver)
    session.commit()
    return RedirectResponse(url="/", status_code=303)