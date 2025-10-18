from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, confloat

# Enable CORS so the Streamlit frontend or other clients can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="ECTS Calculator API")

class CalculateRequest(BaseModel):
    masters_program_academic_year: confloat(gt=0)
    number_of_years_of_bachelor_study: confloat(gt=0)
    total_number_of_units: confloat(gt=0)
    name_of_course_you_want_to_calculate: str
    Accumulated_units: confloat(ge=0)

class CalculateResponse(BaseModel):
    conversion_factor: float
    ECTS: float

@app.post("/calculate", response_model=CalculateResponse)
async def calculate(req: CalculateRequest):
    try:
        conversion_factor = (req.masters_program_academic_year * req.number_of_years_of_bachelor_study) / req.total_number_of_units
        ects = req.Accumulated_units * conversion_factor
        return CalculateResponse(conversion_factor=round(conversion_factor,2), ECTS=round(ects,2))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}")

@app.get("/")
async def root():
    return {"message": "ECTS Calculator API - use /calculate"}







