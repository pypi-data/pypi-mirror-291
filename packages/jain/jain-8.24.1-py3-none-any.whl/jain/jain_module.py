# src/jain/jain_module.py

def greet(name: str) -> str:
    """
    Returns a greeting for the given name.
    """
    return f"Jai Jinendra, {name}!"

def get_tirthankar_name(number: int) -> str:
    """
    Returns the name of the Jain Tirthankar corresponding to the given number.
    
    :param number: The number of the Tirthankar (1 to 24)
    :return: The name of the Tirthankar
    """
    tirthankaras = [
        "Rishabhanatha", "Ajitanatha", "Sambhavanatha", "Abhinandananatha", "Sumatinatha",
        "Padmaprabha", "Suparshvanatha", "Chandraprabha", "Suvidhinatha", "Shitalanatha",
        "Shreyansanatha", "Vasupujya", "Vimalanatha", "Anantanatha", "Dharamanatha",
        "Shantinatha", "Kunthunatha", "Aranatha", "Mallinatha", "Munisuvrata",
        "Naminatha", "Neminatha", "Parshvanatha", "Mahavira"
    ]
    
    if 1 <= number <= 24:
        return tirthankaras[number - 1] + " ji"
    else:
        return "Invalid Tirthankar number. Please enter a number between 1 and 24."

