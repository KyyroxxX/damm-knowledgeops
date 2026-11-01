import pytest
from app.proposals import analyze_proposal_with_ai

def test_analyze_proposal_ergonomics_priority():
    text = "tengo que alargar mucho el brazo y luego agacharme y eso hace danyo a la larga en la espalda"
    # El test valida la evaluacion (usando fallback si bedrock no esta configurado en test local)
    result = analyze_proposal_with_ai(text, "envasado", "llenadora_krones")
    assert result["is_legitimate"] is True
    assert result["priority"] == "HIGH"
    assert "ERGONOMICS" in result["category"]

def test_analyze_proposal_operational_efficiency():
    text = "los recambios de bobina estan a 40 metros de la etiquetadora y perdemos 5 minutos en cada cambio"
    result = analyze_proposal_with_ai(text, "envasado", "etiquetadora", is_anonymous=False)
    assert result["is_legitimate"] is True
    assert result["category"] in ["OPERATIONAL_EFFICIENCY", "ERGONOMICS_HEALTH"]

def test_analyze_proposal_anonymity_mode():
    text = "Mi nombre es Carlos y propongo poner una rampa para no cargar las cajas a pulso"
    result = analyze_proposal_with_ai(text, "envasado", "paletizador", is_anonymous=True)
    assert result["is_legitimate"] is True
    assert "priority" in result
