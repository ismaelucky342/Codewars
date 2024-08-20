int quarter_of(int month)
{
    if (month < 1 || month > 12)
    {
        printf("invalid month");
    }
    else if (month <= 3)
    {
        return 1;
    }
    else if (month > 3 && month <= 6)
    {
        return 2;
    }
    else if (month > 6 && month <= 9)
    {
        return 3;
    }
    else
        return 4;
}