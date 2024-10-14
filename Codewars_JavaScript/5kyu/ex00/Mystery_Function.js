function solved(str)
{
    const strMiddleIndex = Math.floor(str.length / 2); 
    if (str.length % 2 === 0)
    {
      const strSort = str.split('').sort().join('');
   
      return strSort;
    } 
    else 
    {
      const resultStr = str.split('');
      const cutStr = resultStr.splice(strMiddleIndex, 1);
      return resultStr.sort().join('');
    }
 
}