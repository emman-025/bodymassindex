from django.shortcuts import render

from django.shortcuts import render


def convert_to_metric(weight, weight_unit, height_unit, height_m, height_cm, height_ft, height_in):
    """
    Convert all inputs to kg and meters.
    - weight_unit expected: 'kg' or 'lb'
    - height_unit expected: 'm', 'cm', or 'ft'
    """
    # weight → kg
    weight = float(weight)
    if weight_unit == "lb":
        weight_kg = weight * 0.453592
    else:
        weight_kg = weight  # already kg

    # height → meters
    height_m_val = None

    # normalise height_unit just in case template uses full words
    unit = (height_unit or "").lower().strip()

    if unit in ("m", "meter", "meters") and height_m:
        height_m_val = float(height_m)

    elif unit in ("cm", "centimeter", "centimeters") and height_cm:
        height_m_val = float(height_cm) / 100.0

    elif unit in ("ft", "feet") and (height_ft or height_in):
        ft = float(height_ft or 0)
        inch = float(height_in or 0)
        total_inches = ft * 12 + inch
        height_m_val = total_inches * 0.0254

    return weight_kg, height_m_val


def classify_bmi(bmi):
    """Return category string based on BMI value."""
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "healthy"
    elif bmi < 30:
        return "overweight"
    else:
        # treat obese as overweight category for this project
        return "overweight"


def bmi_form(request):
    context = {
        "result": None,
        "category": None,
        "error": None,
    }

    if request.method == "POST":
        sex = (request.POST.get("sex") or "").strip()
        weight = (request.POST.get("weight") or "").strip()
        weight_unit = (request.POST.get("weight_unit") or "").strip()
        height_unit = (request.POST.get("height_unit") or "").strip()
        height_m = (request.POST.get("height_m") or "").strip()
        height_cm = (request.POST.get("height_cm") or "").strip()
        height_ft = (request.POST.get("height_ft") or "").strip()
        height_in = (request.POST.get("height_in") or "").strip()

        # 🔹 basic required fields
        # make sure your form has: name="sex", "weight", "weight_unit", "height_unit"
        if not sex or not weight or not weight_unit or not height_unit:
            context["error"] = "Please fill in all required fields."
            return render(request, "bmi/bmi_form.html", context)

        try:
            weight_kg, height_m_val = convert_to_metric(
                weight, weight_unit, height_unit, height_m, height_cm, height_ft, height_in
            )
        except ValueError:
            context["error"] = "Please enter valid numeric values."
            return render(request, "bmi/bmi_form.html", context)

        # height or weight invalid / missing
        if not height_m_val or height_m_val <= 0 or weight_kg <= 0:
            context["error"] = "Please enter realistic positive values for height and weight."
            return render(request, "bmi/bmi_form.html", context)

        bmi = weight_kg / (height_m_val ** 2)
        category = classify_bmi(bmi)

        context["result"] = round(bmi, 2)
        context["category"] = category
        context["sex"] = sex  # if you want to use it in templates

        # 🔹 render different result pages
        if category == "underweight":
            return render(request, "bmi/underweight.html", context)
        elif category == "healthy":
            return render(request, "bmi/healthy.html", context)
        else:
            return render(request, "bmi/overweight.html", context)

    # GET request → just show form
    return render(request, "bmi/bmi_form.html", context)


