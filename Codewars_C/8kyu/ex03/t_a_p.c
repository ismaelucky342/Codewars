int points(const char const games[10])
{
    int points = 0; 

    for(int i = 0; i < 10; i++)
    {
        int x,y; 
        sscanf(games[i],"%d:%d",&x,&y);
        if (x > y)
        {
            points += 3;
        }else if (x == y){
            points += 1;
        }else{
            points += 0;
        }
    }
    return points;
}