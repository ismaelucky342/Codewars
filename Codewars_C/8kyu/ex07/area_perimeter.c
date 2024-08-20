int area_or_perimeter(int l, int w)
{
    if (l == w)
    {
        return l * w;
    }
    else if (l < w || l > w)
    {
        return 2 * (l + w);
    }
}