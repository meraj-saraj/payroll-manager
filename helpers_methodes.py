import jdatetime

def jalali_to_iso(jalali:str)->str:
    """
    Converting Solar Hijri date to Gregorian date.

    Args:
        jalali: The Hijri date.

    Returns:
        A string Gregrian date.
    """
    y,m,d = jalali.split("/")
    year,month,day = int(y),int(m),int(d)
    g_date = jdatetime.date(year,month,day)
    return g_date.togregorian().isoformat()