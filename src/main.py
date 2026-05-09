from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from typing import List, Optional
from datetime import date
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import os
from fastapi import Form, HTTPException
from fastapi.responses import RedirectResponse

from src import models
from src import schemas
from src import database

app = FastAPI(title="F1 Driver Management API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

get_db = database.get_db



@app.get("/teams/", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    """Получить список всех команд"""
    return db.query(models.Team).all()


@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    """Добавить новую команду"""
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team



@app.get("/drivers/", response_model=List[schemas.Driver])
def read_drivers(db: Session = Depends(get_db)):
    """Получить список всех пилотов"""
    return db.query(models.Driver).all()


@app.post("/drivers/", response_model=schemas.Driver)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    """Зарегистрировать нового пилота"""
    db_driver = db.query(models.Driver).filter(models.Driver.driver_code == driver.driver_code).first()
    if db_driver:
        raise HTTPException(status_code=400, detail="Код пилота уже занят")

    new_driver = models.Driver(**driver.dict())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

@app.get("/drivers-page")
def get_drivers_page(request: Request, db: Session = Depends(get_db)):
    drivers = db.query(models.Driver).all()
    teams = db.query(models.Team).all()
    return templates.TemplateResponse(
        request=request,
        name="drivers.html",
        context={"drivers": drivers, "teams": teams}
    )

from datetime import date


@app.post("/drivers/add")
def add_driver(
        first_name: str = Form(...),
        last_name: str = Form(...),
        driver_code: str = Form(...),
        permanent_number: int = Form(...),
        team_id: int = Form(None),
        db: Session = Depends(get_db)
):
    new_driver = models.Driver(
        first_name=first_name,
        last_name=last_name,
        driver_code=driver_code.upper(),
        permanent_number=permanent_number
    )
    db.add(new_driver)
    db.flush()

    if team_id:
        new_contract = models.Contract(
            driver_id=new_driver.id,
            team_id=team_id,
            start_date=date.today()
        )
        db.add(new_contract)

    db.commit()
    return RedirectResponse(url="/drivers-page", status_code=303)

@app.post("/drivers/delete/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if driver:
        db.delete(driver)
        db.commit()
    return RedirectResponse(url="/drivers-page", status_code=303)

@app.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    """Удалить пилота по ID"""
    db_driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Пилот не найден")
    db.delete(db_driver)
    db.commit()
    return {"message": "Пилот успешно удален"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/teams-page")
def get_teams_page(request: Request, db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return templates.TemplateResponse(
        request=request,
        name="teams.html",
        context={"teams": teams}
    )

@app.post("/teams/add")
def add_team(
    name: str = Form(...),
    full_name: str = Form(...),
    base_location: str = Form(...),
    engine_supplier: str = Form(...),
    db: Session = Depends(get_db)
):
    new_team = models.Team(
        name=name,
        full_name=full_name,
        base_location=base_location,
        engine_supplier=engine_supplier
    )
    db.add(new_team)
    db.commit()
    return RedirectResponse(url="/teams-page", status_code=303)

@app.get("/standings/wcc/{year}")
def get_wcc_standings(year: int, db: Session = Depends(get_db)):
    """
    Кубок Конструкторов (WCC) за конкретный год.
    Вызывает SQL-функцию get_constructor_standings из Шага 3.
    """
    query = text("SELECT * FROM get_constructor_standings(:year)")
    result = db.execute(query, {"year": year}).fetchall()

    if not result:
        return {"message": f"Нет данных за {year} сезон"}

    return [{"team": row[0], "points": float(row[1])} for row in result]


@app.get("/standings/drivers", response_model=List[schemas.DriverStanding])
def get_driver_standings(db: Session = Depends(get_db)):
    """Личный зачет пилотов на основе всех результатов гонок"""
    results = (
        db.query(
            models.Driver.first_name,
            models.Driver.last_name,
            models.Team.name.label("team_name"),
            func.sum(models.race_results.c.points_earned).label("total_points")
        )
        .join(models.race_results, models.Driver.id == models.race_results.c.driver_id)
        .join(models.Team, models.race_results.c.team_id == models.Team.id)
        .group_by(models.Driver.id, models.Team.name)
        .order_by(desc("total_points"))
        .all()
    )

    standings = []
    for index, row in enumerate(results):
        standings.append({
            "rank": index + 1,
            "full_name": f"{row.first_name} {row.last_name}",
            "team_name": row.team_name,
            "total_points": float(row.total_points)
        })
    return standings


@app.get("/drivers/{driver_id}/history", response_model=List[schemas.CareerHistory])
def get_driver_history(driver_id: int, db: Session = Depends(get_db)):
    """История контрактов пилота"""
    history = (
        db.query(
            models.Team.name.label("team_name"),
            models.Contract.start_date,
            models.Contract.end_date,
            models.Contract.salary_m_usd.label("salary")
        )
        .join(models.Contract, models.Team.id == models.Contract.team_id)
        .filter(models.Contract.driver_id == driver_id)
        .order_by(models.Contract.start_date)
        .all()
    )

    if not history:
        raise HTTPException(status_code=404, detail="История карьеры не найдена")

    return history