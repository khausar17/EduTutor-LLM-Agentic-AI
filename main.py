from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import math
import re

app = FastAPI(
    title="Additional Mathematics API",
    description="KSSM Solution of Triangles API",
    version="2.1"
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# HELPER — Strip units from LLM-generated values
#
# WHY THIS EXISTS:
# Gemini sometimes passes "30 km", "75°", "31.455 cm"
# instead of just 30, 75, 31.455.
# FastAPI's float validator cannot parse strings with units.
# This function strips everything except digits, dot, minus.
#
# Examples:
#   clean_num("30 km")    → 30.0
#   clean_num("75°")      → 75.0
#   clean_num("31.455")   → 31.455
#   clean_num(30)         → 30.0
#   clean_num("-1.5")     → -1.5
# =========================================================

def clean_num(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = re.sub(r'[^\d.\-]', '', str(value).strip())
    if not cleaned or cleaned in ['.', '-']:
        raise ValueError(f"Cannot parse '{value}' as a number")
    return float(cleaned)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Additional Mathematics API working",
        "chapter": "Solution of Triangles",
        "version": "2.1",
        "topics": [
            "Sine Rule",
            "Cosine Rule",
            "Area of Triangle",
            "Heron's Formula",
            "Ambiguous Case"
        ]
    }


# =========================================================
# 1. TRIANGLE AREA
# Formula: Area = 1/2 * a * b * sin(C)
# Use when: two sides + included angle known
# =========================================================

@app.get("/triangle-area")
def triangle_area(a: str, b: str, C: str):
    a, b, C = clean_num(a), clean_num(b), clean_num(C)

    sinC = math.sin(math.radians(C))
    area = 0.5 * a * b * sinC

    return {
        "success": True,
        "topic": "Area of Triangle",
        "formula": "Area = 1/2 * a * b * sin(C)",
        "inputs": {"a": a, "b": b, "C": C},
        "result": {"area": round(area, 4)},
        "steps": [
            f"sin({C}) = {round(sinC, 4)}",
            f"Area = 0.5 × {a} × {b} × {round(sinC, 4)}",
            f"Area = {round(area, 4)}"
        ]
    }


# =========================================================
# 2. SINE RULE — FIND SIDE
# Formula: a/sin(A) = b/sin(B)
# Use when: one side-angle pair + another angle known
# =========================================================

@app.get("/sine/find-side")
def sine_find_side(a: str, A: str, B: str):
    a, A, B = clean_num(a), clean_num(A), clean_num(B)

    sinA = math.sin(math.radians(A))
    sinB = math.sin(math.radians(B))
    b    = (a * sinB) / sinA

    return {
        "success": True,
        "topic": "Sine Rule - Find Side",
        "formula": "a/sin(A) = b/sin(B)",
        "inputs": {"a": a, "A": A, "B": B},
        "result": {"b": round(b, 4)},
        "steps": [
            f"sin({A}) = {round(sinA, 4)}",
            f"sin({B}) = {round(sinB, 4)}",
            f"b = ({a} × {round(sinB, 4)}) / {round(sinA, 4)}",
            f"b = {round(b, 4)}"
        ]
    }


# =========================================================
# 3. SINE RULE — FIND ANGLE
# Formula: a/sin(A) = b/sin(B)
# Use when: one side-angle pair + another side known
# =========================================================

@app.get("/sine/find-angle")
def sine_find_angle(a: str, A: str, b: str):
    a, A, b = clean_num(a), clean_num(A), clean_num(b)

    sinB = (b * math.sin(math.radians(A))) / a

    if sinB < -1 or sinB > 1:
        return {
            "success": False,
            "error": "No valid triangle exists"
        }

    B = math.degrees(math.asin(sinB))

    return {
        "success": True,
        "topic": "Sine Rule - Find Angle",
        "formula": "a/sin(A) = b/sin(B)",
        "inputs": {"a": a, "A": A, "b": b},
        "result": {"B": round(B, 4)},
        "steps": [
            f"sin(B) = ({b} × sin({A})) / {a}",
            f"sin(B) = {round(sinB, 4)}",
            f"B = asin({round(sinB, 4)})",
            f"B = {round(B, 4)}°"
        ]
    }


# =========================================================
# 4. COSINE RULE — FIND SIDE
# Formula: a² = b² + c² - 2bc cos(A)
# Use when: two sides + included angle known
# =========================================================

@app.get("/cosine/find-side")
def cosine_find_side(b: str, c: str, A: str):
    b, c, A = clean_num(b), clean_num(c), clean_num(A)

    cosA = math.cos(math.radians(A))
    a    = math.sqrt(b**2 + c**2 - 2 * b * c * cosA)

    return {
        "success": True,
        "topic": "Cosine Rule - Find Side",
        "formula": "a² = b² + c² - 2bc cos(A)",
        "inputs": {"b": b, "c": c, "A": A},
        "result": {"a": round(a, 4)},
        "steps": [
            f"cos({A}) = {round(cosA, 4)}",
            f"a² = {b}² + {c}² - 2({b})({c})({round(cosA, 4)})",
            f"a = {round(a, 4)}"
        ]
    }


# =========================================================
# 5. COSINE RULE — FIND ANGLE
# Formula: cos(A) = (b² + c² - a²) / 2bc
# Use when: all three sides known
# =========================================================

@app.get("/cosine/find-angle")
def cosine_find_angle(a: str, b: str, c: str):
    a, b, c = clean_num(a), clean_num(b), clean_num(c)

    cosA = (b**2 + c**2 - a**2) / (2 * b * c)

    if cosA < -1 or cosA > 1:
        return {
            "success": False,
            "error": "Invalid triangle"
        }

    A = math.degrees(math.acos(cosA))

    return {
        "success": True,
        "topic": "Cosine Rule - Find Angle",
        "formula": "cos(A) = (b² + c² - a²) / 2bc",
        "inputs": {"a": a, "b": b, "c": c},
        "result": {"A": round(A, 4)},
        "steps": [
            f"cos(A) = ({b}² + {c}² - {a}²) / (2 × {b} × {c})",
            f"cos(A) = {round(cosA, 4)}",
            f"A = acos({round(cosA, 4)})",
            f"A = {round(A, 4)}°"
        ]
    }


# =========================================================
# 6. HERON'S FORMULA
# Formula: Area = sqrt(s(s-a)(s-b)(s-c))
# Use when: all three sides known, no angle given
# =========================================================

@app.get("/heron-area")
def heron_area(a: str, b: str, c: str):
    a, b, c = clean_num(a), clean_num(b), clean_num(c)

    s = (a + b + c) / 2
    discriminant = s * (s - a) * (s - b) * (s - c)

    if discriminant < 0:
        return {
            "success": False,
            "error": "Invalid triangle — sides do not satisfy triangle inequality"
        }

    area = math.sqrt(discriminant)

    return {
        "success": True,
        "topic": "Heron's Formula",
        "formula": "Area = sqrt(s(s-a)(s-b)(s-c))",
        "inputs": {"a": a, "b": b, "c": c},
        "result": {
            "semi_perimeter": round(s, 4),
            "area": round(area, 4)
        },
        "steps": [
            f"s = ({a} + {b} + {c}) / 2",
            f"s = {round(s, 4)}",
            f"Area = sqrt({round(s,4)} × {round(s-a,4)} × {round(s-b,4)} × {round(s-c,4)})",
            f"Area = {round(area, 4)}"
        ]
    }


# =========================================================
# 7. AMBIGUOUS CASE
# Formula: h = b sin(A)
# Use when: two sides + non-included angle (SSA)
# =========================================================

@app.get("/ambiguous-case")
def ambiguous_case(a: str, b: str, A: str):
    a, b, A = clean_num(a), clean_num(b), clean_num(A)

    h = b * math.sin(math.radians(A))

    if a < h:
        result = "No triangle exists"
    elif math.isclose(a, h, rel_tol=1e-9):
        result = "One right triangle exists"
    elif h < a < b:
        result = "Two triangles exist"
    else:
        result = "One triangle exists"

    return {
        "success": True,
        "topic": "Ambiguous Case",
        "formula": "h = b sin(A)",
        "inputs": {"a": a, "b": b, "A": A},
        "result": {
            "h": round(h, 4),
            "case": result
        },
        "steps": [
            f"h = {b} × sin({A})",
            f"h = {round(h, 4)}",
            f"Comparing a = {a} with h = {round(h, 4)}",
            result
        ]
    }


# =========================================================
# 8. VERIFY STEP
# Validates a student's intermediate calculation value
# Used by Hint Agent only — does NOT complete the solution
# =========================================================

@app.get("/verify-step")
def verify_step(step_type: str, value: str):
    value = clean_num(value)

    rules = {
        "sin_value":   (-1,   1,    "sin value must be between -1 and 1"),
        "cos_value":   (-1,   1,    "cos value must be between -1 and 1"),
        "angle_deg":   (0,    180,  "angle must be between 0° and 180°"),
        "side_length": (0,    None, "side length must be positive"),
        "area":        (0,    None, "area must be positive")
    }

    if step_type not in rules:
        return {"valid": False, "error": f"Unknown step_type '{step_type}'"}

    low, high, rule_desc = rules[step_type]
    too_low  = value < low
    too_high = high is not None and value > high
    is_valid = not too_low and not too_high

    return {
        "step_type": step_type,
        "value":     value,
        "valid":     is_valid,
        "rule":      rule_desc,
        "feedback":  "Value is valid" if is_valid else f"Invalid: {rule_desc}"
    }


# =========================================================
# 9. WHICH FORMULA
# Returns the correct formula to use based on known values
# Used by Hint Agent only — guides without solving
# =========================================================

@app.get("/which-formula")
def which_formula(
    known_sides: int,
    known_angles: int,
    has_included_angle: bool = False,
    want_to_find: str = "side"
):
    if known_sides == 3 and want_to_find == "angle":
        return {
            "formula": "Cosine Rule",
            "why": "All 3 sides known, finding angle",
            "form": "cos A = (b² + c² - a²) / 2bc",
            "hint_question": "You have all 3 sides. Which formula uses all 3 sides to find an angle?"
        }

    if known_sides == 2 and has_included_angle and want_to_find == "side":
        return {
            "formula": "Cosine Rule",
            "why": "Two sides + included angle, finding third side",
            "form": "a² = b² + c² - 2bc cos A",
            "hint_question": "You know two sides and the angle BETWEEN them. Which formula fits that?"
        }

    if known_sides == 1 and known_angles == 2:
        return {
            "formula": "Sine Rule",
            "why": "One side + two angles",
            "form": "a/sin A = b/sin B",
            "hint_question": "You have a side and its opposite angle. What rule connects sides to their opposite angles?"
        }

    if known_sides == 2 and known_angles == 1 and not has_included_angle:
        return {
            "formula": "Sine Rule (check ambiguous case)",
            "why": "Two sides + non-included angle (SSA)",
            "form": "a/sin A = b/sin B",
            "hint_question": "Before using the Sine Rule, how many triangles could exist with these values?",
            "warning": "Ambiguous case possible"
        }

    if known_sides == 2 and want_to_find == "area":
        return {
            "formula": "Area = ½ ab sin C",
            "why": "Two sides + included angle for area",
            "hint_question": "You want area and have two sides. Which area formula uses two sides and an angle?"
        }

    if known_sides == 3 and want_to_find == "area":
        return {
            "formula": "Heron's Formula",
            "why": "Three sides known, finding area without angle",
            "form": "Area = √s(s-a)(s-b)(s-c)",
            "hint_question": "You have all 3 sides but no angle. Do you know a formula that finds area using only sides?"
        }

    return {
        "formula": "Insufficient information",
        "hint_question": "What information does the question give you? List the sides and angles you know."
    }

# =========================================================
# 10. FIND ANGLE FROM AREA
# Formula: sin C = (2 × Area) / (a × b)
# Use when: Area + two sides known, need the included angle
# =========================================================

@app.get("/find-angle-from-area")
def find_angle_from_area(area: str, a: str, b: str):
    area, a, b = clean_num(area), clean_num(a), clean_num(b)

    sinC = (2 * area) / (a * b)

    if sinC < -1 or sinC > 1:
        return {
            "success": False,
            "error": "No valid angle exists — check your area and side values"
        }

    C = math.degrees(math.asin(sinC))

    return {
        "success": True,
        "topic": "Find Angle from Area",
        "formula": "sin C = (2 × Area) / (a × b)",
        "inputs": {"area": area, "a": a, "b": b},
        "result": {"C": round(C, 4)},
        "steps": [
            f"sin C = (2 × {area}) / ({a} × {b})",
            f"sin C = {round(sinC, 4)}",
            f"C = arcsin({round(sinC, 4)})",
            f"C = {round(C, 4)}°"
        ]
    }